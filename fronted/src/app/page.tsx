"use client"
import { useState } from "react"
import UrlInput from "../../components/UrlInput"
import BusinessMap from "../../components/BusinessMap"
import AgentCard from "../../components/AgentCard"

export default function Home() {
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<any>(null)
  const [error, setError] = useState<string | null>(null)
  const [tab, setTab] = useState<"map" | "card">("map")

  const analyze = async (url: string) => {
    setLoading(true); setError(null); setResult(null)
    try {
      const res = await fetch("http://localhost:8000/analyze", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url })
      })
      const data = await res.json()
      if (!res.ok) throw new Error(data.error)
      setResult(data)
    } catch (e: any) {
      setError(e.message)
    }
    setLoading(false)
  }

  return (
    <main className="max-w-3xl mx-auto px-4 py-10">
      <h1 className="text-2xl font-semibold mb-1">Business Agent Card Generator</h1>
      <p className="text-gray-500 mb-6 text-sm">
        Enter any public business URL. We'll scan it and generate an AI-readable agent card.
      </p>

      <UrlInput onAnalyze={analyze} loading={loading} />

      {error && <p className="text-red-500 mt-4 text-sm">{error}</p>}

      {result && (
        <div className="mt-8">
          <p className="text-sm text-gray-500 mb-4">
            Scraped <strong>{result.pages_scraped}</strong> pages from{" "}
            <code className="bg-gray-100 px-1 rounded text-xs">{result.url}</code>
          </p>

          <div className="flex gap-2 mb-4">
            {(["map", "card"] as const).map(t => (
              <button key={t} onClick={() => setTab(t)}
                className={`px-4 py-2 rounded-lg text-sm font-medium border transition-colors
                  ${tab === t ? "bg-indigo-600 text-white border-indigo-600" : "bg-white text-gray-600 border-gray-300 hover:border-gray-400"}`}>
                {t === "map" ? "Business Map" : "Agent Card"}
              </button>
            ))}
          </div>

          {tab === "map" && <BusinessMap data={result.business_map} allUrls={result.all_discovered_urls ?? []} />}
          {tab === "card" && <AgentCard data={result.agent_card} />}
        </div>
      )}
    </main>
  )
}