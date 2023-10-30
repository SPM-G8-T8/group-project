<template>
  <v-dialog v-model="dialog" width="500px" activator="parent" persistent>
    <v-card>
      <v-card-title>Upload Certification</v-card-title>
      <v-card-text>
        <v-text-field
          v-model="certificationName"
          label="Certification Name"
        ></v-text-field>
        <v-text-field
          v-model="certifyingAgency"
          label="Certifying Agency"
        ></v-text-field>
        <v-text-field
          v-model="awardee_name"
          label="Awardee Name"
        ></v-text-field>
        Certification Date:
        <input type="date" v-model="certificationDate" />
        <v-file-input
          clearable
          label="File input"
          v-model="file"
        ></v-file-input>
      </v-card-text>
      <v-alert v-if="errorMessage">{{ errorMessage }}</v-alert>
      <v-card-actions class="justify-center">
        <v-btn color="primary" type="submit" @click="submitForm">Submit</v-btn>
        <v-btn color="primary" @click="closeDialog">Close</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import { UploadStaffSkillCert } from "@/api/api";
import axios from "axios";

export default {
  props: {
    staffId: Number,
    skillId: Number,
  },
  data() {
    return {
      file: null,
      localStaffId: this.staffId,
      localSkillId: this.skillId,
      certificationName: "",
      certificationDate: null,
      certifyingAgency: "",
      awardee_name: "",
      errorMessage: "",
      dialog: false,
    };
  },
  methods: {
    submitForm() {
      console.log(this.certificationDate)
      console.log(this.staffId)
      const formData = new FormData();
      let data = {
        staff_id: this.localStaffId,
        skill_id: this.localSkillId,
        certification_name: this.certificationName,
        certifying_agency: this.certifyingAgency,
        certification_date: this.certificationDate,
        awardee_name: this.awardee_name,
      }
      for (const key in data) {
        formData.append(key, data[key]);
      }
      if (this.file) {
        formData.append("file", this.file[0]);
      }

      axios
        .post(`${UploadStaffSkillCert}`, formData, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        })
        .then((response) => {
          console.log("Response:", response.data);
        })
        .catch((error) => {
          console.error("Error:", error);
          this.errorMessage =
            "Error uploading File, please ensure that file is PDF/PNG/JPG";
        });
        alert("File uploaded successfully!")
        this.closeDialog()
    },

    updateFormData(key, value) {
      this.formData[key] = value;
    },

    closeDialog() {
      this.dialog = false;
    },
  },
};
</script>
