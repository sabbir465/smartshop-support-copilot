import type { Decision } from "../types/models";

interface DecisionCardProps {
  decision: Decision;
}

const decisionStyles = {
  approve: {
    label: "Approved",
    description: "The order satisfies all refund-policy requirements.",
    classes: "border-emerald-200 bg-emerald-50 text-emerald-800",
  },
  deny: {
    label: "Denied",
    description: "The refund request violates a strict policy rule.",
    classes: "border-red-200 bg-red-50 text-red-800",
  },
  store_credit: {
    label: "Store credit",
    description: "The item qualifies for store credit instead of a cash refund.",
    classes: "border-amber-200 bg-amber-50 text-amber-800",
  },
  manual_review: {
    label: "Manual review",
    description: "A human support specialist must review this request.",
    classes: "border-blue-200 bg-blue-50 text-blue-800",
  },
};

function DecisionCard({ decision }: DecisionCardProps) {
  if (!decision) {
    return (
      <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
        <p className="text-sm font-semibold text-slate-500">Final decision</p>

        <p className="mt-2 text-xl font-bold text-slate-900">
          Waiting for customer request
        </p>
      </section>
    );
  }

  const config = decisionStyles[decision];

  return (
    <section
      className={`rounded-3xl border p-6 shadow-sm ${config.classes}`}
    >
      <p className="text-sm font-semibold uppercase tracking-wider">
        Final decision
      </p>

      <div className="mt-3 flex items-center justify-between gap-6">
        <div>
          <h2 className="text-3xl font-bold">{config.label}</h2>

          <p className="mt-2 text-sm opacity-80">{config.description}</p>
        </div>

        <div className="rounded-2xl bg-white/60 px-5 py-3 text-sm font-semibold">
          Policy validated
        </div>
      </div>
    </section>
  );
}

export default DecisionCard;