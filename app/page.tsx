'use client';

import React from 'react';
import EmojiRow from '../components/EmojiRow';
import Footer from '../components/Footer';

type EmojiItem = { char: string; label: string; url?: string };
type TodayData = { date: string; emojis: EmojiItem[] };

export default function HomePage() {
  const [data, setData] = React.useState<TodayData | null>(null);

  React.useEffect(() => {
    fetch('/data/today.json', { cache: 'no-store' })
      .then(r => r.ok ? r.json() : Promise.reject(r.statusText))
      .then(setData)
      .catch(() => setData({ date: '', emojis: [] }));
  }, []);

  return (
    <div className="min-h-screen w-full flex flex-col items-center justify-between overflow-hidden">
      <header className="w-full flex items-center justify-center pt-6">
        <h1 className="tracking-widest uppercase font-semibold text-lg md:text-xl">Today in Emojis</h1>
      </header>
      <main className="flex-1 w-full flex items-center justify-center">
        {data && data.emojis && data.emojis.length > 0 ? (
          <EmojiRow emojis={data.emojis} />
        ) : (
          <div className="text-black/40">Loading…</div>
        )}
      </main>
      <footer className="w-full">
        <Footer />
      </footer>
    </div>
  );
}
