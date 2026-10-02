import "./globals.css";

export const metadata = {
  title: "Phase 6: Student Agent Chat",
  description: "Have a conversation with the student database agent.",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
