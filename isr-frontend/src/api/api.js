let rootURL;

if (import.meta.env.VITE_APP_ENV == 'prod') {
  rootURL = "https://spm-backend-tfiy.onrender.com";
} else if (import.meta.env.VITE_APP_ENV == 'staging') {
  rootURL = "https://spm-backend-staging.onrender.com"
} else {
  rootURL = "http://localhost:8000";
}

export const getRoleListing = rootURL + "/listing/";
export const createRoleListing = rootURL + "/listing/create/";
export const editRoleListing = rootURL + "/listing/edit/";
export const getRoleListingByCreator = rootURL + "/listing/created-by/";

export const getSkills = rootURL + "/skills/";
export const getSkillsByName = rootURL + "/skills/byName?skill_name=";
export const createSkills = rootURL + "/skills/create/";
export const editSkills = rootURL + "/skills/editSkill/";
export const deleteSkill = rootURL + "/skills/deleteSkill/";

export const getSkillMatch = rootURL + "/skill-match/matching-percentage/";
export const deactivateListing = rootURL + "/listing/deactivate";
export const getAllStaffMatch = rootURL + "/skill-match/findMatches/";

export const getStaffRoles = rootURL + "/staff-roles/";
export const getRoles = rootURL + "/roles/";
export const getStaffRO = rootURL + "/staff-ro/"

export const getRoleApplication = rootURL + "/applicants/";
export const createRoleApplication = rootURL + "/applicants/create/";

export const getAllStaff = rootURL + "/all-staff/";
export const getStaffDetails = rootURL + "/staff/";
export const getStaffSkills = rootURL + "/staff-skills/";
export const getStaffSkillsSBRP = rootURL + "/staff-skills-sbrp/";
export const updateStaffSkills = rootURL + "/staff-skills/add/";
export const UploadStaffSkillCert = rootURL + "/staff-skills/upload-cert/"
export const FetchStaffSkillCert = rootURL + "/staff-skills/get-cert/"

