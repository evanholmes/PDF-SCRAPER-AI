import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "BID-AI | The Bid Master",
  description:
    "AI-Powered RFQ/RFP Tender-Bid Expert for ALL-PRO SIGNS & WESTCOAST CNC",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="antialiased">{children}</body>
    </html>
  );
}
