---
layout: default
title: "Quem Faz o #MUSEUdeMEMES"
permalink: /museudememes/quem/
redirect_from:
  - /museudememes/expediente/
  - /museudememes/museu/quem-faz/
custom_color: museudememes
custom_font: space

features18:
  enable: true
  services:
    - image: "/assets/img/photos/about11.webp"
      image_2x: "/assets/img/photos/about11@2x.webp"
      alt: "Equipe do #MUSEUdeMEMES"
      image_right: false
      icon: "/assets/img/icons/solid/employees.svg"
      icon_bg: "bg-pale-primary"
      icon_color: "text-primary"
      title: "Uma equipe multidisciplinar"
      description: "O #MUSEUdeMEMES é constituído por pesquisadoras e pesquisadores de diversas áreas — comunicação, ciências sociais, museologia, design, educação e ciência da computação. Reunimos profissionais e estudantes que compartilham o interesse pela cultura de internet e acreditam no valor da memória digital como patrimônio coletivo. Nossa equipe atua de forma colaborativa e aberta, em constante diálogo com a comunidade acadêmica e com criadores de conteúdo digital."
      list_items:
        - "Pesquisa e curadoria de acervo digital"
        - "Gestão museológica e exposições"
        - "Produção editorial e comunicação"
        - "Desenvolvimento de tecnologias abertas"
      button:
        text: "Conheça o Acervo"
        url: "/museudememes/acervo/"
        class: "primary"

team3:
  subtitle: "Equipe"
  title: "Quem pesquisa e produz o museu."
  description: "Nossa equipe reúne pesquisadores, catalogadores, designers e comunicadores que trabalham diariamente para manter o acervo vivo e a pesquisa em memética digital avançando."

team2:
  subtitle: "Coordenação"
  title: "Board do #MUSEUdeMEMES"
  description: "A coordenação é composta por pesquisadoras e pesquisadores sênior responsáveis pelas diretrizes institucionais, parcerias e projetos estratégicos do museu."
  button:
    label: "Fale Conosco"
    url: "/contact/"
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
          <p class="fs-16 text-uppercase text-muted mb-3">Expediente</p>
          <h1 class="display-1 mb-3">As pessoas que fazem o <span class="underline-3 style-1 primary"><em>#MUSEUdeMEMES</em></span> acontecer.</h1>
          <p class="lead fs-lg px-md-12">Pesquisadores, curadores, designers e comunicadores unidos pela preservação da memória digital brasileira.</p>
        </div>
      </div>
    </div>
  </section>

  {% include components/sections/museudememes/features-18.html %}
  {% include components/sections/museudememes/team-2.html %}
  {% include components/sections/museudememes/team-3.html %}

  {% include components/footer/footer.html
      style="default"
      bg_color="bg-primary"
      text_color="text-inverse"
      widget_title_class="text-white"
      container_padding="pt-14 pb-13 pt-md-16 pb-md-15"
      cta=false
  %}
</div>
