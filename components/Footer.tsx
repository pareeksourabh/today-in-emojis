'use client';

// components/Footer.tsx (Floating Dock)
import React from 'react';
import { getReaction, setReaction, Reaction } from '../utils/storage';

const REACTIONS = [
  { id: 'like',    char: '❤️', label: 'Like' },
  { id: 'neutral', char: '🤔', label: 'Neutral' },
  { id: 'dislike', char: '👎', label: 'Dislike' },
] as const;

export default function Footer() {
  const [reaction, setReactionState] = React.useState<Reaction>(null);
  const [mounted, setMounted] = React.useState(false);

  React.useEffect(() => {
    setMounted(true);
    setReactionState(getReaction());
  }, []);

  const set = (v: Reaction) => { setReaction(v); setReactionState(v); };

  return (
    <div className="w-full py-2 sm:py-3 md:py-5 px-4">
      <div className="flex flex-col items-center gap-2 sm:gap-3 md:gap-5">
        {/* Dock */}
        <div className="flex items-center justify-center">
          <div className="flex items-center gap-2 sm:gap-3 md:gap-4 rounded-full border border-black/10 bg-white/60 backdrop-blur px-3 sm:px-4 py-2">
            {REACTIONS.map(r => (
              <button
                key={r.id}
                onClick={() => set(r.id)}
                aria-label={r.label}
                aria-pressed={mounted ? reaction === r.id : false}
                title={r.label}
                className={[
                  "reaction-btn w-9 h-9 sm:w-10 sm:h-10 md:w-12 md:h-12 rounded-full transition-colors",
                  mounted && reaction === r.id ? "bg-gray-200" : "bg-transparent hover:bg-gray-100"
                ].join(" ")}
              >
                <span className="text-xl sm:text-2xl md:text-3xl leading-none select-none">{r.char}</span>
              </button>
            ))}
          </div>
        </div>

        {/* What's this link */}
        <div className="flex items-center justify-center">
          <a
            href="https://github.com/pareeksourabh/today-in-emojis#readme"
            target="_blank"
            rel="noopener noreferrer"
            className={[
              "reaction-btn inline-flex items-center justify-center",
              "rounded-full px-4 py-2 text-xs sm:text-sm font-medium",
              "bg-amber-300 text-white hover:bg-amber-400",
              "focus:outline-none focus:ring-2 focus:ring-amber-500/40",
              "transition-transform hover:scale-[1.03]"
            ].join(" ")}
            aria-label="Open README on GitHub"
            title="What's this project?"
          >
            What's this?
          </a>
        </div>
      </div>
    </div>
  );
}

