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
    updateStaffSkills(staff_skills) {
      this.staff_skills = staff_skills;
    },
    resetState() {
      this.staff_details = null;
      this.staff_skills = [];
    },
  },
});
