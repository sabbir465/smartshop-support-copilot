import type { Decision } from "../types/models";

interface DecisionCardProps {
  decision: Decision;
  isLoading: boolean;
}

function DecisionCard({
  decision,
  isLoading,
}: DecisionCardProps) {
  if (isLoading) {
    return (
      <section className="overflow-hidden rounded-3xl border border-blue-200 bg-gradient-to-r from-blue-50 to-indigo-50 shadow-sm">
        <div className="flex flex-col gap-5 px-7 py-6 sm:flex-row sm:items-center sm:justify-between">
          <div>
            <p className="text-xs font-semibold uppercase tracking-[0.18em] text-blue-700">
              Final decision
            </p>

            <div className="mt-2 flex items-center gap-3">
              <span className="flex h-10 w-10 items-center justify-center rounded-full bg-blue-100">
                <span className="h-4 w-4 animate-spin rounded-full border-2 border-blue-600 border-t-transparent" />
              </span>

              <div>
                <h3 className="text-2xl font-bold text-blue-950">
                  Evaluation in progress
                </h3>

                <p className="mt-1 text-sm text-blue-800">
                  The agent is validating customer, order, and policy
                  information.
                </p>
              </div>
            </div>
          </div>

          <div className="rounded-2xl border border-blue-200 bg-white/70 px-5 py-4">
            <div className="space-y-2 text-sm text-slate-700">
              <p>✓ Identifying customer</p>
              <p>✓ Retrieving order details</p>
              <p>✓ Applying refund policy</p>
            </div>
          </div>
        </div>
      </section>
    );
  }

  if (!decision) {
    return (
      <section className="rounded-3xl border border-slate-200 bg-white px-7 py-6 shadow-sm">
        <p className="text-xs font-semibold uppercase tracking-[0.18em] text-slate-500">
          Final decision
        </p>

        <div className="mt-2 flex items-center gap-3">
          <span className="flex h-10 w-10 items-center justify-center rounded-full bg-slate-100 text-lg">
            ◷
          </span>

          <div>
            <h3 className="text-xl font-bold text-slate-900">
              Waiting for customer request
            </h3>

            <p className="mt-1 text-sm text-slate-500">
              Submit a refund request to begin policy evaluation.
            </p>
          </div>
        </div>
      </section>
    );
  }

  const decisionConfig = {
    approve: {
      title: "Approved",
      description:
        "The order satisfies all refund-policy requirements.",
      badge: "Policy validated",
      icon: "✓",
      containerClass:
        "border-emerald-200 bg-gradient-to-r from-emerald-50 to-green-50",
      iconClass: "bg-emerald-100 text-emerald-700",
      labelClass: "text-emerald-700",
      titleClass: "text-emerald-900",
      badgeClass:
        "border-emerald-200 bg-white/70 text-emerald-700",
    },
    deny: {
      title: "Denied",
      description:
        "The refund request violates a strict policy rule.",
      badge: "Policy enforced",
      icon: "×",
      containerClass:
        "border-red-200 bg-gradient-to-r from-red-50 to-rose-50",
      iconClass: "bg-red-100 text-red-700",
      labelClass: "text-red-700",
      titleClass: "text-red-900",
      badgeClass: "border-red-200 bg-white/70 text-red-700",
    },
    store_credit: {
      title: "Store credit",
      description:
        "The request qualifies for store credit rather than a cash refund.",
      badge: "Alternative resolution",
      icon: "↗",
      containerClass:
        "border-blue-200 bg-gradient-to-r from-blue-50 to-cyan-50",
      iconClass: "bg-blue-100 text-blue-700",
      labelClass: "text-blue-700",
      titleClass: "text-blue-900",
      badgeClass:
        "border-blue-200 bg-white/70 text-blue-700",
    },
    manual_review: {
      title: "Manual review",
      description:
        "A support specialist must review this request before proceeding.",
      badge: "Escalated",
      icon: "!",
      containerClass:
        "border-amber-200 bg-gradient-to-r from-amber-50 to-yellow-50",
      iconClass: "bg-amber-100 text-amber-700",
      labelClass: "text-amber-700",
      titleClass: "text-amber-900",
      badgeClass:
        "border-amber-200 bg-white/70 text-amber-700",
    },
  };

  const config = decisionConfig[decision];

  return (
    <section
      className={`overflow-hidden rounded-3xl border shadow-sm ${config.containerClass}`}
    >
      <div className="flex flex-col gap-5 px-7 py-6 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <p
            className={`text-xs font-semibold uppercase tracking-[0.18em] ${config.labelClass}`}
          >
            Final decision
          </p>

          <div className="mt-2 flex items-center gap-3">
            <span
              className={`flex h-11 w-11 items-center justify-center rounded-full text-xl font-bold ${config.iconClass}`}
            >
              {config.icon}
            </span>

            <div>
              <h3
                className={`text-2xl font-bold ${config.titleClass}`}
              >
                {config.title}
              </h3>

              <p className="mt-1 text-sm text-slate-600">
                {config.description}
              </p>
            </div>
          </div>
        </div>

        <span
          className={`w-fit rounded-full border px-4 py-2 text-xs font-semibold ${config.badgeClass}`}
        >
          {config.badge}
        </span>
      </div>
    </section>
  );
}

export default DecisionCard;