<template>
    <v-dialog v-model="dialog" width="900px" activator="parent" persistent>
        <v-card>
            <v-card-title>
                Potential Candidates
            </v-card-title>
            <v-card-text>
                <v-table>
                    <thead>
                        <tr>
                            <th>Name</th>
                            <th>Email</th>
                            <th>Current Role</th>
                            <th>Match Rate</th>
                            <th></th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="(detail, index) in allStaffMatch" :key="index">
                            <td>{{ allStaff[detail[0]-1]["staff_fname"] }} {{ allStaff[detail[0]-1]["staff_lname"] }}</td>
                            <td>{{ allStaff[detail[0]-1]["email"] }}</td>
                            <td>{{ allStaff[detail[0]-1]["dept"] }}</td>
                            <td>{{ detail[1]['matching_percentage'] }}%</td>
                            <td>
                                <v-btn color="primary">
                                    Skill Details
                                    <SkillsDetailDialog :details="detail"/>
                                </v-btn>
                            </td>
                        </tr>
                    </tbody>
                </v-table>
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
import SkillsDetailDialog from "@/components/SkillsDetailDialog.vue";
import axios from "axios";
import { getAllStaff, getAllStaffMatch } from "@/api/api.js";

export default{
    props: {
        selectedRole: Number,
    },
    components:{
        SkillsDetailDialog
    },
    data(){
        return {
            dialog: false,
            allStaffMatch: [],
            allStaff: [],
            details: []
        }
    },

    watch:{
        dialog(newVal){
            if(newVal){
                this.getTopCandidates();
                console.log(this.selectedRole)
            }
        }
    },

    methods: {
        getTopCandidates(){
            axios
            .get(`${getAllStaffMatch}${this.selectedRole}`)
            .then((response) => {
                console.log(response.data)
                this.allStaffMatch = response.data;
            }).catch((error) =>{
                console.error(error)
            })

            axios
            .get(getAllStaff)
            .then((response) => {
                this.allStaff = response.data
            }).catch((error) =>{
                console.error(error)
            })
        },
        

        closeDialog(){
            this.dialog = false;
        }
    }
}
</script>