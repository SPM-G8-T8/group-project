<template>
    <v-container>
        <v-row>
            <v-col cols="12">
                <h1>Skills</h1>
            </v-col>
        </v-row>
        <v-row>
            <v-col cols="8">
                <p>Search for skills</p>
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
            <div v-for="skill in skills" :key="skill.skill_id">
                <v-col cols="4">
                    <v-card width="350">
                        <v-row>
                            <v-col cols="6">
                                <v-card-title>{{ skill.skill_name }}</v-card-title>
                            </v-col>
                            <v-col>
                                <v-card-actions>
                                    <v-btn color="orange">Edit</v-btn>
                                </v-card-actions>
                            </v-col> 
                        </v-row>

                        <v-row>
                            <v-col cols="6">
                                <v-card-subtitle>{{ skill.skill_status }}</v-card-subtitle>
                            </v-col>
                            <v-col>
                                <!-- add delete button here -->
                            </v-col>
                        </v-row>
                    </v-card>
                </v-col>
            </div>
        </v-row>
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

                <v-row class="flex-1-1-100 ma-2 pa-2">
                    <v-card-actions>
                        <v-btn color="success" @click="addSkills">Save</v-btn>
                        <v-btn color="grey" @click="overlay = false">Cancel</v-btn>
                    </v-card-actions>
                </v-row>
            </v-card>
        </v-overlay>
    </v-container>
</template>

<script>
import axios from 'axios';
export default {
    data() {
        return {
            skills: [],
            overlay: false,
            delete_overlay: false,
            name: "",
            status: ""
        }
    }, 
    computed: {
        //
    },
    methods: {
        getAllSkills() {
            axios.get('http://localhost:8000/skills')
            .then(response => {
                this.skills = response.data.items;
                console.log(this.skills);
            })
            .catch(error => {
                console.log(error);
            })
        },
        addSkills() {
            axios.post('http://localhost:8000/skills/create', {
                skill_id: this.skills.length + 1,
                skill_name: this.name,
                skill_status: this.status
            })
            .then(response => {
                console.log(response);
                window.location.reload();
            })
            .catch(error => {
                console.log(this.status)
                console.log(error);
            })
        }
        // add delete function here
    },
    mounted() {
        this.getAllSkills();
    }
}
</script>