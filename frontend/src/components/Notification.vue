<script setup lang="ts">
import { ref, inject } from "vue";
import type { Emitter } from "mitt";
import type { SnackbarStatus, Events } from "@/types/emitter";

// Props
const show = ref(false);
const snackbarStatus = ref<SnackbarStatus>({ msg: "" });

// Event listeners bus
const emitter = inject<Emitter<Events>>("emitter");
emitter?.on("snackbarShow", (snackbar: SnackbarStatus) => {
  show.value = true;
  snackbarStatus.value = snackbar;
});

function closeDialog() {
  show.value = false;
}
</script>

<template>
  <v-snackbar
    v-model="show"
    :timeout="snackbarStatus.timeout ? snackbarStatus.timeout : 2000"
    location="top"
    color="tooltip"
  >
    <v-icon
      :icon="snackbarStatus.icon"
      :color="snackbarStatus.color"
      class="mx-2"
    />
    {{ snackbarStatus.msg }}
    <template v-slot:actions>
      <v-btn @click="closeDialog" variant="text">
        <v-icon icon="mdi-close" />
      </v-btn>
    </template>
  </v-snackbar>
</template>
