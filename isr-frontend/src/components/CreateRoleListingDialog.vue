<template>
  <v-dialog v-model="dialog" width="500px" activator="parent" persistent>
    <v-card>
      <v-card-title> Create Role Listing </v-card-title>
      <v-card-text>
        <v-row>
          <v-col cols="6">
            <v-text-field
              label="Role Listing ID"
              variant="outlined"
              density="compact"
              hide-details="auto"
            ></v-text-field>
          </v-col>
          <v-col cols="6">
            <v-text-field
              label="Role ID"
              variant="outlined"
              density="compact"
              hide-details="auto"
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
            >
            </v-text-field>
          </v-col>
        </v-row>

        <v-divider class="my-3"></v-divider>

        <v-textarea
          label="Role Listing Description"
          variant="outlined"
          hide-details="auto"
        >
        </v-textarea>

        <v-divider class="my-3"></v-divider>

        <v-row>
          <v-col cols="6">
            <v-text-field
              label="Role Listing Start Date"
              variant="outlined"
              type="date"
            >
            </v-text-field>
          </v-col>
          <v-col cols="6">
            <v-text-field
              label="Role Listing End Date"
              variant="outlined"
              type="date"
            >
            </v-text-field>
          </v-col>
        </v-row>
      </v-card-text>
      <v-card-actions class="justify-center">
        <v-btn color="primary" text @click="dialog = false"> Cancel </v-btn>
        <v-btn color="primary" text @click="dialog = false"> Create </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  data() {
    return {
      dialog: false,
    };
  },
  methods: {
    //
  },
};
</script>
