/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        mint: {
          50: '#f0fdf4',
          100: '#dcfce7',
          400: '#4ade80',
          500: '#22c55e', // Primary Brand Color
          600: '#16a34a',
          700: '#15803d',
        },
        slate: {
          800: '#1e293b',
          900: '#0f172a',
        }
      },
    },
  },
  plugins: [],
}
