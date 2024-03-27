import type { App } from "vue";

import { loadFonts } from "./webfontloader";
import vuetify from "./vuetify";
import router from "./router";
import pinia from "./pinia";
import primevue, { registerComponents } from "./primevue";

export function registerPlugins(app: App) {
  loadFonts();
  app.use(vuetify).use(router).use(pinia).use(primevue);
  registerComponents(app);
}
