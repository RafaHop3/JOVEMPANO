/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        inter: ['Inter', 'sans-serif'],
        editorial: ['Playfair Display', 'serif'],
        mono: ['JetBrains Mono', 'monospace'],
      },
      colors: {
        terminalBg: '#000000',
        neonGreen: '#39ff14',
        neonCyan: '#00fff5',
        neonRed: '#ff003c',
        terminalMuted: '#5a7d7c',
      }
    },
  },
  plugins: [],
}
