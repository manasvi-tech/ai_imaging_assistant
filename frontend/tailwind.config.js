/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
    "./node_modules/flowbite/**/*.js",
  ],
  theme: {
    extend: {
      colors:{
        navbar: '#206f6a'
      },
      fontFamily: {
        dancing: ['"Dancing Script"', 'cursive'], // Add this line
      }
    },
  },
  plugins: [
    require('flowbite/plugin')
  ],
}

