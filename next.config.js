/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'export',
  // Removed basePath and assetPrefix for custom domain (todayinemojis.com)
  // Site now serves from root instead of /today-in-emojis subdirectory
}

module.exports = nextConfig
