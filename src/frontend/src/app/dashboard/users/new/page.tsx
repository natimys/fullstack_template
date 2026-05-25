import { UserForm } from "@/modules/users/components/user-form";

export default function NewUserPage() {
  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold">Create user</h1>
      <UserForm mode="create" />
    </div>
  );
}
