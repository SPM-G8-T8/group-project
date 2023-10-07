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

    },
    closeDialog(){
        this.dialog = false;
    }
  }
}
</script>