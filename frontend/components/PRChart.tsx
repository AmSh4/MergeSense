
import { ResponsiveContainer, LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid } from 'recharts'

type PR = {
  id: number
  title: string
  lines_changed: number
}

export default function PRChart({ prs } : { prs: PR[] }) {
  // derive some fake risk values if not analyzed yet (for demo)
  const data = prs.map(p => ({ name: p.title.slice(0,12), value: Math.min(1, Math.round((p.lines_changed/2000)*100)/100) }))
  return (
    <div style={{ width: '100%', height: 220 }}>
      <ResponsiveContainer>
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="name" />
          <YAxis domain={[0,1]} />
          <Tooltip />
          <Line type="monotone" dataKey="value" stroke="#8884d8" strokeWidth={2} />
        </LineChart>
      </ResponsiveContainer>
    </div>
  )
}
