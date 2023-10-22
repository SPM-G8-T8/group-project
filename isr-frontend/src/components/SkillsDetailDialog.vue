<template>
    <v-dialog v-model="dialog" width="500px" activator="parent" persistent>
        <v-card>
            <v-card-title>
                Skills Details
            </v-card-title>
            <v-card-text>
                <v-row>
                    <h4>Skills Matched:</h4> {{ matchedSkills }}
                </v-row>
                <v-row>
                    <h4>Skills Absent:</h4> {{ missingSkills }}
                </v-row>
                <v-row>                        
                    <h4>Other Skills: </h4> {{ otherSkills }}
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
export default{
    props:{
        details: Array
    },

    data(){
        return {
            dialog: false,
            allSkills: {},
            matchedSkills: [],
            missingSkills: [],
            otherSkills: [],
            matchedSkillsString: "",
            missingSkillsString: "",
        }
    },

    watch: {
        dialog(newVal){
            if(newVal){
                this.getAllSkills();
                this.matchedSkills = this.details[1]['matched']
                this.missingSkills = this.details[1]['unmet']
                this.otherSkills = this.details[1]['unused']
                // this.generateSkillName(this.matchedSkills, this.missingSkills)
            }
        }
    },

    methods: {
        getAllSkills(){
            axios
            .get(getSkills)
            .then((response) => {
                console.log(response.data.items)
                this.allSkills = response.data.items
            }).catch((error) =>{
                console.error("Error fetching skills: " + error)
            })
        },
        // generateSkillName(matchedSkillsArr, missingSkillsArr){
        //     if(matchedSkillsArr > 1){
        //         for(let i=0; i<matchedSkillsArr.length; i++){
        //             let objSkill = this.allSkills[matchedSkillsArr[i]]
        //             this.matchedSkillsString += objSkill["skill_name"] + " "
        //         }
        //     } if (missingSkillsArr.length > 1) {
        //         for(let i=0; i<missingSkillsArr.length; i++){
        //             let objSkill = this.allSkills[missingSkillsArr[i]]
        //             console.log(objSkill)
        //             this.missingSkillsString += objSkill["skill_name"] + " "
        //         }
        //     } else {
        //         this.matchedSkillsString = this.allSkills[matchedSkillsArr[0] -1]
        //         this.missingSkillsString = this.allSkills[missingSkillsArr[0] -1]
        //     }
        // },
        closeDialog(){
            this.dialog = false;
        }
    }
}


</script>