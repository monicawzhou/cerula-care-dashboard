import styles from "./PatientListSearch.module.css";

export default function PatientListSearch({ search, onSearchChange, statusFilter, onStatusFilterChange }) {
  return (
    <div className={styles.wrapper}>
      <input
        type="search"
        placeholder="Search by name or email…"
        value={search}
        onChange={(e) => onSearchChange(e.target.value)}
        className={styles.search}
        aria-label="Search patients"
      />
      <select
        value={statusFilter}
        onChange={(e) => onStatusFilterChange(e.target.value)}
        className={styles.select}
        aria-label="Filter by status"
      >
        <option value="all">All statuses</option>
        <option value="active">Active</option>
        <option value="inactive">Inactive</option>
        <option value="discharged">Discharged</option>
      </select>
    </div>
  );
}
