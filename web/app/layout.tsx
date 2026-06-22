import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Jossie Eyes - Neural Sensory Guide",
  description: "An assistive device for visually impaired individuals that uses Azure AI to describe the world through spatial audio.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}