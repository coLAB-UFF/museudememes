# Manual de Edição — #MUSEUdeMEMES
> Referência técnica para criação e edição de conteúdo no site Jekyll.  
> Este arquivo alimentará o manual formal quando solicitado.

---

## 1. Layout dos Posts do Blog

Todo post do blog usa:

```yaml
layout: museudememes/artigo
```

O arquivo de layout está em `_layouts/museudememes/artigo.html`.  
Ele carrega automaticamente o esquema de cores violeta/âmbar/lilás (museudememes).

---

## 2. Front Matter — Campos Padrão

```yaml
---
layout: museudememes/artigo
title: "Título do Post"
date: 2025-04-01
last_modified: 2025-04-10          # exibido como "Última atualização"
authors_line: "Jane Smith & John Doe"  # string de exibição no header e nas listagens
authors:                           # array para busca de cards com avatar/bio
  - Jane Smith
  - John Doe
category: Pesquisa                 # categoria principal (uma só)
featured_image: /assets/img/photos/bg5.webp  # imagem de destaque (opcional)
excerpt: "Breve descrição para listagens."
tags:
  - Tag Um
  - Tag Dois
---
```

### Regras dos campos de autores

| Campo | Tipo | Uso |
|---|---|---|
| `authors_line` | string | Exibido no header do artigo e nas listagens do blog |
| `authors` | array de nomes | Usado para buscar avatar, cargo e bio em `_data/team_members.yml` e `_data/team_board.yml` |

- Se o nome em `authors` não corresponder a nenhum membro registrado nos dados, o card exibe ícone genérico + nome.
- `authors_line` pode ser qualquer string: `"Jane Smith"`, `"Jane Smith & John Doe"`, `"Equipe MUSEUdeMEMES"` etc.

---

## 3. Galeria de Imagens Inline

### Declaração no front matter

Cada galeria recebe um nome livre (ex: `galeria_variacoes`, `galeria_contexto`).  
Cada item tem `url` (obrigatório) e `alt` (opcional, vira legenda no lightbox).

```yaml
galeria_variacoes:
  - url: /assets/img/photos/b1.webp
    alt: "Variação original do meme"
  - url: /assets/img/photos/b2.webp
    alt: "Remix norte-americano"
  - url: /assets/img/photos/b3.webp
    alt: "Versão brasileira com legenda"
  - url: /assets/img/photos/b4.webp
    alt: "Adaptação política — eleições 2022"
```

### Uso no corpo do post

```liquid
{% include components/blog/gallery.html id="galeria_variacoes" cols=2 %}
{% include components/blog/gallery.html id="galeria_contexto" cols=3 caption="Legenda opcional da galeria" %}
```

| Parâmetro | Obrigatório | Descrição |
|---|---|---|
| `id` | Sim | Nome da chave no front matter |
| `cols` | Não (padrão: 2) | Número de colunas no desktop (2–5) |
| `caption` | Não | Legenda exibida abaixo da galeria |

#### Combinações comuns

| Front matter (n imagens) | `cols=` | Resultado |
|---|---|---|
| 2 imagens | `cols=2` | 1 linha × 2 colunas |
| 4 imagens | `cols=2` | 2 linhas × 2 colunas |
| 3 imagens | `cols=3` | 1 linha × 3 colunas |
| 6 imagens | `cols=3` | 2 linhas × 3 colunas |
| 4 imagens | `cols=4` | 1 linha × 4 colunas |
| 8 imagens | `cols=4` | 2 linhas × 4 colunas |

No mobile, a galeria sempre colapsa para 2 colunas (`row-cols-2`).  
As imagens se expandem via glightbox ao clicar (agrupadas por galeria).

---

## 4. Embeds de Vídeo e Mídia

### YouTube

```liquid
{% include components/blog/embed.html platform="youtube" id="dQw4w9WgXcQ" %}
```

Gera iframe 16:9 responsivo com `rel=0` (sem vídeos sugeridos).

### TikTok

```liquid
{% include components/blog/embed.html platform="tiktok" id="7123456789012345678" %}
```

O `id` é o número no final da URL do TikTok (ex: `tiktok.com/@user/video/7123456789012345678`).  
Renderiza iframe centralizado de 325 × 740px.

### Tumblr

