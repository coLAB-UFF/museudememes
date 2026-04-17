---
layout: default
title: "Referências"
permalink: /museudememes/referencias/
custom_color: museudememes
custom_font: space

hero:
  title: "Banco de Referências"
  subtitle: "Pesquise artigos, livros e textos acadêmicos sobre memética digital e cultura de internet."
  buttons:
    - label: "Ver Acervo"
      url: /museudememes/acervo/
      class: "btn-lg btn-primary rounded-pill me-2"
    - label: "Contribuir"
      url: "https://docs.google.com/spreadsheets/d/1hBXejeFBPMGAhKx028zAgcgTje5ln35l75npiI7Mfjs/edit"
      class: "btn-lg btn-outline-primary rounded-pill"

  image: /assets/img/photos/sa1.webp
  image2x: /assets/img/photos/sa1@2x.webp

features17:
  enable: true
  subtitle: "Áreas Temáticas"
  title:
    before: "Explore referências por"
    highlight: "área"
    after: "de conhecimento."
  features:
    - title: "Comunidades e Subculturas"
      icon: "/assets/img/icons/solid/team.svg"
      bg_color: "bg-pale-purple"
      icon_color: "text-purple"
      description: "Grupos de interesse, fandoms e microculaturas digitais."
    - title: "Emoções e Afeto"
      icon: "/assets/img/icons/solid/love.svg"
      bg_color: "bg-pale-pink"
      icon_color: "text-pink"
      description: "Expressão emocional e vínculos sociais mediados por memes."
    - title: "Imagem e Cultura Vernacular"
      icon: "/assets/img/icons/solid/image.svg"
      bg_color: "bg-pale-yellow"
      icon_color: "text-yellow"
      description: "Produção imagética não-profissional e remix visual em rede."
    - title: "Internet e Política"
      icon: "/assets/img/icons/solid/bullhorn.svg"
      bg_color: "bg-pale-red"
      icon_color: "text-red"
      description: "Memes em campanhas, ativismo e comunicação política online."
    - title: "Marketing e Consumo"
      icon: "/assets/img/icons/solid/shopping-bag.svg"
      bg_color: "bg-pale-orange"
      icon_color: "text-orange"
      description: "Publicidade, branding e estratégias de marketing viral."
    - title: "Media Literacy e Educação"
      icon: "/assets/img/icons/solid/clipboard.svg"
      bg_color: "bg-pale-green"
      icon_color: "text-green"
      description: "Letramento midiático e uso pedagógico de memes."
    - title: "Narrativa e Linguagem"
      icon: "/assets/img/icons/solid/chatting.svg"
      bg_color: "bg-pale-violet"
      icon_color: "text-violet"
      description: "Intertextualidade, formatos narrativos e semiótica dos memes."
    - title: "Psicologia e Cognição"
      icon: "/assets/img/icons/solid/bulb.svg"
      bg_color: "bg-pale-sky"
      icon_color: "text-sky"
      description: "Processos cognitivos e comportamento nas redes digitais."
    - title: "Redes Sociais e Viralidade"
      icon: "/assets/img/icons/solid/sharing.svg"
      bg_color: "bg-pale-fuchsia"
      icon_color: "text-fuchsia"
      description: "Propagação viral, algoritmos e dinâmicas de plataformas."
    - title: "Sociobiologia e Filosofia"
      icon: "/assets/img/icons/solid/layers.svg"
      bg_color: "bg-pale-navy"
      icon_color: "text-navy"
      description: "Fundamentos evolucionistas e teoria memética clássica."
    - title: "Outros"
      icon: "/assets/img/icons/solid/note.svg"
      bg_color: "bg-pale-ash"
      icon_color: "text-muted"
      description: "Referências que não se enquadram nas demais categorias."

referencias:
  title: "Base de Referências"
  subtitle: "Atualizada automaticamente via Google Sheets"
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
        otherLink=true
        otherLinkText="Sign In"
        otherLinkModal="modal-signin"
        otherBtnText="Sign Up"
        otherBtnModal="modal-signup"
    %}
  </header>

  <section class="wrapper bg-soft-primary">
    <div class="container pt-10 pb-14 pt-md-14 pb-md-17 text-center">
      <div class="row">
        <div class="col-lg-9 col-xxl-8 mx-auto">
          <h1 class="display-1 mb-3">Banco de <span class="underline-3 style-1 primary"><em>Referências</em></span></h1>
          <p class="lead fs-lg px-md-12">Artigos, livros e textos sobre memética digital, cultura de internet e comunicação em rede.</p>
        </div>
      </div>
    </div>
  </section>

  {% include components/sections/demo2/hero.html %}

  {% include components/sections/museudememes/features-17.html %}

  {% include components/sections/museudememes/referencias.html %}

  {% include components/footer/footer.html
      style="default"
      bg_color="bg-primary"
      text_color="text-inverse"
      widget_title_class="text-white"
      container_padding="pt-14 pb-13 pt-md-16 pb-md-15"
      cta=false
  %}
</div>
