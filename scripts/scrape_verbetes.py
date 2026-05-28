#!/usr/bin/env python3
"""
Scraper de verbetes do museudememes.com.br → arquivos .md para Jekyll.

Uso:
    python scripts/scrape_verbetes.py

Dependências:
    pip install requests beautifulsoup4 markdownify lxml
"""

import os
import re
import json
import time
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup, NavigableString, Tag
import markdownify

# ──────────────────────────────────────────────
# Configuração
# ──────────────────────────────────────────────

SITEMAP_URL  = "https://museudememes.com.br/wp-sitemap-posts-bunch_collection-1.xml"
OUTPUT_DIR   = Path(__file__).parent.parent / "_memes"
DELAY_SECS   = 1.2
DEFAULT_DATE = "2024-01-01"

# Headers completos para bypass do ModSecurity
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Cache-Control": "max-age=0",
}

SESSION = requests.Session()
SESSION.headers.update(HEADERS)

# Nomes de seções esperadas (insensíveis a maiúsculas/acentos)
SECTION_NAMES = {
    "origem":                  "Origem",
    "disseminação e repercussão": "Disseminação e Repercussão",
    "disseminacao e repercussao": "Disseminação e Repercussão",
    "disseminação":             "Disseminação e Repercussão",
    "gênero e formatos":        "Gênero e Formatos",
    "genero e formatos":        "Gênero e Formatos",
    "gênero":                   "Gênero e Formatos",
}

# h2s que NÃO são título nem seção de conteúdo
SKIP_H2 = {"ficha técnica", "ficha tecnica", "exemplos notáveis", "exemplos notaveis",
            "about us", "contact us", "sobre o(a) curador(a)"}

# ──────────────────────────────────────────────
# markdownify customizado
# ──────────────────────────────────────────────

class VerbeteMarkdownConverter(markdownify.MarkdownConverter):
    """Converte HTML para markdown preservando embeds/iframes como HTML bruto."""

    def convert_iframe(self, el, text, **kwargs):
        return f"\n\n{str(el)}\n\n"

    def convert_script(self, el, text, **kwargs):
        src = el.get("src", "")
        if any(x in src for x in ["platform.twitter", "instagram.com", "tiktok.com"]):
            return f"\n\n{str(el)}\n\n"
        return ""

    def convert_blockquote(self, el, text, **kwargs):
        cls = " ".join(el.get("class", []))
        if any(x in cls for x in ["twitter-tweet", "instagram-media", "tiktok-embed"]):
            return f"\n\n{str(el)}\n\n"
        return super().convert_blockquote(el, text, **kwargs)

    def convert_figure(self, el, text, **kwargs):
        if el.find("iframe"):
            return f"\n\n{str(el)}\n\n"
        return text or ""


def html_to_md(html_fragment: str) -> str:
    md = VerbeteMarkdownConverter(
        heading_style=markdownify.ATX,
        bullets="-",
        strip=["style"],
    ).convert(html_fragment)
    md = re.sub(r'\n{3,}', '\n\n', md)
    return md.strip()


def normalize(text: str) -> str:
    """Normaliza texto para comparação (minúsculas, sem acentos comuns)."""
    return (text.strip().lower()
            .replace("ã", "a").replace("â", "a").replace("á", "a").replace("à", "a")
            .replace("é", "e").replace("ê", "e").replace("è", "e")
            .replace("í", "i").replace("î", "i")
            .replace("ó", "o").replace("ô", "o").replace("õ", "o")
            .replace("ú", "u").replace("û", "u")
            .replace("ç", "c"))


# ──────────────────────────────────────────────
# Extração de dados
# ──────────────────────────────────────────────

def get_urls_from_sitemap(sitemap_url: str) -> list[str]:
    resp = SESSION.get(sitemap_url, timeout=30)
    resp.raise_for_status()
    root = ET.fromstring(resp.content)
    ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    return [loc.text.strip() for loc in root.findall(".//sm:loc", ns)]


