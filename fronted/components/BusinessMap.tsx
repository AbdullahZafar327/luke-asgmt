type EvidenceValue = string | string[] | Record<string, string>

function toStringEvidence(evidence: EvidenceValue): string {
  if (!evidence) return ""
  if (Array.isArray(evidence)) return evidence.filter(Boolean).join(", ")
  if (typeof evidence === "object") return Object.values(evidence).filter(Boolean).join(", ")
  return String(evidence)
}

function Badge({ children, variant = "default" }: { children: React.ReactNode; variant?: "default" | "warn" | "ok" }) {
  const colors = {
    default: "bg-gray-100 text-gray-600",
    warn: "bg-amber-50 text-amber-700",
    ok: "bg-green-50 text-green-700"
  }
  return (
    <span className={`inline-block text-xs px-2 py-0.5 rounded-full font-medium ${colors[variant]}`}>
      {children}
    </span>
  )
}

function Section({ title, icon, children }: { title: string; icon: string; children: React.ReactNode }) {
  return (
    <div className="border border-gray-200 rounded-xl p-4 bg-white">
      <div className="flex items-center gap-2 mb-3">
        <span className="text-base">{icon}</span>
        <h3 className="text-sm font-semibold text-gray-700">{title}</h3>
      </div>
      {children}
    </div>
  )
}

function EvidenceTag({ evidence }: { evidence: EvidenceValue }) {
  const text = toStringEvidence(evidence)
  if (!text) return null
  return (
    <p className="text-xs text-gray-400 mt-2 truncate" title={text}>
      <span className="font-medium text-gray-500">Evidence:</span> {text}
    </p>
  )
}

function Unknown() {
  return <span className="text-gray-400 italic text-sm">unknown</span>
}

export default function BusinessMap({ data, allUrls = [] }: { data: any, allUrls: string[] }) {
  if (!data) return null

  const biz = data.what_the_business_is
  const services = data.products_or_services ?? []
  const actions = data.customer_actions_possible ?? []
  const tools = data.tools_and_forms ?? []
  const contact = data.contact_info ?? {}
  const payment = data.payment_methods
  const auth = data.auth_required
  const missing = data.missing_or_unclear ?? []
  const pages = data.pages_analyzed ?? []

  return (
    <div className="flex flex-col gap-3">

      {/* What the business is */}
      <Section title="What this business is" icon="🏢">
        {biz?.value && biz.value !== "unknown"
          ? <p className="text-sm text-gray-800">{biz.value}</p>
          : <Unknown />}
        <EvidenceTag evidence={biz?.evidence} />
      </Section>

      {/* Products / Services */}
      <Section title="Products & Services" icon="📦">
        {services.length > 0 && services[0]?.name !== "unknown" ? (
          <div className="flex flex-wrap gap-2">
            {services.map((s: any, i: number) => (
              <Badge key={i} variant="ok">{s.name}</Badge>
            ))}
          </div>
        ) : <Unknown />}
        <EvidenceTag evidence={services[0]?.evidence} />
      </Section>

      {/* Customer Actions */}
      <Section title="Customer Actions" icon="⚡">
        {actions.length > 0 && actions[0]?.action !== "unknown" ? (
          <div className="flex flex-col gap-2">
            {actions.map((a: any, i: number) => (
              <div key={i} className="flex items-start gap-2">
                <Badge variant="default">{a.action}</Badge>
                {a.how && a.how !== "unknown" && (
                  <span className="text-xs text-gray-500 mt-0.5">→ {a.how}</span>
                )}
              </div>
            ))}
          </div>
        ) : <Unknown />}
      </Section>

      {/* Contact + Payment side by side */}
      <div className="grid grid-cols-2 gap-3">
        <Section title="Contact Info" icon="📞">
          <div className="flex flex-col gap-1 text-sm">
            {contact.phone && contact.phone !== "unknown" && contact.phone !== "Unknown"
              ? <span className="text-gray-700">📱 {contact.phone}</span>
              : <span className="text-gray-400 text-xs">No phone found</span>}
            {contact.email && contact.email !== "unknown" && contact.email !== "Unknown"
              ? <span className="text-gray-700">✉️ {contact.email}</span>
              : <span className="text-gray-400 text-xs">No email found</span>}
            {contact.address && contact.address !== "unknown" && contact.address !== "Unknown"
              ? <span className="text-gray-700">📍 {contact.address}</span>
              : <span className="text-gray-400 text-xs">No address found</span>}
          </div>
        </Section>

        <Section title="Payment & Auth" icon="💳">
          <div className="flex flex-col gap-1 text-sm">
            <div>
              <span className="text-xs text-gray-500">Payment: </span>
              {payment?.value && payment.value !== "unknown" && payment.value !== "Unknown"
                ? <span className="text-gray-700">{payment.value}</span>
                : <span className="text-gray-400 italic">unknown</span>}
            </div>
            <div>
              <span className="text-xs text-gray-500">Auth required: </span>
              {auth?.value && auth.value !== "unknown" && auth.value !== "Unknown"
                ? <Badge variant="warn">{auth.value}</Badge>
                : <span className="text-gray-400 italic">unknown</span>}
            </div>
          </div>
        </Section>
      </div>

      {/* Tool integrations */}
      {tools.length > 0 && tools[0]?.tool !== "unknown" && (
        <Section title="Tools & Forms Detected" icon="🔧">
          <div className="flex flex-wrap gap-2">
            {tools.map((t: any, i: number) => (
              <Badge key={i} variant="default">{t.tool}</Badge>
            ))}
          </div>
        </Section>
      )}

      {/* Missing / unclear */}
      {missing.length > 0 && (
        <Section title="Missing or Unclear" icon="⚠️">
          <div className="flex flex-wrap gap-2">
            {missing.map((m: string, i: number) => (
              <Badge key={i} variant="warn">{m}</Badge>
            ))}
          </div>
          <p className="text-xs text-gray-400 mt-2">
            These fields could not be confirmed from the website evidence.
          </p>
        </Section>
      )}

      {/* Pages analyzed */}
      <Section title="Pages Analyzed" icon="🔍">
        <div className="flex flex-col gap-1">
          {pages.map((p: string, i: number) => (
            <a key={i} href={p} target="_blank" rel="noreferrer"
              className="text-xs text-indigo-500 hover:underline truncate">{p}</a>
          ))}
        </div>
      </Section>

      <Section title="Sitemap" icon="🔍">
        {allUrls.length > 0 && (
          <>
            <div className="flex flex-col gap-1 max-h-48 overflow-y-auto pr-1">
              {allUrls.map((p, i) => (
                <a key={i} href={p} target="_blank" rel="noreferrer"
                className="text-xs font-medium text-indigo-500 hover:text-indigo-500 mb-1 hover:underline flex items-center gap-1">
                  <span className="inline-block w-1.5 h-1.5 rounded-full bg-gray-300 flex-shrink-0"/>
                  {p}
                </a>
              ))}
            </div>
          </>
        )}
      </Section>

    </div>
  )
}