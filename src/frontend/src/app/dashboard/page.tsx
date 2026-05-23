"use client";

import { useAuth } from "@/providers/auth-provider";

export default function DashboardPage() {
  const { user } = useAuth();

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold">Dashboard</h1>
      <p className="text-muted-foreground">
        Welcome{user ? `, ${user.name}` : ""}. Select a module from the sidebar.
      </p>
    </div>
  );
}
