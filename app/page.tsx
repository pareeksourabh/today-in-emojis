'use client';

import React from 'react';
import EmojiRow from '../components/EmojiRow';
import Footer from '../components/Footer';

type EmojiItem = { char: string; label: string; url?: string };
type TodayData = { date: string; emojis: EmojiItem[] };

export default function HomePage() {
  const [data, setData] = React.useState<TodayData | null>(null);

  React.useEffect(() => {
    fetch('data/today.json', { cache: 'no-store' })
      .then(r => r.ok ? r.json() : Promise.reject(r.statusText))
      .then(setData)
      .catch(() => setData({ date: '', emojis: [] }));
  }, []);

  return (
    <div className="h-full w-full flex flex-col items-center justify-between overflow-hidden">
      <header className="w-full flex items-center justify-center pt-2 sm:pt-3 md:pt-5 flex-shrink-0">
        <h1 className="tracking-widest uppercase font-semibold text-xs sm:text-sm md:text-base lg:text-lg">Today in Emojis</h1>
      </header>
      <main className="flex-1 w-full flex items-center justify-center min-h-0">
        {data && data.emojis && data.emojis.length > 0 ? (
          <EmojiRow emojis={data.emojis} />
        ) : (
          <div className="text-black/40">Loading…</div>
        )}
      </main>
      <footer className="w-full flex-shrink-0">
        <Footer />
      </footer>
    </div>
  );
}
