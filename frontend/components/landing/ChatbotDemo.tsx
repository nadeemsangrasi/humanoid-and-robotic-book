/**
 * ChatbotDemo Component
 *
 * Landing page section showcasing the AI chatbot assistant with a demo animation.
 */

"use client";

import { useRef, useState, useEffect } from "react";
import Link from "next/link";
import { motion, useInView, AnimatePresence } from "framer-motion";
import { MessageSquare, ArrowRight, Sparkles, Bot, User } from "lucide-react";
import { cn } from "@/lib/utils";

const demoMessages = [
  {
    role: "user" as const,
    content: "What is inverse kinematics?",
  },
  {
    role: "assistant" as const,
    content:
      "Inverse kinematics (IK) is the mathematical process of calculating joint configurations needed to position an end effector at a desired location. Unlike forward kinematics, IK works backward from the target position to find joint angles.",
  },
  {
    role: "user" as const,
    content: "Can you show me a Python example?",
  },
  {
    role: "assistant" as const,
    content:
      "Here's a simple 2-link arm IK example using the geometric approach. The code calculates elbow and shoulder angles given a target (x, y) position using the law of cosines.",
  },
];

function TypingIndicator() {
  return (
    <div className="flex items-center gap-1">
      <span className="w-2 h-2 rounded-full bg-foreground-muted animate-typing-dot" />
      <span className="w-2 h-2 rounded-full bg-foreground-muted animate-typing-dot" />
      <span className="w-2 h-2 rounded-full bg-foreground-muted animate-typing-dot" />
    </div>
  );
}

export function ChatbotDemo() {
  const ref = useRef(null);
  const isInView = useInView(ref, { once: true, margin: "-100px" });
  const [visibleMessages, setVisibleMessages] = useState(0);
  const [isTyping, setIsTyping] = useState(false);

  // Animate messages appearing one by one
  useEffect(() => {
    if (!isInView) return;

    if (visibleMessages < demoMessages.length) {
      setIsTyping(true);
      const typingDelay = demoMessages[visibleMessages].role === "assistant" ? 1500 : 800;

      const timer = setTimeout(() => {
        setIsTyping(false);
        setVisibleMessages((prev) => prev + 1);
      }, typingDelay);

      return () => clearTimeout(timer);
    }
  }, [isInView, visibleMessages]);

  return (
    <section ref={ref} className="py-24 bg-background">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid lg:grid-cols-2 gap-12 items-center">
          {/* Chat demo mockup */}
          <motion.div
            initial={{ opacity: 0, x: -30 }}
            animate={isInView ? { opacity: 1, x: 0 } : { opacity: 0, x: -30 }}
            transition={{ duration: 0.5 }}
            className="order-2 lg:order-1"
          >
            <div className="relative rounded-2xl overflow-hidden shadow-2xl border border-border bg-background-secondary">
              {/* Chat header */}
              <div className="h-14 bg-gradient-primary flex items-center px-4 gap-3">
                <div className="w-8 h-8 rounded-full bg-white/20 flex items-center justify-center">
                  <Bot className="w-5 h-5 text-white" />
                </div>
                <div>
                  <div className="text-white font-medium text-sm">
                    AI Assistant
                  </div>
                  <div className="text-white/70 text-xs">
                    Powered by RAG
                  </div>
                </div>
                <div className="ml-auto flex items-center gap-1">
                  <span className="w-2 h-2 rounded-full bg-accent animate-pulse" />
                  <span className="text-white/70 text-xs">Online</span>
                </div>
              </div>

              {/* Messages area */}
              <div className="h-80 overflow-y-auto p-4 space-y-4">
                <AnimatePresence>
                  {demoMessages.slice(0, visibleMessages).map((msg, index) => (
                    <motion.div
                      key={index}
                      initial={{ opacity: 0, y: 10 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ duration: 0.3 }}
                      className={cn(
                        "flex",
                        msg.role === "user" ? "justify-end" : "justify-start"
                      )}
                    >
                      <div
                        className={cn(
                          "max-w-[85%] rounded-2xl px-4 py-2.5",
                          msg.role === "user"
                            ? "message-user"
                            : "message-bot"
                        )}
                      >
                        <div className="flex items-start gap-2">
                          {msg.role === "assistant" && (
                            <Sparkles className="w-4 h-4 text-primary mt-0.5 flex-shrink-0" />
                          )}
                          <p className="text-sm leading-relaxed">
                            {msg.content}
                          </p>
                        </div>
                      </div>
                    </motion.div>
                  ))}
                </AnimatePresence>

                {/* Typing indicator */}
                {isTyping && visibleMessages < demoMessages.length && (
                  <motion.div
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    className={cn(
                      "flex",
                      demoMessages[visibleMessages].role === "user"
                        ? "justify-end"
                        : "justify-start"
                    )}
                  >
                    <div className="message-bot px-4 py-3">
                      <TypingIndicator />
                    </div>
                  </motion.div>
                )}
              </div>

              {/* Input area mockup */}
              <div className="h-16 border-t border-border bg-background px-4 flex items-center gap-3">
                <div className="flex-1 h-10 rounded-full bg-background-secondary border border-border px-4 flex items-center">
                  <span className="text-sm text-foreground-muted">
                    Ask about robotics...
                  </span>
                </div>
                <button className="w-10 h-10 rounded-full bg-gradient-primary flex items-center justify-center">
                  <MessageSquare className="w-5 h-5 text-white" />
                </button>
              </div>
            </div>
          </motion.div>

          {/* Content */}
          <motion.div
            initial={{ opacity: 0, x: 30 }}
            animate={isInView ? { opacity: 1, x: 0 } : { opacity: 0, x: 30 }}
            transition={{ duration: 0.5, delay: 0.2 }}
            className="order-1 lg:order-2"
          >
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-secondary/10 text-secondary text-sm font-medium mb-4">
              <Bot className="w-4 h-4" />
              AI Assistant
            </div>

            <h2 className="text-3xl sm:text-4xl font-bold text-foreground mb-4">
              Ask Anything About the Book
            </h2>

            <p className="text-lg text-foreground-secondary mb-6">
              Our AI assistant uses retrieval-augmented generation (RAG) to
              provide accurate answers directly from the textbook content.
            </p>

            <ul className="space-y-3 mb-8">
              {[
                "Get instant explanations for complex concepts",
                "Request code examples in Python or ROS2",
                "Ask follow-up questions for deeper understanding",
                "Reference specific chapters and sections",
              ].map((feature, index) => (
                <motion.li
                  key={feature}
                  initial={{ opacity: 0, x: 20 }}
                  animate={
                    isInView ? { opacity: 1, x: 0 } : { opacity: 0, x: 20 }
                  }
                  transition={{ duration: 0.3, delay: 0.3 + index * 0.05 }}
                  className="flex items-center gap-3"
                >
                  <Sparkles className="w-5 h-5 text-secondary flex-shrink-0" />
                  <span className="text-foreground-secondary">{feature}</span>
                </motion.li>
              ))}
            </ul>

            <Link
              href="/chat"
              className={cn(
                "inline-flex items-center gap-2 px-6 py-3 rounded-lg",
                "bg-gradient-to-r from-secondary to-primary text-white font-medium",
                "hover:opacity-90 transition-opacity",
                "shadow-md hover:shadow-lg"
              )}
            >
              Try the Assistant
              <ArrowRight className="w-5 h-5" />
            </Link>
          </motion.div>
        </div>
      </div>
    </section>
  );
}

export default ChatbotDemo;
