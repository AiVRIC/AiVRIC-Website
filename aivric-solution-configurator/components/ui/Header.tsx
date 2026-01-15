import React from 'react';
import Link from 'next/link';
import Button from './Button';

export default function Header(){
  return (
    <header className="flex items-center justify-between mb-6">
      <div>
        <Link href="/" className="text-2xl font-bold">AiVRIC</Link>
        <div className="text-sm text-gray-500">Solution Configurator</div>
      </div>
      <div className="flex items-center gap-2">
        <Link href="/configurator"><Button variant="secondary">Start</Button></Link>
        <Link href="/results"><Button variant="ghost">Results</Button></Link>
      </div>
    </header>
  );
}
