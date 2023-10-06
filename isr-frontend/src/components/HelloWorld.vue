<template>
  <v-container class="fill-height">
    <v-responsive class="align-center text-center fill-height">
      <v-img height="300" src="@/assets/logo.svg" />

      <div class="text-body-2 font-weight-light mb-n1">Welcome to</div>

      <h1 class="text-h2 font-weight-bold">Vuetify</h1>

      <div class="py-14" />

      <v-row class="d-flex align-center justify-center">
        <v-col cols="auto">
          <router-link :to="{ path: '/role-listing' }">
            <v-btn color="primary"> HR Role Listings </v-btn>
          </router-link>
        </v-col>

        <v-col cols="auto">
          <router-link :to="{ path: '/view-listing' }">
            <v-btn color="primary"> Staff Role Listings </v-btn>
          </router-link>
        </v-col>
      </v-row>
    </v-responsive>
  </v-container>
</template>

<script setup>
//
</script>
