import React from 'react';

export default function TooltipTerm({ term, title }: { term: string; title: string }) {
  return (
    <span className="relative group">
      <abbr className="underline decoration-dotted cursor-help" title={title}>
        {term}
      </abbr>
      <span className="invisible group-hover:visible opacity-0 group-hover:opacity-100 transition-all absolute z-10 left-0 -top-8 bg-black text-white text-xs px-2 py-1 rounded">
        {title}
      </span>
    </span>
  );
}
