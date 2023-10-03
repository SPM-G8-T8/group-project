<template>
  <v-row>
    <v-col class="text-center">
      <div>
        <v-btn
          variant="plain"
          @click="$emit('changePage', page - 1)"
          v-if="page > 1"
          >&lt;</v-btn
        >
        <v-btn
          variant="plain"
          @click="$emit('changePage', page - 1)"
          v-if="page > 1"
        >
          {{ page - 1 }}
        </v-btn>
        <v-btn
          variant="plain"
          @click="$emit('changePage', page)"
          :class="{ active: true }"
          disabled
        >
          {{ page }}
        </v-btn>
        <v-btn
          variant="plain"
          @click="$emit('changePage', page + 1)"
          v-if="page < totalPages"
        >
          {{ page + 1 }}
        </v-btn>
        <v-btn
          variant="plain"
          @click="$emit('changePage', page + 1)"
          v-if="page < totalPages"
        >
          &gt;
        </v-btn>
      </div>
    </v-col>
  </v-row>
</template>
<script>
export default {
  emits: ["changePage"],
  props: ["page", "totalPages", "total"],
};
</script>

<style scoped>
.v-btn {
  min-width: 30px;
  padding: 0;
  margin: 3px;
}
.active {
  background-color: #1976d2;
  color: white;
}
</style>
