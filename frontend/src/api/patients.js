import { api } from "./client.js";

/** GET / – list all patients */
export function fetchPatients() {
  return api.get("/");
}

/** GET /patient/:id – get one patient */
export function fetchPatient(id) {
  return api.get(`/patient/${id}`);
}

/** POST /patients – create patient */
export function createPatient(data) {
  return api.post("/patients", data);
}

/** PUT /patients/:id – update patient */
export function updatePatient(id, data) {
  return api.put(`/patients/${id}`, data);
}

/** GET /patients/:id/health-screening-scores – last 6 months */
export function fetchHealthScreenings(patientId) {
  return api.get(`/patients/${patientId}/health-screening-scores`);
}
