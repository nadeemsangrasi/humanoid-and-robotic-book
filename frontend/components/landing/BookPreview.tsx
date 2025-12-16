/**
 * BookPreview Component
 *
 * Landing page section showcasing the textbook with a preview/mockup.
 */

"use client";

import { useRef } from "react";
import Link from "next/link";
import { motion, useInView } from "framer-motion";
import { BookOpen, ArrowRight, CheckCircle2 } from "lucide-react";
import { cn } from "@/lib/utils";

const bookFeatures = [
  "15+ comprehensive chapters",
  "Interactive code examples",
  "ROS2 and Gazebo tutorials",
  "URDF robot modeling",
  "Control theory fundamentals",
  "Real-world applications",
];

export function BookPreview() {
  const ref = useRef(null);
  const isInView = useInView(ref, { once: true, margin: "-100px" });

  return (
    <section ref={ref} className="py-24 bg-background-secondary">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid lg:grid-cols-2 gap-12 items-center">
          {/* Content */}
          <motion.div
            initial={{ opacity: 0, x: -30 }}
            animate={isInView ? { opacity: 1, x: 0 } : { opacity: 0, x: -30 }}
            transition={{ duration: 0.5 }}
          >
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-primary/10 text-primary text-sm font-medium mb-4">
              <BookOpen className="w-4 h-4" />
              The Textbook
            </div>

            <h2 className="text-3xl sm:text-4xl font-bold text-foreground mb-4">
              Your Complete Guide to Humanoid Robotics
            </h2>

            <p className="text-lg text-foreground-secondary mb-8">
              From mathematical foundations to practical implementations, this
              textbook covers everything you need to understand and build
              humanoid robots.
            </p>

            {/* Features list */}
            <ul className="space-y-3 mb-8">
              {bookFeatures.map((feature, index) => (
                <motion.li
                  key={feature}
                  initial={{ opacity: 0, x: -20 }}
                  animate={
                    isInView ? { opacity: 1, x: 0 } : { opacity: 0, x: -20 }
                  }
                  transition={{ duration: 0.3, delay: 0.2 + index * 0.05 }}
                  className="flex items-center gap-3"
                >
                  <CheckCircle2 className="w-5 h-5 text-accent flex-shrink-0" />
                  <span className="text-foreground-secondary">{feature}</span>
                </motion.li>
              ))}
            </ul>

            <Link
              href="/book"
              className={cn(
                "inline-flex items-center gap-2 px-6 py-3 rounded-lg",
                "bg-gradient-primary text-white font-medium",
                "hover:opacity-90 transition-opacity",
                "shadow-md hover:shadow-lg"
              )}
            >
              Start Reading
              <ArrowRight className="w-5 h-5" />
            </Link>
          </motion.div>

          {/* Book mockup */}
          <motion.div
            initial={{ opacity: 0, x: 30 }}
            animate={isInView ? { opacity: 1, x: 0 } : { opacity: 0, x: 30 }}
            transition={{ duration: 0.5, delay: 0.2 }}
            className="relative"
          >
            <div className="relative aspect-[4/3] rounded-2xl overflow-hidden shadow-2xl border border-border bg-background">
              {/* Fake browser chrome */}
              <div className="absolute top-0 left-0 right-0 h-8 bg-background-tertiary border-b border-border flex items-center px-3 gap-2">
                <div className="w-3 h-3 rounded-full bg-red-400" />
                <div className="w-3 h-3 rounded-full bg-yellow-400" />
                <div className="w-3 h-3 rounded-full bg-green-400" />
                <div className="flex-1 mx-4">
                  <div className="h-4 bg-background rounded text-xs flex items-center justify-center text-foreground-muted">
                    physical-ai-book
                  </div>
                </div>
              </div>

              {/* Content preview */}
              <div className="absolute top-8 inset-x-0 bottom-0 p-6 overflow-hidden">
                <div className="space-y-4">
                  <div className="h-8 bg-gradient-primary rounded w-3/4" />
                  <div className="space-y-2">
                    <div className="h-3 bg-foreground-muted/20 rounded w-full" />
                    <div className="h-3 bg-foreground-muted/20 rounded w-5/6" />
                    <div className="h-3 bg-foreground-muted/20 rounded w-4/6" />
                  </div>
                  <div className="flex gap-4 pt-4">
                    <div className="flex-1 p-4 rounded-lg bg-background-secondary border border-border">
                      <div className="h-2 bg-primary/30 rounded w-1/2 mb-2" />
                      <div className="space-y-1">
                        <div className="h-2 bg-foreground-muted/15 rounded" />
                        <div className="h-2 bg-foreground-muted/15 rounded w-4/5" />
                      </div>
                    </div>
                    <div className="flex-1 p-4 rounded-lg bg-background-secondary border border-border">
                      <div className="h-2 bg-secondary/30 rounded w-1/2 mb-2" />
                      <div className="space-y-1">
                        <div className="h-2 bg-foreground-muted/15 rounded" />
                        <div className="h-2 bg-foreground-muted/15 rounded w-3/5" />
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              {/* Decorative gradient overlay */}
              <div className="absolute inset-0 bg-gradient-to-t from-background/50 to-transparent pointer-events-none" />
            </div>

            {/* Floating badge */}
            <motion.div
              initial={{ scale: 0 }}
              animate={isInView ? { scale: 1 } : { scale: 0 }}
              transition={{ duration: 0.3, delay: 0.5, type: "spring" }}
              className="absolute -bottom-4 -right-4 px-4 py-2 rounded-full bg-accent text-white font-medium shadow-lg"
            >
              Free Access
            </motion.div>
          </motion.div>
        </div>
      </div>
    </section>
  );
}

export default BookPreview;
