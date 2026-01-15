import './globals.css';
import React from 'react';

export const metadata = {
  title: 'AiVRIC Solution Configurator'
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <main className="min-h-screen">
          <div className="max-w-6xl mx-auto p-6">{children}</div>
        </main>
      </body>
    </html>
  );
}
