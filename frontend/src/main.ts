import { createApp } from "vue";
import { createPinia } from "pinia";
import ElementPlus from "element-plus";
import "element-plus/dist/index.css";
import router from "./router";
import App from "./App.vue";
import "./styles/main.scss";
import draggable from "vuedraggable";
import { setupAntd } from "./plugins/antd";

const app = createApp(App);

app.use(createPinia());
app.use(router);
app.use(ElementPlus);
app.component("Draggable", draggable);

setupAntd(app);

app.mount("#app");
