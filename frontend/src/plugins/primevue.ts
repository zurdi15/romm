import type { App } from "vue";

import PrimeVue from 'primevue/config';
import Card  from 'primevue/card';
import InputText from 'primevue/inputtext';
import Password from 'primevue/password';
import Button from 'primevue/button';

export function registerComponents(app: App) {
    app.component('Card', Card);
    app.component('InputText', InputText);
    app.component('Password', Password);
    app.component('Button', Button);
}

export default PrimeVue;
