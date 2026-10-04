'use client'

import { useEffect, useState } from 'react'
import {
  LineChart, Line, BarChart, Bar,
  XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, ReferenceLine
} from 'recharts'

// ── API base ────────────────────────────────────────────────────────────────
const API = 'https://aero-metrics.onrender.com'

async function get(path: string) {
  try {
    const res = await fetch(`${API}${path}`)
    if (!res.ok) return null
    return res.json()
  } catch {
    return null
  }
}

// ── Small helpers ───────────────────────────────────────────────────────────
function Badge({ label, ok }: { label: string; ok?: boolean }) {
  return (
    <span className={`inline-flex items-center gap-1 rounded-full px-2 py-0.5 text-xs font-medium
      ${ok !== false ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'}`}>
      <span className={`w-1.5 h-1.5 rounded-full ${ok !== false ? 'bg-green-500' : 'bg-red-500'}`} />
      {label}
    </span>
  )
}

function Card({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <div className="rounded-2xl bg-white shadow-sm p-5">
      <h2 className="text-sm font-bold text-slate-600 mb-3 border-b pb-2 uppercase tracking-wide">{title}</h2>
      {children}
    </div>
  )
}

function Stat({ label, value, sub, color = 'teal' }:
  { label: string; value: string; sub?: string; color?: 'teal' | 'blue' | 'amber' | 'green' | 'red' }) {
  const border: Record<string, string> = {
    teal: 'border-teal-500 bg-teal-50 text-teal-700',
    blue: 'border-blue-500 bg-blue-50 text-blue-700',
    amber: 'border-amber-500 bg-amber-50 text-amber-700',
    green: 'border-green-500 bg-green-50 text-green-700',
    red: 'border-red-500 bg-red-50 text-red-700',
  }
  return (
    <div className={`rounded-xl border-l-4 p-4 shadow-sm ${border[color]}`}>
      <p className="text-xs font-semibold uppercase tracking-wide opacity-60">{label}</p>
      <p className="mt-1 text-2xl font-black">{value}</p>
      {sub && <p className="mt-0.5 text-xs opacity-60">{sub}</p>}
    </div>
  )
}

