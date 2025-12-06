/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#FEF2F2',   // red-50
          100: '#FEE2E2',  // red-100
          200: '#FECACA',  // red-200
          300: '#FCA5A5',  // red-300
          400: '#F87171',  // red-400
          500: '#EF4444',  // red-500
          600: '#DC2626',  // red-600 - Main brand color (BRED)
          700: '#B91C1C',  // red-700 - Hover states
          800: '#991B1B',  // red-800
          900: '#7F1D1D',  // red-900
        },
      },
    },
  },
  plugins: [],
}
