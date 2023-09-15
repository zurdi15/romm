import { nextTick } from "vue";
import { createI18n } from "vue-i18n";

import { api } from "./services/api";

export const SUPPORTED_LOCALES = ["en", "fr"];

export function setupI18n() {
  const locale = window.navigator.language.split("-")[0];
  const i18n = createI18n({
    legacy: false,
    locale: locale,
    fallbackLocale: "en",
  });

  // Load the default locale file
  loadLocaleMessages(i18n, "en").then(() => {
    // Set the locale from the browser language
    setI18nLanguage(i18n, locale);
  });

  return i18n;
}

export async function setI18nLanguage(i18n, locale) {
  const { value: fallbackLocale } = i18n.global.fallbackLocale;

  // If the locale is not supported, use the fallback locale
  const selectedLocale = SUPPORTED_LOCALES.includes(locale)
    ? locale
    : fallbackLocale;

  // If the locale hasn't been loaded yet, load it
  if (!i18n.global.availableLocales.includes(selectedLocale)) {
    await loadLocaleMessages(i18n, selectedLocale);
  }

  // Set the i18n instance locale
  i18n.global.locale.value = selectedLocale;
  
  // Set the HTML lang attribute
  document.querySelector("html").setAttribute("lang", selectedLocale);

  // Set the default language for the API requests
  api.defaults.headers.common["Accept-Language"] = selectedLocale;
}

export async function loadLocaleMessages(i18n, locale) {
  const messages = await import(`./locales/${locale}.json`);
  i18n.global.setLocaleMessage(locale, messages.default);
  return nextTick();
}
