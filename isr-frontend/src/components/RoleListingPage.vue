<template>
  <v-container>
    <v-row>
      <v-col>
        <p class="text-h5 py-3">Role Listings</p>
      </v-col>
      <v-col>
        <v-text-field
          v-model="search"
          variant="outlined"
          placeholder="Search Role Listing..."
        >
        </v-text-field>
      </v-col>
      <v-col>
        <v-btn color="primary" @click="searchRoleListings"> Search </v-btn>
      </v-col>
    </v-row>

    <v-divider></v-divider>

    <div class="d-flex flex-row mt-7 mr-10 mb-5">
      <p class="text-h6">Search Results</p>
      <v-spacer></v-spacer>
      <v-btn color="primary">
        + Create Role Listing
        <CreateRoleListingDialog />
      </v-btn>
    </div>
    <div>
      <v-table>
        <thead>
          <tr>
            <th class="text-center text-h6">Role</th>
            <th class="text-center text-h6">Description</th>
            <th class="text-center text-h6">Listing Open</th>
            <th class="text-center text-h6">Listing Close</th>
            <th class="text-center text-h6">Actions</th>
            <th class="text-center text-h6">Applicants</th>
          </tr>
        </thead>
        <tr v-for="(listing, index) in roleListings" :key="index">
          <td class="text-center pl-4">{{ listing.role_id }}</td>
          <td class="text-center pl-4">
            {{
              listing.role_listing_desc
                ? listing.role_listing_desc
                : "No Description"
            }}
          </td>
          <td class="text-center">{{ listing.role_listing_open }}</td>
          <td class="text-center">{{ listing.role_listing_close }}</td>
          <td class="text-center">
            <v-btn color="grey" class="my-2 mx-3"
              >Edit
              <EditRoleListingDialog />
            </v-btn>
          </td>
          <td class="text-center py-1">
            <v-btn color="blue">View applicants</v-btn>
          </td>
        </tr>
      </v-table>
    </div>
    <PaginationToolBar
      :page="page"
      :totalPages="totalPages"
      @change-page="changePage"
    />
  </v-container>
</template>

<script>
import CreateRoleListingDialog from "@/components/CreateRoleListingDialog.vue";
import EditRoleListingDialog from "@/components/EditRoleListingDialog.vue";
import PaginationToolBar from "./PaginationToolBar.vue";
import { getRoleListing } from "@/api/api.js";
import axios from "axios";

export default {
  components: {
    CreateRoleListingDialog,
    EditRoleListingDialog,
    PaginationToolBar,
  },
  data() {
    return {
      roleListings: [],
      search: "",
      page: 1,
      size: 2,
      total: null,
      totalPages: 1,
    };
  },
  computed: {
    hasNext() {
      return this.page < this.totalPages;
    },
    hasPrev() {
      return this.page > 1;
    },
  },
  methods: {
    fetchRoleListings(queryParams) {
      axios
        .get(getRoleListing, { params: queryParams })
        .then((response) => {
          this.roleListings = response.data.items;
          this.page = response.data.page;
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
        hide_expired: false,
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
