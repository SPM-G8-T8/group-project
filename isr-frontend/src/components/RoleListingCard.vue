<template>
  <v-card class="my-5" min-height="200" color="blue-grey-lighten-5">
    <v-card-title>
      {{ roleListing.role.role_name }}
    </v-card-title>

    <v-card-text>
      <v-row>
        <v-col cols="12" md="8">
          <v-card-subtitle class="font-italic pa-0">
            Listing ID: {{ roleListing.role_listing_id }}
          </v-card-subtitle>
          <div class="my-2">
            <p class="text-subtitle-2">Job Description</p>
            <p>
              {{ roleListing.role_listing_desc }}
            </p>
          </div>
        </v-col>
        <v-col cols="12" md="4">
          <v-card border>
            <v-card-text class="text-center">
              <p class="text-body-1">
                Closing Date: {{ roleListing.role_listing_close }}
              </p>
            </v-card-text>
            <v-card-actions>
              <v-btn class="w-100" variant="tonal">Learn More </v-btn>
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>
    </v-card-text>
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
