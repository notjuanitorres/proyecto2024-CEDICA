<script setup>
    import HomeHero from '@/components/HomeHero.vue';
    import AboutWidget from '@/components/AboutWidget.vue';
    import NewsWidget from '@/components/NewsWidget.vue';
    import ContactForm from '@/components/ContactForm.vue';
    import FooterWidget from '@/components/FooterWidget.vue';
</script>

<template>
    <main>
        <HomeHero></HomeHero>
        <NewsWidget></NewsWidget>
        <AboutWidget></AboutWidget>
        <h1 class="title has-text-centered">Contactanos</h1>
        <section id="contact-us" class="container section is-medium has-background-white">
            <ContactForm></ContactForm>
        </section>
        <FooterWidget></FooterWidget>
    </main>
</template>

<style>
html {
    scroll-behavior: smooth;
}
</style>