<template>
  <v-container>
    <v-row>
      <v-col  cols="12" lg="4">
        <p class="text-h5 py-3">Role Listings</p>
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

    <div class="d-flex flex-row mt-7 mr-10 mb-5">
      <p class="text-h6">Search Results</p>
      <v-spacer></v-spacer>
      <v-btn color="primary" v-if="sys_role == 'hr'">
        + Create Role Listing
        <CreateRoleListingDialog :roleList="roleList" :staffList="staffList" />
      </v-btn>
    </div>
    <div>
      <v-table density="compact">
        <thead>
          <tr>
            <th class="text-center text-h6">Role</th>
            <th class="text-center text-h6">Description</th>
            <th class="text-center text-h6">Listing Open</th>
            <th class="text-center text-h6">Listing Close</th>
            <th v-if="sys_role=='hr'" class="text-center text-h6">Actions</th>
            <th class="text-center text-h6">Applicants</th>
            <th class="text-center text-h6">Potential Candidates</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(listing, index) in roleListings" :key="index">
            <td class="text-center pl-4">{{ listing.role.role_name }}</td>
            <td class="text-center pl-4">
              {{
                listing.role_listing_desc
                ? listing.role_listing_desc
                : "No Description"
              }}
            </td>
            <td class="text-center">{{ listing.role_listing_open }}</td>
            <td class="text-center">{{ listing.role_listing_close }}</td>
            <td v-if="sys_role == 'hr'" class="text-center">
              <v-btn color="grey" class="my-2" density="compact" @click="deactivateListingBtn(listing.role_listing_id)">Deactivate</v-btn>
              <v-btn color="grey" class="my-2 mx-3" density="compact" @click="openEditDialog(listing.role_listing_id)">Edit
                <EditRoleListingDialog :roleList="roleList" :staffList="staffList" :selectedListingId='listing.role_listing_id' />
              </v-btn>
            </td>
            <td class="text-center py-1">
              <v-btn color="blue" density="compact" @click="viewApplicants(listing.role_id, listing.role_listing_id)">View applicants</v-btn>
            </td>
            <td class="text-center py-1">
              <v-btn color="blue-grey" density="compact" class="my-2 mx-3" @click="openCandidateDialog(listing.role_id)">Potential Candidates
                <CandidatesDialog :selectedRole="listing.role_id"/>
              </v-btn>
            </td>
          </tr>
        </tbody>
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
import CandidatesDialog from "@/components/CandidatesDialog.vue";
import { getRoleListing, getRoleListingByCreator,deactivateListing, getAllStaff, getRoles } from "@/api/api.js";
import { useAppStore } from "@/store/app";
import axios from "axios";

export default {
  components: {
    CreateRoleListingDialog,
    EditRoleListingDialog,
    PaginationToolBar,
    CandidatesDialog
  },
  data() {
    return {
      roleListings: [],
      search: "",
      page: 1,
      size: 10,
      total: null,
      totalPages: 1,
      selectedListingId: null,
      selectedRole: null,
      employeeId: null,
      sys_role: "",
      staffList: [],
      roleList: [],
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
      // console.log(`employee ID: ${this.employeeId}`)
      // console.log(`sys_role: ${this.sys_role}`)
      if (this.sys_role == "hr") {
        axios
          .get(getRoleListing, { params: queryParams })
          .then((response) => {
            console.log(response.data)
            this.roleListings = response.data.items;
            this.page = response.data.page;
            this.total = response.data.total;
            this.totalPages = response.data.pages;
          })
          .catch((error) => {
            console.error("Error fetching role listings:", error);
          });
      } else {
        axios
          .get(`${getRoleListingByCreator}${this.employeeId}`, { params: queryParams })
          .then((response) => {
            this.roleListings = response.data.items;
            this.page = response.data.page;
            this.total = response.data.total;
            this.totalPages = response.data.pages;
          })
          .catch((error) => {
            console.error("Error fetching role listings:", error);
          });
      }
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
    openEditDialog(listingId) {
      this.selectedListingId = listingId;
      console.log(this.selectedListingId + " printed")
    },
    openCandidateDialog(roleId){
      this.selectedRole = roleId;
      console.log(this.selectedRole + " printed")
    },
    viewApplicants(roleID, listingID) {
      this.$router.push({
        name: "ViewApplicants",
        params: { roleID: roleID, listingID: listingID },
      });
    },
    deactivateListingBtn(listingID) {
      axios.patch(`${deactivateListing}${listingID}`).then(() => {
        // Reload the table to reflect the change
        this.getRoleListings();
      }).catch((err) => {
        console.error(err);
        // You may want to add error messages telling your user about the error
      })
    },
    getAllStaff() {
      axios.get(getAllStaff).then((response) => {
        console.log(response.data)
        this.staffList = response.data
      }).catch((error) => {
        console.error(error)
      })
    },
    getRoles() {
      axios.get(getRoles).then((response) => {
        this.roleList = response.data
      }).catch((error) => {
        console.error(error)
      })
    },
  },
  mounted() {
    const appStore = useAppStore();
    // this.employeeId = window.sessionStorage.getItem("employeeId")
    //   ? window.sessionStorage.getItem("employeeId")
    //   : 1; // for testing, default to 1
    console.log(`staff_details: ${JSON.stringify(appStore.staff_details)}`);
    this.employeeId = appStore.staff_details.staff_id;
    this.sys_role = appStore.staff_details.sys_role;
    this.getRoleListings();
    this.getAllStaff();
    this.getRoles();
  },
};
</script>
