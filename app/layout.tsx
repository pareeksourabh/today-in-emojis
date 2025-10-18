// app/layout.tsx
import type { Metadata, Viewport } from 'next';
import '../styles/globals.css';

export const metadata: Metadata = {
  metadataBase: new URL('https://pareeksourabh.github.io/today-in-emojis'),
  title: 'Today in Emojis',
  description: "Today's vibe - in five emojis. Feel the day. Read it only if you must.",
  openGraph: {
    title: 'Today in Emojis',
    description: "The world's daily vibe check - five emojis, zero scroll.",
    type: 'website',
    images: [{ url: '/og.png', width: 1200, height: 630 }],
  },
  twitter: { card: 'summary_large_image' },
};

export const viewport: Viewport = {
  themeColor: '#FAFAFA',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
