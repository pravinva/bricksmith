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
          50: '#fff1ef',
          100: '#ffd9d2',
          200: '#ffb3a6',
          300: '#ff8d79',
          400: '#ff674d',
          500: '#ff4d35',
          600: '#FF3621',
          700: '#d62d1b',
          800: '#ad2416',
          900: '#851c10',
        },
        dbx: {
          navy: '#1B3139',
          cyan: '#00A8E1',
          lava: '#FF3621',
        },
      },
    },
  },
  plugins: [require('@tailwindcss/typography')],
}
