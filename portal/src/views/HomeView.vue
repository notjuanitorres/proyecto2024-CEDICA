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
        <ContactForm></ContactForm>
        <FooterWidget></FooterWidget>
    </main>
</template>

<style>
html {
    scroll-behavior: smooth;
}
</style>