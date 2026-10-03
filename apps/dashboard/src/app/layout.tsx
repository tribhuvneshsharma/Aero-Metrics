import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'Aero-Metrics | Real-Time Airfare Price Index (APIx)',
  description: 'High-frequency supplementary airfare price measurement platform for NSO / MoSPI and RBI — SIH 2026',
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-slate-100">{children}</body>
    </html>
  )
}

