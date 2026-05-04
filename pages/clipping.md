---
layout: default
title: "O #MUSEU na Mídia"
permalink: /museudememes/clipping/
redirect_from:
  - /museudememes/museu/por-que/na-midia/
custom_color: museudememes
custom_font: space
scroll_top_btn:
  enable: true

features18:
  enable: true
  services:
    - image: "/images_static/page_clipping01.png"
      image_2x: "/images_static/page_clipping01.png"
      alt: "O #MUSEUdeMEMES na Mídia"
      image_right: false
      icon: "/assets/img/icons/lineal/megaphone.svg"
      icon_bg: "bg-pale-primary"
      icon_color: "icon-svg-primary"
      title: "Presença na imprensa"
      description: "Acompanhe a cobertura jornalística do #MUSEUdeMEMES — reportagens, entrevistas e menções nos principais veículos de comunicação sobre memética e cultura digital brasileira."
      list_items:
        - "Reportagens e entrevistas sobre o acervo e as pesquisas"
        - "Cobertura de exposições e eventos institucionais"
        - "Menções em artigos de opinião e análises culturais"
      button:
        url: "#noticias"
        text: "Ver todas as notícias"
        class: "primary"
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
        <h1 class="display-1 mb-3">O #MUSEU <span class="underline-3 style-2 primary">na Mídia</span></h1>
        <p class="lead fs-lg px-md-12">Cobertura jornalística, entrevistas e menções ao #MUSEUdeMEMES na imprensa e nos meios digitais.</p>
      </div>
    </div>
  </div>
</section>

{% include components/sections/museudememes/features-18.html %}

{% include components/sections/museudememes/clipping-noticias.html %}

{% include components/footer/footer.html
    style="default"
    bg_color="bg-primary"
    text_color="text-inverse"
    widget_title_class="text-white"
    container_padding="pt-14 pb-13 pt-md-16 pb-md-15"
    cta=false
%}
</div>
