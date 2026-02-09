import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { fetchPatient } from "../../api/patients";
import PatientDetailView from "./PatientDetailView";
import PatientForm from "./PatientForm";
import CareTeamSection from "../careTeam/CareTeamSection";
import ScreeningsSection from "../screenings/ScreeningsSection";
import styles from "./PatientDetailPanel.module.css";

export default function PatientDetailPanel({ patientId, showCreateForm, onCloseCreateForm }) {
  const navigate = useNavigate();
  const [editing, setEditing] = useState(false);
  const [creating, setCreating] = useState(false);
  const isCreating = creating || showCreateForm;

  const { data: patient, isLoading, error } = useQuery({
    queryKey: ["patient", patientId],
    queryFn: () => fetchPatient(patientId),
    enabled: !!patientId && !isCreating,
  });

  const handleCloseCreate = (created) => {
    setCreating(false);
    onCloseCreateForm?.();
    if (created?.id) navigate(`/patients/${created.id}`);
  };

  if (isCreating) {
    return (
      <div className={styles.panel}>
        <PatientForm
          onSuccess={handleCloseCreate}
          onCancel={() => {
            setCreating(false);
            onCloseCreateForm?.();
          }}
        />
      </div>
    );
  }

  if (!patientId) {
    return (
      <div className={styles.empty}>
        <p>Select a patient from the list or create a new one.</p>
        <button type="button" className={styles.createBtn} onClick={() => setCreating(true)}>
          Create new patient
        </button>
      </div>
    );
  }

  if (isLoading) return <div className={styles.loading}>Loading patient…</div>;
  if (error) return <div className={styles.error}>Failed to load: {error.message}</div>;
  if (!patient) return null;

  if (editing) {
    return (
      <div className={styles.panel}>
        <PatientForm
          patient={patient}
          onSuccess={() => setEditing(false)}
          onCancel={() => setEditing(false)}
        />
      </div>
    );
  }

  return (
    <div className={styles.panel}>
      <PatientDetailView patient={patient} onEdit={() => setEditing(true)} />
      <CareTeamSection patientId={patientId} />
      <ScreeningsSection patientId={patientId} />
    </div>
  );
}