def extract_date(soup: BeautifulSoup) -> str:
    # 1) meta article:published_time
    meta = soup.find("meta", property="article:published_time")
    if meta and meta.get("content"):
        return meta["content"][:10]

    # 2) JSON-LD
    for script in soup.find_all("script", type="application/ld+json"):
        try:
            data = json.loads(script.string or "")
            if isinstance(data, list):
                data = data[0]
            if isinstance(data, dict) and data.get("datePublished"):
                return data["datePublished"][:10]
        except Exception:
            pass

    # 3) time[datetime]
    time_el = soup.find("time", datetime=True)
    if time_el:
        return time_el["datetime"][:10]

    return DEFAULT_DATE


def extract_title(soup: BeautifulSoup) -> str:
    """
    O título está no PRIMEIRO h2 da página (não num h1).
    Ignora h2s que correspondem a nomes de seção ou de skip.
    """
    # Tentar og:title primeiro
    og = soup.find("meta", property="og:title")
    if og and og.get("content"):
        title = og["content"].strip()
        # Remover sufixo " – #MUSEUdeMEMES" se presente
        title = re.sub(r'\s*[–\-]\s*#?MUSEUdeMEMES.*$', '', title, flags=re.I).strip()
        if title:
            return title

    # Fallback: primeiro h2 que não seja seção conhecida
    for h2 in soup.find_all("h2"):
        text = h2.get_text(strip=True)
        norm = normalize(text)
        if norm not in SKIP_H2 and norm not in SECTION_NAMES:
            return text
    return ""


def collect_section_html(h2_el: Tag) -> str:
    """Coleta todo HTML entre este h2 e o próximo h2."""
    fragments = []
    for sibling in h2_el.next_siblings:
        if isinstance(sibling, NavigableString):
            continue
        if isinstance(sibling, Tag):
            if sibling.name == "h2":
                break
            # Pular elementos de navegação/rodapé que aparecem no fluxo
            cls = " ".join(sibling.get("class", []))
            if any(x in cls for x in ["nav-", "footer", "sidebar", "widget"]):
                continue
            fragments.append(str(sibling))
    return "\n".join(fragments)


def extract_sections(soup: BeautifulSoup) -> dict[str, str]:
    """
    Retorna dict com chaves: "Origem", "Disseminação e Repercussão", "Gênero e Formatos"
    e valores em markdown.
    """
    result = {"Origem": "", "Disseminação e Repercussão": "", "Gênero e Formatos": ""}

    for h2 in soup.find_all("h2"):
        text  = h2.get_text(strip=True)
        norm  = normalize(text)

        canonical = SECTION_NAMES.get(norm)
        if canonical and canonical in result:
            html_frag = collect_section_html(h2)
            if html_frag:
                result[canonical] = html_to_md(html_frag)

    return result


def extract_ficha_tecnica(soup: BeautifulSoup) -> dict:
    """
    Ficha Técnica usa:
      <div class="content-title">Label</div>
      <div class="content-desc">Valor</div>
    como pares de irmãos dentro do mesmo parent div.
    """
    fields = {
        "criador":    "",
        "ano_origem": "",
        "plataforma": "",
        "formato":    "",
        "midia":      "",
    }

    for title_div in soup.find_all("div", class_="content-title"):
        label = normalize(title_div.get_text(strip=True))
        desc_div = title_div.find_next_sibling("div", class_="content-desc")
        if not desc_div:
            continue
        value = desc_div.get_text(strip=True)

        if "criador" in label:
            fields["criador"] = value
        elif "período" in label or "periodo" in label or "circula" in label:
            fields["ano_origem"] = value
        elif "plataforma" in label:
            fields["plataforma"] = value
        elif "formato" in label:
            fields["formato"] = value
        elif "mídia" in label or "midia" in label:
            fields["midia"] = value

    return fields


def extract_curator(soup: BeautifulSoup) -> str:
    """
    Curador: link dentro da seção marcada por span.dual-text-first com texto "Sobre o(a) curador(a)".
    Pegar o link cujo texto NÃO é um email.
    """
    for span in soup.find_all("span", class_="dual-text-first"):
        if "curador" in normalize(span.get_text(strip=True)):
            # Subir até a seção pai
            section = span.find_parent("section") or span.find_parent(
                "div", class_=lambda c: c and "kc_row" in " ".join(c)
            )
            if section:
                for a in section.find_all("a"):
                    text = a.get_text(strip=True)
                    href = a.get("href", "")
                    # Pular emails e links genéricos
                    if text and "@" not in text and "email-protection" not in href:
                        return text
    return ""


