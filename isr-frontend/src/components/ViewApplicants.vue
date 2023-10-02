<template>
  <v-container>
    <v-row>
        <v-col cols="12" class="mt-4">
            <v-card>
            <v-card-title>
                <h3 class="text-h6">Role name</h3>
            </v-card-title>
            <v-card-text>
                <p class="text-h6">Role description</p>
            </v-card-text>
            <v-card-actions>
                <v-btn color="blue">Number of applicants</v-btn>
            </v-card-actions>
            </v-card>
        </v-col>
    </v-row>
    <v-row>
        <v-col cols="4" class="mt-2">
            <h2>Applicants</h2>
        </v-col>
        <v-col cols="8">
            <v-text-field
                label="Search for applicant name"
                outlined
                v-model="search"
                append-inner-icon="mdi-magnify"
                append-icon="mdi-close"
                @click:append="clearSearch"
            ></v-text-field>
        </v-col>
        <v-col cols="12" md="6" lg="4">
            <v-card>
            <v-card-title>
                <h3 class="text-h6">Applicant name</h3>
            </v-card-title>
            <v-card-text>
                <p class="text-h6">Applicant's matching skills list</p>
            </v-card-text>
            <v-card-actions>
                <v-btn color="blue">View full profile</v-btn>
            </v-card-actions>
            </v-card>
        </v-col>
    </v-row>
  </v-container>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
        search: ""
    };
  },
  methods: {
    clearSearch() {
            this.search = "";
    },
  },
  mounted() {
  },
};
</script>
