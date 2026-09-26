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
