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
      <v-col cols="6">
        <h2>Skills:</h2>
        <ul>
          <li v-for="skill in staff_skills" :key="skill.skill_id">
            {{ skill.skill.skill_name }} - {{ skill.ss_status }} 
            <br />
            <p class="font-weight-medium mt-2">Update Skill:</p>
            <div class="mb-5 mt-2">
            <v-btn color="primary">
              Upload Cert
              <FileUpload :staffId="this.employeeId" :skillId="skill.skill_id"/>
            </v-btn>
            <v-btn class="ml-3" @click="previewCert(skill.skill_id)"> Preview Cert </v-btn>
            </div>
          </li>
        </ul>
      </v-col>
      <v-col cols="6" v-if="addedSkillsList.length > 0">
      <h2>Added Skills:</h2>
          <ul>
          <li v-for="skill in addedSkillsList" :key="skill.skill_id">
            {{ skill.skill_name }} - unverified
            <br />
            <p class="font-weight-medium mt-2">Update Skill:</p>
            <div class="mb-5 mt-2">
            <v-btn color="primary">
              Upload Cert
              <FileUpload :staffId="this.employeeId" :skillId="skill.skill_id"/>
            </v-btn>
            <v-btn class="ml-3" @click="previewCert(skill.skill_id)"> Preview Cert </v-btn>
            </div>
          </li>
        </ul>
      </v-col>
    </v-row>
    <v-row>
    <h2>Add a Skill:</h2>
    </v-row>
    <v-row>
    <v-select
    v-model="select"
    clearable label="Item"
    :items="this.skillList"
    variant="outlined" class="mt-3">
    </v-select>
    </v-row>
    <v-row>
    <v-btn color="primary" type="submit" @click="AddSkillbyId()">
      Add Skill
    </v-btn>
    </v-row>
  </v-container>
</template>

<script>
import FileUpload from "@/components/FileUpload.vue";
import { getStaffSkills } from "@/api/api";
import { FetchStaffSkillCert } from "@/api/api";
import { getSkills } from "@/api/api";
import { getSkillsByName } from "@/api/api";

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
      selectedSkillId: null,
      testList: null,
      addedSkillsList: [],
      skillList: [],
      select: null,
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
    this.getSkillList();
  },
  methods: {
    AddSkillbyId(){
      axios
      .get(`${getSkillsByName}${this.select}`)
      .then((response) => {
        console.log(JSON.stringify(response.data));
        this.addedSkillsList.push(response.data);
        alert("Skill Added Successfully!");
      })
      .catch((error) => {
        console.log(JSON.stringify(error));
      });
    },
    async getStaffSkills(employeeId) {
      axios
        .get(`${getStaffSkills}${this.employeeId}`)
        .then((response) => {
          console.log(JSON.stringify(response.data));
          this.staff_skills = response.data;
        })
        .catch((error) => {
          console.log(JSON.stringify(error));
        });
    },
    async getSkillList() {
      axios
        .get(getSkills)
        .then((response) => {
          console.log(`skillList: ${JSON.stringify(response.data)}`)
          this.testList = response.data;
          this.testList.forEach((skillObject) => {
            this.skillList.push(skillObject.skill_name);
          })
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
