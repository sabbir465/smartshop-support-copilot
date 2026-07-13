import type { FormEvent } from "react";
import type { ChatMessage } from "../types/models";

interface ChatPanelProps {
  messages: ChatMessage[];
  input: string;
  isLoading: boolean;
  onInputChange: (value: string) => void;
  onSend: () => void;
}

function ChatPanel({
  messages,
  input,
  isLoading,
  onInputChange,
  onSend,
}: ChatPanelProps) {
  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    onSend();
  }

  return (
    <section className="flex min-h-[620px] flex-col rounded-3xl border border-slate-200 bg-white shadow-sm">
      <div className="border-b border-slate-200 px-6 py-5">
        <p className="text-sm font-semibold text-slate-900">
          Customer chat
        </p>

        <p className="mt-1 text-sm text-slate-500">
          Refund assistance powered by policy-grounded tools
        </p>
      </div>

      <div className="flex-1 space-y-5 overflow-y-auto p-6">
        {messages.map((message) => {
          const isCustomer = message.role === "customer";

          return (
            <div
              key={message.id}
              className={`flex ${
                isCustomer ? "justify-end" : "justify-start"
              }`}
            >
              <div
                className={`max-w-[82%] rounded-2xl px-5 py-4 text-sm leading-6 ${
                  isCustomer
                    ? "rounded-br-md bg-blue-600 text-white"
                    : "rounded-bl-md bg-slate-100 text-slate-700"
                }`}
              >
                <p className="mb-1 text-xs font-semibold opacity-75">
                  {isCustomer ? "Customer" : "SmartShop AI"}
                </p>

                <p>{message.content}</p>
              </div>
            </div>
          );
        })}

        {isLoading && (
          <div className="flex justify-start">
            <div className="rounded-2xl rounded-bl-md bg-slate-100 px-5 py-4">
              <p className="text-xs font-semibold text-slate-500">
                SmartShop AI
              </p>

              <p className="mt-1 text-sm text-slate-600">
                Reviewing customer, order, and policy information...
              </p>
            </div>
          </div>
        )}
      </div>

      <form
        onSubmit={handleSubmit}
        className="border-t border-slate-200 p-5"
      >
        <div className="flex gap-3">
          <input
            type="text"
            value={input}
            onChange={(event) => onInputChange(event.target.value)}
            placeholder="Describe your refund request..."
            disabled={isLoading}
            className="min-w-0 flex-1 rounded-xl border border-slate-300 px-4 py-3 text-sm outline-none transition focus:border-blue-500 focus:ring-4 focus:ring-blue-100 disabled:cursor-not-allowed disabled:bg-slate-100"
          />

          <button
            type="submit"
            disabled={isLoading || !input.trim()}
            className="rounded-xl bg-blue-600 px-6 py-3 text-sm font-semibold text-white transition hover:bg-blue-700 disabled:cursor-not-allowed disabled:bg-slate-400"
          >
            {isLoading ? "Reviewing..." : "Send"}
          </button>
        </div>
      </form>
    </section>
  );
}

export default ChatPanel;