"use client";

import type { UserRead } from "@/modules/users/types";

interface UserDeleteDialogProps {
  user: UserRead | null;
  onClose: () => void;
  onConfirm: () => void;
  isPending: boolean;
}

export function UserDeleteDialog({
  user,
  onClose,
  onConfirm,
  isPending,
}: UserDeleteDialogProps) {
  if (!user) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50">
      <div className="w-full max-w-md rounded-lg bg-background p-6 shadow-lg">
        <h2 className="text-lg font-semibold">Delete user</h2>
        <p className="mt-2 text-sm text-muted-foreground">
          Are you sure you want to delete <strong>{user.name}</strong>? This
          action cannot be undone.
        </p>
        <div className="mt-6 flex justify-end space-x-2">
          <button
            onClick={onClose}
            disabled={isPending}
            className="inline-flex items-center justify-center rounded-md border bg-background px-4 py-2 text-sm font-medium hover:bg-muted disabled:opacity-50"
          >
            Cancel
          </button>
          <button
            onClick={onConfirm}
            disabled={isPending}
            className="inline-flex items-center justify-center rounded-md bg-destructive px-4 py-2 text-sm font-medium text-destructive-foreground hover:bg-destructive/90 disabled:opacity-50"
          >
            {isPending ? "Deleting..." : "Delete"}
          </button>
        </div>
      </div>
    </div>
  );
}
