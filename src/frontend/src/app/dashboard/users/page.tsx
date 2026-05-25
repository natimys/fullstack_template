import Link from "next/link";
import { UsersTable } from "@/modules/users/components/users-table";

export default function UsersPage() {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold">Users</h1>
        <Link
          href="/dashboard/users/new"
          className="inline-flex items-center justify-center rounded-md bg-primary px-4 py-2 text-sm font-medium text-primary-foreground hover:bg-primary/90"
        >
          Add user
        </Link>
      </div>
      <UsersTable />
    </div>
  );
}
