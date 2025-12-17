import Script from "next/script";
import type { Metadata } from "next";
import "./globals.css";
import { AuthProvider } from "@/components/auth/AuthProvider";
import { Navbar } from "@/components/layout/Navbar";
import { InstantChatProvider } from "@/components/instant-chat";
import { NAVBAR_HEIGHT } from "@/lib/constants";

export const metadata: Metadata = {
  title: "Physical AI & Humanoid Robotics",
  description:
    "Interactive textbook chatbot for Physical AI and Humanoid Robotics",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" suppressHydrationWarning>
      <head>
        <Script
          src="https://cdn.platform.openai.com/deployments/chatkit/chatkit.js"
          strategy="beforeInteractive"
        />
      </head>
      <body className="antialiased">
        <AuthProvider>
          <Navbar />
          <main style={{ paddingTop: NAVBAR_HEIGHT }}>{children}</main>
          <InstantChatProvider />
        </AuthProvider>
      </body>
    </html>
  );
}
