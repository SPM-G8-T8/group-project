<template>
  <v-container>
    <v-row>
      <v-col>
        <p class="text-h5 py-3">Role Listings</p>
      </v-col>
      <v-col>
        <v-text-field v-model="search" variant="outlined" placeholder="Search Role Listing...">
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
            <th class="text-h6">Role</th>
            <th class="text-h6">Description</th>
            <th class="text-h6">Listing Open</th>
            <th class="text-h6">Listing Close</th>
            <th class="text-h6">Actions</th>
            <th class="text-h6">Applicants</th>
          </tr>
        </thead>
        <tr v-for="(listing, index) in roleListings" :key="index">
          <td class="text-h6">{{ listing.role_id }}</td>
          <td class="text-h6">
            {{
              listing.role_listing_desc
              ? listing.role_listing_desc
              : "No Description"
            }}
          </td>
          <td class="text-h6">{{ listing.role_listing_open }}</td>
          <td class="text-h6">{{ listing.role_listing_close }}</td>
          <td><v-btn color="grey" class="my-2 mx-3">Edit
              <EditRoleListingDialog />
            </v-btn></td>
          <td class="text-h6 py-1"><v-btn color="blue">View applicants</v-btn></td>
        </tr>
      </v-table>
    </div>
    <div>
      <v-btn :disabled="!hasPrev" @click="prevPage">prev page</v-btn>

      <v-btn @click="goToPage(i)" :disabled="i === page" v-for="i in range(Math.max(1, page - 2), Math.min(totalPages, page + 2))">
        {{ i }}
      </v-btn>

      <v-btn :disabled="!hasNext" @click="nextPage">next page</v-btn>

      <p>Total Pages: {{ totalPages }}</p>
      <p>Total Listings: {{ total }}</p>
    </div>
  </v-container>
</template>

<script>
import CreateRoleListingDialog from "@/components/CreateRoleListingDialog.vue";
import EditRoleListingDialog from "@/components/EditRoleListingDialog.vue";
import { getRoleListing } from "@/api/api.js";
import axios from "axios";


export default {
  components: {
    CreateRoleListingDialog,
    EditRoleListingDialog
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
    }
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
    range(start, end) {
      const result = [];
      for (let i = start; i <= end; i++) {
        result.push(i);
      }
      return result;
    },
    nextPage() {
      this.page++;
      this.fetchRoleListings({ page: this.page, size: this.size, hide_expired: false });
    },
    prevPage() {
      this.page--;
      this.fetchRoleListings({ page: this.page, size: this.size, hide_expired: false });
    },
    goToPage(page) {
      this.fetchRoleListings({ page: page, size: this.size, hide_expired: false });

    }
  },
  mounted() {
    this.getRoleListings();
  },
};
</script>
