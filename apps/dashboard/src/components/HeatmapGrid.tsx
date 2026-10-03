'use client'

export default function HeatmapGrid({ matrix }: { matrix: any[] }) {
  if (!matrix || matrix.length === 0) return <p className="text-sm text-slate-500">No heatmap data available.</p>

  const dates: string[] = matrix[0]?.series?.map((s: any) => s.date.slice(5)) ?? []

  const color = (v: number) => {
    const delta = v - 100
    if (delta > 6)  return 'bg-red-600 text-white'
    if (delta > 3)  return 'bg-orange-400 text-white'
    if (delta > 0)  return 'bg-yellow-200 text-yellow-900'
    if (delta > -3) return 'bg-green-100 text-green-900'
    return 'bg-green-500 text-white'
  }

  return (
    <div className="overflow-x-auto">
      <table className="min-w-full text-xs border-collapse">
        <thead>
          <tr>
            <th className="sticky left-0 bg-white px-2 py-1 text-left font-semibold text-slate-600 border-b">Route</th>
            {dates.map((d) => (
              <th key={d} className="px-1 py-1 text-center font-medium text-slate-500 border-b whitespace-nowrap">{d}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {matrix.map((row) => (
            <tr key={row.route_code} className="hover:bg-slate-50">
              <td className="sticky left-0 bg-white px-2 py-1 font-mono font-semibold text-slate-700 border-b">
                {row.route_code}
              </td>
              {row.series.map((s: any) => (
                <td
                  key={s.date}
                  className={`px-1 py-1 text-center rounded border-b ${color(s.index_value)}`}
                  title={`${row.route_code} | ${s.date} | Index: ${s.index_value}`}
                >
                  {s.index_value.toFixed(1)}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
      <div className="mt-3 flex gap-4 text-xs text-slate-500">
        <span className="flex items-center gap-1"><span className="w-3 h-3 rounded bg-green-500 inline-block"/>↓ &gt;3%</span>
        <span className="flex items-center gap-1"><span className="w-3 h-3 rounded bg-green-100 inline-block"/>Slight fall</span>
        <span className="flex items-center gap-1"><span className="w-3 h-3 rounded bg-yellow-200 inline-block"/>Slight rise</span>
        <span className="flex items-center gap-1"><span className="w-3 h-3 rounded bg-orange-400 inline-block"/>↑ 3–6%</span>
        <span className="flex items-center gap-1"><span className="w-3 h-3 rounded bg-red-600 inline-block"/>↑ &gt;6%</span>
      </div>
    </div>
  )
}

