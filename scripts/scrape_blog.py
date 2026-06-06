#!/usr/bin/env python3
"""
Scraper de posts do blog museudememes.com.br → arquivos .md para Jekyll.

Uso:
    python scripts/scrape_blog.py

Dependências:
    pip install requests beautifulsoup4 markdownify lxml
"""

import os
import re
import json
import time
import mimetypes
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup, NavigableString, Tag
import markdownify

# ──────────────────────────────────────────────
# Configuração
# ──────────────────────────────────────────────

BLOG_SITEMAP_URL = "https://museudememes.com.br/wp-sitemap-posts-post-1.xml"
REST_API_URL     = "https://museudememes.com.br/wp-json/wp/v2/posts"
OUTPUT_DIR       = Path(__file__).parent.parent / "_posts"
IMAGES_DIR       = Path.home() / "Downloads" / "museudememes-blog-images"
ASSETS_PATH      = "/assets/img/blog"   # prefixo YAML — usuário moverá depois
DELAY_SECS       = 1.5
DEFAULT_DATE     = "2020-01-01"

# Palavras que identificam imagens de logo/rodapé a ignorar
SKIP_IMG_WORDS = ["logo", "logofinal", "colab-foo", "uff-foo", "inct-foo",
                  "tag-", "avatar", "gravatar"]

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

# Session separada para API JSON
API_HEADERS = HEADERS.copy()
API_HEADERS["Accept"] = "application/json,*/*;q=0.8"
API_SESSION = requests.Session()
API_SESSION.headers.update(API_HEADERS)


# ──────────────────────────────────────────────
# markdownify customizado
# ──────────────────────────────────────────────

class BlogMarkdownConverter(markdownify.MarkdownConverter):
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

    def convert_img(self, el, text, **kwargs):
        # Imagens já foram removidas do soup antes da conversão —
        # se alguma sobrar (não filtrada), ignorar.
        return ""


def html_to_md(html_fragment: str) -> str:
    md = BlogMarkdownConverter(
        heading_style=markdownify.ATX,
        bullets="-",
        strip=["style", "script"],
    ).convert(html_fragment)
    md = re.sub(r'\n{3,}', '\n\n', md)
    return md.strip()


def yaml_escape(value: str) -> str:
    return value.replace('"', '\\"').replace('\n', ' ').replace('\r', '')


# ──────────────────────────────────────────────
# Fontes de dados
# ──────────────────────────────────────────────

def get_urls_from_sitemap(sitemap_url: str) -> list[str]:
    resp = SESSION.get(sitemap_url, timeout=30)
    resp.raise_for_status()
    root = ET.fromstring(resp.content)
    ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    return [loc.text.strip() for loc in root.findall(".//sm:loc", ns)]


def get_dates_from_api() -> dict[str, str]:
    """Retorna dict slug → 'YYYY-MM-DD' via WP REST API."""
    dates = {}
    page = 1
    while True:
        resp = API_SESSION.get(
            REST_API_URL,
            params={"per_page": 100, "_fields": "date,slug", "page": page},
            timeout=30,
        )
        if resp.status_code == 400:
            break  # sem mais páginas
        resp.raise_for_status()
        data = resp.json()
        if not data:
            break
        for post in data:
            dates[post["slug"]] = post["date"][:10]
        if len(data) < 100:
            break
        page += 1
    return dates


# ──────────────────────────────────────────────
# Extração de metadados
# ──────────────────────────────────────────────

def extract_title(soup: BeautifulSoup) -> str:
    og = soup.find("meta", property="og:title")
    if og and og.get("content"):
        title = og["content"].strip()
        title = re.sub(r'\s*[–\-]\s*#?MUSEUdeMEMES.*$', '', title, flags=re.I).strip()
        if title:
            return title
    h1 = soup.find("h1")
    return h1.get_text(strip=True) if h1 else ""


