---
layout: default
title: "Reserva Técnica"
permalink: /museudememes/reserva/
redirect_from:
  - /museudememes/museu/reserva-tecnica/
custom_color: museudememes
custom_font: space
scroll_top_btn:
  enable: true

features18:
  enable: true
  services:
    - image: "/assets/img/photos/about3.webp"
      image_2x: "/assets/img/photos/about3@2x.webp"
      alt: "Reserva Técnica do #MUSEUdeMEMES"
      image_right: true
      icon: "/assets/img/icons/lineal/server.svg"
      icon_bg: "bg-pale-primary"
      icon_color: "text-primary"
      list_color: "bullet-soft-primary"
      title: "Datasets abertos para pesquisa"
      description: "A Reserva Técnica reúne os conjuntos de dados produzidos e organizados pelo #MUSEUdeMEMES, disponibilizados gratuitamente para pesquisadores mediante cadastro e compromisso ético."
      list_items:
        - "Corpus de memes por tema, período e plataforma"
        - "Dados de circulação e engajamento nas redes sociais"
        - "Metadados de catalogação museológica"
        - "Documentação de variações e remixagens"
      button:
        url: "#datasets"
        text: "Ver Datasets Disponíveis"
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

<!-- Hero -->
<section class="wrapper bg-soft-primary">
  <div class="container pt-10 pb-14 pt-md-14 pb-md-17 text-center">
    <div class="row">
      <div class="col-lg-9 col-xxl-8 mx-auto">
        <h1 class="display-1 mb-3">Reserva <span class="underline-3 style-2 primary">Técnica</span></h1>
        <p class="lead fs-lg px-md-12">O repositório de dados abertos do #MUSEUdeMEMES — datasets para pesquisa acadêmica sobre memética e cultura digital brasileira.</p>
      </div>
    </div>
  </div>
</section>

<!-- Features Section 18 -->
{% include components/sections/museudememes/features-18.html %}

<!-- Datasets Section -->
{% include components/sections/museudememes/reserva-datasets.html %}

{% include components/footer/footer.html
    style="default"
    bg_color="bg-primary"
    text_color="text-inverse"
    widget_title_class="text-white"
    container_padding="pt-14 pb-13 pt-md-16 pb-md-15"
    cta=false
%}

</div>

<!-- reCAPTCHA (explicit render para suportar múltiplos widgets na página) -->
{% if site.recaptcha_site_key and site.recaptcha_site_key != "" %}
<script>
  // Callback chamado pelo reCAPTCHA após carregar
  window.initRecaptchas = function () {
    document.querySelectorAll('.g-recaptcha').forEach(function (el) {
      if (el.dataset.rendered) return; // evita dupla renderização
      var widgetId = grecaptcha.render(el, {
        sitekey: el.dataset.sitekey
      });
      el.dataset.widgetId = String(widgetId);
      el.dataset.rendered = '1';
    });
  };
</script>
<script src="https://www.google.com/recaptcha/api.js?onload=initRecaptchas&render=explicit" async defer></script>
{% endif %}

<script>
(function () {
  'use strict';

  var APPS_SCRIPT_URL = '{{ site.google_apps_script_url }}';

  document.querySelectorAll('.dataset-request-form').forEach(function (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();

      // Validação Bootstrap nativa
      if (!form.checkValidity()) {
        form.classList.add('was-validated');
        return;
      }

      var feedback     = form.querySelector('.form-feedback');
      var btn          = form.querySelector('button[type=submit]');
      var datasetId    = form.dataset.datasetId;
      var datasetTitle = form.dataset.datasetTitle;
      var downloadUrl  = form.dataset.downloadUrl;

      // Verificar reCAPTCHA usando o widget ID armazenado no elemento
      var recaptchaToken = '';
      var recaptchaWidget = form.querySelector('.g-recaptcha');
      if (recaptchaWidget && typeof grecaptcha !== 'undefined') {
        var widgetId = recaptchaWidget.dataset.widgetId;
        recaptchaToken = grecaptcha.getResponse(
          widgetId !== undefined ? parseInt(widgetId, 10) : undefined
        );
        if (!recaptchaToken) {
          var rcFeedback = form.querySelector('.recaptcha-feedback');
          if (rcFeedback) rcFeedback.style.display = 'block';
          return;
        }
      }

      // Desabilitar botão
      btn.disabled = true;
      var originalBtnText = btn.innerHTML;
      btn.innerHTML = '<span class="spinner-border spinner-border-sm me-2" role="status"></span>Processando…';

      // Esconder feedback anterior
      feedback.style.display = 'none';
      feedback.className = 'form-feedback alert mb-3';

      // Coletar IP e enviar
      fetch('https://api.ipify.org?format=json')
        .catch(function () { return { ip: 'desconhecido' }; })
        .then(function (r) { return r.json ? r.json() : r; })
        .then(function (ipData) {

          var payload = {
            dataset_id:      datasetId,
            dataset_title:   datasetTitle,
            ip:              (ipData && ipData.ip) ? ipData.ip : 'desconhecido',
            recaptcha_token: recaptchaToken,
            nome:            form.querySelector('[name=nome]').value.trim(),
            instituicao:     form.querySelector('[name=instituicao]').value.trim(),
            cidade:          form.querySelector('[name=cidade]').value.trim(),
            pais:            form.querySelector('[name=pais]').value.trim(),
            telefone:        form.querySelector('[name=telefone]').value.trim(),
            email:           form.querySelector('[name=email]').value.trim(),
            etica:           form.querySelector('[name=etica]').checked
          };

          // GET + query params: sobrevive ao redirect 302 do Apps Script
          // (POST body é perdido no redirect script.google.com → script.googleusercontent.com).
          // mode: 'no-cors' evita o erro CORS; resposta é opaca mas a requisição chega.
          var params = new URLSearchParams({
            dataset_id:    payload.dataset_id,
            dataset_title: payload.dataset_title,
            ip:            payload.ip,
            nome:          payload.nome,
            instituicao:   payload.instituicao,
            cidade:        payload.cidade,
            pais:          payload.pais,
            telefone:      payload.telefone,
            email:         payload.email,
            etica:         payload.etica ? '1' : '0'
          });
          return fetch(APPS_SCRIPT_URL + '?' + params.toString(), {
            mode: 'no-cors'
          });
        })
        .then(function () {
          // Requisição enviada — disparar download e mostrar confirmação
          if (downloadUrl) {
            window.open(downloadUrl, '_blank');
            feedback.textContent = '✓ Download iniciado! Obrigado por seguir nossos protocolos de pesquisa.';
            btn.innerHTML = '<i class="uil uil-check me-1"></i>Download liberado';
          } else {
            feedback.textContent = '✓ Cadastro registrado! O arquivo deste dataset estará disponível em breve.';
            btn.innerHTML = '<i class="uil uil-check me-1"></i>Cadastro registrado';
          }
          feedback.classList.add('alert-success');
          feedback.style.display = 'block';
        })
        .catch(function (err) {
          feedback.textContent = 'Erro ao processar a solicitação: ' + (err.message || err);
          feedback.classList.add('alert-danger');
          feedback.style.display = 'block';
          btn.disabled = false;
          btn.innerHTML = originalBtnText;
        });
    });
  });
})();
</script>