```liquid
{% include components/blog/embed.html platform="tumblr" id="SEU-BLOG.tumblr.com/post/123456" ratio="4x3" %}
```

### iframe genérico

```liquid
{% include components/blog/embed.html platform="iframe" url="https://example.com/embed" ratio="16x9" %}
```

| Parâmetro | Opções | Padrão |
|---|---|---|
| `platform` | `youtube`, `tiktok`, `tumblr`, `iframe` | — |
| `id` | string | — |
| `url` | URL completa (só para `iframe` genérico) | — |
| `ratio` | `16x9`, `4x3`, `1x1`, `21x9` | `16x9` |

---

## 5. Tags

Tags declaradas no front matter aparecem automaticamente como pílulas coloridas (lilás) ao fim do texto.

```yaml
tags:
  - Memética
  - Cultura Digital
  - Brasil
```

Cada tag leva a `/blog/tag/nome-da-tag/`.  
Não há limite de tags, mas recomenda-se no máximo 5.

---

## 6. Molduras SVG (Verbetes do Acervo)

Para os verbetes (`_memes/*.md`), a imagem de destaque pode ser emoldurada com SVGs da pasta `/molduras/`.

```yaml
feature_meme_image: /assets/img/memes/capivara.webp
moldura: moldura_circle   # nome do arquivo SVG sem extensão
```

Se `moldura:` for omitido, a imagem aparece sem moldura (retangular arredondada).  
Se `feature_meme_image:` for omitido, usa `hero_image:`; se ausente, usa `featured_image:`.

### Molduras disponíveis

| Valor do campo `moldura:` | Descrição |
|---|---|
| `moldura_circle` | Círculo central |
| `moldura_laranja` | Moldura laranja retangular |
| `moldura_lilas` | Moldura lilás retangular |
| `moldura_landscape_verde` | Paisagem — verde |
| `moldura_landscape_paspatur_verde` | Paisagem com paspatur — verde |
| `moldura_landscape_rosa` | Paisagem — rosa |
| `moldura_landscape_amarela` | Paisagem — amarela |
| `moldura_landscape_vermelha` | Paisagem — vermelha |
| `moldura_portrait_rustica` | Retrato rústico |

Qualquer novo arquivo `.svg` adicionado à pasta `/molduras/` funciona automaticamente — basta indicar o nome (sem `.svg`) no campo `moldura:`.

---

## 7. Campos dos Verbetes do Acervo (`_memes/*.md`)

```yaml
layout: meme/verbete          # definido automaticamente pelo _config.yml
title: "Nome do Meme"
nome_meme: "Capivara do WhatsApp"  # subtítulo descritivo (fallback: title)
authors_line: "Jane Smith"
authors:
  - Jane Smith
date: 2025-01-15
last_modified: 2025-03-05
hero_image: /assets/img/photos/pp7.webp
feature_meme_image: /assets/img/memes/capivara.webp
moldura: moldura_circle
criador: "Anônimo"
ano_origem: "2020"
plataforma: "WhatsApp"        # string ou array
formato: "Imagem"
categoria: "Meme de Humor"
tema: "Fauna Brasileira"
palavras_chaves:
  - capivara
  - animais
  - humor
gallery:
  - url: /assets/img/photos/pp2.webp
    alt: "Variação 1"
  - url: /assets/img/photos/pp3.webp
    alt: "Variação 2"
```

### Seções do corpo do verbete

O corpo segue 5 seções recomendadas:

```markdown
## Descrição Geral
## Origens
## Disseminação
## Estética e Linguagem
## Impacto Social e Cultural
```

---

## 8. Dados de Autores / Curadores

Os cards de autores e curadores buscam dados em:

- `_data/team_members.yml` → campo `members`
- `_data/team_board.yml` → campo `members`

Cada entrada deve ter:

```yaml
- name: "Jane Smith"          # deve corresponder exatamente ao valor em authors: ou page.author:
  role: "Pesquisadora Sênior"
  bio: "Mini-bio exibida no card."
  avatar_image: /assets/img/avatars/jane.webp
  avatar_image2x: /assets/img/avatars/jane@2x.webp   # opcional
```

Se o nome não for encontrado nos dados, o card exibe um ícone genérico com o nome.

---

*Última atualização deste arquivo: 2026-04-16*
