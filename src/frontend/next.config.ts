import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: "standalone",
  skipTrailingSlashRedirect: true,
  async rewrites() {
    return [
      {
        source: "/api/:path*/",
        destination: `${process.env.API_INTERNAL_URL || "http://localhost:8000"}/:path*/`,
      },
      {
        source: "/api/:path*",
        destination: `${process.env.API_INTERNAL_URL || "http://localhost:8000"}/:path*`,
      },
    ];
  },
};

export default nextConfig;
