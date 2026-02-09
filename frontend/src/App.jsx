import { Routes, Route, Navigate } from "react-router-dom";
import Layout from "./layout/Layout";
import PatientsPage from "./pages/PatientsPage";

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Layout />}>
        <Route index element={<Navigate to="/patients" replace />} />
        <Route path="patients" element={<PatientsPage />} />
        <Route path="patients/:patientId" element={<PatientsPage />} />
      </Route>
      <Route path="*" element={<Navigate to="/patients" replace />} />
    </Routes>
  );
}
