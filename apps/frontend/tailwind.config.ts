/** @type {import('tailwindcss').Config} */
const config = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        'med-green': '#1a6b4f',
        'med-light': '#f5f5f5',
      },
      height: {
        '125': '31.25rem',
      },
    },
  },
  plugins: [],
}
export default config
