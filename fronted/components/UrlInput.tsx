"use client"
import { useState } from "react"

export default function UrlInput({ onAnalyze, loading }: { onAnalyze: (url: string) => void, loading: boolean }) {
  const [url, setUrl] = useState("")
  return (
    <div className="flex gap-2">
      <input value={url} onChange={e => setUrl(e.target.value)}
        onKeyDown={e => e.key === "Enter" && url && onAnalyze(url)}
        placeholder="https://mario-pizza.com"
        className="flex-1 border border-gray-300 rounded-lg px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"/>
      <button onClick={() => onAnalyze(url)} disabled={loading || !url}
        className="bg-indigo-600 hover:bg-indigo-700 disabled:opacity-50 text-white px-5 py-2.5 rounded-lg text-sm font-medium transition-colors">
        {loading ? "Analyzing…" : "Analyze"}
      </button>
    </div>
  )
}