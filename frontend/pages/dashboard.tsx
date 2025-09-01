
import { useEffect, useState } from 'react'
import PRChart from '../components/PRChart'

type PR = {
  id: number
  title: string
  author: string
  lines_changed: number
  files_changed: number
  comments: number
  tests_modified: boolean
}

export default function Dashboard() {
  const [prs, setPrs] = useState<PR[]>([])
  const [loading, setLoading] = useState(false)

  useEffect(()=>{
    setLoading(true)
    fetch((process.env.NEXT_PUBLIC_API_URL ?? 'http://localhost:8000') + '/api/prs')
      .then(r=>r.json()).then(d=>{ setPrs(d); setLoading(false) })
      .catch(()=> setLoading(false))
  },[])

  return (
    <div className='p-8 min-h-screen bg-slate-50'>
      <div className='max-w-5xl mx-auto'>
        <div className='bg-white p-6 rounded-2xl shadow flex items-center justify-between'>
          <div>
            <h2 className='text-2xl font-bold'>PR Dashboard</h2>
            <p className='text-sm text-slate-500'>Live list of pull requests and their risk analysis.</p>
          </div>
        </div>

        <div className='mt-6 grid grid-cols-1 lg:grid-cols-3 gap-4'>
          <div className='col-span-2 bg-white p-4 rounded shadow'>
            <h3 className='font-semibold mb-2'>PRs</h3>
            {loading && <div className='text-slate-500'>Loading...</div>}
            {prs.length===0 && !loading && <div className='text-slate-500'>No PRs yet. Add one via API.</div>}
            {prs.map(pr=> (
              <div key={pr.id} className='p-3 border-b flex justify-between items-center'>
                <div>
                  <div className='font-medium'>{pr.title}</div>
                  <div className='text-sm text-slate-500'>by {pr.author} • {pr.lines_changed} lines</div>
                </div>
                <div className='flex gap-2'>
                  <button onClick={async ()=>{
                    const r = await fetch((process.env.NEXT_PUBLIC_API_URL ?? 'http://localhost:8000') + `/api/prs/${pr.id}/analyze`)
                    const j = await r.json()
                    alert('Risk score: ' + (j.risk_score ?? 'N/A'))
                  }} className='px-3 py-1 border rounded'>Analyze</button>
                </div>
              </div>
            ))}
          </div>
          <div className='bg-white p-4 rounded shadow'>
            <h3 className='font-semibold mb-2'>Risk Chart</h3>
            <PRChart prs={prs} />
          </div>
        </div>
      </div>
    </div>
  )
}
