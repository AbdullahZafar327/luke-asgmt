export default function AgentCard({ data }: { data: any }) {
  return (
    <pre className="bg-gray-950 text-green-300 text-xs p-5 rounded-xl overflow-auto leading-relaxed">
      {JSON.stringify(data, null, 2)}
    </pre>
  )
}