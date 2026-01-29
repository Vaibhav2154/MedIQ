import type { Metadata } from 'next'
import Navbar from '@/components/landing/Navbar'
import Hero from '@/components/landing/Hero'
import Engine from '@/components/landing/Engine'
import Pipeline from '@/components/landing/Pipeline'
import Problem from '@/components/landing/Problem'
import Stats from '@/components/landing/Stats'
import TargetUsers from '@/components/landing/TargetUsers'
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
        <Hero />
        <Engine />
        <Problem />
        <Pipeline />
        <Stats />
        <TargetUsers />
        {children}
      </body>
    </html>
  )
}
