<script setup>
    import HomeHero from '@/components/HomeHero.vue';
    import AboutWidget from '@/components/AboutWidget.vue';
    import ContactForm from '@/components/ContactForm.vue';
    import FooterWidget from '@/components/FooterWidget.vue';
    import Last3NewsWidget from "@/components/Last3NewsWidget.vue";
    
</script>

<template>
    <main>
        <HomeHero></HomeHero>
        <section id="about-us" class="container section has-background-white">
            <h2 class="title has-text-centered gradient-text is-large-text">Quienes Somos</h2>
            <AboutWidget></AboutWidget>
        </section>
        <section id="last-news" class="container section">
            <h2 class="title has-text-centered gradient-text is-large-text">Ultimas Novedades</h2>
            <Last3NewsWidget></Last3NewsWidget>
        </section>
        <section id="contact-us" class="container section has-background-white">
            <h2 class="title has-text-centered gradient-text is-large-text">Contactanos</h2>
            <ContactForm></ContactForm>
        </section>
        <FooterWidget></FooterWidget>
    </main>
</template>

<style>
@import '../assets/home.css';
html {
    scroll-behavior: smooth;
}
</style>
