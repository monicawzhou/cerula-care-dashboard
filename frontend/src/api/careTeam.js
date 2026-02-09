import { api } from "./client.js";

/** GET /care-team-members – list all (for assignment dropdown) */
export function fetchAllCareTeamMembers() {
  return api.get("/care-team-members");
}

/** GET /patients/:id/care-team – assigned members */
export function fetchPatientCareTeam(patientId) {
  return api.get(`/patients/${patientId}/care-team`);
}

/** POST /patients/:id/care-team/:memberId – assign */
export function assignCareTeamMember(patientId, careTeamMemberId) {
  return api.post(`/patients/${patientId}/care-team/${careTeamMemberId}`);
}

/** DELETE /patients/:id/care-team/:memberId – unassign */
export function unassignCareTeamMember(patientId, careTeamMemberId) {
  return api.delete(`/patients/${patientId}/care-team/${careTeamMemberId}`);
}
