<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <h1>
          Skills Profile:
          {{ staff_details ? staff_details.staff_fname : "User Unavailable" }}
        </h1>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12">
        <h2>Skills:</h2>
        <ul>
          <li v-for="skill in staff_skills" :key="skill.skill_id">
            {{ skill.skill.skill_name }} - {{ skill.ss_status }}
            <v-btn color="primary">
              Upload Cert
              <FileUpload :staffId="this.employeeId" :skillId="skill.skill_id"/>
            </v-btn>
            <v-btn @click="previewCert(skill.skill_id)"> Preview Cert </v-btn>
          </li>
        </ul>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import FileUpload from "@/components/FileUpload.vue";
import { getStaffSkills } from "@/api/api";
import { UpdateStaffSkills } from "@/api/api";
import { FetchStaffSkillCert } from "@/api/api";
import axios from "axios";
import { useAppStore } from "@/store/app";

export default {
  components: {
    FileUpload,
  },
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
    this.employeeId = appStore.staff_details
      ? appStore.staff_details.staff_id
      : 1;
    this.staff_details = appStore.staff_details;
    this.getStaffSkills(this.employeeId);
  },
  methods: {
    async getStaffSkills(employeeId) {
      axios
        .get(`${getStaffSkills}${this.employeeId}`)
        .then((response) => {
          console.log(JSON.stringify(response.data));
          this.staff_skills = response.data;
          this.staff_skills.forEach((skillObject) => {
            this.availableSkills.push(skillObject.skill.skill_name);
            this.selectedSkill = skillObject.skill.skill_name;
            this.selectedStatus = skillObject.ss_status;
            console.log(`skillobject: ${skillObject.skill_id}`);
          });
        })
        .catch((error) => {
          console.log(JSON.stringify(error));
        });
    },
    previewCert(skillId) {
      console.log(this.employeeId)
      console.log(skillId)
      axios
        .get(`${FetchStaffSkillCert}${this.employeeId}/${skillId}`)
        .then((response) => {
          console.log(response);
          let previewUrl = response.data;
          window.open(previewUrl, '_blank')

        })
        .catch((error) => {
          alert("Error fetching cert preview");
          console.log(error);
        });
    },
  },
};
</script>