def extract_excerpt(soup: BeautifulSoup) -> str:
    og = soup.find("meta", property="og:description")
    if og and og.get("content"):
        return og["content"].strip()
    desc = soup.find("meta", attrs={"name": "description"})
    if desc and desc.get("content"):
        return desc["content"].strip()
    return ""


def extract_featured_image_url(soup: BeautifulSoup) -> str:
    """URL da imagem destaque (não baixa ainda)."""
    img_div = soup.find("div", class_="blog-four__image")
    if img_div:
        img = img_div.find("img")
        if img and img.get("src"):
            return img["src"]
    og = soup.find("meta", property="og:image")
    if og and og.get("content"):
        return og["content"].strip()
    return ""


def extract_categoria(soup: BeautifulSoup) -> str:
    for a in soup.find_all("a", rel=True):
        rel = " ".join(a.get("rel", []))
        if "category" in rel:
            return a.get_text(strip=True)
    return ""


def extract_tags(soup: BeautifulSoup) -> list[str]:
    tags = []
    for a in soup.find_all("a", rel=True):
        rel = " ".join(a.get("rel", []))
        if rel.strip() == "tag":
            text = a.get_text(strip=True)
            if text:
                tags.append(text)
    return tags


def extract_authors(soup: BeautifulSoup, content_div: Tag | None) -> list[str]:
    """
    Extrai autores/tradutores da caixa de autor (kc-feature-boxes) dentro do conteúdo.
    Fallback: link /author/ na página.
    """
    authors = []

    if content_div:
        for fb in content_div.find_all(class_="kc-feature-boxes"):
            pos_el    = fb.find(class_="content-position")
            title_el  = fb.find(class_="content-title")
            if not title_el:
                continue
            pos_text = pos_el.get_text(strip=True) if pos_el else ""
            name     = title_el.get_text(strip=True)
            if name and ("por" in pos_text.lower() or "tradução" in pos_text.lower() or "traducao" in pos_text.lower()):
                if name not in authors:
                    authors.append(name)

    if not authors:
        # Fallback: WP author link
        for a in soup.find_all("a", href=lambda h: h and "/author/" in h):
            name = a.get_text(strip=True)
            if name and name not in authors:
                authors.append(name)

    return authors


# ──────────────────────────────────────────────
# Extração de imagens + download
# ──────────────────────────────────────────────

def should_skip_img(src: str) -> bool:
    src_lower = src.lower()
    return any(word in src_lower for word in SKIP_IMG_WORDS)


def get_ext_from_response(resp: requests.Response, url: str) -> str:
    """Determina extensão do arquivo pela URL ou Content-Type."""
    parsed_path = urlparse(url).path
    _, ext = os.path.splitext(parsed_path)
    if ext and len(ext) <= 5:
        return ext.lower()
    ct = resp.headers.get("Content-Type", "")
    ext = mimetypes.guess_extension(ct.split(";")[0].strip()) or ".jpg"
    # mimetypes às vezes retorna .jpe — normalizar
    if ext == ".jpe":
        ext = ".jpg"
    return ext


def download_image(url: str, dest: Path) -> bool:
    """Baixa uma imagem para dest. Retorna True se ok."""
    try:
        resp = SESSION.get(url, timeout=30, stream=True)
        resp.raise_for_status()
        dest.write_bytes(resp.content)
        return True
    except Exception as e:
        print(f"    [img] ERRO ao baixar {url}: {e}")
        return False


