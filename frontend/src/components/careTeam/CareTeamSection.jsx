import { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import {
  fetchPatientCareTeam,
  fetchAllCareTeamMembers,
  assignCareTeamMember,
  unassignCareTeamMember,
} from "../../api/careTeam";
import styles from "./CareTeamSection.module.css";

export default function CareTeamSection({ patientId }) {
  const queryClient = useQueryClient();
  const [selectedMemberId, setSelectedMemberId] = useState("");

  const { data: assigned = [], isLoading } = useQuery({
    queryKey: ["careTeam", patientId],
    queryFn: () => fetchPatientCareTeam(patientId),
    enabled: !!patientId,
  });

  const { data: allMembers = [] } = useQuery({
    queryKey: ["careTeamMembers"],
    queryFn: fetchAllCareTeamMembers,
    enabled: !!patientId,
  });

  const assignMutation = useMutation({
    mutationFn: () => assignCareTeamMember(patientId, selectedMemberId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["careTeam", patientId] });
      setSelectedMemberId("");
    },
  });

  const unassignMutation = useMutation({
    mutationFn: (memberId) => unassignCareTeamMember(patientId, memberId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["careTeam", patientId] });
    },
  });

  const assignedIds = new Set((assigned || []).map((m) => m.id));
  const available = allMembers.filter((m) => !assignedIds.has(m.id));

  return (
    <section className={styles.section}>
      <h2 className={styles.title}>Care team</h2>
      {isLoading ? (
        <p className={styles.muted}>Loading…</p>
      ) : (
        <>
          <ul className={styles.list}>
            {assigned.length === 0 ? (
              <li className={styles.muted}>No care team members assigned.</li>
            ) : (
              assigned.map((m) => (
                <li key={m.id} className={styles.item}>
                  <span>
                    {m.first_name} {m.last_name}
                    <span className={styles.role}> ({m.role?.replace("_", " ")})</span>
                    {m.email && (
                      <span className={styles.email}> — {m.email}</span>
                    )}
                  </span>
                  <button
                    type="button"
                    className={styles.unassignBtn}
                    onClick={() => unassignMutation.mutate(m.id)}
                    disabled={unassignMutation.isPending}
                    aria-label={`Unassign ${m.first_name} ${m.last_name}`}
                  >
                    Unassign
                  </button>
                </li>
              ))
            )}
          </ul>
          {available.length > 0 && (
            <div className={styles.addRow}>
              <select
                value={selectedMemberId}
                onChange={(e) => setSelectedMemberId(e.target.value)}
                className={styles.select}
                aria-label="Choose care team member to assign"
              >
                <option value="">Add a care team member…</option>
                {available.map((m) => (
                  <option key={m.id} value={m.id}>
                    {m.first_name} {m.last_name} ({m.role?.replace("_", " ")})
                  </option>
                ))}
              </select>
              <button
                type="button"
                className={styles.assignBtn}
                disabled={!selectedMemberId || assignMutation.isPending}
                onClick={() => assignMutation.mutate()}
              >
                {assignMutation.isPending ? "Assigning…" : "Assign"}
              </button>
            </div>
          )}
          {assignMutation.isError && (
            <p className={styles.error}>{assignMutation.error?.message}</p>
          )}
          {unassignMutation.isError && (
            <p className={styles.error}>{unassignMutation.error?.message}</p>
          )}
        </>
      )}
    </section>
  );
}
