<template>
    <v-container>
        <v-row>
            <v-col cols="12">
                <h1>Skills</h1>
            </v-col>
        </v-row>
        <v-row>
            <v-col cols="8">
                <v-text-field
                    label="Search"
                    outlined
                    v-model="search"
                    append-inner-icon="mdi-magnify"
                    append-icon="mdi-close"
                    @click:append="clearSearch">
                </v-text-field>
            </v-col>
            <v-col cols="4">
                <v-btn @click="overlay = !overlay">
                    <v-icon icon="mdi-plus"></v-icon>
                    Add new skills
                </v-btn>
            </v-col>
        </v-row>
        <v-row>
            <v-col cols="12">
                <p>Skills list</p>
            </v-col>
        </v-row>
        <v-row>
            <div v-for="skill in searchSkills()" :key="skill.skill_id">
                <v-col cols="4">
                    <v-card width="350">
                        <v-row>
                            <v-col cols="8">
                                <v-card-title>{{ skill.skill_name }}</v-card-title>
                            </v-col>
                            <v-col>
                                <v-card-actions>
                                    <!-- to add modal @click and listen for modal close event. editSkill doesn't work!-->
                                    <v-btn @click="editSkill(skill)" color="orange">Edit</v-btn>
                                    
                                </v-card-actions>
                            </v-col> 
                        </v-row>
                        

                        <v-row class="mb-1">
                            <v-col cols="6">
                                <v-card-subtitle>Status: {{ skill.skill_status }}</v-card-subtitle>
                            </v-col>
                            <v-col>
                                <!-- add delete button here -->
                            </v-col>
                        </v-row>
                    </v-card>
                    
                </v-col>
            </div>
        

        </v-row>
        <v-overlay v-model="editVisible" class="align-center justify-center" color="rgba(0, 0, 0, 0.8">
            <SkillAdminEdit
                    :skill_id="selected.skill_id"
                    :skill_name="selected.skill_name"
                    :skill_status="selected.skill_status"
                    @closeEditModal="handleCloseModal"
                />
        </v-overlay>


        
        <v-overlay v-model="overlay" class="align-center justify-center">
            <v-card class="d-flex flex-wrap mx-auto w-auto">
                <v-card-title>Add new skill</v-card-title>
                <v-row class="flex-1-1-100 ma-2 pa-2">
                    <v-col cols="4">Skill Name</v-col>
                    <v-col cols="8">
                        <v-text-field
                            label="Skill name"
                            outlined
                            v-model="name"
                        ></v-text-field>
                    </v-col>
                </v-row>
                <v-row class="flex-1-1-100 ma-2 pa-2">
                    <v-col cols="4">Skill status</v-col>
                    <v-col cols="8">
                        <v-select
                            :items="['Active', 'Inactive']"
                            label="Status"
                            outlined
                            v-model="status"
                        ></v-select>
                    </v-col>
                </v-row>
                <div v-if="name_exists">
                    <v-alert
                        closable
                        title="Skill name already exists"
                        type="error"
                        variant="outlined"
                    ></v-alert>
                </div>
                <v-row class="flex-1-1-100 ma-2 pa-2">
                    <v-card-actions>
                        <v-btn color="success" @click="addSkills">Save</v-btn>
                        <v-btn color="grey" @click="overlay = false, name = '', status = '', name_exists=false">Cancel</v-btn>
                    </v-card-actions>
                </v-row>
            </v-card>
        </v-overlay>
    </v-container>
</template>

<script>
import axios from 'axios';
import SkillAdminEdit from '@/components/SkillAdminEdit';
export default {
    data() {
        return {
            skills: [],
            overlay: false,
            delete_overlay: false,
            name: "",
            status: "",
            unavail_names: [],
            name_exists: false,
            search: "",
            selected: null,
            editVisible: false,
        }
    }, 
    components:{
        SkillAdminEdit
    },
    computed: {
        //
    },
    methods: {
        editSkill(skill){
            this.selected = skill;
            this.editVisible = true;
            

        },
        getAllSkills() {
            axios.get('http://localhost:8000/skills')
            .then(response => {
                console.log(response.data);
                this.skills = response.data;
                this.unavail_names = this.skills.map(skills => skills.skill_name);
                // Q: What is the map function trying to do and why does it not work?
                // A: The map function is trying to get the skill_name from the skills array and store it in the unavail_names array.
                //    It does not work because the skills array is empty.
                
            })
            .catch(error => {
                console.log(error);
            })
        },
        searchSkills() {
            let result = this.skills.filter(skill => {
                return skill.skill_name.toLowerCase().includes(this.search.toLowerCase());
            });
            return result;
        },
        clearSearch() {
            this.search = "";
        },
        addSkills() {
            if (this.unavail_names.includes(this.name)) {
                this.name_exists = true;
            } else {
                this.name_exists = false;
                axios.post('http://localhost:8000/skills/create', {
                    skill_id: this.skills.slice(-1)[0].skill_id + 1,
                    skill_name: this.name,
                    skill_status: this.status
                })
                .then(response => {
                    console.log(response);
                    // window.location.reload();
                    this.getAllSkills();
                    this.overlay = false;
                })
                .catch(error => {
                    console.log(skill_id)
                    console.log(error);
                })
            }
        },
        handleCloseModal() {
            // Handle the modal close event here
            this.getAllSkills();
            this.editVisible = false;
            // this.selected = null; // For example, clear the selected data when the modal is closed
            
            
        },
        // add delete function here

    },
    mounted() {
        this.getAllSkills();
    }
}
</script>