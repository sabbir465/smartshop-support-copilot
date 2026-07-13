function Header() {
  return (
    <header className="border-b border-slate-200 bg-white">
      <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-5">
        <div>
          <p className="text-xs font-semibold uppercase tracking-[0.22em] text-blue-600">
            SmartShop
          </p>

          <h1 className="mt-1 text-2xl font-bold text-slate-900">
            Support Copilot
          </h1>
        </div>

        <div className="flex items-center gap-2 rounded-full border border-emerald-200 bg-emerald-50 px-4 py-2">
          <span className="h-2.5 w-2.5 rounded-full bg-emerald-500" />

          <span className="text-sm font-medium text-emerald-700">
            Agent online
          </span>
        </div>
      </div>
    </header>
  );
}

export default Header;