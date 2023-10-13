// Composables
import { createRouter, createWebHistory } from "vue-router";

const routes = [
  {
    path: "/",
    component: () => import("@/layouts/default/Default.vue"),
    children: [
      {
        path: "",
        name: "Home",
        // route level code-splitting
        // this generates a separate chunk (about.[hash].js) for this route
        // which is lazy-loaded when the route is visited.
        component: () =>
          import(/* webpackChunkName: "home" */ "@/views/Home.vue"),
      },
      {
        path: "role-listing",
        name: "RoleListing",
        component: () => import("@/views/RoleListing.vue"),
      },
      {
        path: "view-listing",
        name: "ViewListing",
        component: () => import("@/views/ViewListing.vue"),
      },
      {
        path: "skills",
        name: "Skills",
        component: () => import("@/views/Skills.vue"),
      },
      {
        path: "role-listing/:roleID/:listingID",
        name: "ViewApplicants",
        component: () => import("@/views/ViewApplicants.vue"),
      },
      {
        path: "role-application",
        name: "ApplyRole",
        component: () => import("@/views/ApplyRole.vue"),
      },
      {
        path: "profile",
        name: "Profile",
        component: () => import("@/views/Profile.vue"),
      },
    ],
  },
  {
    path: "/login",
    name: "Login",
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "home" */ "@/views/Login.vue"),
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
