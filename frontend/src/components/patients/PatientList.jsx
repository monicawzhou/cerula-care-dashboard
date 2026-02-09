import { useState, useMemo } from "react";
import { Link } from "react-router-dom";
import PatientListSearch from "./PatientListSearch";
import PatientListItem from "./PatientListItem";
import styles from "./PatientList.module.css";

const PAGE_SIZE = 15;

export default function PatientList({ patients, isLoading, error, selectedId, onNewPatient }) {
  const [search, setSearch] = useState("");
  const [statusFilter, setStatusFilter] = useState("all");
  const [page, setPage] = useState(1);

  const filtered = useMemo(() => {
    const s = search.trim().toLowerCase();
    let list = patients;
    if (statusFilter !== "all") list = list.filter((p) => (p.status || "").toLowerCase() === statusFilter);
    if (s) {
      list = list.filter(
        (p) =>
          (p.first_name || "").toLowerCase().includes(s) ||
          (p.last_name || "").toLowerCase().includes(s) ||
          (p.email || "").toLowerCase().includes(s)
      );
    }
    return list;
  }, [patients, search, statusFilter]);

  const totalPages = Math.max(1, Math.ceil(filtered.length / PAGE_SIZE));
  const start = (page - 1) * PAGE_SIZE;
  const paged = filtered.slice(start, start + PAGE_SIZE);

  if (error) {
    return (
      <div className={styles.error}>
        Failed to load patients: {error.message}
      </div>
    );
  }

  return (
    <div className={styles.wrapper}>
      {onNewPatient && (
        <button type="button" className={styles.newBtn} onClick={onNewPatient}>
          New patient
        </button>
      )}
      <PatientListSearch
        search={search}
        onSearchChange={setSearch}
        statusFilter={statusFilter}
        onStatusFilterChange={(v) => {
          setStatusFilter(v);
          setPage(1);
        }}
      />
      <div className={styles.list}>
        {isLoading ? (
          <div className={styles.loading}>Loading patients…</div>
        ) : paged.length === 0 ? (
          <div className={styles.empty}>
            {filtered.length === 0 && patients.length > 0
              ? "No patients match your filters."
              : "No patients yet."}
          </div>
        ) : (
          <>
            {paged.map((p) => (
              <Link
                key={p.id}
                to={`/patients/${p.id}`}
                className={selectedId === p.id ? styles.itemActive : undefined}
              >
                <PatientListItem patient={p} />
              </Link>
            ))}
          </>
        )}
      </div>
      {totalPages > 1 && (
        <div className={styles.pagination}>
          <button
            type="button"
            disabled={page <= 1}
            onClick={() => setPage((x) => x - 1)}
            aria-label="Previous page"
          >
            Previous
          </button>
          <span>
            Page {page} of {totalPages}
          </span>
          <button
            type="button"
            disabled={page >= totalPages}
            onClick={() => setPage((x) => x + 1)}
            aria-label="Next page"
          >
            Next
          </button>
        </div>
      )}
    </div>
  );
}
