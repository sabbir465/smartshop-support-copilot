import type { ReasoningLog } from "../types/models";

interface ReasoningPanelProps {
  logs: ReasoningLog[];
}

function ReasoningPanel({ logs }: ReasoningPanelProps) {
  return (
    <section className="min-h-[620px] rounded-3xl border border-slate-200 bg-slate-950 text-white shadow-sm">
      <div className="border-b border-slate-800 px-6 py-5">
        <p className="text-sm font-semibold">Agent execution timeline</p>

        <p className="mt-1 text-sm text-slate-400">
          Auditable tool calls and policy decisions
        </p>
      </div>

      <div className="space-y-0 p-6">
        {logs.map((log, index) => {
          const isLast = index === logs.length - 1;

          return (
            <div key={log.id} className="relative flex gap-4">
              {!isLast && (
                <div className="absolute left-[11px] top-7 h-full w-px bg-slate-700" />
              )}

              <div
                className={`relative z-10 mt-1 h-6 w-6 shrink-0 rounded-full border-4 border-slate-950 ${
                  log.status === "complete"
                    ? "bg-emerald-400"
                    : log.status === "active"
                      ? "bg-blue-400"
                      : "bg-slate-600"
                }`}
              />

              <div className="pb-8">
                <p className="font-semibold text-slate-100">{log.title}</p>

                <p className="mt-2 text-sm leading-6 text-slate-400">
                  {log.detail}
                </p>

                <span
                  className={`mt-3 inline-flex rounded-full px-3 py-1 text-xs font-medium ${
                    log.status === "complete"
                      ? "bg-emerald-400/10 text-emerald-300"
                      : log.status === "active"
                        ? "bg-blue-400/10 text-blue-300"
                        : "bg-slate-700 text-slate-400"
                  }`}
                >
                  {log.status}
                </span>
              </div>
            </div>
          );
        })}
      </div>
    </section>
  );
}

export default ReasoningPanel;