import styles from "./PatientListItem.module.css";

export default function PatientListItem({ patient }) {
  const name = [patient.first_name, patient.last_name].filter(Boolean).join(" ") || "—";
  const status = (patient.status || "").toLowerCase();

  return (
    <div className={styles.item}>
      <div className={styles.name}>{name}</div>
      <div className={styles.meta}>
        {patient.email && <span className={styles.email}>{patient.email}</span>}
        {status && (
          <span className={styles.status} data-status={status}>
            {status}
          </span>
        )}
      </div>
    </div>
  );
}
