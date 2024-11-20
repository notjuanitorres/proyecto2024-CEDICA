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
        <Last3NewsWidget></Last3NewsWidget>
        <br>
        <br>
        <br>
        <br>
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