def collect_and_remove_content_images(
    content_div: Tag,
    slug: str,
    featured_url: str,
) -> tuple[list[dict], str | None]:
    """
    Coleta todas as <img> relevantes de content_div, remove-as do soup
    e faz download para ~/Downloads/museudememes-blog-images/{slug}/.

    Retorna:
      - galeria: lista de dicts {url: str, alt: str}  (com paths YAML)
      - featured_local_path: path YAML para a imagem destaque, ou None
    """
    slug_dir = IMAGES_DIR / slug
    slug_dir.mkdir(parents=True, exist_ok=True)

    # 1) Imagem destaque
    featured_local = None
    if featured_url and not should_skip_img(featured_url):
        resp = None
        try:
            resp = SESSION.get(featured_url, timeout=30, stream=True)
            resp.raise_for_status()
            ext = get_ext_from_response(resp, featured_url)
            fname = f"featured{ext}"
            dest = slug_dir / fname
            dest.write_bytes(resp.content)
            featured_local = f"{ASSETS_PATH}/{slug}/{fname}"
        except Exception as e:
            print(f"    [featured] ERRO: {e}")

    # 2) Imagens inline do conteúdo
    galeria = []
    img_counter = 0

    # Coletar todas as imgs antes de remover
    imgs_to_process = []
    for img in content_div.find_all("img"):
        src = img.get("src", "")
        if not src:
            continue
        if should_skip_img(src):
            continue
        if "museudememes" not in src and "wp-content" not in src:
            continue
        # Pular se é a mesma que a featured
        if src == featured_url:
            img.decompose()
            continue
        # Pular versões redimensionadas da featured (ex: -1086x420)
        featured_base = re.sub(r'-\d+x\d+(\.\w+)$', r'\1', featured_url) if featured_url else ""
        if featured_base and featured_base in src:
            img.decompose()
            continue
        imgs_to_process.append(img)

    for img in imgs_to_process:
        src = img.get("src", "")
        alt = img.get("alt", "")
        img_counter += 1
        fname_stem = f"img-{img_counter:03d}"

        try:
            resp = SESSION.get(src, timeout=30, stream=True)
            resp.raise_for_status()
            ext = get_ext_from_response(resp, src)
            fname = f"{fname_stem}{ext}"
            dest = slug_dir / fname
            dest.write_bytes(resp.content)
            galeria.append({
                "url": f"{ASSETS_PATH}/{slug}/{fname}",
                "alt": alt,
            })
        except Exception as e:
            print(f"    [img-{img_counter:03d}] ERRO: {e}")

        img.decompose()

    # Remover <figure> que ficaram vazias após remover imgs
    for fig in content_div.find_all("figure"):
        if not fig.find("iframe") and not fig.get_text(strip=True):
            fig.decompose()

    return galeria, featured_local


# ──────────────────────────────────────────────
# Extração de conteúdo
# ──────────────────────────────────────────────

def extract_content(content_div: Tag) -> str:
    """
    Converte div.text em markdown após:
    - Remover caixas de autor (kc-feature-boxes)
    - Remover <style> e <script> do KingComposer
    - Imagens já foram removidas em etapa anterior
    """
    # Remover caixas de autor
    for fb in content_div.find_all(class_="kc-feature-boxes"):
        fb.decompose()

    # Remover a div vazia kc_clfw que fica no topo
    for el in content_div.find_all(class_="kc_clfw"):
        el.decompose()

    # Remover <style> inline do KingComposer (frequentes e poluem o markdown)
    for style in content_div.find_all("style"):
        style.decompose()

    html_str = str(content_div)
    return html_to_md(html_str)


# ──────────────────────────────────────────────
# Montagem do arquivo .md
# ──────────────────────────────────────────────

def build_front_matter(
    title: str,
    date: str,
    authors: list[str],
    categoria: str,
    tags: list[str],
    featured_image: str,
    excerpt: str,
    galeria: list[dict],
) -> str:
    authors_line = " & ".join(authors) if authors else ""

    authors_yaml = ""
    if authors:
        lines = "\n".join(f'  - "{yaml_escape(a)}"' for a in authors)
        authors_yaml = f"authors:\n{lines}"
    else:
        authors_yaml = "authors: []"

    tags_yaml = ""
    if tags:
        lines = "\n".join(f'  - "{yaml_escape(t)}"' for t in tags)
        tags_yaml = f"tags:\n{lines}"
    else:
        tags_yaml = "tags: []"

    galeria_yaml = ""
    if galeria:
        items = []
        for item in galeria:
            items.append(f'  - url: {item["url"]}\n    alt: "{yaml_escape(item["alt"])}"')
        galeria_yaml = "galeria_imagens:\n" + "\n".join(items)
    else:
        galeria_yaml = "galeria_imagens: []"

    return f"""---
layout: museudememes/artigo
title: "{yaml_escape(title)}"
date: "{date}"
last_modified: ""
authors_line: "{yaml_escape(authors_line)}"
{authors_yaml}
categoria: "{yaml_escape(categoria)}"
featured_image: {featured_image or "/assets/img/photos/bg5.webp"}
excerpt: "{yaml_escape(excerpt)}"
{tags_yaml}
{galeria_yaml}
---"""


