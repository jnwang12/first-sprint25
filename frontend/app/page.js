"use client";

import { useState } from "react";

const API_URL = "http://127.0.0.1:8000/api/agent/ask";
const QUESTION = "How many records have the name prad?";

export default function Home() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function askAgent() {
    setLoading(true);
    setError("");
    try {
      // Solution (Phase 5):
      // 1. Use fetch(API_URL, ...) to POST JSON with { question: QUESTION }.
      //    Set the Content-Type header to application/json.
      // 2. Check response.ok; throw an Error if the request failed.
      // 3. Await response.json() and print it with console.log.
      const response = await fetch(API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: QUESTION }),
      });
      if (!response.ok) {
        throw new Error(`Agent request failed (HTTP ${response.status})`);
      }
      const data = await response.json();
      console.log("Agent response:", data);
    } catch (error) {
      console.error("Agent request failed:", error);
      setError(error.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <main>
      <p className="eyebrow">Phase 5 · FE → BE Integration</p>
      <h1>Ask the student agent</h1>
      <p>{QUESTION}</p>
      <button type="button" onClick={askAgent} disabled={loading}>
        {loading ? "Asking…" : "Ask agent"}
      </button>
      <p className="hint">Open your browser console to see the response.</p>
      {error && <p role="alert">{error}</p>}
    </main>
  );
}
