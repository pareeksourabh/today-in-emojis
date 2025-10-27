import React from 'react';

type EmojiItem = { char: string; label: string; url?: string; title?: string };

export default function EmojiRow({ emojis }: { emojis: EmojiItem[] }) {
  return (
    <div className="w-full overflow-x-auto px-2 sm:px-4">
      <div className="flex items-center justify-center gap-2 sm:gap-4 md:gap-6 lg:gap-8 py-2 sm:py-4 md:py-8 min-w-max">
        {emojis.slice(0, 5).map((e, idx) => {
          const content = (
            <span
              className="emoji-btn text-[40px] sm:text-[60px] md:text-[80px] lg:text-[100px] leading-none select-none"
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
                  title={e.title || e.label || ''}
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
