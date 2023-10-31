<template>
    <v-card class="d-flex flex-wrap mx-auto w-auto">
        <v-row class="flex-1-1-100 ma-2 pa-2">
            <v-card-title>
                {{ editedSkillName }}
            </v-card-title>
        </v-row>
        <v-row class="flex-1-1-100 ma-2 pa-2"><v-text-field v-model="editedSkillName"></v-text-field></v-row>
        <v-row class="flex-1-1-100 ma-2 pa-2">
            <v-card-text>
                <p>Skill ID: {{ skill_id }}</p>
                <v-select v-model="editedSkillStatus" :items="['Active', 'Inactive']" outlined dense></v-select>
            </v-card-text>
        </v-row>
        <v-card-actions>
            <v-btn @click="updateSkill">Update</v-btn>
            <v-btn @click="closeModal">Close</v-btn>
            <v-btn @click="showConfirmDeleteModal=true;">Delete</v-btn>
        </v-card-actions>
    </v-card>

    <!-- Delete Confirmation Modal -->
    <v-dialog v-model="showConfirmDeleteModal">
      <v-card class="d-flex flex-wrap mx-auto w-auto" max-width="800">
        <v-card-title>Delete Skill</v-card-title>
        <v-card-text>Are you sure you want to delete this skill?</v-card-text>
        <v-card-actions>
          <v-btn @click="confirmDelete">Yes</v-btn>
          <v-btn @click="cancelDelete">No</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

  </template>
  
<style>
.v-card__title {
    font-size: 24px;
    font-weight: bold;
    text-align: center;
}
.v-card__text {
    font-size: 18px;
    text-align: center;
}
</style>

<script>
  import { editSkills, deleteSkill } from '@/api/api';
  import axios from 'axios';
  
  export default {
    props: {
      skill_id: {
        type: Number,
        required: true
      },
      skill_name: {
        type: String,
        required: true
      },
      skill_status: {
        type: String,
        required: true
      }
    },
    data() {
      return {
        editedSkillName: this.skill_name, // Create a copy of the prop
        editedSkillStatus: this.skill_status, // Create a copy of the prop
        showConfirmDeleteModal: false
        // note: if I don't use the copy, the prop value edit will cause errors in reactivity.
      };
    },
    methods: {
        updateSkill() {
            const updatedSkillData = {
              skill_name: this.editedSkillName, 
              skill_status: this.editedSkillStatus,
            };
  
            axios
            .put(`${editSkills}${this.skill_id}`, updatedSkillData)
            .then((response) => {
                console.log('Skill updated:', response);
                if (response.status == 200) {
                alert("Skill updated successfully");
                }
            })
            .catch((error) => {
                console.error('Error updating skill:', error);
            });
        },
        closeModal() {
          this.$emit('closeEditModal');
        },
        showDeleteConfirmation() {
           this.showConfirmDeleteModal = true;
        },
        confirmDelete() {
            // Perform the deletion
            axios.delete(`${deleteSkill}${this.skill_id}`)
            .then((response) => {
                console.log('Skill deleted:', response);
                if (response.status === 200) {
                alert("Skill deleted successfully");
                this.$emit('closeEditModal'); // Close the modal after deletion
                }
            })
            .catch((error) => {
                console.error('Error deleting skill:', error);
            });

            this.showConfirmDeleteModal = false; // Close the confirmation modal
        },
        cancelDelete() {
            this.showConfirmDeleteModal = false; // Close the confirmation modal
        },
    },
  };
</script>
  