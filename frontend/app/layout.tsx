import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Mega CRM AI",
  description: "نظام CRM متكامل مع ذكاء اصطناعي",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="ar" dir="rtl">
      <body>{children}</body>
    </html>
  );
}
