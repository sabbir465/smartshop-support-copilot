import {
  useEffect,
  useRef,
  type FormEvent,
} from "react";

import type { ChatMessage } from "../types/models";

interface ChatPanelProps {
  messages: ChatMessage[];
  input: string;
  isLoading: boolean;
  isListening: boolean;
  isSpeechSupported: boolean;
  voiceError: string | null;
  onInputChange: (value: string) => void;
  onSend: () => void;
  onStartListening: () => void;
  onStopListening: () => void;
}

function ChatPanel({
  messages,
  input,
  isLoading,
  isListening,
  isSpeechSupported,
  voiceError,
  onInputChange,
  onSend,
  onStartListening,
  onStopListening,
}: ChatPanelProps) {
  const messagesEndRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({
      behavior: "smooth",
    });
  }, [messages, isLoading, isListening]);
  
  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    onSend();
  }

  function handleMicrophoneClick() {
    if (isListening) {
      onStopListening();
    } else {
      onStartListening();
    }
  }

  return (
    <section className="flex min-h-[620px] flex-col rounded-3xl border border-slate-200 bg-white shadow-sm">
      <div className="border-b border-slate-200 px-6 py-5">
        <div className="flex items-start justify-between gap-4">
          <div>
            <p className="text-sm font-semibold text-slate-900">
              Customer chat
            </p>

            <p className="mt-1 text-sm text-slate-500">
              Refund assistance powered by policy-grounded tools
            </p>
          </div>

          {isSpeechSupported && (
            <span className="rounded-full bg-blue-50 px-3 py-1 text-xs font-medium text-blue-700">
              Voice enabled
            </span>
          )}
        </div>
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

              <div className="mt-2 flex items-center gap-3">
                <div className="flex gap-1">
                  <span className="h-2 w-2 animate-bounce rounded-full bg-blue-500 [animation-delay:-0.3s]" />
                  <span className="h-2 w-2 animate-bounce rounded-full bg-blue-500 [animation-delay:-0.15s]" />
                  <span className="h-2 w-2 animate-bounce rounded-full bg-blue-500" />
                </div>

                <p className="text-sm text-slate-600">
                  Reviewing customer, order, and policy information...
                </p>
              </div>
            </div>
          </div>
        )}



        {isListening && (
          <div className="flex justify-center">
            <div className="flex items-center gap-3 rounded-full border border-red-200 bg-red-50 px-4 py-2 text-sm font-medium text-red-700">
              <span className="h-2.5 w-2.5 animate-pulse rounded-full bg-red-500" />
              Listening — speak your refund request
            </div>
          </div>
        )}
      <div ref={messagesEndRef} />
      </div>

      <form
        onSubmit={handleSubmit}
        className="border-t border-slate-200 p-5"
      >
        {voiceError && (
          <p className="mb-3 rounded-lg bg-red-50 px-3 py-2 text-sm text-red-700">
            {voiceError}
          </p>
        )}

        {!isSpeechSupported && (
          <p className="mb-3 rounded-lg bg-amber-50 px-3 py-2 text-sm text-amber-700">
            Voice recognition is unavailable in this browser. Use Chrome
            or enter the request manually.
          </p>
        )}

        <div className="flex gap-3">
          <input
            type="text"
            value={input}
            onChange={(event) => onInputChange(event.target.value)}
            placeholder={
              isListening
                ? "Listening..."
                : "Describe your refund request..."
            }
            disabled={isLoading}
            className="min-w-0 flex-1 rounded-xl border border-slate-300 px-4 py-3 text-sm outline-none transition focus:border-blue-500 focus:ring-4 focus:ring-blue-100 disabled:cursor-not-allowed disabled:bg-slate-100"
          />

          <button
            type="button"
            onClick={handleMicrophoneClick}
            disabled={!isSpeechSupported || isLoading}
            aria-label={
              isListening
                ? "Stop voice recording"
                : "Start voice recording"
            }
            className={`flex h-12 w-12 shrink-0 items-center justify-center rounded-xl border text-xl transition ${
              isListening
                ? "border-red-300 bg-red-100 text-red-700 hover:bg-red-200"
                : "border-slate-300 bg-white text-slate-700 hover:border-blue-400 hover:bg-blue-50"
            } disabled:cursor-not-allowed disabled:opacity-40`}
          >
            {isListening ? "■" : "🎤"}
          </button>

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