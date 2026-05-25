"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { useCreateUser, useUpdateUser } from "@/modules/users/hooks/use-users";
import type { UserRead, UserCreate, UserUpdate } from "@/modules/users/types";

interface UserFormProps {
  mode: "create" | "edit";
  user?: UserRead | null;
}

export function UserForm({ mode, user }: UserFormProps) {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [role, setRole] = useState("user");
  const [isActive, setIsActive] = useState(true);

  const createMutation = useCreateUser();
  const updateMutation = useUpdateUser(user?.id ?? 0);
  const router = useRouter();

  useEffect(() => {
    if (user) {
      setName(user.name);
      setEmail(user.email);
      setRole(user.role);
      setIsActive(user.is_active);
    }
  }, [user]);

  const isPending = createMutation.isPending || updateMutation.isPending;

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    if (mode === "create") {
      const payload: UserCreate = { name, email, password, role };
      createMutation.mutate(payload, {
        onSuccess: () => router.push("/dashboard/users"),
      });
    } else {
      const payload: UserUpdate = {};
      if (name !== user?.name) payload.name = name;
      if (email !== user?.email) payload.email = email;
      if (password) payload.password = password;
      if (role !== user?.role) payload.role = role;
      if (isActive !== user?.is_active) payload.is_active = isActive;

      if (Object.keys(payload).length === 0) {
        router.push("/dashboard/users");
        return;
      }

      updateMutation.mutate(payload, {
        onSuccess: () => router.push("/dashboard/users"),
      });
    }
  };

  return (
    <form onSubmit={handleSubmit} className="max-w-lg space-y-4">
      <div className="space-y-2">
        <label htmlFor="name" className="text-sm font-medium leading-none">
          Name
        </label>
        <input
          id="name"
          value={name}
          onChange={(e) => setName(e.target.value)}
          required
          className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
        />
      </div>

      <div className="space-y-2">
        <label htmlFor="email" className="text-sm font-medium leading-none">
          Email
        </label>
        <input
          id="email"
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
          className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
        />
      </div>

      <div className="space-y-2">
        <label htmlFor="password" className="text-sm font-medium leading-none">
          Password {mode === "edit" && <span className="text-muted-foreground">(leave blank to keep current)</span>}
        </label>
        <input
          id="password"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required={mode === "create"}
          className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
        />
      </div>

      <div className="space-y-2">
        <label htmlFor="role" className="text-sm font-medium leading-none">
          Role
        </label>
        <select
          id="role"
          value={role}
          onChange={(e) => setRole(e.target.value)}
          className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
        >
          <option value="user">User</option>
          <option value="admin">Admin</option>
        </select>
      </div>

      {mode === "edit" && (
        <div className="flex items-center space-x-2">
          <input
            id="is_active"
            type="checkbox"
            checked={isActive}
            onChange={(e) => setIsActive(e.target.checked)}
            className="h-4 w-4 rounded border-gray-300 text-primary focus:ring-primary"
          />
          <label htmlFor="is_active" className="text-sm font-medium leading-none">
            Active
          </label>
        </div>
      )}

      {(createMutation.isError || updateMutation.isError) && (
        <p className="text-sm text-destructive">
          Failed to save user. Please try again.
        </p>
      )}

      <div className="flex space-x-2">
        <button
          type="submit"
          disabled={isPending}
          className="inline-flex items-center justify-center rounded-md bg-primary px-4 py-2 text-sm font-medium text-primary-foreground hover:bg-primary/90 disabled:opacity-50"
        >
          {isPending
            ? "Saving..."
            : mode === "create"
              ? "Create user"
              : "Save changes"}
        </button>
        <button
          type="button"
          onClick={() => router.push("/dashboard/users")}
          disabled={isPending}
          className="inline-flex items-center justify-center rounded-md border bg-background px-4 py-2 text-sm font-medium hover:bg-muted disabled:opacity-50"
        >
          Cancel
        </button>
      </div>
    </form>
  );
}
