<template>
  <v-container>
    <v-row>
      <v-col cols="12" lg="4">
        <p class="text-h5 py-3">Role Application</p>
      </v-col>
    </v-row>

    <v-divider></v-divider>
    <v-row>
      <v-col cols="12" lg="4">
        <p class="text-h3 font-weight-bold py-3">Skill Match Percentage</p>
      </v-col>
      <v-col cols="12" lg="4">
        <v-card-actions class="justify-start">
      <v-btn color="primary" text @click="applyRole">Apply</v-btn>
      <v-btn color="primary" elevated :to="{ path: 'view-listing' }"
        >Cancel</v-btn
      >
    </v-card-actions>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { createRoleApplication } from "@/api/api.js";
import axios from "axios";

export default {
  methods: {
    applyRole() {
        axios
          .post(createRoleApplication, {
            role_app_id: 102000,
            role_listing_id: 3,
            staff_id: 2,
            role_app_ts_create: "2023-10-04T04:52:31",
            role_app_status: "applied"
          })
          .then((response) => {
            console.log(response);
            this.errorMessage = "";
            this.createdSuccess = true;
            alert("Role Application Created!");
          })
          .catch((error) => {
            console.log(error);
            this.errorMessage = error.response.data.detail;
          });
    },
  },
};
</script>
