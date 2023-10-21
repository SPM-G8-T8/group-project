<template>
    <v-dialog v-model="dialog" width="700px" activator="parent" persistent>
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
                        <tr>
                            <td></td>
                            <td></td>
                            <td></td>
                            <td></td>
                            <td>
                                <v-btn color="primary">
                                    Skill Details
                                    <SkillsDetailDialog/>
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
import axios from "axios";
import SkillsDetailDialog from "@/components/SkillsDetailDialog.vue";

export default{
    components:{
        SkillsDetailDialog
    },
    data(){
        return {
            dialog: false,
        }
    },

    methods: {

        closeDialog(){
            this.dialog = false;
        }
    }
}
</script>