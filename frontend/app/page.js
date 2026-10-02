"use client";

import { useState } from "react";

const API_URL = "http://127.0.0.1:8000/api/agent/chat";

export default function Home() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [conversationId, setConversationId] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function sendMessage(event) {
    event.preventDefault();
    const question = input.trim();
    if (!question || loading) return;

    setMessages([...messages, { role: "user", content: question }]);
    setInput("");
    setLoading(true);
    setError("");
    try {
      // Solution (Phase 6):
      // 1. POST { question, conversation_id: conversationId } to API_URL as JSON.
      // 2. Check response.ok, then await response.json().
      // 3. Save data.conversation_id with setConversationId for the next turn.
      // 4. Append { role: "assistant", content: data.answer } with setMessages.
      const response = await fetch(API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question, conversation_id: conversationId }),
      });
      if (!response.ok) {
        throw new Error(`Chat request failed (HTTP ${response.status})`);
      }
      const data = await response.json();
      setConversationId(data.conversation_id);
      setMessages((previous) => [...previous, { role: "assistant", content: data.answer }]);
    } catch (error) {
      console.error("Chat request failed:", error);
      setError(error.message);
      setMessages(messages);
      setInput(question);
    } finally {
      setLoading(false);
    }
  }

  function newChat() {
    setMessages([]);
    setInput("");
    setConversationId(null);
    setError("");
  }

  return (
    <main>
      <p className="eyebrow">Phase 6 · Chatbot</p>
      <h1>Chat with the student agent</h1>
      <p className="hint">Ask about the database, then ask a follow-up question.</p>
      <button type="button" className="secondary" onClick={newChat} disabled={loading}>
        New chat
      </button>
      <div className="messages" role="log" aria-label="Conversation" aria-live="polite">
        {messages.length === 0 && (
          <p className="hint">Try: How many records have the name prad?</p>
        )}
        {messages.map((message, index) => (
          <div key={index} className={`message ${message.role}`}>
            <strong>{message.role === "user" ? "You" : "Agent"}</strong>
            <p>{message.content}</p>
          </div>
        ))}
        {loading && <p role="status">Agent is thinking…</p>}
      </div>
      <form onSubmit={sendMessage}>
        <label htmlFor="question">Your message</label>
        <div className="composer">
          <input
            id="question"
            value={input}
            onChange={(event) => setInput(event.target.value)}
            placeholder="Ask about student records…"
            disabled={loading}
            autoComplete="off"
          />
          <button type="submit" disabled={loading || !input.trim()}>
            {loading ? "Sending…" : "Send"}
          </button>
        </div>
      </form>
      {error && <p role="alert">{error}</p>}
      <p className="hint"><a href="/button">Phase 5 button reference</a></p>
    </main>
  );
}
