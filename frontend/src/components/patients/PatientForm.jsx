import { useState, useEffect } from "react";
import { useQueryClient } from "@tanstack/react-query";
import { createPatient, updatePatient } from "../../api/patients";
import styles from "./PatientForm.module.css";

const STATUS_OPTIONS = [
  { value: "active", label: "Active" },
  { value: "inactive", label: "Inactive" },
  { value: "discharged", label: "Discharged" },
];

const GENDER_OPTIONS = [
  { value: "", label: "—" },
  { value: "female", label: "Female" },
  { value: "male", label: "Male" },
  { value: "non_binary", label: "Non-binary" },
  { value: "other", label: "Other" },
  { value: "prefer_not_to_say", label: "Prefer not to say" },
];

function toInputDate(str) {
  if (!str) return "";
  try {
    const d = new Date(str);
    return d.toISOString().slice(0, 10);
  } catch {
    return "";
  }
}

export default function PatientForm({ patient, onSuccess, onCancel }) {
  const isEdit = !!patient;
  const queryClient = useQueryClient();
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState(null);
  const [form, setForm] = useState({
    first_name: "",
    last_name: "",
    date_of_birth: "",
    gender: "",
    email: "",
    status: "active",
  });

  useEffect(() => {
    if (patient) {
      setForm({
        first_name: patient.first_name || "",
        last_name: patient.last_name || "",
        date_of_birth: toInputDate(patient.date_of_birth),
        gender: patient.gender || "",
        email: patient.email || "",
        status: (patient.status || "active").toLowerCase(),
      });
    }
  }, [patient]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setSubmitting(true);
    const payload = {
      first_name: form.first_name.trim(),
      last_name: form.last_name.trim(),
      status: form.status,
      email: form.email.trim() || null,
      date_of_birth: form.date_of_birth || null,
      gender: form.gender || null,
    };
    try {
      if (isEdit) {
        await updatePatient(patient.id, payload);
        await queryClient.invalidateQueries({ queryKey: ["patient", patient.id] });
        await queryClient.invalidateQueries({ queryKey: ["patients"] });
      } else {
        const created = await createPatient(payload);
        await queryClient.invalidateQueries({ queryKey: ["patients"] });
        onSuccess(created);
        return;
      }
      onSuccess();
    } catch (err) {
      setError(err.message || "Something went wrong.");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <section className={styles.section}>
      <h2 className={styles.title}>{isEdit ? "Edit patient" : "New patient"}</h2>
      <form onSubmit={handleSubmit} className={styles.form}>
        {error && <div className={styles.error}>{error}</div>}
        <div className={styles.row}>
          <label>
            First name <span className={styles.required}>*</span>
          </label>
          <input
            name="first_name"
            value={form.first_name}
            onChange={handleChange}
            required
            maxLength={100}
          />
        </div>
        <div className={styles.row}>
          <label>
            Last name <span className={styles.required}>*</span>
          </label>
          <input
            name="last_name"
            value={form.last_name}
            onChange={handleChange}
            required
            maxLength={100}
          />
        </div>
        <div className={styles.row}>
          <label>Email</label>
          <input
            name="email"
            type="email"
            value={form.email}
            onChange={handleChange}
          />
        </div>
        <div className={styles.row}>
          <label>Date of birth</label>
          <input
            name="date_of_birth"
            type="date"
            value={form.date_of_birth}
            onChange={handleChange}
          />
        </div>
        <div className={styles.row}>
          <label>Gender</label>
          <select name="gender" value={form.gender} onChange={handleChange}>
            {GENDER_OPTIONS.map((o) => (
              <option key={o.value || "empty"} value={o.value}>
                {o.label}
              </option>
            ))}
          </select>
        </div>
        <div className={styles.row}>
          <label>Status</label>
          <select name="status" value={form.status} onChange={handleChange}>
            {STATUS_OPTIONS.map((o) => (
              <option key={o.value} value={o.value}>
                {o.label}
              </option>
            ))}
          </select>
        </div>
        <div className={styles.actions}>
          <button type="button" onClick={onCancel} className={styles.cancelBtn}>
            Cancel
          </button>
          <button type="submit" disabled={submitting} className={styles.submitBtn}>
            {submitting ? "Saving…" : isEdit ? "Save changes" : "Create patient"}
          </button>
        </div>
      </form>
    </section>
  );
}
