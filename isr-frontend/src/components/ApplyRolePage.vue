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
            <v-chip v-for="(skill, index) in roleSkills" :key="index" class="mx-1" :color="(this.availableSkills.includes(skill.skill_name))? 'green': 'grey'">{{ skill.skill_name }}</v-chip>
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
import { createRoleApplication, getRoleListing, getStaffSkills } from "@/api/api.js";
import { useAppStore } from "@/store/app";
import axios from "axios";

export default {
  setup() {
    const appStore = useAppStore(); 
    return { appStore };
  },
  data() {
    return {
      roleListing: null,
      roleSkills: [],
      employeeId: null,
      staff_skills: [],
      availableSkills: [],
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
      console.log(this.appStore)
      
      axios
        .post(createRoleApplication, {
          role_listing_id: this.$route.params.listingID,
          staff_id: this.appStore.staff_details.staff_id,
        })
        .then((response) => {
          console.log(response);
          this.errorMessage = "";
          this.createdSuccess = true;
          alert("Role Application Created!");
        })
        .catch((error) => {
          console.log(error);
          alert("Already applied for this role!");
        });
    },
    getStaffSkills(){
      axios
        .get(`${getStaffSkills}${this.employeeId}`)
        .then((response) => {
          console.log(JSON.stringify(response.data));
          this.staff_skills = response.data;
          this.staff_skills.forEach((skillObject) => {
            this.availableSkills.push(skillObject.skill.skill_name);
          });
          console.log(`==== staff's available skills: ${this.availableSkills}`)
        })
        .catch((error) => {
          console.log("Failed to get staff skills")
          console.log(JSON.stringify(error));
        });
    }
  },
  mounted() {
    const appStore = useAppStore(); 
    this.employeeId = appStore.staff_details.staff_id;
    this.getListingDetails();
    this.getRequiredSkills();
    this.getStaffSkills();
  },
};
</script>
