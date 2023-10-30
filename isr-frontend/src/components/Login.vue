<template>
  <v-container class="fill-height my-2">
    <v-responsive class="align-center text-center fill-height">
      <v-img height="300" src="@/assets/challenge.png" />

      <div class="text-h4 font-weight-light mb-n1">All-In-One</div>
      <div class="py-1" />

      <h1 class="text-h4 font-weight-bold">Skill-based Role Portal</h1>

      <v-card class="mx-auto my-3 px-6 py-8" max-width="344">
        <v-form v-model="form" @submit.prevent="onSubmit">
          <v-text-field
            v-model="username"
            :readonly="loading"
            :rules="[required]"
            class="mb-2"
            label="Email"
            variant="outlined"
            density="compact"
            hide-details="auto"
          ></v-text-field>

          <v-text-field
            type="password"
            v-model="password"
            :readonly="loading"
            :rules="[required]"
            label="Password"
            placeholder="Enter your password"
            variant="outlined"
            density="compact"
            hide-details="auto"
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

      <v-card>
        <v-card-title> Accounts </v-card-title>
        <v-card-text>
          <p>HR: john.doe@example.com</p>
          <p>Staff: jane.smith@example.com</p>
          <p>Manager: bob.johnson@example.com</p>
        </v-card-text>
      </v-card>
    </v-responsive>
  </v-container>
</template>

<script>
import { getStaffDetails, getStaffSkills } from "@/api/api";
import { useAppStore } from "@/store/app";
import { mapActions } from "pinia";
import axios from "axios";

console.log('env', import.meta.env)

export default {
  data: () => ({
    form: false,
    username: null,
    password: null,
    loading: false,
  }),
  methods: {
    onSubmit(e) {
      e.preventDefault();
      if (!this.form) return;
      this.loading = true;
      setTimeout(() => (this.loading = false), 2000);
      const { username } = this;
      
      axios
        .get(getStaffDetails, { params: { staff_email: username } })
        .then((response) => {
          console.log(response);
          this.updateStaffDetails(response.data);

          const { staff_id } = response.data;

          axios
            .get(getStaffSkills + `${staff_id}`)
            .then((response) => {
              console.log(response);
              this.updateStaffSkills(response.data);
            })
            .catch((error) => {
              console.log(`Error: ${error}`);
            });

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
    ...mapActions(useAppStore, ["updateStaffDetails", "updateStaffSkills"]),
  },
};
</script>
