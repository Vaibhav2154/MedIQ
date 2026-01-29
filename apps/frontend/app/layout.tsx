import type { Metadata } from 'next'
import Navbar from '@/components/landing/Navbar'
import './globals.css'

export const metadata: Metadata = {
  title: 'MedIQ - Consent-aware Healthcare Data Sharing',
  description: 'AI-powered system to convert human consent into enforceable digital policies',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>
        <Navbar />
        {children}
      </body>
    </html>
  )
}
