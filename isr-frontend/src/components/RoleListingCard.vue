<template>
  <v-card class="my-5" color="blue-grey-lighten-5">
    
      
      <v-card-title style="font-size: medium">
        {{ roleListing.role.role_name }}
        <v-row>
          <v-col cols="6">
            <v-card-subtitle class="d-flex font-italic pa-0">
              ID: {{ roleListing.role_listing_id }}
            </v-card-subtitle>
          </v-col>
          <v-col cols="6"  v-if="getSkillsMatch(roleListing.role_listing_id)">
            <v-card-subtitle class="text-primary text-right">
              Skills match: {{ getSkillsMatch(roleListing.role_listing_id) }}
            </v-card-subtitle>
          </v-col>
          <v-card-text v-else class="text-warning">
              Skills match not available for staff {{ staffId }} and role {{ roleListing.role_listing_id }}
            </v-card-text>
        </v-row>
      </v-card-title>
      
       

      <v-card-text>
        Closing Date: {{ roleListing.role_listing_close }}
      </v-card-text>

      <v-card-actions class="justify-end">
        <v-btn color="primary" elevated :to="{ path: 'role-listing' }"
          >View Info</v-btn
        >
      </v-card-actions>
  </v-card>
</template>
<script>
import axios from 'axios';
import { matchSkills } from "@/api/api.js";
export default {
  props: {
    roleListing: {
      type: Object,
      required: true,
    },
    staffId: {
      type: String,
      required: true,
    }
  },
  data() {
    return {
      skillsMatch: 0,
    };
  },
  methods: {
    getSkillsMatch(role_listing_id){
      let skills_match_endpoint = matchSkills + `/${this.staffId}/${role_listing_id}`;
      console.log(skills_match_endpoint)
      axios.get(skills_match_endpoint).then((response) => {
        return response.data.matching_percentage;
      });
    }

  },
  mounted() {
  }
};
</script>
