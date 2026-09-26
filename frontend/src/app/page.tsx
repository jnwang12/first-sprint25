"use client";

import { useEffect, useState } from "react";
import { askAboutPrad, fetchStudents, type PradAnswer, type Student } from "@/lib/api";

export default function Home() {
  const [students, setStudents] = useState<Student[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [version, setVersion] = useState(0);

  const [answer, setAnswer] = useState<PradAnswer | null>(null);
  const [asking, setAsking] = useState(false);
  const [agentError, setAgentError] = useState("");

  async function askAgent() {
    setAsking(true);
    setAgentError("");
    setAnswer(null);
    try {
      setAnswer(await askAboutPrad());
    } catch (cause) {
      setAgentError(cause instanceof Error ? cause.message : "Unable to get an answer.");
    } finally {
      setAsking(false);
    }
  }

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
      <p className="eyebrow">FIRST SPRINT / PHASE 3</p>
      <h1>Student records</h1>
      <p>Live Supabase records, retrieved by Python and displayed as tuples.</p>
      <section className="agent-card" aria-labelledby="agent-heading">
        <p className="eyebrow">PYDANTIC AI + TOOL CALLS</p>
        <h2 id="agent-heading">How many records have a name of Prad?</h2>
        <p>
          Ask the agent to count matching names from a fresh database snapshot.
          The agent calls a database tool to retrieve names; matching ignores capitalization.
        </p>
        <button type="button" onClick={askAgent} disabled={asking}>
          {asking ? "Asking the agent…" : "Ask about Prad"}
        </button>
        {asking && <p role="status">Reading the database and waiting for the agent…</p>}
        {agentError && <p className="error" role="alert">{agentError}</p>}
        {answer && <div className="agent-answer" role="status">
          <p>{answer.answer}</p>
          <small>Database tool calls: {answer.tool_calls} · {answer.records_analyzed} records retrieved.</small>
        </div>}
        <p className="agent-hint">Requires GEMINI_API_KEY in backend/.env. Each click makes a model request.</p>
      </section>
      <h2>Phase 1 · Student tuples</h2>
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
