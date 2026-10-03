'use client'
import {
  LineChart, Line, BarChart, Bar,
  XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend, ReferenceLine
} from 'recharts'

interface SeriesPoint { index_date: string; headline_apix: number }

export function HeadlineTrendChart({ data }: { data: SeriesPoint[] }) {
  return (
    <ResponsiveContainer width="100%" height={280}>
      <LineChart data={data} margin={{ top: 8, right: 20, left: 0, bottom: 0 }}>
        <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
        <XAxis
          dataKey="index_date"
          tickFormatter={(v: string) => v.slice(5)}
          tick={{ fontSize: 11 }}
        />
        <YAxis domain={['auto', 'auto']} tick={{ fontSize: 11 }} />
        <Tooltip
          formatter={(v: number) => [v.toFixed(2), 'APIx']}
          labelFormatter={(l: string) => `Date: ${l}`}
        />
        <ReferenceLine y={100} stroke="#94a3b8" strokeDasharray="4 2" label={{ value: 'Base 100', fontSize: 10 }} />
        <Line
          type="monotone" dataKey="headline_apix"
          stroke="#0d9488" strokeWidth={2.5} dot={false}
          name="Headline APIx"
        />
      </LineChart>
    </ResponsiveContainer>
  )
}

interface LeadPoint { horizon: string; average_fare: number }

export function LeadTimeCurveChart({ data }: { data: LeadPoint[] }) {
  return (
    <ResponsiveContainer width="100%" height={240}>
      <BarChart data={data} margin={{ top: 8, right: 20, left: 0, bottom: 0 }}>
        <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
        <XAxis dataKey="horizon" tick={{ fontSize: 12 }} />
        <YAxis tick={{ fontSize: 11 }} tickFormatter={(v: number) => `₹${(v / 1000).toFixed(1)}k`} />
        <Tooltip formatter={(v: number) => [`₹${v.toFixed(0)}`, 'Avg Fare']} />
        <Bar dataKey="average_fare" fill="#1e3a5f" radius={[4, 4, 0, 0]} name="Avg Median Fare" />
      </BarChart>
    </ResponsiveContainer>
  )
}

interface RoutePoint { index_date: string; index_value: number }

export function RouteIndexChart({ data, routeCode }: { data: RoutePoint[]; routeCode: string }) {
  return (
    <ResponsiveContainer width="100%" height={200}>
      <LineChart data={data}>
        <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
        <XAxis dataKey="index_date" tickFormatter={(v: string) => v.slice(5)} tick={{ fontSize: 10 }} />
        <YAxis domain={['auto', 'auto']} tick={{ fontSize: 10 }} />
        <Tooltip formatter={(v: number) => [v.toFixed(2), routeCode]} />
        <Line type="monotone" dataKey="index_value" stroke="#f59e0b" strokeWidth={2} dot={false} />
      </LineChart>
    </ResponsiveContainer>
  )
}

