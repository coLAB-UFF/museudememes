---
layout: default
title: "Escritório Modelo de Memes"
permalink: /museudememes/escritorio-modelo/
custom_color: museudememes
custom_font: space

facts7:
  subtitle: "Em Números"
  title: "O Escritório Modelo"
  highlight: "produz e pesquisa"
  title_end: "cultura de internet."
  description:
    - "O Escritório Modelo de Memes é o laboratório criativo do #MUSEUdeMEMES — um espaço de pesquisa aplicada, formação profissional e produção de conhecimento sobre memética digital."
    - "Aqui desenvolvemos metodologias originais, formamos pesquisadores e produzimos publicações que alimentam tanto o acervo do museu quanto o debate acadêmico sobre cultura de internet."
  items:
    - value: 85
      color: "primary"
      title: "Projetos catalogados"
    - value: 72
      color: "yellow"
      title: "Pesquisadores formados"
    - value: 90
      color: "green"
      title: "Acervos organizados"
    - value: 65
      color: "violet"
      title: "Publicações abertas"

features5:
  shape_color: "primary"
  title: "Onde a pesquisa encontra a criação"
  description: "O Escritório reúne pesquisadores, criadores de conteúdo e profissionais de comunicação para produzir conhecimento sobre memética digital de forma colaborativa e aberta."
  list_color: "primary"
  list_icon: "uil uil-check"
  image_columns:
    - images:
        - src: "/images_static/page_escritorio02.png"
          srcset: ""
          alt: "Escritório Modelo"
          classes: "mb-5"
        - src: "/images_static/meme_ata.png"
          srcset: ""
          alt: "Pesquisa de memes"
          classes: ""
    - images:
        - src: "/images_static/meme_sombrio.png"
          srcset: ""
          alt: "Catalogação digital"
          classes: "mb-5"
        - src: "/images_static/meme_quarta.png"
          srcset: ""
          alt: "Produção de conteúdo"
          classes: ""
  lists:
    - items:
        - "Pesquisa aplicada em memética"
        - "Formação de pesquisadores"
        - "Curadoria colaborativa"
    - items:
        - "Produção editorial aberta"
        - "Parcerias acadêmicas"
        - "Relatórios de pesquisa"

features6:
  image:
    src: "/images_static/page_escritorio01.png"
    srcset: ""
    alt: "Ferramentas do Escritório Modelo"
  title: "Metodologias abertas para a memética digital"
  description: "Desenvolvemos e aplicamos protocolos originais para coleta, análise e catalogação de memes — todos disponíveis abertamente para uso por outros pesquisadores e instituições."
  list_color: "yellow"
  list_icon: "uil uil-check"
  lists:
    - items:
        - "Thesaurus de cultura digital"
        - "Protocolos de catalogação"
        - "Ferramentas de análise de rede"
    - items:
        - "Guias de alfabetização midiática"
        - "Bases de dados abertas"
        - "Kits educativos"

cta4:
  bg_class: "bg-primary"
  subtitle: "Colabore com o Escritório"
  title: "Junte-se à"
  title_highlight: "pesquisa"
  highlight_style: "underline-3 style-2 yellow"
  title_end: "sobre cultura de internet"
  button:
    label: "Fale com a Equipe"
    url: "/contact/"
    style: "btn btn-white rounded-pill"

escritorio_final:
  subtitle: "O que fazemos"
  title: "Pesquisa, formação e produção em memética digital"
  description: "Do levantamento de acervos à publicação de pesquisas, o Escritório Modelo de Memes cobre todo o ciclo de conhecimento sobre cultura de internet — com rigor acadêmico e abertura colaborativa."
  button:
    label: "Conheça o Acervo"
    url: "/museudememes/acervo/"
    class: "btn btn-primary rounded-pill"
  features:
    - icon: "/assets/img/icons/solid/bulb.svg"
      label: "Pesquisa aplicada"
    - icon: "/assets/img/icons/solid/graph.svg"
      label: "Análise de dados"
    - icon: "/assets/img/icons/solid/pen-tool.svg"
      label: "Produção editorial"
    - icon: "/assets/img/icons/solid/rocket.svg"
      label: "Publicação aberta"
---
<div class="content-wrapper">
  <header class="wrapper bg-white">
    {% include components/navbar/navbar.html
        classList="center-nav navbar-light"
        centerNav=true
        otherClassList="w-100 d-flex ms-auto"
        otherBtn=true
        otherBtnClassList="btn btn-sm btn-primary rounded"
        otherBtnText="Área Restrita"
        otherBtnLink="/museudememes/admin"
    %}
  </header>

  <section class="wrapper bg-soft-primary">
    <div class="container pt-10 pb-14 pt-md-14 pb-md-17 text-center">
      <div class="row">
        <div class="col-lg-9 col-xxl-8 mx-auto">
          <h1 class="display-1 mb-3">Escritório <span class="underline-3 style-1 primary"><em>Modelo</em></span> de Memes</h1>
          <p class="lead fs-lg px-md-12">Laboratório de pesquisa aplicada, formação e produção de conhecimento sobre memética digital e cultura de internet.</p>
        </div>
      </div>
    </div>
  </section>

  {% include components/sections/museudememes/facts-7.html %}
  {% include components/sections/museudememes/features-6.html %}
  {% include components/sections/museudememes/features-5.html %}
  {% include components/sections/museudememes/cta-4.html %}
  {% include components/sections/museudememes/escritorio-final.html %}
  {% include components/sections/demo34/screenshots.html %}

  {% include components/footer/footer.html
      style="default"
      bg_color="bg-primary"
      text_color="text-inverse"
      widget_title_class="text-white"
      container_padding="pt-14 pb-13 pt-md-16 pb-md-15"
      cta=false
  %}
</div>
