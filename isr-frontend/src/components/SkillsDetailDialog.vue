<template>
    <v-dialog v-model="dialog" width="500px" activator="parent" persistent>
        <v-card>
            <v-card-title>
                Skills Details
            </v-card-title>
            <v-card-text>
                <v-row>
                    <v-col cols="6">
                        <h4>Skills Matched:</h4>
                    </v-col>
                </v-row>
                <v-row>
                    <v-col cols="6">
                        <h4>Skills Absent:</h4>
                    </v-col>
                </v-row>
                <v-row>
                    <v-col cols="6">
                        <h4>Other Skills:</h4>
                    </v-col>
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
import axios from "axios";

export default{
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