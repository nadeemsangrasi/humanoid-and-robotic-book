/**
 * Landing Page
 *
 * Modern landing page with hero, features, previews, and footer.
 */

import { Hero, Features, BookPreview, ChatbotDemo } from "@/components/landing";
import { Footer } from "@/components/layout/Footer";

export default function HomePage() {
  return (
    <>
      <Hero />
      <Features />
      <BookPreview />
      <ChatbotDemo />
      <Footer />
    </>
  );
}
