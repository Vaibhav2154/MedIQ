import Hero from '@/components/landing/Hero'
import Engine from '@/components/landing/Engine'
import Problem from '@/components/landing/Problem'
import Pipeline from '@/components/landing/Pipeline'
import Stats from '@/components/landing/Stats'
import TargetUsers from '@/components/landing/TargetUsers'

export default function Page() {
  return (
    <main>
      <Hero />
      <Engine />
      <Problem />
      <Pipeline />
      <Stats />
      <TargetUsers />
    </main>
  )
}
