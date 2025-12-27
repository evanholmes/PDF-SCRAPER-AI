import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        "bid-primary": "#2563EB",
        "bid-success": "#16A34A",
        "bid-warning": "#F59E0B",
        "bid-danger": "#DC2626",
        "tier-1": "#DC2626",
        "tier-2": "#F59E0B",
        "tier-3": "#6B7280",
        "flow-fulfill": "#16A34A",
        "flow-partner": "#8B5CF6",
        "flow-assign": "#3B82F6",
        "flow-broker": "#F59E0B",
      },
    },
  },
  plugins: [],
};

export default config;
