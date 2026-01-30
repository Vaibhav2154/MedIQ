import Navbar from "@/components/landing/Navbar";
import Hero from "@/components/landing/Hero";
import Stats from "@/components/landing/Stats";
import Problem from "@/components/landing/Problem";
import Engine from "@/components/landing/Engine";
import Pipeline from "@/components/landing/Pipeline";
import TargetUsers from "@/components/landing/TargetUsers";

export default function Home() {
  return (
    <main className="min-h-screen bg-slate-50">
      <Navbar />
      <Hero />
      
      <Problem />
      <Engine />
      <Pipeline />
      <Stats />
      <TargetUsers />
    </main>
  );
}
