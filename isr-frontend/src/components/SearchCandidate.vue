<template>
    <v-container>
        <v-row>
            <v-col cols="12" lg="4">
                <p class="text-h5 py-3">Search for Candidates</p>
            </v-col>
            <v-col cols="12" lg="8">
                <v-text-field
                v-model="search"
                variant="outlined"
                placeholder="Search for Candidates..."
                density="compact"
                append-inner-icon="mdi-magnify"
                rounded
                @update:model-value="searchCandidates"
                clearable
                >
                </v-text-field>
            </v-col>
        </v-row>
        
        <v-divider></v-divider>

        <div class="d-flex flex-row mt-7 mr-10 mb-5">
            <p class="text-h6">Search Results</p>
            <v-spacer></v-spacer>
        </div>

        <div>
            <v-table>
                <thead>
                    <tr>
                        
                    </tr>
                </thead>
            </v-table>
        </div>

    </v-container>

</template>

<script>


</script>