def build_body(content_md: str, has_gallery: bool) -> str:
    body = content_md
    if has_gallery:
        body += "\n\n{% include components/blog/gallery.html id=\"galeria_imagens\" cols=2 %}"
    return body


# ──────────────────────────────────────────────
# Scraping de um post
# ──────────────────────────────────────────────

def scrape_post(url: str, date_from_api: str) -> tuple[str, str] | None:
    slug = urlparse(url).path.rstrip("/").split("/")[-1]

    try:
        resp = SESSION.get(url, timeout=30)
        resp.raise_for_status()
    except requests.RequestException as e:
        print(f"  ERRO HTTP: {e}")
        return None

    soup = BeautifulSoup(resp.text, "lxml")

    # Verificar bloqueio ModSecurity
    h1 = soup.find("h1")
    if h1 and "not acceptable" in h1.get_text(strip=True).lower():
        print(f"  BLOQUEADO pelo ModSecurity")
        return None

    content_div = soup.find("div", class_="text")

    # Metadados
    title          = extract_title(soup)
    date           = date_from_api or DEFAULT_DATE
    excerpt        = extract_excerpt(soup)
    categoria      = extract_categoria(soup)
    tags           = extract_tags(soup)
    featured_url   = extract_featured_image_url(soup)
    authors        = extract_authors(soup, content_div)

    # Imagens: coletar, baixar e remover do soup
    galeria, featured_local = collect_and_remove_content_images(
        content_div, slug, featured_url
    ) if content_div else ([], None)

    # Conteúdo em markdown
    content_md = extract_content(content_div) if content_div else ""

    # Front matter
    front_matter = build_front_matter(
        title=title,
        date=date,
        authors=authors,
        categoria=categoria,
        tags=tags,
        featured_image=featured_local or (f"{ASSETS_PATH}/{slug}/featured.jpg" if featured_url else ""),
        excerpt=excerpt,
        galeria=galeria,
    )

    body     = build_body(content_md, bool(galeria))
    content  = f"{front_matter}\n\n{body}\n"
    filename = f"{date}-{slug}.md"
    return filename, content


# ──────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────

def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)

    print("Buscando datas via WP REST API...")
    dates = get_dates_from_api()
    print(f"  {len(dates)} posts com data encontrados\n")

    print(f"Buscando sitemap: {BLOG_SITEMAP_URL}")
    urls = get_urls_from_sitemap(BLOG_SITEMAP_URL)
    print(f"Total de posts no sitemap: {len(urls)}\n")

    stats = {"ok": 0, "erro": 0, "pulado": 0}

    for i, url in enumerate(urls, 1):
        slug = urlparse(url).path.rstrip("/").split("/")[-1]
        print(f"[{i:2d}/{len(urls)}] {slug}", end=" ... ", flush=True)

        existing = list(OUTPUT_DIR.glob(f"*-{slug}.md"))
        if existing:
            print(f"PULADO (já existe: {existing[0].name})")
            stats["pulado"] += 1
            continue

        date_from_api = dates.get(slug, DEFAULT_DATE)
        result = scrape_post(url, date_from_api)

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
    print(f"Arquivos .md em: {OUTPUT_DIR}")
    print(f"Imagens em:      {IMAGES_DIR}")


if __name__ == "__main__":
    main()
