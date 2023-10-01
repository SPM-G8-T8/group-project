<template>
  <v-container>
    <v-row>
      <v-col cols="12" lg="4">
        <p class="text-h5 py-3">Open Role Listings</p>
      </v-col>
      <v-col cols="12" lg="8">
        <v-text-field
          v-model="search"
          variant="outlined"
          placeholder="Search Role Listing..."
          density="compact"
          append-inner-icon="mdi-magnify"
          rounded
          @update:model-value="searchRoleListings"
        >
        </v-text-field>
      </v-col>
    </v-row>

    <v-divider></v-divider>

    <div class="d-flex flex-row mt-7">
      <p class="text-h6">Search Results</p>
      <v-spacer></v-spacer>
    </div>
    <div class="my-3">
      <RoleListingCard
        v-for="(listing, index) in roleListings"
        :key="index"
        :roleListing="listing"
      />
    </div>
  </v-container>
</template>

<script>
import { getRoleListing } from "@/api/api.js";
import RoleListingCard from "@/components/RoleListingCard.vue";
import axios from "axios";

export default {
  components: {
    RoleListingCard,
  },
  data() {
    return {
      roleListings: [],
      search: "",
      page: 1,
      size: null,
    };
  },
  methods: {
    fetchRoleListings(queryParams) {
      console.log("Fetching Role Listings...");

      axios
        .get(getRoleListing, { params: queryParams })
        .then((response) => {
          this.roleListings = response.data.items;
        })
        .catch((error) => {
          console.error("Error fetching role listings:", error);
        });
    },
    getRoleListings() {
      const queryParams = {
        page: this.page || 1,
        size: this.size,
      };
      this.fetchRoleListings(queryParams);
    },
    searchRoleListings() {
      const queryParams = {
        page: this.page || 1,
        size: this.size,
        filter: this.search,
      };
      this.fetchRoleListings(queryParams);
    },
  },
  mounted() {
    this.getRoleListings();
  },
};
</script>
