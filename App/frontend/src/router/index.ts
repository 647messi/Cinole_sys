import { createRouter, createWebHistory } from "vue-router"
import SupplierCreateView from "../testviews/SupplierCreateView.vue"

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      redirect: "/test/suppliers/create",
    },
    {
      path: "/test/suppliers/create",
      name: "supplier-create-test",
      component: SupplierCreateView,
    },
  ],
})

export default router