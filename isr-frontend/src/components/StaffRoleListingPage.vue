<template>
  <v-container>
    <v-row>
      <v-col cols="12" lg="4">
        <p class="text-h5 py-3">Open Role Listings</p>
      </v-col>
      <v-col cols="12" lg="8">
        <!-- <v-text-field
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
        </v-text-field> -->
      </v-col>
    </v-row>

    <v-divider></v-divider>

    <v-row class="my-3">
      <v-expansion-panels>
        <v-expansion-panel elevation="0">
          <v-expansion-panel-title>
            <p class="text-h6">Search Results ({{ total }})</p>
            <template v-slot:actions>
              <v-icon icon="mdi-filter">
              </v-icon>
            </template>
          </v-expansion-panel-title>
          <v-expansion-panel-text style="border: 1px solid lightgray;">
            <v-row>
              <v-col cols="12" sm="6" lg="4">
                <p>Role</p>
                <v-select
                  :items="roles"
                  item-title="role_name"
                  item-value="role_id"
                  variant="outlined"
                  density="compact"
                  hide-details="auto"
                  clearable
                  v-model="role_filter"
                ></v-select>
              </v-col>

              <v-col cols="12" sm="6" lg="4">
                  <p>Skills</p>
                  <v-autocomplete
                    open-text
                    :items="skills"
                    item-title="skill_name"
                    item-value="skill_id"
                    variant="outlined"
                    density="compact"
                    hide-details="auto"
                    multiple
                    v-model="skills_filter"
                  >
                  <template v-slot:chip="{ props, item }">
                  <v-chip
                    v-bind="props"
                    :text="item.raw.name"
                  ></v-chip>
                </template>
                </v-autocomplete>
              </v-col>
            </v-row>
            <v-row class="justify-end">
              <v-btn variant="flat" @click="searchRoleListings">Apply Filter</v-btn>
            </v-row>
          </v-expansion-panel-text>
        </v-expansion-panel>
      </v-expansion-panels>
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
import { getRoleListing, getRoles, getSkills } from "@/api/api.js";
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
      skills: [],
      skills_filter: [],
    };
  },
  methods: {
    fetchRoleListings(queryParams) {
      console.log("Fetching Role Listings...");

      axios
        .get(getRoleListing, { params: queryParams })
        .then((response) => {
          console.log(response.data);
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
        skills_filter: this.skills_filter
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
          // console.log(response.data);
          this.roles = response.data;
        })
        .catch((error) => {
          console.error("Error fetching role listings:", error);
        });
    },
    getSkills() {
      axios.get(getSkills).then((response) => {
        // console.log(response.data)
        this.skills = response.data
      }).catch((error) => {
        console.error("Error fetching skills:", error);
      });
    },
    
  },
  mounted() {
    this.getRoleListings();
    this.getRoles();
    this.getSkills();
  },
};
</script>
