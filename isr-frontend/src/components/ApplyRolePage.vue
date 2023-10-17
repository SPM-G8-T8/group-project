<template>
  <v-container>
    <v-row>
      <v-col cols="12" lg="4">
        <p class="text-h5 py-3">Role Application</p>
        <p class="text-caption font-italic">Posted On {{ listingCreationDate }}</p>
      </v-col>
    </v-row>

    <v-divider></v-divider>
    <v-row v-if="roleListing == null">
      <v-progress-circular></v-progress-circular>
    </v-row>

    <v-row class="my-2" v-else>
      <v-col cols="12" lg="8">
        <p class="text-h6">{{ roleListing.role.role_name }}</p>

        <div class="my-5" style="min-height: 100px;">
          <p class="text-subtitle-2">Listing Description</p>
          <p class="text-body-2">{{ roleListing.role_listing_desc }}</p>
        </div>

        <div class="my-5" style="min-height: 100px;">
          <p class="text-subtitle-2">Role Description</p>
          <p class="text-body-2">{{ roleListing.role.role_description }}</p>
        </div>

        <div class="my-5" style="min-height: 100px;">
          <p class="text-subtitle-2">Skills Required</p>
          <div class="my-2">
            <v-chip v-for="(skill, index) in roleSkills" :key="index" class="mx-1">{{ skill.skill_name }}</v-chip>
          </div>
        </div>

      </v-col>
      <v-col cols="12" lg="4">
        <v-card color="blue-lighten-4">
          <v-card-title>
            <p class="text-h6">Apply for Role</p>
          </v-card-title>
          <v-card-text>
            Closing date: {{ roleListing.role_listing_close }}
          </v-card-text>
          <v-card-actions class="justify-center">
            <v-btn color="primary" @click="applyRole">Apply</v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { createRoleApplication, getRoleListing } from "@/api/api.js";
import axios from "axios";

export default {
  data() {
    return {
      roleListing: null,
      roleSkills: []
    };
  },
  computed: {
    listingCreationDate() {
      if (this.roleListing == null) {
        return ""
      } else {
        return this.roleListing.role_listing_ts_create.split("T")[0]
      }
      
    }
  },
  methods: {
    getListingDetails() {
      axios
        .get(`${getRoleListing}${this.$route.params.listingID}`)
        .then((response) => {
          this.roleListing = response.data;
        })
        .catch((error) => {
          console.log(error);
        });
    },
    getRequiredSkills() {
      axios.get(`${getRoleListing}${this.$route.params.listingID}/skills`)
        .then((response) => {
          this.roleSkills = response.data;
        })
        .catch((error) => {
          console.log(error);
        });
    },
    applyRole() {
        axios
          .post(createRoleApplication, {
            role_app_id: 102000,
            role_listing_id: 3,
            staff_id: 2,
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
  mounted() {
    this.getListingDetails();
    this.getRequiredSkills();
  },
};
</script>
