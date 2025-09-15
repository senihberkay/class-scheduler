/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'ozu-blue': '#1e3a8a',
        'ozu-light-blue': '#3b82f6',
        'ozu-dark': '#1f2937',
        'ozu-gray': '#6b7280',
        'ozu-red': '#a30050',
        'ozu-red-light': '#c42a6a',
        'ozu-red-dark': '#8a0044',
      },
      fontFamily: {
        'sans': ['Inter', 'system-ui', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
