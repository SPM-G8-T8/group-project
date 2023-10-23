<template>
    <v-dialog v-model="dialog" width="500px" activator="parent" persistent>
        <v-card>
            <v-card-title>
                Skills Details
            </v-card-title>
            <v-card-text>
                <v-row>
                    <h4>Skills Matched:</h4> {{ matchedSkillsString }}
                </v-row>
                <v-row >
                    <h4>Skills Absent:</h4> {{ missingSkillsString }}
                </v-row>
                <v-row>
                    <h4>Other Skills: </h4> {{ otherSkillsString }}
                </v-row>
            </v-card-text>
            <v-card-actions class="justify-center">
                <v-btn color="primary" @click="closeDialog">
                    Close
                </v-btn>
            </v-card-actions>

        </v-card>
    </v-dialog>
</template>

<script>
import { getSkills } from "@/api/api.js"
import axios from "axios";
export default {
    props: {
        details: Array
    },

    data() {
        return {
            dialog: false,
            allSkills: null,
            matchedSkills: [],
            missingSkills: [],
            otherSkills: [],
            matchedSkillsString: "",
            missingSkillsString: "",
            otherSkillsString: "",
        }
    },

    watch: {
        dialog(newVal) {
            if (newVal) {
                this.getAllSkills().then(() => {
                    console.log("Fetched skills")
                    console.log(this.allSkills)
                    console.log(this.details)
                    this.matchedSkills = this.details[1]['matched']
                    this.missingSkills = this.details[1]['unmet']
                    this.otherSkills = this.details[1]['unused']
                    this.generateSkillName(this.matchedSkills, this.missingSkills, this.otherSkills)
                })

            }
        }
    },

    methods: {
        async getAllSkills() {
            if (!this.allSkills) {
                const response = await axios.get(getSkills);
                console.log(response.data.items);
                this.allSkills = response.data.items;
            }
        },
        generateSkillName(matchedSkillsArr, missingSkillsArr, otherSkillsArr) {
            if (this.allSkills) {
                this.matchedSkillsString = matchedSkillsArr
                    .map((skillId) => {
                        const skill = this.allSkills.find((s) => s.skill_id === skillId);
                        return skill ? skill.skill_name : "";
                    })
                    .join(", ");
                this.missingSkillsString = missingSkillsArr
                    .map((skillId) => {
                        const skill = this.allSkills.find((s) => s.skill_id === skillId);
                        return skill ? skill.skill_name : "";
                    })
                    .join(", ");
                this.otherSkillsString = otherSkillsArr
                    .map((skillId) => {
                        const skill = this.allSkills.find((s) => s.skill_id === skillId);
                        return skill ? skill.skill_name : "";
                    })
                    .join(", ");
                if(!this.matchedSkillsString){
                    this.matchedSkillsString = "No matched skills"
                } if(!this.missingSkillsString){
                    this.missingSkillsString = "No missing skills"
                } if(!this.otherSkillsString){
                    this.otherSkillsString = "No other skills"
                }
            }
        },
        closeDialog() {
            this.dialog = false;
        }
    }
}


</script>