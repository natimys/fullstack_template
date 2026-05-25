"use client";

import { useParams } from "next/navigation";
import { useUser } from "@/modules/users/hooks/use-users";
import { UserForm } from "@/modules/users/components/user-form";

export default function EditUserPage() {
  const params = useParams();
  const id = Number(params.id);
  const { data: user, isLoading, isError } = useUser(id);

  if (isLoading) {
    return <p className="text-muted-foreground">Loading user...</p>;
  }

  if (isError || !user) {
    return <p className="text-destructive">User not found.</p>;
  }

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold">Edit user</h1>
      <UserForm mode="edit" user={user} />
    </div>
  );
}
