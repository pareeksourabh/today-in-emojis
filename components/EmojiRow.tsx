import React from 'react';

type EmojiItem = { char: string; label: string; url?: string };

export default function EmojiRow({ emojis }: { emojis: EmojiItem[] }) {
  return (
    <div className="flex items-center justify-center gap-8 md:gap-10 py-10">
      {emojis.slice(0, 5).map((e, idx) => {
        const content = (
          <span
            className="emoji-btn text-[80px] md:text-[120px] leading-none select-none"
            role="img"
            aria-label={e.label || 'emoji'}
          >
            {e.char}
          </span>
        );
        return (
          <div key={idx} className="flex items-center justify-center">
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
  );
}