// ── Heatmap ─────────────────────────────────────────────────────────────────
function HeatmapTable({ matrix }: { matrix: any[] }) {
  if (!matrix?.length) return <p className="text-sm text-slate-400">No data.</p>
  const dates: string[] = matrix[0]?.series?.map((s: any) => s.date.slice(5)) ?? []
  const cell = (v: number) => {
    const d = v - 100
    if (d > 6)  return 'bg-red-500 text-white'
    if (d > 3)  return 'bg-orange-400 text-white'
    if (d > 0)  return 'bg-yellow-200 text-yellow-900'
    if (d > -3) return 'bg-emerald-100 text-emerald-900'
    return 'bg-emerald-500 text-white'
  }
  return (
    <div className="overflow-x-auto text-xs">
      <table className="min-w-full border-collapse">
        <thead>
          <tr>
            <th className="sticky left-0 bg-white px-2 py-1 text-left text-slate-500 border-b">Route</th>
            {dates.map(d => <th key={d} className="px-1 py-1 text-center text-slate-400 border-b whitespace-nowrap">{d}</th>)}
          </tr>
        </thead>
        <tbody>
          {matrix.map(row => (
            <tr key={row.route_code} className="hover:bg-slate-50">
              <td className="sticky left-0 bg-white px-2 py-1 font-mono font-semibold text-teal-700 border-b">{row.route_code}</td>
              {row.series.map((s: any) => (
                <td key={s.date} className={`px-1 py-1 text-center rounded border-b ${cell(s.index_value)}`} title={`${row.route_code} | ${s.date} | ${s.index_value}`}>
                  {s.index_value.toFixed(1)}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
      <div className="mt-2 flex gap-3 text-xs text-slate-400">
        {[['bg-emerald-500','↓ >3%'],['bg-emerald-100','Slight fall'],['bg-yellow-200','Slight rise'],['bg-orange-400','↑ 3–6%'],['bg-red-500','↑ >6%']].map(([c,l]) =>
          <span key={l} className="flex items-center gap-1"><span className={`w-3 h-3 rounded ${c} inline-block`}/>{l}</span>
        )}
      </div>
    </div>
  )
}

// ── Main page (client component) ─────────────────────────────────────────────
export default function Dashboard() {
  const [headline, setHeadline]   = useState<any>(null)
  const [daily,    setDaily]      = useState<any>(null)
  const [heatmap,  setHeatmap]    = useState<any>(null)
  const [leadTime, setLeadTime]   = useState<any>(null)
  const [quality,  setQuality]    = useState<any>(null)
  const [routes,   setRoutes]     = useState<any>(null)
  const [apiOk,    setApiOk]      = useState(false)
  const [loading,  setLoading]    = useState(true)

  useEffect(() => {
    async function load() {
      const [h, d, hm, lt, q, r] = await Promise.all([
        get('/v1/index/headline'),
        get('/v1/index/daily?limit=30'),
        get('/v1/analytics/heatmap?limit_days=14'),
        get('/v1/analytics/lead-time'),
        get('/v1/data-quality/summary'),
        get('/v1/routes'),
      ])
      setHeadline(h); setDaily(d); setHeatmap(hm)
      setLeadTime(lt); setQuality(q); setRoutes(r)
      setApiOk(h !== null)
      setLoading(false)
    }
    load()
    const interval = setInterval(load, 60_000)
    return () => clearInterval(interval)
  }, [])

  const pct1 = headline?.one_day_change_pct
  const pct7 = headline?.seven_day_change_pct

  return (
    <div className="min-h-screen bg-slate-100">
      {/* Header */}
      <header className="bg-[#1e3a5f] text-white px-6 py-4 shadow-lg">
        <div className="max-w-7xl mx-auto flex flex-wrap items-center justify-between gap-3">
          <div>
            <h1 className="text-xl font-black tracking-tight">
              ✈ Aero-Metrics <span className="text-teal-300">APIx</span>
            </h1>
            <p className="text-xs text-slate-300 mt-0.5">
              Real-Time Airfare Price Index · SIH 2026 PS-56 · NSO / MoSPI &amp; RBI
            </p>
          </div>
          <div className="flex items-center gap-3 flex-wrap">
            {loading
              ? <span className="text-xs text-slate-400 animate-pulse">Loading…</span>
              : <Badge label={apiOk ? 'API Connected' : 'API Offline'} ok={apiOk} />
            }
            <Badge label={`Source: ${headline?.source_mode ?? 'replay_fixture'}`} />
            <span className="text-xs text-slate-400">Updated: {headline?.index_date ?? '—'}</span>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 py-6 space-y-5">
        {/* Offline banner */}
        {!loading && !apiOk && (
          <div className="rounded-xl bg-red-50 border border-red-200 text-red-700 px-4 py-3 text-sm font-medium">
            ⚠️ Cannot reach the FastAPI backend at <code className="font-mono">{API}</code>. 
            Run: <code className="font-mono bg-red-100 px-1 rounded">uvicorn apps.api.main:app --port 8000</code>
          </div>
        )}

        {/* Stat row */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
          <Stat label="Headline APIx" value={headline ? headline.headline_apix.toFixed(2) : '—'} sub="Base period = 100.00" color="teal" />
          <Stat label="1-Day Change" value={pct1 != null ? `${pct1 > 0 ? '+' : ''}${pct1.toFixed(2)}%` : '—'} sub="vs previous day" color={pct1 == null ? 'blue' : pct1 > 0 ? 'red' : 'green'} />
          <Stat label="7-Day Change" value={pct7 != null ? `${pct7 > 0 ? '+' : ''}${pct7.toFixed(2)}%` : '—'} sub="rolling week" color={pct7 == null ? 'blue' : pct7 > 0 ? 'amber' : 'green'} />
          <Stat label="Coverage" value={headline ? `${(headline.coverage_ratio * 100).toFixed(1)}%` : '—'} sub={`Status: ${headline?.quality_status ?? '—'}`} color="blue" />
        </div>

        {/* Trend */}
        <Card title="📈 30-Day Headline APIx Trend">
          {daily?.series?.length ? (
            <>
              <ResponsiveContainer width="100%" height={260}>
                <LineChart data={daily.series} margin={{ top: 8, right: 16, left: 0, bottom: 0 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
                  <XAxis dataKey="index_date" tickFormatter={(v: string) => v.slice(5)} tick={{ fontSize: 11 }} />
                  <YAxis domain={['auto', 'auto']} tick={{ fontSize: 11 }} />
                  <Tooltip formatter={(v: number) => [v.toFixed(2), 'APIx']} labelFormatter={(l: string) => `Date: ${l}`} />
                  <ReferenceLine y={100} stroke="#94a3b8" strokeDasharray="4 2" label={{ value: 'Base 100', fontSize: 10 }} />
                  <Line type="monotone" dataKey="headline_apix" stroke="#0d9488" strokeWidth={2.5} dot={false} name="Headline APIx" />
                </LineChart>
              </ResponsiveContainer>
              <p className="text-xs text-slate-400 mt-2">
                Daily arithmetic median across 80 route-horizon cells (16 routes × 5 horizons). Base = 100.00.
              </p>
            </>
          ) : <p className="text-sm text-slate-400">{loading ? 'Loading…' : 'No trend data.'}</p>}
        </Card>

        {/* Heatmap */}
        <Card title="🗺 Route × Date Heatmap (14 days)">
          <HeatmapTable matrix={heatmap?.matrix ?? []} />
        </Card>

        {/* Lead-time */}
        <Card title="⏱ Booking Horizon Elasticity (T+1 → T+45)">
          {leadTime?.series?.length ? (
            <>
              <ResponsiveContainer width="100%" height={230}>
                <BarChart data={leadTime.series} margin={{ top: 8, right: 16, left: 0, bottom: 0 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
                  <XAxis dataKey="horizon" tick={{ fontSize: 12 }} />
                  <YAxis tick={{ fontSize: 11 }} tickFormatter={(v: number) => `₹${(v / 1000).toFixed(1)}k`} />
                  <Tooltip formatter={(v: number) => [`₹${(v as number).toFixed(0)}`, 'Avg Fare']} />
                  <Bar dataKey="average_fare" fill="#1e3a5f" radius={[4, 4, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
              <p className="text-xs text-slate-400 mt-2">
                Last-minute (T+1) fares average 65% higher than advance bookings (T+45) — dynamic yield management in action.
              </p>
            </>
          ) : <p className="text-sm text-slate-400">{loading ? 'Loading…' : 'No lead-time data.'}</p>}
        </Card>

        {/* Routes + Quality */}
        <div className="grid md:grid-cols-2 gap-5">
          <Card title="🛫 Basket Routes (DGCA-Weighted)">
            {routes?.routes ? (
              <table className="w-full text-xs">
                <thead>
                  <tr className="bg-slate-50 text-slate-500 uppercase text-left">
                    <th className="px-2 py-1.5">Route</th>
                    <th className="px-2 py-1.5">Org → Dst</th>
                    <th className="px-2 py-1.5 text-right">Weight</th>
                  </tr>
                </thead>
                <tbody>
                  {routes.routes.map((rt: any) => (
                    <tr key={rt.route_code} className="border-t hover:bg-teal-50 transition-colors">
                      <td className="px-2 py-1.5 font-mono font-semibold text-teal-700">{rt.route_code}</td>
                      <td className="px-2 py-1.5 text-slate-600">{rt.origin} → {rt.destination}</td>
                      <td className="px-2 py-1.5 text-right text-slate-500">{(rt.weight * 100).toFixed(1)}%</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            ) : <p className="text-sm text-slate-400">{loading ? 'Loading…' : 'No route data.'}</p>}
          </Card>

          <Card title="🔍 Data Quality Summary">
            {quality ? (
              <div className="space-y-2.5 text-sm">
                {[
                  ['Quality Status', <Badge key="qs" label={quality.quality_status} ok={quality.quality_status === 'pass'} />],
                  ['Quality Score', <span key="sc" className="font-semibold text-teal-700">{(quality.quality_score * 100).toFixed(1)}%</span>],
                  ['Coverage Ratio', <span key="cr" className="font-semibold text-blue-700">{(quality.coverage_ratio * 100).toFixed(1)}%</span>],
                  ['Total Quotes Processed', <span key="tq" className="font-semibold">{quality.total_quotes_processed?.toLocaleString()}</span>],
                  ['Valid Quote Rate', <span key="vq" className="font-semibold text-green-700">{(quality.valid_quotes_rate * 100).toFixed(1)}%</span>],
                  ['Imputed Observations', <span key="io" className="font-semibold text-amber-700">{quality.imputed_observations_count}</span>],
                  ['Source Mode', <code key="sm" className="text-xs bg-slate-100 px-2 py-0.5 rounded font-mono">{quality.source_mode}</code>],
                ].map(([label, val]) => (
                  <div key={label as string} className="flex justify-between items-center border-b pb-2">
                    <span className="text-slate-500">{label}</span>
                    {val}
                  </div>
                ))}
              </div>
            ) : <p className="text-sm text-slate-400">{loading ? 'Loading…' : 'No quality data.'}</p>}
          </Card>
        </div>

        {/* Methodology */}
        <Card title="📋 IMF CPI Manual Compliant Methodology">
          <div className="grid sm:grid-cols-3 gap-4 text-sm">
            <div className="bg-slate-50 rounded-lg p-3">
              <p className="font-semibold text-slate-700 mb-1">Elementary Aggregation</p>
              <p className="text-slate-500 text-xs">Route-horizon median of valid canonical mandatory total fares. Resilient to 200–400% intraday surge outliers.</p>
            </div>
            <div className="bg-slate-50 rounded-lg p-3">
              <p className="font-semibold text-slate-700 mb-1">Index Formula</p>
              <p className="text-slate-500 text-xs font-mono leading-relaxed">
                RouteIndex = 100 × Σ v(h)·[P(r,h,t)/P(r,h,0)]<br />
                APIx = Σ w(r)·RouteIndex(r,t)
              </p>
            </div>
            <div className="bg-slate-50 rounded-lg p-3">
              <p className="font-semibold text-slate-700 mb-1">Missing Data Policy</p>
              <p className="text-slate-500 text-xs">Carry forward ≤ 2 days (flagged). Beyond 2 days: exclude cell, re-normalise weights. Below 70%: mark 'degraded'.</p>
            </div>
          </div>
        </Card>

        <footer className="text-center text-xs text-slate-400 py-4">
          Aero-Metrics APIx · SIH 2026 PS-56 · MoSPI / NSO &amp; RBI Supplementary Index · Source: <span className="font-mono">replay_fixture</span> · v0.1.0
        </footer>
      </main>
    </div>
  )
}
