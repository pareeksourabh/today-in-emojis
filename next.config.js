/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'export',
  basePath: process.env.NODE_ENV === 'production' ? '/today-in-emojis' : '',
  assetPrefix: process.env.NODE_ENV === 'production' ? '/today-in-emojis' : '',
}

module.exports = nextConfig
