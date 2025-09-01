
import Link from 'next/link'

export default function Home() {
  return (
    <main className='min-h-screen flex items-center justify-center bg-slate-50'>
      <div className='max-w-2xl p-8 bg-white rounded-2xl shadow'>
        <h1 className='text-2xl font-bold'>CodeFlow Insights</h1>
        <p className='mt-4'>A demo dashboard that flags risky PRs using a small ML model.</p>
        <div className='mt-6 flex gap-4'>
          <Link href='/dashboard'><a className='px-4 py-2 bg-blue-600 text-white rounded'>Open Dashboard</a></Link>
        </div>
      </div>
    </main>
  )
}
