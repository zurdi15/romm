import { createApp } from "vue";
import { createVuetify } from "vuetify";

import { registerPlugins } from "@/plugins";
import { setupI18n } from "./i18n";
import App from "./App.vue";

const app = createApp(App);
registerPlugins(app);

// Event bus
import mitt from "mitt";
const emitter = mitt();
app.provide("emitter", emitter);

// i18n
const i18n = setupI18n();
app.use(i18n);

app.mount("#app");

export default createVuetify({
  defaults: {
    VBtn: {
      rounded: 0,
    },
  },
});
