import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "First Sprint · Workshop Starter",
  description: "A hands-on Next.js, TypeScript, and Python workshop.",
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return <html lang="en"><body>{children}</body></html>;
}
