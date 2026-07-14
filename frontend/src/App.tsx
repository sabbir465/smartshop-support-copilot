import axios from "axios";

import ChatPanel from "./components/ChatPanel";
import DecisionCard from "./components/DecisionCard";
import Header from "./components/Header";
import ReasoningPanel from "./components/ReasoningPanel";
import { sendChatMessage } from "./services/api";

import type {
  ChatMessage,
  Decision,
  ReasoningLog,
} from "./types/models";

import { useCallback, useRef, useState } from "react";

import { useSpeechRecognition } from "./hooks/useSpeechRecognition";
import { speakText } from "./services/speech";

const initialMessages: ChatMessage[] = [
  {
    id: 1,
    role: "assistant",
    content:
      "Welcome to SmartShop Support. Please provide your email address and order ID.",
  },
];

function App() {
  const [messages, setMessages] =
    useState<ChatMessage[]>(initialMessages);

  const [logs, setLogs] = useState<ReasoningLog[]>([]);

  const [decision, setDecision] =
    useState<Decision>(null);

  const [input, setInput] = useState("");

  const [isLoading, setIsLoading] = useState(false);

  const [voiceError, setVoiceError] = useState<string | null>(null);
  const voiceRequestRef = useRef(false);

  const handleVoiceTranscript = useCallback((transcript: string) => {
    setInput(transcript);
    setVoiceError(null);
    voiceRequestRef.current = true;
  }, []);

  const handleVoiceError = useCallback((message: string) => {
    setVoiceError(message);
    voiceRequestRef.current = false;
  }, []);

  const {
    isSupported: isSpeechSupported,
    isListening,
    startListening,
    stopListening,
  } = useSpeechRecognition({
    onTranscript: handleVoiceTranscript,
    onError: handleVoiceError,
  });

  async function handleSend() {
    const trimmedInput = input.trim();

    if (!trimmedInput || isLoading) {
      return;
    }

    const customerMessage: ChatMessage = {
      id: Date.now(),
      role: "customer",
      content: trimmedInput,
    };

    setMessages((currentMessages) => [
      ...currentMessages,
      customerMessage,
    ]);

    setInput("");
    setDecision(null);
    setIsLoading(true);

    setLogs([
      {
        id: 1,
        title: "Request received",
        detail:
          "The agent is reviewing the customer message and selecting the required tools.",
        status: "active",
      },
    ]);

    try {
      const response = await sendChatMessage(trimmedInput);
      
      if (voiceRequestRef.current) {
        speakText(response.answer);
      }

      const assistantMessage: ChatMessage = {
        id: Date.now() + 1,
        role: "assistant",
        content: response.answer,
      };

      const transformedLogs: ReasoningLog[] =
        response.logs.map((log, index) => ({
          id: index + 1,
          title: log.step,
          detail: log.detail,
          status: "complete",
        }));

      setMessages((currentMessages) => [
        ...currentMessages,
        assistantMessage,
      ]);

      setLogs(transformedLogs);
      setDecision(response.decision);
    } catch (error) {
      let errorMessage =
        "The support service is temporarily unavailable. Please try again.";

      if (axios.isAxiosError(error)) {
        errorMessage =
          error.response?.data?.detail ??
          error.message ??
          errorMessage;
      }

      setMessages((currentMessages) => [
        ...currentMessages,
        {
          id: Date.now() + 1,
          role: "assistant",
          content: errorMessage,
        },
      ]);

      setLogs([
        {
          id: 1,
          title: "Request failed",
          detail:
            "The frontend could not complete the request to the agent backend.",
          status: "complete",
        },
      ]);

      setDecision(null);
    } finally {
      voiceRequestRef.current = false;
      setIsLoading(false);
    }
  }

  return (
    <div className="min-h-screen bg-slate-100">
      <Header />

      <main className="mx-auto max-w-7xl px-6 py-8">
        <div className="mb-8">
          <p className="text-sm font-semibold uppercase tracking-[0.2em] text-blue-600">
            Policy-grounded refund automation
          </p>

          <h2 className="mt-2 max-w-3xl text-4xl font-bold tracking-tight text-slate-900">
            Transparent AI decisions for e-commerce customer support
          </h2>

          <p className="mt-4 max-w-3xl text-base leading-7 text-slate-600">
            The customer-facing assistant handles refund requests while
            the supervisor dashboard displays tool execution and policy
            validation.
          </p>
        </div>

        <div className="grid gap-6 lg:grid-cols-[1.05fr_0.95fr]">
          <ChatPanel
            messages={messages}
            input={input}
            isLoading={isLoading}
            isListening={isListening}
            isSpeechSupported={isSpeechSupported}
            voiceError={voiceError}
            onInputChange={setInput}
            onSend={handleSend}
            onStartListening={startListening}
            onStopListening={stopListening}
          />

          <ReasoningPanel logs={logs} />
        </div>

        <div className="mt-6">
          <DecisionCard decision={decision} />
        </div>
      </main>
    </div>
  );
}

export default App;