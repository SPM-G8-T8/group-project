<template>
  <v-container>
    <v-row>
      <v-col>
        <p class="text-h5 py-3">Role Listings</p>
      </v-col>
      <v-col>
        <v-text-field
          rounded
          density="compact"
          variant="outlined"
          placeholder="Search Role Listing..."
          append-inner-icon="mdi-magnify"
        >
        </v-text-field>
      </v-col>
    </v-row>

    <v-divider></v-divider>

    <div class="d-flex flex-row mt-7">
      <p class="text-h6">Search Results</p>
      <v-spacer></v-spacer>
      <v-btn color="primary">
        + Create Role Listing <CreateRoleListingDialog />
      </v-btn>
    </div>
  </v-container>
</template>
<script setup>
import CreateRoleListingDialog from "@/components/CreateRoleListingDialog.vue";
</script>
