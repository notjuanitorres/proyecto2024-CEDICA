<script setup>
const currentYear = new Date().getFullYear()
</script>
<template>
  <footer
    class="footer section is-medium bg-watercolor-blueish-stain has-text-black shape-divider-bottom"
  >
    <div class="content">
      <div class="container">
        <p class="has-text-centered">
          <br />
          📍 La Plata, Buenos Aires, Argentina <br />
          <strong class="has-text-black">CEDICA &copy;</strong>
          <span id="current-year">{{ currentYear }}</span
          >. Todos los derechos reservados.
          <br />
        </p>
      </div>
      <div class="buttons is-centered pt-2">
          <a
            href="https://www.facebook.com/cedica.equitacionparatodos/"
            target="_blank"
            rel="noopener noreferrer"
            class="button is-black is-outlined"
          >
            <span class="icon">
              <i class="fab fa-facebook-f"></i>
            </span>
          </a>

          <a
            href="https://www.instagram.com/cedica.equitacionparatodos?utm_source=ig_web_button_share_sheet&igsh=ZDNlZDc0MzIxNw=="
            target="_blank"
            rel="noopener noreferrer"
            class="button is-black is-outlined"
          >
            <span class="icon">
              <i class="fab fa-instagram"></i>
            </span>
          </a>

          <a
            href="https://m.me/cedica.equitacionparatodos"
            class="button is-black is-outlined"
            target="_blank"
            rel="noopener noreferrer"
          >
            <span class="icon">
              <i class="fa-brands fa-facebook-messenger"></i>
            </span>
          </a>
        </div>
    </div>
  </footer>
  <p class="is-small mt-2 p-4 has-text-centered">Desarrollado por Grupo19</p>

</template>

<style>
@import '../assets/home.css';
</style>
