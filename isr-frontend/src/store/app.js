// Utilities
import { defineStore } from "pinia";

export const useAppStore = defineStore("app", {
  state: () => ({
    staff_details: null,
    staff_skills: [],
  }),
  actions: {
    updateStaffDetails(staff_details) {
      this.staff_details = staff_details;
    },
  },
});
