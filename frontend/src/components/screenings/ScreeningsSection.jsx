import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";
import { useQuery } from "@tanstack/react-query";
import { fetchHealthScreenings } from "../../api/patients";
import styles from "./ScreeningsSection.module.css";

function formatMonth(str) {
  if (!str) return "";
  try {
    return new Date(str).toLocaleDateString("en-US", {
      month: "short",
      year: "numeric",
    });
  } catch {
    return str;
  }
}

export default function ScreeningsSection({ patientId }) {
  const { data: screenings = [], isLoading, error } = useQuery({
    queryKey: ["healthScreenings", patientId],
    queryFn: () => fetchHealthScreenings(patientId),
    enabled: !!patientId,
  });

  const chartData = screenings.map((s) => ({
    month: formatMonth(s.screening_month),
    rawMonth: s.screening_month,
    score: s.score,
  }));

  if (isLoading) return <section className={styles.section}><p className={styles.muted}>Loading screenings…</p></section>;
  if (error) return <section className={styles.section}><p className={styles.error}>Failed to load: {error.message}</p></section>;

  return (
    <section className={styles.section}>
      <h2 className={styles.title}>Health screening scores (last 6 months)</h2>
      <p className={styles.hint}>Score: 0 = best, 10 = worst.</p>
      {screenings.length === 0 ? (
        <p className={styles.muted}>No screening data for the last 6 months.</p>
      ) : (
        <>
          <div className={styles.chartWrap}>
            <ResponsiveContainer width="100%" height={260}>
              <LineChart data={chartData} margin={{ top: 8, right: 16, left: 0, bottom: 8 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
                <XAxis dataKey="month" tick={{ fontSize: 12 }} />
                <YAxis domain={[0, 10]} tick={{ fontSize: 12 }} width={24} />
                <Tooltip
                  formatter={(value) => [value, "Score"]}
                  labelFormatter={(_, payload) => payload?.[0]?.payload?.month}
                />
                <Line
                  type="monotone"
                  dataKey="score"
                  stroke="#0ea5e9"
                  strokeWidth={2}
                  dot={{ r: 4 }}
                  name="Score"
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
          <table className={styles.table}>
            <thead>
              <tr>
                <th>Month</th>
                <th>Score</th>
              </tr>
            </thead>
            <tbody>
              {screenings.map((s) => (
                <tr key={s.id}>
                  <td>{formatMonth(s.screening_month)}</td>
                  <td>{s.score}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </>
      )}
    </section>
  );
}
