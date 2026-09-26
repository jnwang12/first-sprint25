"use client";

import { useEffect, useState } from "react";
import { fetchStudents, type Student } from "@/lib/api";

export default function Home() {
  const [students, setStudents] = useState<Student[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [version, setVersion] = useState(0);

  useEffect(() => {
    const controller = new AbortController();
    fetchStudents(controller.signal)
      .then((records) => {
        if (!controller.signal.aborted) setStudents(records);
      })
      .catch((cause: unknown) => {
        if (controller.signal.aborted) return;
        setError(cause instanceof TypeError
          ? "Cannot reach the API. Start the Python backend on port 8000."
          : cause instanceof Error ? cause.message : "Unable to load students.");
      })
      .finally(() => {
        if (!controller.signal.aborted) setLoading(false);
      });
    return () => controller.abort();
  }, [version]);

  function refresh() {
    setLoading(true);
    setError("");
    setVersion((current) => current + 1);
  }

  return (
    <main>
      <p className="eyebrow">FIRST SPRINT / PHASE 1</p>
      <h1>Student records</h1>
      <p>Live Supabase records, retrieved by Python and displayed as tuples.</p>
      <div className="toolbar">
        <code>(name, email, major)</code>
        <button type="button" onClick={refresh} disabled={loading}>
          {loading ? "Loading…" : "Refresh records"}
        </button>
      </div>
      {loading && <p role="status">Loading student records…</p>}
      {error && <p className="error" role="alert">{error}</p>}
      {!loading && !error && (
        <section aria-label="Student records">
          <p role="status">{students.length} records</p>
          {students.length === 0 ? <p>No student records are visible.</p> : (
            <ul className="records">
              {students.map((student, index) => (
                <li key={`${student.email}-${index}`}>
                  <code>({[student.name, student.email, student.major]
                    .map((value) => JSON.stringify(value)).join(", ")})</code>
                </li>
              ))}
            </ul>
          )}
        </section>
      )}
      <p className="note">
        Run <code>python -m backend.exercise</code> to see the same records in your terminal.
      </p>
    </main>
  );
}
