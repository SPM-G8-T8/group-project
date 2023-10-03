<template>
  <v-card class="my-5" color="blue-grey-lighten-5">
    <v-card-title style="font-size: medium">
      {{ roleListing.role.role_name }}
      <v-card-subtitle class="d-flex font-italic align-center pa-0">
        ID: {{ roleListing.role_listing_id }}
      </v-card-subtitle>
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
export default {
  props: {
    roleListing: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {};
  },
  methods: {},
};
</script>
