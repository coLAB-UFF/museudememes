---
layout: default
title: "Enviar Doação"
permalink: /museudememes/enviar-doacao/
redirect_from:
  - /museudememes/doacoes/
custom_color: museudememes
custom_font: space
scroll_top_btn:
  enable: true

features18:
  enable: true
  services:
    - image: /images_static/meme_vampetaco.png
      image_2x: /images_static/meme_vampetaco.png
      alt: "Apoie o MUSEUdeMEMES"
      image_right: false
      icon: /assets/img/icons/lineal/heart.svg
      icon_bg: bg-pale-red
      icon_color: icon-svg-red
      title: "Por que apoiar o #MUSEUdeMEMES?"
      description: "O #MUSEUdeMEMES é uma iniciativa acadêmica sem fins lucrativos vinculada à UFMG. Sua doação contribui diretamente para a preservação da cultura digital, o financiamento de pesquisas e a produção de materiais educativos gratuitos."
      list_items:
        - "Manutenção e expansão do acervo digital de memes."
        - "Bolsas para estudantes de iniciação científica e pós-graduação."
        - "Produção de materiais educativos para escolas públicas."
        - "Realização de exposições e eventos culturais abertos ao público."
      button:
        url: "#contato-doacao"
        text: "Quero apoiar"
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
          <h1 class="display-1 mb-3">Enviar <span class="underline-3 style-2 primary">Doação</span></h1>
          <p class="lead fs-lg px-md-12">Apoie a preservação da cultura digital e o financiamento de pesquisas sobre memes — um patrimônio imaterial da nossa época.</p>
        </div>
      </div>
    </div>
  </section>

  {% include components/sections/museudememes/features-18.html %}

  <section id="contato-doacao" class="wrapper bg-light">
    <div class="container py-14 py-md-16">
      <div class="card bg-soft-primary">
        <div class="card-body p-12">
          <div class="row gx-md-8 gx-xl-12 gy-10">
            <div class="col-lg-6">
              <img src="/assets/img/icons/lineal/email.svg" class="svg-inject icon-svg icon-svg-sm mb-4" alt="" />
              <h2 class="display-4 mb-3 pe-lg-10">Fale com a nossa equipe</h2>
              <p class="lead pe-lg-12 mb-0">Sua contribuição faz diferença — seja como pessoa física, empresa ou instituição parceira. Entre em contato para saber mais sobre as formas de apoio ao #MUSEUdeMEMES. Nossa equipe responderá em até 3 dias úteis.</p>
            </div>
            <div class="col-lg-6">
              <form class="contact-form" method="POST" action="{{ site.formspree_doacao_url }}">
                <input type="hidden" name="_subject" value="[Doação ao #MUSEUdeMEMES]">
                <input type="text" name="_gotcha" style="display:none">
                <div class="messages"></div>
                <div class="row gx-4">
                  <div class="col-md-6">
                    <div class="form-floating mb-4">
                      <input id="frm_doacao_name" type="text" name="name" class="form-control border-0" placeholder="Nome" required>
                      <label for="frm_doacao_name">Nome *</label>
                    </div>
                  </div>
                  <div class="col-md-6">
                    <div class="form-floating mb-4">
                      <input id="frm_doacao_email" type="email" name="email" class="form-control border-0" placeholder="email@exemplo.com" required>
                      <label for="frm_doacao_email">E-mail *</label>
                    </div>
                  </div>
                  <div class="col-12">
                    <div class="form-floating mb-4">
                      <textarea id="frm_doacao_message" name="message" class="form-control border-0" placeholder="Sua mensagem" style="height: 150px" required></textarea>
                      <label for="frm_doacao_message">Mensagem *</label>
                    </div>
                  </div>
                  <div class="col-12">
                    <input type="submit" class="btn btn-outline-primary rounded-pill btn-send mb-3" value="Enviar mensagem">
                  </div>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>

  {% include components/footer/footer.html
      style="default"
      bg_color="bg-primary"
      text_color="text-inverse"
      widget_title_class="text-white"
      container_padding="pt-14 pb-13 pt-md-16 pb-md-15"
      cta=false
  %}
</div>
