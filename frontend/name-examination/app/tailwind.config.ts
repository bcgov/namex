import plugin from 'tailwindcss/plugin'

/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [],
  theme: {
    extend: {
      transitionProperty: {
        height: 'height',
      },
      colors: {
        'bcgov-blue3': '#1669bb',
        'bcgov-blue4': '#06527d',
        'bcgov-blue5': '#003366',
        'bcgov-blue8': '#002049',
        'bcgov-gold5': '#fcba19',
        'red-error': '#d32723'
      },
    },
  },
  plugins: [plugin(({ addVariant }) => addVariant('children', '& > *'))],
}
