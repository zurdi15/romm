<script setup lang="ts">
import { ref, inject } from "vue";
import { useDisplay } from "vuetify";
import type { Emitter } from "mitt";
import type { Events } from "@/types/emitter";

import romApi, { type UpdateRom } from "@/services/api/rom";
import storeRoms from "@/stores/roms";

const { xs, mdAndDown, lgAndUp } = useDisplay();
const show = ref(false);
const rom = ref<UpdateRom>();
const romsStore = storeRoms();
const fileNameInputRules = {
  required: (value: string) => !!value || "Required",
  newFileName: (value: string) => !value.includes("/") || "Invalid characters",
};

const emitter = inject<Emitter<Events>>("emitter");
emitter?.on("showEditRomDialog", (romToEdit) => {
  show.value = true;
  rom.value = romToEdit;
});

// Functions
async function updateRom() {
  if (!rom.value) return;

  if (rom.value.file_name.includes("/")) {
    emitter?.emit("snackbarShow", {
      msg: "Couldn't edit rom: invalid file name characters",
      icon: "mdi-close-circle",
      color: "red",
    });
    return;
  } else if (!rom.value.file_name) {
    emitter?.emit("snackbarShow", {
      msg: "Couldn't edit rom: file name required",
      icon: "mdi-close-circle",
      color: "red",
    });
    return;
  }

  show.value = false;
  emitter?.emit("showLoadingDialog", { loading: true, scrim: true });
  await romApi
    .updateRom({ rom: rom.value })
    .then(({ data }) => {
      emitter?.emit("snackbarShow", {
        msg: "Rom updated successfully!",
        icon: "mdi-check-bold",
        color: "green",
      });
      romsStore.update(data);
      emitter?.emit("refreshView", null);
    })
    .catch((error) => {
      console.log(error);
      emitter?.emit("snackbarShow", {
        msg: error.response.data.detail,
        icon: "mdi-close-circle",
        color: "red",
      });
    })
    .finally(() => {
      emitter?.emit("showLoadingDialog", { loading: false, scrim: false });
    });
}

function closeDialog() {
  show.value = false;
}
</script>

<template>
  <v-dialog
    :modelValue="show"
    scroll-strategy="none"
    width="auto"
    :scrim="true"
    @click:outside="closeDialog"
    @keydown.esc="closeDialog"
    no-click-animation
    persistent
    v-if="rom"
  >
    <v-card
      rounded="0"
      :class="{
        'edit-content': lgAndUp,
        'edit-content-tablet': mdAndDown,
        'edit-content-mobile': xs,
      }"
    >
      <v-toolbar density="compact" class="bg-terciary">
        <v-row class="align-center" no-gutters>
          <v-col cols="9" xs="9" sm="10" md="10" lg="11">
            <v-icon icon="mdi-pencil-box" class="ml-5" />
          </v-col>
          <v-col>
            <v-btn
              @click="closeDialog"
              class="bg-terciary"
              rounded="0"
              variant="text"
              icon="mdi-close"
              block
            />
          </v-col>
        </v-row>
      </v-toolbar>
      <v-divider class="border-opacity-25" :thickness="1" />

      <v-card-text>
        <v-row class="pa-2" no-gutters>
          <v-text-field
            @keyup.enter="updateRom()"
            v-model="rom.name"
            label="Name"
            variant="outlined"
            required
            hide-details
          />
        </v-row>
        <v-row class="pa-2" no-gutters>
          <v-text-field
            @keyup.enter="updateRom()"
            v-model="rom.file_name"
            :rules="[
              fileNameInputRules.newFileName,
              fileNameInputRules.required,
            ]"
            label="File name"
            variant="outlined"
            required
            hide-details
          />
        </v-row>
        <v-row class="pa-2" no-gutters>
          <v-textarea
            @keyup.enter="updateRom()"
            v-model="rom.summary"
            label="Summary"
            variant="outlined"
            required
            hide-details
          />
        </v-row>
        <v-row class="pa-2" no-gutters>
          <v-file-input
            @keyup.enter="updateRom()"
            v-model="rom.artwork"
            label="Custom artwork"
            accept="image/*"
            prepend-inner-icon="mdi-image"
            prepend-icon=""
            variant="outlined"
            hide-details
          />
        </v-row>
        <v-row class="justify-center pa-2" no-gutters>
          <v-btn @click="closeDialog" class="bg-terciary">Cancel</v-btn>
          <v-btn @click="updateRom()" class="text-romm-green ml-5 bg-terciary"
            >Apply</v-btn
          >
        </v-row>
      </v-card-text>
    </v-card>
  </v-dialog>
</template>

<style scoped>
.edit-content {
  width: 900px;
}

.edit-content-tablet {
  width: 570px;
}

.edit-content-mobile {
  width: 85vw;
}
</style>
