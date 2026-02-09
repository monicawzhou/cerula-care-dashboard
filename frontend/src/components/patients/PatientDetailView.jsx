import styles from "./PatientDetailView.module.css";

function formatDate(str) {
  if (!str) return "—";
  try {
    return new Date(str).toLocaleDateString("en-US", {
      year: "numeric",
      month: "short",
      day: "numeric",
    });
  } catch {
    return str;
  }
}

export default function PatientDetailView({ patient, onEdit }) {
  const name = [patient.first_name, patient.last_name].filter(Boolean).join(" ") || "—";
  const status = (patient.status || "").toLowerCase();

  return (
    <section className={styles.section}>
      <div className={styles.header}>
        <h2 className={styles.title}>Patient details</h2>
        <button type="button" className={styles.editBtn} onClick={onEdit}>
          Edit
        </button>
      </div>
      <dl className={styles.dl}>
        <dt>Name</dt>
        <dd>{name}</dd>
        <dt>Email</dt>
        <dd>{patient.email || "—"}</dd>
        <dt>Date of birth</dt>
        <dd>{formatDate(patient.date_of_birth)}</dd>
        <dt>Gender</dt>
        <dd>{patient.gender ? String(patient.gender).replace("_", " ") : "—"}</dd>
        <dt>Status</dt>
        <dd>
          <span className={styles.statusBadge} data-status={status}>
            {status || "—"}
          </span>
        </dd>
      </dl>
    </section>
  );
}
