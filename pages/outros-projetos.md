---
layout: default
permalink: /museudememes/outros-projetos/
custom_color: museudememes
custom_font: space

features18:
  enable: true
  services:
    - image: /images_static/outros_oficinas.png
      image_2x: /images_static/outros_oficinas.png
      image_right: false
      icon: /assets/img/icons/lineal/rocket.svg
      icon_bg: bg-pale-primary
      icon_color: icon-svg-primary
      title: "Escritório Modelo de Memes"
      description: "Laboratório de pesquisa aplicada que reúne bolsistas, pesquisadores e projetos financiados em torno de questões emergentes da memética digital."
      list_items:
        - "Projetos com financiamento CNPq e FAPEMIG"
        - "Parcerias com grupos nacionais e internacionais"
        - "Produção científica em acesso aberto"
      button:
        url: "/museudememes/escritorio-modelo/"
        text: "Saiba mais"
        class: "primary"
    - image: /images_static/outros_memeclubes.png
      image_2x: /images_static/outros_memeclubes.png
      image_right: true
      icon: /assets/img/icons/lineal/browser.svg
      icon_bg: bg-pale-violet
      icon_color: icon-svg-violet
      title: "Exposições Digitais"
      description: "Experiências expositivas imersivas que levam o acervo e a pesquisa do museu a públicos amplos, por meio de plataformas digitais e instalações presenciais."
      list_items:
        - "Exposições temáticas com curadoria científica"
        - "Plataformas de visitação virtual"
        - "Catálogos digitais em acesso aberto"
      button:
        url: "/museudememes/exposicoes/"
        text: "Ver exposições"
        class: "violet"
    - image: /images_static/outros_lives.png
      image_2x: /images_static/outros_lives.png
      image_right: false
      icon: /assets/img/icons/lineal/award.svg
      icon_bg: bg-pale-yellow
      icon_color: icon-svg-yellow
      title: "Programa Educativo"
      description: "Ações de alfabetização midiática voltadas a estudantes, professores e pesquisadores, com oficinas, materiais didáticos e eventos de divulgação científica."
      list_items:
        - "Oficinas para escolas públicas"
        - "Materiais didáticos gratuitos para download"
        - "Seminários e eventos abertos à comunidade"
      button:
        url: "/museudememes/sobre/"
        text: "Conhecer o programa"
        class: "yellow"
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
        <h1 class="display-1 mb-3">Outros <span class="underline-3 style-1 primary"><em>Projetos</em></span></h1>
        <p class="lead fs-lg px-md-12">Iniciativas, programas e ações do #MUSEUdeMEMES além do acervo — pesquisa aplicada, exposições e educação midiática.</p>
      </div>
    </div>
  </div>
</section>

{% include components/sections/museudememes/features-18.html %}

{% include components/footer/footer.html
    style="default"
    bg_color="bg-primary"
    text_color="text-inverse"
    widget_title_class="text-white"
    container_padding="pt-14 pb-13 pt-md-16 pb-md-15"
    cta=false
%}
</div>
