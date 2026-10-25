import React from "react";
import notes from "../notes.json";

export type SlideNotes = { n: number; title: string; time: string; paragraphs: string[] };
export const NOTES = notes as { slides: SlideNotes[]; qa: { q: string; a: string }[] };

/** tiny markdown: *[stage direction]*, **bold**, `code` */
export function Md({ text }: { text: string }) {
  const parts = text.split(/(\*\*[^*]+\*\*|\*[^*]+\*|`[^`]+`)/g).filter(Boolean);
  return (
    <>
      {parts.map((p, i) =>
        p.startsWith("**") ? <b key={i}>{p.slice(2, -2)}</b> : p.startsWith("*") ? <em key={i}>{p.slice(1, -1)}</em> : p.startsWith("`") ? <code key={i}>{p.slice(1, -1)}</code> : <React.Fragment key={i}>{p}</React.Fragment>,
      )}
    </>
  );
}
