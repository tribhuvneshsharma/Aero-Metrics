/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        apix: {
          blue: '#1e3a5f',
          teal: '#0d9488',
          amber: '#f59e0b',
          red: '#ef4444',
          green: '#10b981',
          slate: '#64748b',
        },
      },
    },
  },
  plugins: [],
}

