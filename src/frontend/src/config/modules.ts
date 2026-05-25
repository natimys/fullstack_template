import { Users, type LucideIcon } from "lucide-react";

export interface ModuleNav {
  name: string;
  label: string;
  href: string;
  icon: LucideIcon;
  active: boolean;
}

export const moduleNavs: ModuleNav[] = [
  {
    name: "users",
    label: "Users",
    href: "/dashboard/users",
    icon: Users,
    active: true,
  },
];
