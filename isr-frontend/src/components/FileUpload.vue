
<template>
  <v-container>
    <v-file-input clearable label="File input" v-model="file"></v-file-input>
  </v-container>
  <button type="submit" @click="submitForm">Submit</button>
</template>
<script>
import { UploadStaffSkillCert } from "@/api/api";
import axios from "axios";

export default {
  data() {
    return {
      formData: {
        staff_id: '122323',
        skill_id: '11111',
        certification_name: 'he',
        certifying_agency: 'dasd',
        certification_date: '2125-12-12',
        awardee_name: 'HELLO',
      },
      file: null,
    };
  },
  methods: {
    submitForm() {
      console.log(this.file[0])
      const formData = new FormData();
      for (const key in this.formData) {
        formData.append(key, this.formData[key]);
      }
      if (this.file) {
        formData.append('file', this.file[0]);
      }

      axios
        .post(`${UploadStaffSkillCert}`, formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        })
        .then((response) => {
          // Handle the response
          console.log('Response:', response.data);
        })
        .catch((error) => {
          // Handle errors
          console.error('Error:', error);
        });
    },

    updateFormData(key, value) {
      this.formData[key] = value;
    },
  },

};
</script>
