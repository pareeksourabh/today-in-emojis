import React from 'react';

type EmojiItem = { char: string; label: string; url?: string };

export default function EmojiRow({ emojis }: { emojis: EmojiItem[] }) {
  return (
    <div className="w-full overflow-x-auto px-4">
      <div className="flex items-center justify-center gap-4 sm:gap-6 md:gap-8 lg:gap-10 py-10 min-w-max">
        {emojis.slice(0, 5).map((e, idx) => {
          const content = (
            <span
              className="emoji-btn text-[60px] sm:text-[80px] md:text-[100px] lg:text-[120px] leading-none select-none"
              role="img"
              aria-label={e.label || 'emoji'}
            >
              {e.char}
            </span>
          );
          return (
            <div key={idx} className="flex items-center justify-center flex-shrink-0">
              {e.url ? (
                <a
                  href={e.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  aria-label={e.label || 'open related story'}
                  title={e.label || ''}
                >
                  {content}
                </a>
              ) : (
                content
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
