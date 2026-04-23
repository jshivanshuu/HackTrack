/** @type {import('tailwindcss').Config} */
export default {
    content: [
        "./index.html",
        "./src/**/*.{js,ts,jsx,tsx}",
    ],
    theme: {
        extend: {
            colors: {
                background: '#0B0F19',
                card: '#151C2C',
                primary: '#3B82F6',
                secondary: '#10B981',
                threatHigh: '#EF4444',
                threatMedium: '#F59E0B',
                threatLow: '#3B82F6',
                textMain: '#F3F4F6',
                textMuted: '#9CA3AF'
            }
        },
    },
    plugins: [],
}
