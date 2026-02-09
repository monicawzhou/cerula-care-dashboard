import { NavLink } from "react-router-dom";
import styles from "./Sidebar.module.css";

export default function Sidebar() {
  return (
    <div className={styles.sidebar}>
      <h1 className={styles.logo}>Cerula</h1>
      <nav>
        <NavLink to="/patients" className={({ isActive }) => (isActive ? `${styles.navLink} ${styles.active}` : styles.navLink)}>
          Patients
        </NavLink>
      </nav>
    </div>
  );
}
