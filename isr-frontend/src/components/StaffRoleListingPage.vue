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
          clearable
        >
        </v-text-field>
      </v-col>
    </v-row>

    <v-divider></v-divider>

    <div class="d-flex flex-row mt-5">
      <p class="text-h6">Search Results ({{ total }})</p>
      <v-spacer></v-spacer>
    </div>
    <div class="my-3">
      <v-row>
        <v-col
          cols="12"
          sm="6"
          lg="4"
          v-for="(listing, index) in roleListings"
          :key="index"
        >
          <RoleListingCard :roleListing="listing" />
        </v-col>
      </v-row>
      <PaginationToolBar
        :page="page"
        :totalPages="totalPages"
        @change-page="changePage"
      />
    </div>
  </v-container>
</template>

<script>
import { getRoleListing } from "@/api/api.js";
import RoleListingCard from "@/components/RoleListingCard.vue";
import PaginationToolBar from "@/components/PaginationToolBar.vue";
import axios from "axios";

export default {
  components: {
    RoleListingCard,
    PaginationToolBar,
  },
  data() {
    return {
      roleListings: [],
      search: "",
      page: 1,
      size: null,
      total: 0,
      totalPages: 1,
    };
  },
  methods: {
    fetchRoleListings(queryParams) {
      console.log("Fetching Role Listings...");

      axios
        .get(getRoleListing, { params: queryParams })
        .then((response) => {
          console.log(response.data.total);
          this.roleListings = response.data.items;
          this.total = response.data.total;
          this.totalPages = response.data.pages;
        })
        .catch((error) => {
          console.error("Error fetching role listings:", error);
        });
    },
    getRoleListings() {
      const queryParams = {
        page: this.page || 1,
        size: this.size,
        hide_expired: true,
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
    changePage(newPage) {
      this.page = newPage;

      this.fetchRoleListings({
        page: this.page,
        size: this.size,
        hide_expired: false,
      });
    },
  },
  mounted() {
    this.getRoleListings();
  },
};
</script>
