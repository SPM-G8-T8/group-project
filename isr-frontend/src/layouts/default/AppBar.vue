<template>
  <v-app-bar flat class="bg-light-blue-darken-4">
    <v-app-bar-title>
      <router-link
        to="/"
        class="text-decoration-none text-white text-h5 font-weight-bold"
        >Skill-based Role Portal</router-link
      >
    </v-app-bar-title>
    <v-spacer></v-spacer>
    <v-list class="bg-light-blue-darken-4 d-flex flex-row" v-if="staff_details">
      <v-list-item
        v-for="(item, index) in navMenu[staff_details.sys_role]"
        :key="index"
      >
        <router-link :to="item.to" class="text-decoration-none text-white">
          {{ item.title }}
        </router-link>
      </v-list-item>
      <v-list-item>
        <router-link to="/" class="text-decoration-none text-white">
          View Listings
        </router-link>
      </v-list-item>
      <v-list-item>
        <router-link to="/profile" class="text-decoration-none text-white">
          My Profile
        </router-link>
      </v-list-item>
      <v-list-item @click="logout">
        <v-icon icon="mdi-logout"></v-icon>
        Logout
      </v-list-item>
    </v-list>
  </v-app-bar>
</template>

<script setup>
import { useAppStore } from "@/store/app";
import { storeToRefs } from "pinia";
import { onBeforeMount } from "vue";
import { useRouter } from "vue-router";

const appStore = useAppStore();
const { staff_details } = storeToRefs(appStore);
const { resetState } = appStore;

const router = useRouter();

const navMenu = {
  hr: [
    {
      title: "Manage Listings",
      to: "/role-listing",
    },
    {
      title: "Manage Skills",
      to: "/skills"
    }
  ],
  staff: [],
  manager: [
    {
      title: "Manage Listings",
      to: "/role-listing",
    },
  ],
};

const logout = () => {
  resetState();
  router.push({ name: "Login" });
};

onBeforeMount(() => {
  console.log(staff_details.value);
  if (!staff_details.value) {
    router.push({ name: "Login" });
  }
});
</script>
