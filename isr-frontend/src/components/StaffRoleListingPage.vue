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
          append-icon="mdi-magnify"
          rounded
          @click:append="searchRoleListings"
          clearable
          hide-details="auto"
        >
        </v-text-field>
      </v-col>
    </v-row>

    <v-divider></v-divider>

    <v-row class="my-3">
      <v-col cols="12" lg="4">
        <p class="text-h6">Search Results ({{ total }})</p>
      </v-col>
      <v-spacer></v-spacer>
      <v-col cols="12" lg="4">
        <v-select
          label="Filter By Role"
          :items="roles"
          item-title="role_name"
          item-value="role_id"
          variant="outlined"
          density="compact"
          hide-details="auto"
          clearable
          v-model="role_filter"
          @update:model-value="searchRoleListings"
        ></v-select>
      </v-col>
    </v-row>
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
import { getRoleListing, getRoles } from "@/api/api.js";
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
      roles: [],
      role_filter: null,
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
      console.log("Searching Role Listings...");
      const queryParams = {
        page: this.page || 1,
        size: this.size,
        hide_expired: true,
        filter: this.search,
        role_filter: this.role_filter,
      };
      this.fetchRoleListings(queryParams);
    },
    changePage(newPage) {
      this.page = newPage;

      this.fetchRoleListings({
        page: this.page,
        size: this.size,
        hide_expired: false,
        filter: this.search,
        role_filter: this.role_filter,
      });
    },
    getRoles() {
      axios
        .get(getRoles)
        .then((response) => {
          console.log(response.data);
          this.roles = response.data;
        })
        .catch((error) => {
          console.error("Error fetching role listings:", error);
        });
    },
  },
  mounted() {
    this.getRoleListings();
    this.getRoles();
  },
};
</script>
