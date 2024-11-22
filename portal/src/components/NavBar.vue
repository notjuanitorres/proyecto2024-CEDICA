<script setup>
    import { RouterLink } from 'vue-router'
    
    document.addEventListener('DOMContentLoaded', () => {
        const $navbarBurgers = Array.prototype.slice.call(document.querySelectorAll('.navbar-burger'), 0);
        $navbarBurgers.forEach( el => {
        el.addEventListener('click', () => {
            const target = el.dataset.target;
            const $target = document.getElementById(target);
            el.classList.toggle('is-active');
            $target.classList.toggle('is-active');
        });
    });

});
</script>
<template>
    <nav class="navbar px-2 pr-4 py-2 is-fixed-top" role="navigation" aria-label="main navigation">
        <div class="navbar-brand">
            <a class="navbar-item" href="/">
                <img
                    src="/img/cedica_isologotipo.png"
                    alt="CEDICA isologotipo"
                />
            </a>
            <a role="button" class="navbar-burger" aria-label="menu" aria-expanded="false" data-target="navbar">
            <span aria-hidden="true"></span>
            <span aria-hidden="true"></span>
            <span aria-hidden="true"></span>
            <span aria-hidden="true"></span>
            </a>
        </div>

        <div id="navbar" class="navbar-menu">
            <div class="navbar-end">
                <RouterLink to="/nosotros" class="navbar-item">Sobre Nosotros</RouterLink>
                <RouterLink to="/noticias" class="navbar-item">Noticias</RouterLink>
                <RouterLink to="/#contact-us" class="navbar-item">Contacto</RouterLink>
            </div>
        </div>
    </nav>
</template>

