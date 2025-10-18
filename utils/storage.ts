export type Reaction = 'like' | 'neutral' | 'dislike' | null;

const KEY = 'tie:reaction:v1';

export function getReaction(): Reaction {
  if (typeof window === 'undefined') return null;
  try {
    const v = window.localStorage.getItem(KEY);
    if (v === 'like' || v === 'neutral' || v === 'dislike') return v;
    return null;
  } catch {
    return null;
  }
}

export function setReaction(value: Reaction) {
  if (typeof window === 'undefined' || value === null) return;
  try { window.localStorage.setItem(KEY, value); } catch {}
}
