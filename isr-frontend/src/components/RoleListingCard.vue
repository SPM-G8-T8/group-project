<template>
  <v-card class="my-1" color="blue-grey-lighten-5">
    <v-card-title style="font-size: medium">
      {{ roleListing.role.role_name }}
      <v-card-subtitle class="d-flex font-italic align-center pa-0">
        ID: {{ roleListing.role_listing_id }}
      </v-card-subtitle>
      <v-card-subtitle class="d-flex font-italic align-center pa-0">
        Match Skills: {{ match_skills }}%
      </v-card-subtitle>
    </v-card-title>

    <v-card-text>
      Closing Date: {{ roleListing.role_listing_close }}
    </v-card-text>

    <v-card-actions class="justify-end">
     <v-btn color="primary" elevated :to="{ name: 'ApplyRole', params: { listingID: roleListing.role_listing_id } }"
        >Apply</v-btn
      >
    </v-card-actions>
  </v-card>
</template>
<script>
import { getSkillMatch } from "@/api/api";
import axios from "axios";
import { useAppStore } from "@/store/app";

export default {
  props: {
    roleListing: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      employeeId: 1,
      match_skills: null,
    };
  },
  mounted() {
    const appStore = useAppStore();
    // this.employeeId = window.sessionStorage.getItem("employeeId")
    //   ? window.sessionStorage.getItem("employeeId")
    //   : 1; // for testing, default to 1
    console.log(`staff_details: ${JSON.stringify(appStore.staff_details)}`)
    this.employeeId = appStore.staff_details ? appStore.staff_details.staff_id : 1;


    // this.employeeId = window.sessionStorage.getItem("employeeId")
    this.getMatchSkills(this.roleListing.role_listing_id);
  },
  methods: {
    async getMatchSkills(roleId) {
      console.log(`${getSkillMatch}/${this.employeeId}/${roleId}`);
      axios
        .get(`${getSkillMatch}/${this.employeeId}/${roleId}`)
        .then((response) => {
          console.log(JSON.stringify(response.data));
          this.match_skills = response.data.data.matching_percentage;
        })
        .catch((error) => {
          console.log(JSON.stringify(error));
        });
    },
  },
  computed: {},
};
</script>
