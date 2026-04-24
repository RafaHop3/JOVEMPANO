/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        // Frutiger Aero: fontes arredondadas e amigáveis dos anos 2000
        sans:      ['Nunito', 'Segoe UI', 'Trebuchet MS', 'system-ui', 'sans-serif'],
        nunito:    ['Nunito', 'sans-serif'],
        editorial: ['Nunito', 'Trebuchet MS', 'Georgia', 'serif'],
        mono:      ['Segoe UI', 'Trebuchet MS', 'sans-serif'],
      },
      colors: {
        // Paleta Frutiger Aero
        aeroBlue:    '#1e90ff',
        aeroSky:     '#a8d8f8',
        aeroCyan:    '#5ac8fa',
        aeroGreen:   '#73d936',
        aeroGlass:   'rgba(255,255,255,0.55)',
        glossyWhite: 'rgba(255,255,255,0.90)',
        deepBlue:    '#0a2a52',
        midBlue:     '#1e5fa0',
        softBlue:    '#5ba3d8',
      },
      borderRadius: {
        'aero': '18px',
        'aero-lg': '22px',
      },
      boxShadow: {
        'aero-sm': '0 2px 0 rgba(255,255,255,0.85) inset, 0 4px 16px rgba(30,100,200,0.10)',
        'aero':    '0 2px 0 rgba(255,255,255,0.90) inset, 0 8px 32px rgba(30,100,200,0.14)',
        'aero-lg': '0 3px 0 rgba(255,255,255,0.95) inset, 0 16px 48px rgba(30,100,220,0.20)',
      },
      backdropBlur: {
        'aero': '16px',
      },
    },
  },
  plugins: [],
}
