import flowbite from 'flowbite/plugin'

/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
    "./node_modules/flowbite/**/*.js", // ✅ Required for Flowbite components
  ],
  theme: {
    extend: {},
  },
  plugins: [
    flowbite, // ✅ Proper place for Flowbite plugin
  ],
}
