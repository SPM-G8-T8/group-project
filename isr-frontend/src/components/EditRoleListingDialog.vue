<template>
    <v-dialog v-model="dialog" width="500px" activator="parent" persistent>
        <v-card>
            <v-card-title>
                Edit Role Listing
            </v-card-title>
            <v-card-text>
                <v-form v-model="isFormValid">
                    <v-row>
                        <v-col cols="6"> 
                            <v-text-field
                                label="Role Listing ID"
                                variant="outlined"
                                density="compact"
                                hide-details="auto"
                                v-model="roleListingId"
                                disabled
                                :rules="[rules.required, rules.number]"
                            ></v-text-field>
                        </v-col>
                        <v-col cols="6">
                            <v-text-field
                                label="Role ID"
                                variant="outlined"
                                density="compact"
                                hide-details="auto"
                                v-model="roleId"
                                disabled
                                :rules="[rules.required, rules.number]"
                            >
                            </v-text-field>
                        </v-col>
                    </v-row>

                    <v-row>
                        <v-col cols="6">
                        <v-text-field
                            label="Role Listing Source"
                            variant="outlined"
                            density="compact"
                            hide-details="auto"
                            v-model="roleListingSource"
                            :rules="[rules.required, rules.number]"
                            :disabled="editSuccess"
                        >
                        </v-text-field>
                        </v-col>
                    </v-row>

                    <v-divider class="my-3"></v-divider>
                    
                    <v-textarea
                        label="Role Listing Description"
                        variant="outlined"
                        hide-details="auto"
                        density="compact"
                        v-model="roleListingDesc"
                        :disabled="editSuccess"
                    >
                    </v-textarea>

                    <v-divider class="my-3"></v-divider>

                    <v-row>
                        <v-col cols="6">
                        <v-text-field
                            label="Role Listing Open Date"
                            variant="outlined"
                            density="compact"
                            type="date"
                            v-model="roleListingOpen"
                            :rules="[rules.required]"
                            hide-details="auto"
                            :disabled="editSuccess"
                        >
                        </v-text-field>
                        </v-col>
                        <v-col cols="6">
                        <v-text-field
                            label="Role Listing Close Date"
                            variant="outlined"
                            density="compact"
                            type="date"
                            v-model="roleListingClose"
                            :rules="[rules.required]"
                            hide-details="auto"
                            :min="roleListingOpen"
                            :disabled="roleListingOpen.length == 0 || editSuccess"
                        >
                        </v-text-field>
                        </v-col>
                    </v-row>
                </v-form>
                <v-alert class="mt-3" type="warning" v-if="errorMessage.length > 0">
                    <span v-html="errorMessage"> </span>
                </v-alert>

                <v-alert
                    class="mt-3"
                    type="success"
                    v-if="editSuccess"
                    text="Role Listing Successfully Edited!"
                >
                </v-alert>
            </v-card-text>
            <v-card-actions class="justify-center">
                <v-btn color="primary" text @click="closeDialog"> Close </v-btn>
                <v-btn
                color="primary"
                text
                @click="editRoleList"
                :disabled="!isFormValid"
                v-if="!editSuccess"
                >
                Update
                </v-btn>
            </v-card-actions>
        </v-card>
    </v-dialog>
</template>
<script>
import axios from "axios";
import { editRoleListing, getRoleListing } from "@/api/api.js";

export default {
  props: {
    selectedListingId: Number,
},
  data() {
    return {
      dialog: false,
      roleListingId: "",
      roleId: "",
      roleListingSource: "",
      roleListingDesc: "",
      roleListingOpen: "",
      roleListingClose: "",
      isFormValid: false,
      errorMessage: "",
      editSuccess: false,

      rules: {
        required: (value) => !!value || "Field is required.",
        number: (value) => !isNaN(parseInt(value)) || "Field must be a number.",
      },
    };
  },

  watch: {
    dialog(newVal){
        console.log("showDialog")
        if (newVal) {
            this.fetchListingDetails();
        }
    }
  },

  methods: {    
    fetchListingDetails(){
        console.log("fetchlisting")
        this.roleListingId = this.selectedListingId;
        axios.get(`${getRoleListing}/${this.selectedListingId}`)
        .then(response => {
            this.roleId = response.data.role_id
            this.roleListingSource = response.data.role_listing_source
            this.roleListingDesc = response.data.role_listing_desc
            this.roleListingOpen = response.data.role_listing_open
            this.roleListingClose = response.data.role_listing_close
        })
        .catch(error=>{
            console.log(error)
        })
    },

    editRoleList(){
        if (this.roleListingOpen > this.roleListingClose) {
            this.errorMessage = "Open Date must be before Close Date.";
        } else {
            axios
            .put(`${editRoleListing}/${this.selectedListingId}`,{
                role_listing_source: this.roleListingSource,
                role_listing_desc: this.roleListingDesc,
                role_listing_open: this.roleListingOpen,
                role_listing_close: this.roleListingClose,
            })
            .then((response) => {
                console.log(response);
                this.editSuccess = true;
                // this.$router.go() // reload
            })         
            .catch((error) => {
                console.log(error);
                this.errorMessage = error.response.data.detail;
            });
        }
 
    },

    closeDialog(){
        this.errorMessage = "";
        this.dialog = false;
        if(this.editSuccess){
            this.$router.go();
        }
        this.editSuccess = false;

    }
  }
}
</script>