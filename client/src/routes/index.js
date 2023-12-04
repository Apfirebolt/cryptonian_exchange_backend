import { createRouter, createWebHistory } from "vue-router";
import Home from "../views/home.vue";
import NotFound from "../views/not-found.vue";

const routes = [
  {
    path: "/",
    name: "Home",
    component: Home,
  },
  {
    path: "/items",
    name: "ItemList",
    component: () => import("../views/items.vue"),
  },
  {
    path: "/:catchAll(.*)",
    name: "NotFound",
    component: NotFound,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
