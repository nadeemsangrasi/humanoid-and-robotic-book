/**
 * Navbar Component
 *
 * Main navigation bar with logo, navigation links, auth buttons, and theme toggle.
 * Includes mobile hamburger menu with responsive breakpoints.
 */

"use client";

import { useState, useCallback } from "react";
import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { Menu, X, BookOpen, MessageSquare, LogOut, User } from "lucide-react";
import { useSession, signOut } from "@/lib/auth-client";
import { ThemeToggle } from "./ThemeToggle";
import { cn } from "@/lib/utils";
import { NAVBAR_HEIGHT } from "@/lib/constants";

interface NavLinkProps {
  href: string;
  children: React.ReactNode;
  icon?: React.ReactNode;
  onClick?: () => void;
}

function NavLink({ href, children, icon, onClick }: NavLinkProps) {
  const pathname = usePathname();
  const isActive = pathname === href;

  return (
    <Link
      href={href}
      onClick={onClick}
      className={cn(
        "inline-flex items-center gap-2 px-3 py-2 rounded-lg text-sm font-medium",
        "transition-colors duration-200",
        isActive
          ? "bg-primary/10 text-primary"
          : "text-foreground-secondary hover:text-foreground hover:bg-hover-bg hover:transition-colors"
      )}
    >
      {icon}
      {children}
    </Link>
  );
}

export function Navbar() {
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const { data: session, isPending } = useSession();
  const router = useRouter();

  const toggleMobileMenu = useCallback(() => {
    setIsMobileMenuOpen((prev) => !prev);
  }, []);

  const closeMobileMenu = useCallback(() => {
    setIsMobileMenuOpen(false);
  }, []);

  const handleSignOut = useCallback(async () => {
    await signOut({
      fetchOptions: {
        onSuccess: () => {
          router.push("/");
          closeMobileMenu();
        },
      },
    });
  }, [router, closeMobileMenu]);

  return (
    <header
      className="fixed top-0 left-0 right-0 z-40 bg-background/80 backdrop-blur-md border-b border-border"
      style={{ height: NAVBAR_HEIGHT }}
    >
      <nav className="h-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-full">
          {/* Logo */}
          <Link
            href="/"
            className="flex items-center gap-2 font-bold text-lg text-foreground hover:text-primary transition-colors"
          >
            <div className="w-8 h-8 rounded-lg bg-gradient-primary flex items-center justify-center">
              <BookOpen className="w-5 h-5 text-white" />
            </div>
            <span className="hidden sm:inline">Physical AI</span>
          </Link>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center gap-2">
            <NavLink href="/book" icon={<BookOpen className="w-4 h-4" />}>
              Book
            </NavLink>
            <NavLink href="/chat" icon={<MessageSquare className="w-4 h-4" />}>
              Chat
            </NavLink>
          </div>

          {/* Desktop Actions */}
          <div className="hidden md:flex items-center gap-3">
            <ThemeToggle size="sm" />

            {isPending ? (
              <div className="w-20 h-9 rounded-lg bg-background-secondary animate-pulse" />
            ) : session?.user ? (
              <div className="flex items-center gap-3">
                <div className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-background-secondary">
                  <User className="w-4 h-4 text-foreground-muted" />
                  <span className="text-sm text-foreground-secondary max-w-[120px] truncate">
                    {session.user.name || session.user.email}
                  </span>
                </div>
                <button
                  onClick={handleSignOut}
                  className={cn(
                    "inline-flex items-center gap-2 px-3 py-2 rounded-lg",
                    "text-sm font-medium text-foreground-secondary",
                    "hover:text-foreground hover:bg-hover-bg transition-colors"
                  )}
                >
                  <LogOut className="w-4 h-4" />
                  <span className="sr-only sm:not-sr-only">Sign Out</span>
                </button>
              </div>
            ) : (
              <div className="flex items-center gap-2">
                <Link
                  href="/login"
                  className={cn(
                    "px-4 py-2 rounded-lg text-sm font-medium",
                    "text-foreground-secondary hover:text-foreground",
                    "hover:bg-hover-bg transition-colors"
                  )}
                >
                  Sign In
                </Link>
                <Link
                  href="/register"
                  className={cn(
                    "px-4 py-2 rounded-lg text-sm font-medium",
                    "bg-gradient-primary text-white",
                    "hover:opacity-90 transition-opacity"
                  )}
                >
                  Sign Up
                </Link>
              </div>
            )}
          </div>

          {/* Mobile Menu Button */}
          <div className="flex md:hidden items-center gap-2">
            <ThemeToggle size="sm" />
            <button
              onClick={toggleMobileMenu}
              className={cn(
                "p-2 rounded-lg",
                "text-foreground-secondary hover:text-foreground",
                "hover:bg-hover-bg transition-colors"
              )}
              aria-label={isMobileMenuOpen ? "Close menu" : "Open menu"}
              aria-expanded={isMobileMenuOpen}
            >
              {isMobileMenuOpen ? (
                <X className="w-6 h-6" />
              ) : (
                <Menu className="w-6 h-6" />
              )}
            </button>
          </div>
        </div>
      </nav>

      {/* Mobile Menu */}
      {isMobileMenuOpen && (
        <div className="md:hidden absolute top-full left-0 right-0 bg-background border-b border-border shadow-lg">
          <div className="px-4 py-4 space-y-2">
            {/* Navigation Links */}
            <NavLink
              href="/book"
              icon={<BookOpen className="w-4 h-4" />}
              onClick={closeMobileMenu}
            >
              Book
            </NavLink>
            <NavLink
              href="/chat"
              icon={<MessageSquare className="w-4 h-4" />}
              onClick={closeMobileMenu}
            >
              Chat
            </NavLink>

            {/* Divider */}
            <hr className="my-3 border-border" />

            {/* Auth Actions */}
            {isPending ? (
              <div className="w-full h-10 rounded-lg bg-background-secondary animate-pulse" />
            ) : session?.user ? (
              <div className="space-y-2">
                <div className="flex items-center gap-2 px-3 py-2 rounded-lg bg-background-secondary">
                  <User className="w-4 h-4 text-foreground-muted" />
                  <span className="text-sm text-foreground-secondary">
                    {session.user.name || session.user.email}
                  </span>
                </div>
                <button
                  onClick={handleSignOut}
                  className={cn(
                    "w-full flex items-center gap-2 px-3 py-2 rounded-lg",
                    "text-sm font-medium text-foreground-secondary",
                    "hover:text-foreground hover:bg-hover-bg transition-colors"
                  )}
                >
                  <LogOut className="w-4 h-4" />
                  Sign Out
                </button>
              </div>
            ) : (
              <div className="space-y-2">
                <Link
                  href="/login"
                  onClick={closeMobileMenu}
                  className={cn(
                    "block w-full px-4 py-2 rounded-lg text-center",
                    "text-sm font-medium text-foreground-secondary",
                    "border border-border hover:bg-hover-bg transition-colors"
                  )}
                >
                  Sign In
                </Link>
                <Link
                  href="/register"
                  onClick={closeMobileMenu}
                  className={cn(
                    "block w-full px-4 py-2 rounded-lg text-center",
                    "text-sm font-medium bg-gradient-primary text-white",
                    "hover:opacity-90 transition-opacity"
                  )}
                >
                  Sign Up
                </Link>
              </div>
            )}
          </div>
        </div>
      )}
    </header>
  );
}

export default Navbar;
