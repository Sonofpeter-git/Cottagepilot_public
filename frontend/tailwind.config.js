/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      animation: {
        'gradient': 'gradient 8s linear infinite',
      },
      keyframes: {
        'gradient': {
          '0%, 100%': {
            'background-size': '200% 200%',
            'background-position': 'left center'
          },
          '50%': {
            'background-size': '200% 200%',
            'background-position': 'right center'
          },
        },
      },  
      colors: {
        /*Colors*/
        primary: 'var(--primary-color)',
        secondary: 'var(--secondary-color)',
        popUpBg: 'var(--popUpBg)',
        popUpBg2: 'var(--popUpForpopUpBg)',
        extraNeutral: 'var(--extra-neutral-color)',
        highlight: 'var(--highligh-color)',
        select_bg: 'var(--select_bg)',
        borderColor:'var(--border-color)',
        danger: 'var(--danger-color)',
      },
      fontSize: {
        /*Font sizes*/
        title_font : 'var(--Title-font)',
        header_font : 'var(--Header-font)',
        content_font : 'var(--Content-font)',
      }
    },
  },
  plugins: [],
}