<template>
  <v-row class="ma-2 flex-wrap">
    <v-col cols="auto" v-for="match in matched" :key="`match-${match}`" class="pa-2">
      <SkillMatchIcon :skillId="match" :matched="true"/>
    </v-col>
    <v-col cols="auto" v-for="unmatch in unmatched" :key="`unmatch-${unmatch}`" class="pa-2">
      <SkillMatchIcon :skillId="unmatch" :matched="false"/>
    </v-col>
  </v-row>
</template>
  
  <script>
  import axios from 'axios'
  import { getSkillMatch } from '@/api/api'
  import SkillMatchIcon from "@/components/SkillMatchIcon"
  
  export default {
    components: {
      SkillMatchIcon
    },
    props: {
      employeeId: {
        type: Number,
        required: true
      },
      roleId: {
        type: Number,
        required: true
      }
    },
    data() {
      return {
        matched:[],
        unmatched:[]
      }
    },
    async mounted() {
      try {
        const response = await axios.get(`${getSkillMatch}/${this.employeeId}/${this.roleId}`);
        console.log(JSON.stringify(response))
        this.matched = response.data.data.matched;
        this.unmatched = response.data.data.unmet;
      } catch (error) {
        console.log(error)
      }
    }
  }
  </script>
  