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
      },
      fontFamily: {
        'sans': ['Inter', 'system-ui', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
