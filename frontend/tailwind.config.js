/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        mono: ['"JetBrains Mono"', 'Consolas', 'monospace'],
        sans: ['"Inter"', 'system-ui', 'sans-serif'],
        grotesk: ['"Space Grotesk"', 'sans-serif'],
        tilt: ['"Tilt Neon"', 'sans-serif'],
        editorial: ['"Space Grotesk"', '"Inter"', 'sans-serif'],
      },
      colors: {
        neon: {
          cyan: '#00fff5',
          glowCyan: '#7eb8e0',
          blue: '#3b82f6',
          purple: '#a855f7',
          green: '#10b981',
          lime: '#39ff14',
          amber: '#f59e0b',
          rose: '#f43f5e',
        },
        terminal: {
          bg: '#030508',
          deep: '#050811',
          surface: '#0a1628',
          card: 'rgba(10, 22, 40, 0.75)',
          border: 'rgba(0, 255, 245, 0.18)',
          borderHover: 'rgba(0, 255, 245, 0.45)',
          muted: '#8fa8bc',
          text: '#c8d6e3',
          bright: '#f1f5f9',
        },
      },
      boxShadow: {
        'neon-cyan': '0 0 20px rgba(0, 255, 245, 0.25)',
        'neon-cyan-lg': '0 0 35px rgba(0, 255, 245, 0.35)',
        'card-cyber': '0 8px 32px 0 rgba(0, 0, 0, 0.7), inset 0 1px 1px rgba(0, 255, 245, 0.12)',
        'glass-magnetic': '0 12px 40px 0 rgba(0, 0, 0, 0.8), inset 0 1px 0 rgba(255, 255, 255, 0.1)',
      },
      animation: {
        'pulse-neon': 'pulse-neon 2.5s ease-in-out infinite',
        'float-slow': 'float-slow 6s ease-in-out infinite',
        'scanline': 'scanline 8s linear infinite',
      },
      keyframes: {
        'pulse-neon': {
          '0%, 100%': { opacity: '1', filter: 'drop-shadow(0 0 8px rgba(0, 255, 245, 0.6))' },
          '50%': { opacity: '0.7', filter: 'drop-shadow(0 0 2px rgba(0, 255, 245, 0.2))' },
        },
        'float-slow': {
          '0%, 100%': { transform: 'translateY(0)' },
          '50%': { transform: 'translateY(-6px)' },
        },
        'scanline': {
          '0%': { transform: 'translateY(-100%)' },
          '100%': { transform: 'translateY(1000%)' },
        },
      },
    },
  },
  plugins: [],
}
