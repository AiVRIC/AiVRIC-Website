import Link from 'next/link';
import React from 'react';
import Header from '../components/ui/Header';
import Card from '../components/ui/Card';
import Button from '../components/ui/Button';

export default function Home() {
  return (
    <div>
      <Header />
      <div className="grid grid-cols-2 gap-6">
        <Card>
          <h2 className="text-xl font-semibold">Quick Start</h2>
          <p className="text-sm text-gray-600 mt-2">Interactive wizard to configure security solution tiers and integrations.</p>
          <div className="mt-4">
            <Link href="/configurator"><Button>Start Configurator</Button></Link>
          </div>
        </Card>

        <Card>
          <h2 className="text-xl font-semibold">Results</h2>
          <p className="text-sm text-gray-600 mt-2">View example recommendations and export PDF or email results.</p>
          <div className="mt-4">
            <Link href="/results"><Button variant="secondary">View Results</Button></Link>
          </div>
        </Card>
      </div>
    </div>
  );
}
