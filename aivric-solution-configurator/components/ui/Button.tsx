import React from 'react';
import clsx from 'clsx';

export default function Button({ children, variant = 'primary', className = '', ...props }: any) {
  const base = 'inline-flex items-center justify-center rounded-md px-4 py-2 text-sm font-medium focus:outline-none focus:ring-2 focus:ring-offset-2';
  const variants: Record<string,string> = {
    primary: 'bg-sky-600 text-white hover:bg-sky-700 focus:ring-sky-500',
    secondary: 'bg-white text-gray-700 border hover:bg-gray-50 focus:ring-gray-300',
    ghost: 'bg-transparent text-gray-700 hover:bg-gray-50'
  };
  return (
    <button className={clsx(base, variants[variant] ?? variants.primary, className)} {...props}>
      {children}
    </button>
  );
}
