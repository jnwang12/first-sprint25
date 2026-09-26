"use client";

import { useEffect, useRef, useState, type FormEvent } from "react";
import { fetchStudents, sendChat, type ChatMessage, type Student } from "@/lib/api";

type DisplayMessage = ChatMessage & { records?: number; toolCalls?: number };

export default function Home() {
  const [messages, setMessages] = useState<DisplayMessage[]>([]);
  const [draft, setDraft] = useState("");
  const [pending, setPending] = useState("");
  const [error, setError] = useState("");
  const [students, setStudents] = useState<Student[]>([]);
  const [dataStatus, setDataStatus] = useState("Loading records…");
  const activeRequest = useRef<AbortController | null>(null);
  const bottom = useRef<HTMLDivElement>(null);
  const input = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    const controller = new AbortController();
    fetchStudents(controller.signal)
      .then((rows) => {
        if (controller.signal.aborted) return;
        setStudents(rows);
        setDataStatus(rows.length ? "" : "No visible student records.");
      })
      .catch(() => {
        if (!controller.signal.aborted) setDataStatus("Could not load the preview. Chat retrieves fresh data independently.");
      });
    return () => { controller.abort(); activeRequest.current?.abort(); };
  }, []);

  useEffect(() => { bottom.current?.scrollIntoView({ block: "nearest" }); }, [messages, pending, error]);

  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const question = draft.trim();
    if (!question || activeRequest.current) return;
    const controller = new AbortController();
    activeRequest.current = controller;
    setPending(question);
    setDraft("");
    setError("");
    try {
      // Send completed exchanges only. Each tab owns its own transcript.
      const history = messages.slice(-20).map(({ role, content }) => ({ role, content }));
      const response = await sendChat(question, history, controller.signal);
      if (controller.signal.aborted) return;
      console.log("[Phase 6] Chat API response:", response);
      setMessages((current) => [...current,
        { role: "user", content: question },
        { role: "assistant", content: response.answer,
          records: response.records_analyzed, toolCalls: response.tool_calls },
      ]);
    } catch (cause) {
      if (controller.signal.aborted) return;
      setError(cause instanceof Error ? cause.message : "Unable to get a reply.");
      setDraft(question); // Keep the failed question ready to retry; don't duplicate history.
    } finally {
      if (!controller.signal.aborted) {
        activeRequest.current = null;
        setPending("");
        input.current?.focus();
      }
    }
  }

  function newChat() {
    if (activeRequest.current) return;
    setMessages([]);
    setDraft("");
    setError("");
    input.current?.focus();
  }

  return (
    <main>
      <header className="chat-header">
        <div><p className="eyebrow">FIRST SPRINT / PHASE 6</p><h1>Chat with your data.</h1></div>
        <button className="secondary" onClick={newChat} disabled={!!pending}>New chat</button>
      </header>
      <p>Ask about student names, emails, or majors, then follow up naturally.</p>
      <section className="chat-shell" aria-label="Student database chat">
        <div className="transcript" role="log" aria-label="Conversation" aria-live="polite" aria-relevant="additions text">
          {messages.length === 0 && !pending && <div className="chat-welcome">
            <h2>What would you like to know?</h2>
            <p>Start with a question, then ask “What are their majors?”</p>
            <button className="suggestion" onClick={() => { setDraft("How many records have a name of Prad?"); input.current?.focus(); }}>
              How many students are named Prad?
            </button>
          </div>}
          {messages.map((message, index) => <article className={`message ${message.role}`} key={index}>
            <strong>{message.role === "user" ? "You" : "Database assistant"}</strong>
            <p>{message.content}</p>
            {message.role === "assistant" && <small>{message.toolCalls} tool calls · {message.records} records retrieved</small>}
          </article>)}
          {pending && <><article className="message user"><strong>You</strong><p>{pending}</p></article>
            <p className="thinking">Looking up student data and writing a reply…</p></>}
          <div ref={bottom} />
        </div>
        {error && <p className="error" role="alert">{error} Your question is restored below; send it again to retry.</p>}
        <form className="composer" onSubmit={submit}>
          <label htmlFor="question">Your message</label>
          <textarea id="question" ref={input} value={draft} maxLength={500} rows={3}
            placeholder="Ask a question about the students…" disabled={!!pending}
            onChange={(event) => setDraft(event.target.value)}
            onKeyDown={(event) => {
              if (event.key === "Enter" && !event.shiftKey && !event.nativeEvent.isComposing) {
                event.preventDefault(); event.currentTarget.form?.requestSubmit();
              }
            }} />
          <div className="composer-actions"><small>{draft.length}/500 · Shift+Enter for a new line</small>
            <button type="submit" disabled={!!pending || !draft.trim()}>{pending ? "Waiting…" : "Send message"}</button></div>
        </form>
      </section>
      <p className="agent-hint">The last 10 exchanges provide context. New chat or reloading clears the conversation.
        Each message retrieves fresh data and sends it to Gemini.</p>
      <details className="data-preview"><summary>View the student records</summary>
        {dataStatus && <p>{dataStatus}</p>}
        <ul className="records">{students.map((student, index) => <li key={`${student.email}-${index}`}>
          <code>({[student.name, student.email, student.major].map((value) => JSON.stringify(value)).join(", ")})</code>
        </li>)}</ul>
      </details>
    </main>
  );
}
