<template>
  <v-container class="fill-height">
    <v-responsive class="align-center text-center fill-height">
      <v-img height="300" src="@/assets/challenge.png" />

      <div class="text-h4 font-weight-light mb-n1">All-In-One</div>
      <div class="py-1" />

      <h1 class="text-h3 font-weight-bold">Skill-based Role Portal</h1>

      <div class="py-3" />
      <v-card class="mx-auto px-6 py-8" max-width="344">
        <v-form v-model="form" @submit.prevent="onSubmit">
          <v-text-field
            v-model="username"
            :readonly="loading"
            :rules="[required]"
            class="mb-2"
            label="Email"
          ></v-text-field>

          <v-text-field
            type="password"
            v-model="password"
            :readonly="loading"
            :rules="[required]"
            label="Password"
            placeholder="Enter your password"
          ></v-text-field>

          <br />

          <v-btn
            :disabled="!form"
            :loading="loading"
            block
            color="info"
            size="large"
            type="submit"
            variant="elevated"
          >
            Sign In
          </v-btn>
        </v-form>
      </v-card>
    </v-responsive>
  </v-container>
</template>

<script>
import { getStaffDetails } from "@/api/api";
import { useAppStore } from "@/store/app";
import { mapActions } from "pinia";
import axios from "axios";

export default {
  data: () => ({
    form: false,
    username: null,
    password: null,
    loading: false,
  }),
  methods: {
    onSubmit() {
      if (!this.form) return;
      this.loading = true;
      setTimeout(() => (this.loading = false), 2000);
      const { username } = this;

      axios
        .get(getStaffDetails, { params: { staff_email: username } })
        .then((response) => {
          console.log(response);
          this.updateStaffDetails(response.data);
          this.$router.push("/");
        })
        .catch((error) => {
          console.log(`Error: ${error}`);
          alert("Invalid username or password");
        });
    },
    required(v) {
      return !!v || "Field is required";
    },
    ...mapActions(useAppStore, ["updateStaffDetails"]),
  },
};
</script>
