import { useState } from "react";
import { useParams } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { fetchPatients } from "../api/patients";
import PatientList from "../components/patients/PatientList";
import PatientDetailPanel from "../components/patients/PatientDetailPanel";
import styles from "./PatientsPage.module.css";

export default function PatientsPage() {
  const { patientId } = useParams();
  const [showCreateForm, setShowCreateForm] = useState(false);
  const { data: patients = [], isLoading, error } = useQuery({
    queryKey: ["patients"],
    queryFn: fetchPatients,
  });

  return (
    <div className={styles.page}>
      <div className={styles.listPane}>
        <PatientList
          patients={patients}
          isLoading={isLoading}
          error={error}
          selectedId={patientId}
          onNewPatient={() => setShowCreateForm(true)}
        />
      </div>
      <div className={styles.detailPane}>
        <PatientDetailPanel
          patientId={patientId}
          showCreateForm={showCreateForm}
          onCloseCreateForm={() => setShowCreateForm(false)}
        />
      </div>
    </div>
  );
}
