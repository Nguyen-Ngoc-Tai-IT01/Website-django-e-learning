/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html',       // Quét các file HTML dùng chung ở thư mục gốc
    './*/templates/**/*.html',     // Quét toàn bộ HTML nằm bên trong các App (core, courses, users...)
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}