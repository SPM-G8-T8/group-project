<template>
  <v-container>

    <div v-if="loaded">
        <v-row>
            <v-col cols="12" class="mt-4">
                <v-card>
                <v-card-title>
                    <h3 class="text-h5">{{ listingDetails.role.role_name }}</h3>
                </v-card-title>
                <v-card-text>
                    <p class="text-h6">{{ listingDetails.role.role_description }}</p>
                    <p class="text-subtitle-1">{{ listingDetails.role_listing_desc }}</p>
                </v-card-text>
                <v-card-actions>
                    <v-btn color="blue">Number of applicants: {{ applicants.length }}</v-btn>
                </v-card-actions>
                </v-card>
            </v-col>
        </v-row>
    </div>
    <div v-else>
        Loading...
    </div>

    <v-row>
        <v-col cols="4" class="mt-2">
            <h2>Applicants for this role</h2>
        </v-col>
        <v-col cols="8">
            <v-text-field
                label="Search for applicant name"
                outlined
                v-model="search"
                append-inner-icon="mdi-magnify"
                append-icon="mdi-close"
                @click:append="clearSearch"
            ></v-text-field>
        </v-col>
        <div v-show="noApplicants">
            <h2 class="ps-3">No applicants yet</h2>
        </div>
    </v-row>
    <v-row>
        <div v-for="a in searchApplicants()" :key="a.staff_id">
            <v-col cols="12">
                <v-card width="350">
                <v-card-title>
                    <h3 class="text-h6">{{ a.staff_fname }} {{ a.staff_lname }}</h3>
                </v-card-title>
                <v-card-text>
                    <p class="text-subtitle-1">Staff ID: {{ a.staff_id }}</p>
                </v-card-text>
                <v-card-actions>
                    <v-btn color="blue" @click="overlay = !overlay, getStaffRoles(a.staff_id), getStaffSkills(a.staff_id), getStaffRO(a.staff_id)">View full profile</v-btn>
                    <v-overlay v-model="overlay" class="align-center justify-center">
                        <v-card class="my-1" color="blue-grey-lighten-5" width="350">
                            <v-card-title style="font-size: medium">
                                {{ a.staff_fname }} {{ a.staff_lname }}
                            <v-card-subtitle class="d-flex font-italic align-center pa-0">
                                ID: {{ a.staff_id }}
                            </v-card-subtitle>
                            <v-card-subtitle class="d-flex font-italic align-center pa-0">
                                Email: {{ a.email }}
                            </v-card-subtitle>
                            <v-card-subtitle class="d-flex font-italic align-center pa-0">
                                Phone: {{ a.phone }}
                            </v-card-subtitle>
                            <v-card-subtitle class="d-flex font-italic align-center pa-0">
                                Office Address: {{ a.biz_address }}
                            </v-card-subtitle>
                            </v-card-title>

                            <v-card-text>
                            Department: {{ a.dept }} 
                            </v-card-text>

                            <v-card-text v-if="this.staffRO != 0">
                            Reporting Officer: {{ roDetails.staff_fname }} {{ roDetails.staff_lname }} 
                                <v-card-subtitle class="d-flex font-italic align-center pa-0">
                                    RO Contact Email: {{ roDetails.email }}
                                </v-card-subtitle>
                                <v-card-subtitle class="d-flex font-italic align-center pa-0">
                                    RO Contact Phone: {{ roDetails.phone }}
                                </v-card-subtitle>
                            </v-card-text>

                            <v-card-text v-for="roles in roleDetails" :key="roles.role_id">
                                Role: {{ roles.role_name }} - {{ roles.role_description }}
                            </v-card-text>
                            <v-card-text v-if="roleDetails.length==0">No roles listed</v-card-text>
                            <div class="px-4 py-2">
                                <p class="text-h6">Skills:</p>
                                <v-chip-group v-for="skill in skillDetails" :key="skill.skill_id">
                                    <v-chip>{{ skill.skill_name }}</v-chip>
                                </v-chip-group>
                            </div>
                            <v-card-text v-if="skillDetails.length==0">No skills listed</v-card-text>
                        </v-card>
                    </v-overlay>
                </v-card-actions>
                </v-card>
            </v-col>
        </div>
    </v-row>


  </v-container>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
        listingID: this.$route.params.listingID,
        applicants: [],
        listingDetails: [],
        staffRoles: [],
        roleDetails: [],
        staffSkills: [],
        skillDetails: [],
        staffID: 0,
        noApplicants: false,
        loaded: false,
        overlay: false,
        search: "",
        staffRO: 0,
        roDetails: [],
    };
  },
  methods: {
    clearSearch() {
        this.search = "";
    },
    getListingDetails() {
        axios
            .get(`http://localhost:8000/listing/${this.listingID}`)
            .then((response) => {
                this.listingDetails = response.data;
                this.loaded = true;
                console.log(this.listingDetails);
            })
            .catch((error) => {
                console.log(error);
            });
    },
    getApplicantDetails() {
        axios
            .get(`http://localhost:8000/applicants/${this.listingID}`)
            .then((response) => {
                this.applicants = response.data.items;
                console.log(this.applicants)
            })
            .catch((error) => {
                console.log(error);
                this.noApplicants = true;
                console.log(this.noApplicants)
            });
    },
    // need to test below function
    getStaffRoles(staffID) {
        axios
            .get(`http://localhost:8000/staff-roles/${staffID}`)
            .then((response) => {
                this.staffRoles = response.data;
                console.log(this.staffRoles);
                this.roleDetails = [];
                for (let role in this.staffRoles) {
                    axios
                        .get(`http://localhost:8000/roles/${role.staff_role}`)
                        .then((response) => {
                            this.roleDetails.push(response.data);
                            console.log(this.roleDetails);
                        })
                        .catch((error) => {
                            console.log(error);
                        });
                }
            })
            .catch((error) => {
                console.log(error);
                this.staffRoles = [];
                this.roleDetails = [];
            });
    },
    getStaffSkills(staffID) {
        axios
            .get(`http://localhost:8000/staff-skills/${staffID}`)
            .then((response) => {
                this.staffSkills = response.data.items;
                this.skillDetails = [];
                for (let skill = 0; skill < this.staffSkills.length; skill++) {
                    axios
                        .get(`http://localhost:8000/skills/${this.staffSkills[skill].skill_id}`)
                        .then((response) => {
                            this.skillDetails.push(response.data);
                            console.log(this.skillDetails);
                        })
                        .catch((error) => {
                            console.log(error);
                        });
                }
            })
            .catch((error) => {
                console.log(error);
                this.staffSkills = [];
                this.skillDetails = [];
            });
    },
    getStaffRO(staffID) {
        axios.get(`http://localhost:8000/staff-ro/${staffID}`)
            .then((response) => {
                this.staffRO = response.data.RO_id;
                console.log(this.staffRO);
                axios.get(`http://localhost:8000/staff/${this.staffRO}`)
                    .then((response) => {
                        this.roDetails = response.data;
                        console.log(this.roDetails);
                    })
                    .catch((error) => {
                        console.log(error);
                    });
            })
            .catch((error) => {
                console.log(error);
            });
    },
    searchApplicants() {
        let result = this.applicants.filter(applicant => {
            return applicant.staff_fname.concat(" ", applicant.staff_lname).toLowerCase().includes(this.search.toLowerCase());
        });
        return result;
    }
  },
  mounted() {
    this.getListingDetails();
    this.getApplicantDetails();
  },
};

</script>
