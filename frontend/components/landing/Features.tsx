/**
 * Features Component
 *
 * Landing page features section with 4 feature cards.
 */

"use client";

import { motion } from "framer-motion";
import { useInView } from "framer-motion";
import { useRef } from "react";
import {
  GraduationCap,
  Bot,
  Code2,
  Rocket,
  type LucideIcon,
} from "lucide-react";
import { cn } from "@/lib/utils";

interface Feature {
  icon: LucideIcon;
  title: string;
  description: string;
  color: string;
}

const features: Feature[] = [
  {
    icon: GraduationCap,
    title: "Comprehensive Curriculum",
    description:
      "From fundamentals to advanced topics: kinematics, dynamics, control theory, sensors, actuators, and more.",
    color: "from-blue-500 to-cyan-500",
  },
  {
    icon: Bot,
    title: "AI Learning Assistant",
    description:
      "Ask questions about any chapter. Get instant, contextual answers powered by RAG technology.",
    color: "from-purple-500 to-pink-500",
  },
  {
    icon: Code2,
    title: "Runnable Examples",
    description:
      "Every concept comes with code examples in Python, ROS2, and simulation environments.",
    color: "from-green-500 to-emerald-500",
  },
  {
    icon: Rocket,
    title: "Capstone Projects",
    description:
      "Build real robotics projects that integrate everything you learn throughout the book.",
    color: "from-orange-500 to-amber-500",
  },
];

function FeatureCard({ feature, index }: { feature: Feature; index: number }) {
  const ref = useRef(null);
  const isInView = useInView(ref, { once: true, margin: "-100px" });

  return (
    <motion.div
      ref={ref}
      initial={{ opacity: 0, y: 30 }}
      animate={isInView ? { opacity: 1, y: 0 } : { opacity: 0, y: 30 }}
      transition={{ duration: 0.5, delay: index * 0.1 }}
      className={cn(
        "group relative p-6 rounded-2xl",
        "bg-background-secondary border border-border",
        "hover:border-primary/30 hover:shadow-lg",
        "transition-all duration-300"
      )}
    >
      {/* Icon */}
      <div
        className={cn(
          "w-12 h-12 rounded-xl flex items-center justify-center mb-4",
          "bg-gradient-to-br",
          feature.color
        )}
      >
        <feature.icon className="w-6 h-6 text-white" />
      </div>

      {/* Content */}
      <h3 className="text-xl font-semibold text-foreground mb-2 group-hover:text-primary transition-colors">
        {feature.title}
      </h3>
      <p className="text-foreground-secondary leading-relaxed">
        {feature.description}
      </p>

      {/* Hover gradient overlay */}
      <div
        className={cn(
          "absolute inset-0 rounded-2xl opacity-0 group-hover:opacity-5",
          "bg-gradient-to-br transition-opacity duration-300",
          feature.color
        )}
      />
    </motion.div>
  );
}

export function Features() {
  const ref = useRef(null);
  const isInView = useInView(ref, { once: true, margin: "-100px" });

  return (
    <section ref={ref} className="py-24 bg-background">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Section header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={isInView ? { opacity: 1, y: 0 } : { opacity: 0, y: 20 }}
          transition={{ duration: 0.5 }}
          className="text-center mb-16"
        >
          <h2 className="text-3xl sm:text-4xl font-bold text-foreground mb-4">
            Everything You Need to Learn Robotics
          </h2>
          <p className="text-lg text-foreground-secondary max-w-2xl mx-auto">
            A complete learning experience designed to take you from beginner to
            expert in physical AI and humanoid robotics.
          </p>
        </motion.div>

        {/* Feature cards grid */}
        <div className="grid md:grid-cols-2 gap-6">
          {features.map((feature, index) => (
            <FeatureCard key={feature.title} feature={feature} index={index} />
          ))}
        </div>
      </div>
    </section>
  );
}

export default Features;