def yaml_escape(value: str) -> str:
    return value.replace('"', '\\"').replace('\n', ' ').replace('\r', '')


def build_front_matter(title: str, date: str, author: str, ficha: dict) -> str:
    midia_raw = ficha.get("midia", "")
    palavras  = [p.strip() for p in midia_raw.split(",") if p.strip()]
    if palavras:
        palavras_yaml = "\n".join(f'  - "{yaml_escape(p)}"' for p in palavras)
        palavras_field = f"palavras_chaves:\n{palavras_yaml}"
    else:
        palavras_field = "palavras_chaves: []"

    return f"""---
layout: meme/verbete
title: "{yaml_escape(title)}"
date: "{date}"
last_modified: ""
author: "{yaml_escape(author)}"
moldura: ""
category: ""
categoria: ""
tema: ""
ano_origem: "{yaml_escape(ficha.get('ano_origem', ''))}"
formato: "{yaml_escape(ficha.get('formato', ''))}"
criador: "{yaml_escape(ficha.get('criador', ''))}"
plataforma: "{yaml_escape(ficha.get('plataforma', ''))}"
{palavras_field}
featured: false
header_style: overlay
sidebar_position: right
header_image: /assets/img/photos/bg5.webp
featured_image: /assets/img/photos/b1.webp
excerpt: ""
tags: []
gallery: []
---"""


def build_body(sections: dict[str, str]) -> str:
    parts = []
    for heading, content in sections.items():
        if content:
            parts.append(f"## {heading}\n\n{content}")
    return "\n\n".join(parts)


# ──────────────────────────────────────────────
# Scraping de um verbete
# ──────────────────────────────────────────────

def scrape_verbete(url: str) -> tuple[str, str] | None:
    slug = urlparse(url).path.rstrip("/").split("/")[-1]
    try:
        resp = SESSION.get(url, timeout=30)
        resp.raise_for_status()
    except requests.RequestException as e:
        print(f"  ERRO HTTP: {e}")
        return None

    soup = BeautifulSoup(resp.text, "lxml")

    # Verificar se não foi bloqueado
    h1 = soup.find("h1")
    if h1 and "not acceptable" in h1.get_text(strip=True).lower():
        print(f"  BLOQUEADO pelo ModSecurity")
        return None

    date    = extract_date(soup)
    title   = extract_title(soup)
    curator = extract_curator(soup)
    ficha   = extract_ficha_tecnica(soup)
    sections = extract_sections(soup)

    front_matter = build_front_matter(title, date, curator, ficha)
    body         = build_body(sections)

    content  = f"{front_matter}\n\n{body}\n"
    filename = f"{date}-{slug}.md"
    return filename, content


# ──────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────

def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print(f"Buscando sitemap: {SITEMAP_URL}")
    urls = get_urls_from_sitemap(SITEMAP_URL)
    print(f"Total de verbetes no sitemap: {len(urls)}\n")

    stats = {"ok": 0, "erro": 0, "pulado": 0}

    for i, url in enumerate(urls, 1):
        slug = urlparse(url).path.rstrip("/").split("/")[-1]
        print(f"[{i:3d}/{len(urls)}] {slug}", end=" ... ", flush=True)

        existing = list(OUTPUT_DIR.glob(f"*-{slug}.md"))
        if existing:
            print(f"PULADO (já existe: {existing[0].name})")
            stats["pulado"] += 1
            continue

        result = scrape_verbete(url)

        if result is None:
            print("ERRO")
            stats["erro"] += 1
        else:
            filename, content = result
            out_path = OUTPUT_DIR / filename
            out_path.write_text(content, encoding="utf-8")
            print(f"OK → {filename}")
            stats["ok"] += 1

        time.sleep(DELAY_SECS)

    print(f"\n{'='*50}")
    print(f"Concluído: {stats['ok']} OK | {stats['erro']} ERROS | {stats['pulado']} PULADOS")
    print(f"Arquivos em: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
