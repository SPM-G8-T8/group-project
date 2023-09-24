<template>
  <v-dialog v-model="dialog" width="500px" activator="parent" persistent>
    <v-card>
      <v-card-title> Create Role Listing </v-card-title>
      <v-card-text>
        <v-form v-model="isFormValid">
          <v-row>
            <v-col cols="6">
              <v-text-field
                label="Role Listing ID"
                variant="outlined"
                density="compact"
                hide-details="auto"
                v-model="roleListingId"
                :rules="[rules.required, rules.number]"
                :disabled="createdSuccess"
              ></v-text-field>
            </v-col>
            <v-col cols="6">
              <v-text-field
                label="Role ID"
                variant="outlined"
                density="compact"
                hide-details="auto"
                v-model="roleId"
                :rules="[rules.required, rules.number]"
                :disabled="createdSuccess"
              >
              </v-text-field>
            </v-col>
          </v-row>
          <v-row>
            <v-col cols="6">
              <v-text-field
                label="Role Listing Source"
                variant="outlined"
                density="compact"
                hide-details="auto"
                v-model="roleListingSource"
                :rules="[rules.required, rules.number]"
                :disabled="createdSuccess"
              >
              </v-text-field>
            </v-col>
          </v-row>

          <v-divider class="my-3"></v-divider>

          <v-textarea
            label="Role Listing Description"
            variant="outlined"
            hide-details="auto"
            density="compact"
            v-model="roleListingDesc"
            :disabled="createdSuccess"
          >
          </v-textarea>

          <v-divider class="my-3"></v-divider>

          <v-row>
            <v-col cols="6">
              <v-text-field
                label="Role Listing Open Date"
                variant="outlined"
                density="compact"
                type="date"
                v-model="roleListingOpen"
                :rules="[rules.required]"
                hide-details="auto"
                :disabled="createdSuccess"
              >
              </v-text-field>
            </v-col>
            <v-col cols="6">
              <v-text-field
                label="Role Listing Close Date"
                variant="outlined"
                density="compact"
                type="date"
                v-model="roleListingClose"
                :rules="[rules.required]"
                hide-details="auto"
                :min="roleListingOpen"
                :disabled="roleListingOpen.length == 0 || createdSuccess"
              >
              </v-text-field>
            </v-col>
          </v-row>
        </v-form>
        <v-alert class="mt-3" type="warning" v-if="errorMessage.length > 0">
          <span v-html="errorMessage"> </span>
        </v-alert>

        <v-alert
          class="mt-3"
          type="success"
          v-if="createdSuccess"
          text="Role Listing Successfully Created!"
        >
        </v-alert>
      </v-card-text>
      <v-card-actions class="justify-center">
        <v-btn color="primary" text @click="closeForm"> Close </v-btn>
        <v-btn
          color="primary"
          text
          @click="createRoleList"
          :disabled="!isFormValid"
          v-if="!createdSuccess"
        >
          Create
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import axios from "axios";
import { createRoleListing } from "@/api/api.js";

export default {
  data() {
    return {
      dialog: false,
      roleListingId: "",
      roleId: "",
      roleListingSource: "",
      roleListingDesc: "",
      roleListingOpen: "",
      roleListingClose: "",
      isFormValid: false,
      errorMessage: "",
      createdSuccess: false,

      rules: {
        required: (value) => !!value || "Field is required.",
        number: (value) => !isNaN(parseInt(value)) || "Field must be a number.",
      },
    };
  },
  methods: {
    createRoleList() {
      console.log("Role Listing ID: ", this.roleListingId);
      console.log("Role ID: ", this.roleId);
      console.log("Role Listing Source: ", this.roleListingSource);
      console.log("Role Listing Description: ", this.roleListingDesc);
      console.log("Role Listing Open Date: ", this.roleListingOpen);
      console.log("Role Listing Close Date: ", this.roleListingClose);

      if (this.roleListingOpen > this.roleListingClose) {
        this.errorMessage = "Open Date must be before Close Date.";
      } else {
        // Create Role Listing
        axios
          .post(createRoleListing, {
            role_listing_id: this.roleListingId,
            role_id: this.roleId,
            role_listing_source: this.roleListingSource,
            role_listing_desc: this.roleListingDesc,
            role_listing_open: this.roleListingOpen,
            role_listing_close: this.roleListingClose,
            role_listing_creator: 1,
          })
          .then((response) => {
            console.log(response);
            this.errorMessage = "";
            this.createdSuccess = true;
          })
          .catch((error) => {
            console.log(error);
            this.errorMessage = error.response.data.detail;
          });
      }
    },

    closeForm() {
      this.roleListingId = "";
      this.roleId = "";
      this.roleListingSource = "";
      this.roleListingDesc = "";
      this.roleListingOpen = "";
      this.roleListingClose = "";
      this.errorMessage = "";
      this.createdSuccess = false;

      this.dialog = false;
    },
  },
};
</script>
