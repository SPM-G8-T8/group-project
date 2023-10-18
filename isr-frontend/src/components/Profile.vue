<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <h1>Skills Profile: {{ staff_details ? staff_details.staff_fname : 'User Unavailable' }}</h1>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12">
        <h2>Skills:</h2>
        <ul>
          <li v-for="skill in staff_skills" :key="skill.skill_id">
            {{ skill.skill.skill_name }} - {{ skill.ss_status }}
          </li>
        </ul>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12">
        <h2>Update Skills:</h2>
        <form @submit.prevent="updateSkills">
          <v-select
            v-model="selectedSkill"
            :items="availableSkills"
            label="Select a Skill"
            item-text="skill_name"
            item-value="skill_id"
          ></v-select>
          <v-select
            v-model="selectedStatus"
            :items="['active', 'in-progress', 'unverified']"
            label="Select Status"
          ></v-select>
          <v-btn type="submit" color="primary">Update Skill</v-btn>
        </form>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { getStaffSkills } from "@/api/api";
import axios from "axios";
import { useAppStore } from "@/store/app";

export default {
  data() {
    return {
      employeeId: 1,
      staff_skills: null,
      staff_details: null,
      selectedSkill: null,
      selectedStatus: null,
      selectedSkillId: null,
      availableSkills: [],
    };
  },
  mounted() {
    const appStore = useAppStore();
    console.log(`staff_details: ${JSON.stringify(appStore.staff_details)}`);
    this.employeeId = appStore.staff_details ? appStore.staff_details.staff_id : 1;
    this.staff_details = appStore.staff_details;
    this.getStaffSkills(this.employeeId);
  },
  methods: {
    async getStaffSkills(employeeId) {
      axios.get(`${getStaffSkills}${this.employeeId}`)
        .then((response) => {
          console.log(JSON.stringify(response.data));
            this.staff_skills = response.data;
            this.staff_skills.forEach((skillObject) => {
            this.availableSkills.push(skillObject.skill.skill_name);
            this.selectedSkill = skillObject.skill.skill_name;
            this.selectedStatus = skillObject.ss_status;
            console.log(`skillobject: ${skillObject.skill_id}`)
            });
        })
        .catch((error) => {
          console.log(JSON.stringify(error));
        });
    },
    updateSkills() {
      this.staff_skills.forEach((skillObject) => {
        if (skillObject.skill.skill_name === this.selectedSkill) {
          this.selectedSkillId = skillObject.skill_id;
        }
      });
        axios({
        url:`http://localhost:8000/staff-skills/update/${this.employeeId}?skill_id=${this.selectedSkillId}&skill_status=${this.selectedStatus}`,
        method:"PUT",
        headers:{
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": 'GET, POST, PUT, DELETE, OPTIONS'
        }
    }).then((response) => {
      alert("Skill updated!");
      console.log(response);
      this.getStaffSkills(this.employeeId);
    })
    .catch((error) => {
        alert("Skill updated, please refresh the page to see changes!");
        console.log(error);

    });
    },
  },
};
</script>