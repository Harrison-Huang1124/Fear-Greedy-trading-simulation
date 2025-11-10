/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
    "./public/index.html"
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        'neural-blue': '#667eea',
        'neural-purple': '#764ba2',
        'fear-red': '#ef4444',
        'greed-green': '#10b981',
        'neutral-gray': '#6b7280',
      },
      backgroundImage: {
        'neural-gradient': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        'neural-mesh': 'radial-gradient(at 0% 0%, rgba(102, 126, 234, 0.3) 0px, transparent 50%), radial-gradient(at 100% 0%, rgba(118, 75, 162, 0.3) 0px, transparent 50%), radial-gradient(at 100% 100%, rgba(102, 126, 234, 0.2) 0px, transparent 50%), radial-gradient(at 0% 100%, rgba(118, 75, 162, 0.2) 0px, transparent 50%)',
      },
      animation: {
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'glow': 'glow 2s ease-in-out infinite alternate',
      },
      keyframes: {
        glow: {
          '0%': { boxShadow: '0 0 5px rgba(102, 126, 234, 0.5)' },
          '100%': { boxShadow: '0 0 20px rgba(102, 126, 234, 0.8), 0 0 30px rgba(118, 75, 162, 0.6)' },
        }
      }
    },
  },
  plugins: [],
}

