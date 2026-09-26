export const API_BASE_URL = (
  process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"
).replace(/\/$/, "");

export type Student = { name: string; email: string; major: string };

export async function fetchStudents(signal?: AbortSignal): Promise<Student[]> {
  const response = await fetch(`${API_BASE_URL}/api/students`, {
    cache: "no-store",
    signal,
  });
  if (!response.ok) {
    throw new Error("Unable to load students. Check the Python backend and Supabase settings.");
  }
  return response.json();
}

// TODO (Phase 5): Add a request to your future agent endpoint.
// TODO (Phase 6): Extend that request for conversation history.

export type PradAnswer = {
  question: string;
  answer: string;
  records_analyzed: number;
};

export async function askAboutPrad(): Promise<PradAnswer> {
  let response: Response;
  try {
    response = await fetch(`${API_BASE_URL}/api/agent/prad`, {
      method: "POST",
      cache: "no-store",
    });
  } catch {
    throw new Error("Cannot reach the API. Start the Python backend on port 8000.");
  }
  if (!response.ok) {
    const body = await response.json().catch(() => null);
    throw new Error(typeof body?.detail === "string" ? body.detail : "Unable to get an agent answer.");
  }
  return response.json();
}
