'use client'
import { ReactNode } from 'react'
import { clsx } from 'clsx'

interface StatCardProps {
  label: string
  value: string | number
  sub?: string
  color?: 'teal' | 'blue' | 'amber' | 'green' | 'red'
  icon?: ReactNode
}

const colorMap = {
  teal:  'border-teal-500  bg-teal-50   text-teal-700',
  blue:  'border-blue-600  bg-blue-50   text-blue-800',
  amber: 'border-amber-500 bg-amber-50  text-amber-700',
  green: 'border-green-500 bg-green-50  text-green-700',
  red:   'border-red-500   bg-red-50    text-red-700',
}

export default function StatCard({ label, value, sub, color = 'teal', icon }: StatCardProps) {
  return (
    <div className={clsx('rounded-xl border-l-4 p-4 shadow-sm', colorMap[color])}>
      <div className="flex items-center justify-between">
        <p className="text-xs font-semibold uppercase tracking-wide opacity-70">{label}</p>
        {icon && <span className="opacity-60">{icon}</span>}
      </div>
      <p className="mt-1 text-2xl font-bold">{value}</p>
      {sub && <p className="mt-0.5 text-xs opacity-70">{sub}</p>}
    </div>
  )
}

