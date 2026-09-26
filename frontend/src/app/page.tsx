// TODO (Phase 5): Add a client component with a button that calls your backend.
// TODO (Phase 5): Log the response to the browser console.
// TODO (Phase 6): Replace the button experiment with a conversational chat UI.

export default function Home() {
  return (
    <main>
      <p className="eyebrow">FIRST SPRINT / 26</p>
      <h1>Your workshop starts here.</h1>
      <p>
        This is the Next.js starter page. You will build the interaction in
        Phase 5 and the chatbot in Phase 6.
      </p>
      <p>
        Begin with <code>backend/exercise.py</code> and follow the six phases in{" "}
        <code>docs/workshop.md</code>.
      </p>
      <p className="note">
        No database queries, agent calls, or frontend requests are implemented.
      </p>
    </main>
  );
}
