---
layout: default
title: "Nossas Exposições"
permalink: /museudememes/exposicoes/
redirect_from:
  - /museudememes/museu/por-que/nossas-exposicoes/
custom_color: museudememes
custom_font: space

hero34:
  background: "bg-gradient-primary"
  title: "Exposições do"
  typed_text:
    - "#MUSEUdeMEMES"
    - "Acervo Digital"
    - "Cultura de Internet"
    - "Memória Coletiva"
  subtitle: "Explore nossas exposições temáticas sobre memes, cultura digital e memória coletiva da internet brasileira."
  button:
    url: "/museudememes/acervo/"
    class: "btn btn-primary rounded-pill"
    label: "Ver o Acervo Completo"
  images:
    - image: "/assets/img/demos/vc1.webp"
      image2x: "/assets/img/demos/vc1@2x.webp"
    - image: "/assets/img/demos/vc2.webp"
      image2x: "/assets/img/demos/vc2@2x.webp"
    - image: "/assets/img/demos/vc3.webp"
      image2x: "/assets/img/demos/vc3@2x.webp"
    - image: "/assets/img/demos/vc4.webp"
      image2x: "/assets/img/demos/vc4@2x.webp"
    - image: "/assets/img/demos/vc5.webp"
      image2x: "/assets/img/demos/vc5@2x.webp"
    - image: "/assets/img/demos/vc6.webp"
      image2x: "/assets/img/demos/vc6@2x.webp"
    - image: "/assets/img/demos/vc7.webp"
      image2x: "/assets/img/demos/vc7@2x.webp"
    - image: "/assets/img/demos/vc8.webp"
      image2x: "/assets/img/demos/vc8@2x.webp"

counter:
  number: 4
  title: "Exposições temáticas sobre memes e cultura digital"
  subtitle: "Em destaque"

portfolio11:
  subtitle: "Curadoria Temática"
  title: "Exposições em destaque"
---
<div class="content-wrapper">
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

  {% include components/sections/demo34/hero.html %}
  {% include components/sections/museudememes/exposicoes-counter.html %}
  {% include components/sections/museudememes/portfolio-11.html %}

  {% include components/footer/footer.html
      style="default"
      bg_color="bg-primary"
      text_color="text-inverse"
      widget_title_class="text-white"
      container_padding="pt-14 pb-13 pt-md-16 pb-md-15"
      cta=false
  %}
</div>
