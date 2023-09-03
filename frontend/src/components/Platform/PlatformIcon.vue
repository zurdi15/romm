<script setup>
import { ref } from "vue";

const props = defineProps(["platform"]);
const platformIconUrl = ref(
  `/assets/platforms/${props.platform.slug.toLowerCase()}.ico`
);

function onImageError() {
  platformIconUrl.value =
    props.platform.logo_url || "/assets/platforms/default.ico";
}
</script>

<template>
  <v-img :src="platformIconUrl" @error="onImageError" />
</template>
