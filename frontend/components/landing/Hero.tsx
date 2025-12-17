/**
 * Hero Component
 *
 * Landing page hero section with headline, subheadline, and CTA buttons.
 */

"use client";

import Link from "next/link";
import { motion } from "framer-motion";
import { BookOpen, MessageSquare, ArrowRight } from "lucide-react";
import { cn } from "@/lib/utils";

export function Hero() {
  return (
    <section className="relative min-h-[calc(100vh-64px)] flex items-center justify-center overflow-hidden">
      {/* Background gradient */}
      <div className="absolute inset-0 bg-gradient-to-br from-primary/5 via-background to-secondary/5" />

      {/* Animated background elements */}
      <div className="absolute inset-0 overflow-hidden">
        <motion.div
          className="absolute -top-1/2 -right-1/2 w-full h-full rounded-full bg-gradient-to-br from-primary/10 to-transparent blur-3xl"
          animate={{
            scale: [1, 1.1, 1],
            rotate: [0, 10, 0],
          }}
          transition={{
            duration: 20,
            repeat: Infinity,
            ease: "easeInOut",
          }}
        />
        <motion.div
          className="absolute -bottom-1/2 -left-1/2 w-full h-full rounded-full bg-gradient-to-tr from-secondary/10 to-transparent blur-3xl"
          animate={{
            scale: [1, 1.2, 1],
            rotate: [0, -10, 0],
          }}
          transition={{
            duration: 25,
            repeat: Infinity,
            ease: "easeInOut",
          }}
        />
      </div>

      <div className="relative z-10 max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-16 text-center">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
        >
          {/* Badge */}
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-primary/10 text-primary text-sm font-medium mb-6">
            <span className="w-2 h-2 rounded-full bg-accent animate-pulse" />
            Interactive Textbook
          </div>

          {/* Headline */}
          <h1 className="text-4xl sm:text-5xl lg:text-6xl font-bold text-foreground mb-6 leading-tight">
            Master{" "}
            <span className="text-gradient">Physical AI</span>
            <br />& Humanoid Robotics
          </h1>

          {/* Subheadline */}
          <p className="text-lg sm:text-xl text-foreground-secondary max-w-2xl mx-auto mb-10">
            A comprehensive textbook covering robotics fundamentals, control
            systems, kinematics, ROS2, and simulation. Learn with an AI
            assistant that knows every chapter.
          </p>

          {/* CTA Buttons */}
          <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
            <Link
              href="/book"
              className={cn(
                "inline-flex items-center gap-2 px-6 py-3 rounded-lg",
                "bg-gradient-primary text-white font-medium text-lg",
                "hover:opacity-90 transition-opacity",
                "shadow-lg hover:shadow-xl"
              )}
            >
              <BookOpen className="w-5 h-5" />
              Read the Book
              <ArrowRight className="w-5 h-5" />
            </Link>
            <Link
              href="/chat"
              className={cn(
                "inline-flex items-center gap-2 px-6 py-3 rounded-lg",
                "border-2 border-primary text-primary font-medium text-lg",
                "hover:bg-primary/10 transition-colors"
              )}
            >
              <MessageSquare className="w-5 h-5" />
              Ask AI Assistant
            </Link>
          </div>
        </motion.div>

        {/* Stats */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.3 }}
          className="mt-16 grid grid-cols-2 md:grid-cols-4 gap-8"
        >
          {[
            { value: "15+", label: "Chapters" },
            { value: "100+", label: "Examples" },
            { value: "AI", label: "Powered" },
            { value: "Free", label: "Access" },
          ].map((stat, index) => (
            <div key={index} className="text-center">
              <div className="text-3xl font-bold text-foreground">
                {stat.value}
              </div>
              <div className="text-sm text-foreground-muted">{stat.label}</div>
            </div>
          ))}
        </motion.div>
      </div>
    </section>
  );
}

export default Hero;
