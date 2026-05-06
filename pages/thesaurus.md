---
layout: default
title: "Thesaurus"
permalink: /museudememes/thesaurus/
custom_color: museudememes
custom_font: space
scroll_top_btn:
  enable: true

features18:
  enable: true
  services:
    - image: /images_static/page_thesaurus01.png
      image_2x: /images_static/page_thesaurus01.png
      alt: "Diagrama de conceitos do Thesaurus de Memes"
      image_right: false
      icon: /assets/img/icons/lineal/agenda.svg
      icon_bg: bg-pale-primary
      icon_color: icon-svg-primary
      title: "Um vocabulário vivo da cultura digital"
      description: "O Thesaurus do #MUSEUdeMEMES é um vocabulário controlado e colaborativo que reúne os principais conceitos, categorias e termos utilizados no estudo, catalogação e análise dos memes como objetos culturais."
      list_items:
        - "Termos definidos com base em referências acadêmicas em memética, semiótica e comunicação digital."
        - "Cada entrada inclui definição, categorias, relações com outros conceitos e exemplos documentados no acervo."
        - "Atualizado continuamente pela equipe de pesquisa e curadoria do museu."
        - "Ferramenta de referência para pesquisadores, educadores e curadores."
      button:
        url: "/museudememes/acervo/"
        text: "Explorar o Acervo"
        class: "primary"
---
<div class="content-wrapper">
<header class="wrapper bg-white">
  {% include components/navbar/navbar.html
      classList="center-nav navbar-light"
      centerNav=true
      logoAlt=false
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
        <h1 class="display-1 mb-3"><span class="underline-3 style-1 primary"><em>Thesaurus</em></span> de Memes</h1>
        <p class="lead fs-lg px-md-12">Vocabulário controlado do #MUSEUdeMEMES — conceitos, categorias e termos para o estudo da cultura de internet e da memética digital.</p>
      </div>
    </div>
  </div>
</section>

{% include components/sections/museudememes/features-18.html %}

{% include components/sections/museudememes/thesaurus-entries.html %}

{% include components/footer/footer.html
    style="default"
    bg_color="bg-primary"
    text_color="text-inverse"
    widget_title_class="text-white"
    container_padding="pt-14 pb-13 pt-md-16 pb-md-15"
    cta=false
%}
</div>
