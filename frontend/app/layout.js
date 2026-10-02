import "./globals.css";

export const metadata = {
  title: "Phase 5: Student Agent",
  description: "Call the student agent from a Next.js button.",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
