import { useEffect, useState } from "react";
import axios from "../api/axios"; // Axios instance

export default function PatientDropdownWithSearch({ onSelect }) {
  const [patients, setPatients] = useState([]);
  const [search, setSearch] = useState("");

  useEffect(() => {
    const fetchPatients = async () => {
      try {
        const res = await axios.get("/api/v1/patients");
        setPatients(res.data);
      } catch (err) {
        console.error("Failed to load patients", err);
      }
    };
    fetchPatients();
  }, []);

  const filtered = patients.filter((p) =>
    p.name.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="my-4">
      <input
        type="text"
        placeholder="Search Patient"
        className="border p-2 w-full rounded mb-2"
        value={search}
        onChange={(e) => setSearch(e.target.value)}
      />
      <select
        onChange={(e) => onSelect(e.target.value)}
        className="border p-2 w-full rounded"
      >
        <option value="">Select a patient</option>
        {filtered.map((patient) => (
          <option key={patient.id} value={patient.id}>
            {patient.name}
          </option>
        ))}
      </select>
    </div>
  );
}
