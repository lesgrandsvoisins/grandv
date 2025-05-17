/* eslint-disable import/no-extraneous-dependencies, global-require */
module.exports = {
    // content: [
    //     './templates/**/*.html'
    //     //   './**'
    //     //   // './src/**/*.{astro,html,js,jsx,svelte,ts,tsx,vue}',
    //     //   // './node_modules/astro-boilerplate-components/**/*.{js,ts,jsx,tsx}',
    // ],
    theme: {
        extend: {},
    },
    darkMode: 'class',
    plugins: [
        require('@tailwindcss/aspect-ratio'),
        require('@tailwindcss/typography'),
    ],
};