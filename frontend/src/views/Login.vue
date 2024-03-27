<script setup lang="ts">
import identityApi from "@/services/api/identity";
import storeAuth from "@/stores/auth";
import storeHeartbeat from "@/stores/heartbeat";
import type { Events } from "@/types/emitter";
import type { Emitter } from "mitt";
import { inject, onBeforeMount, ref, h } from "vue";
import { useRouter } from "vue-router";

// Props
const heartbeatStore = storeHeartbeat();
const auth = storeAuth();
const emitter = inject<Emitter<Events>>("emitter");
const router = useRouter();
const username = ref();
const password = ref();
const visiblePassword = ref(false);
const logging = ref(false);

function login() {
  logging.value = true;
  identityApi
    .login(username.value, password.value)
    .then(() => {
      const next = (router.currentRoute.value.query?.next || "/").toString();
      router.push(next);
    })
    .catch(({ response, message }) => {
      const errorMessage =
        response.data?.detail ||
        response.data ||
        message ||
        response.statusText;

      emitter?.emit("snackbarShow", {
        msg: `Unable to login: ${errorMessage}`,
        icon: "mdi-close-circle",
        color: "red",
      });
      console.error(
        `[${response.status} ${response.statusText}] ${errorMessage}`
      );
    })
    .finally(() => {
      logging.value = false;
    });
}

onBeforeMount(async () => {
  // Check if authentication is enabled
  if (!auth.enabled) {
    return router.push({ name: "dashboard" });
  }
});
</script>

<template>
  <div id="bg" class="bg"></div>

  <div class="p-container fill-height justify-center">
    <Card id="card" class="py-8 px-5" style="width: 500px">
      <template #content>
        <div class="p-row">
          <div class="p-col">
            <img
              src="/assets/isotipo.svg"
              class="mx-auto"
              alt="logo"
              style="width: 200px; height: 200px"
            />

            <div class="text-white justify-center mt-2">
              <div class="p-col-10 p-md-8">
                <InputText
                  v-model="username"
                  @keydown.enter.native="login()"
                  prepend="mdi-account"
                  placeholder="Username"
                />
                <Password
                  v-model="password"
                  @keydown.enter.native="login()"
                  placeholder="Password"
                  :toggleMask="visiblePassword"
                  @click.native="visiblePassword = !visiblePassword"
                />
              </div>
            </div>

            <div class="justify-center">
              <div class="p-col-10 p-md-8">
                <Button
                  @click="login()"
                  :disabled="logging"
                  class="romm-accent-1"
                  icon="mdi-chevron-right-circle-outline"
                  :loading="logging"
                  loading-text="Logging in..."
                  :loader="h('ProgressSpinner', { color: 'romm-accent-1' })"
                >
                  Login
                </Button>
              </div>
            </div>
          </div>
        </div>
      </template>
    </Card>

    <div class="position-absolute" id="version">
      <span class="text-white">{{ heartbeatStore.VERSION }}</span>
    </div>
  </div>
</template>

<style scoped>
#bg {
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  position: absolute;
  background: url("/assets/login_bg.png") center center;
  background-size: cover;
}
#card {
  background: rgba(0, 0, 0, 0.35);
  backdrop-filter: blur(10px);
}
#version {
  text-shadow: 1px 1px 1px #000000, 0 0 1px #000000;
  bottom: 0.3rem;
  right: 0.5rem;
}
</style>
