<template>
    <v-chip :color="matched ? 'primary' : 'grey lighten-2'" text-color="white">
        {{ skill.skill_name}}
        <v-icon right>{{ matched ? 'mdi-check' : 'mdi-close' }} </v-icon>
    </v-chip>
</template>

<script>
import axios from 'axios';
import { GET_SKILL } from '@/api/api';

export default {
  props: {
    skillId: {
      type: Number,
      required: true,
    },
    matched:{
      type: Boolean,
      required: true,
    }
  },
  data() {
    return {
      skill: {},
      error: null
    };
  },
  async mounted() {
    try {
      const response = await axios.get(`${GET_SKILL}/${this.skillId}`);
      this.skill = response.data;
    } catch (error) {
      this.error = 'Failed to load skill';
      console.error(error);
    }
  },
};
</script>