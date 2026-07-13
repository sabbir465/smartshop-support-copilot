export type Decision =
  | "approve"
  | "deny"
  | "store_credit"
  | "manual_review"
  | null;

export interface ChatMessage {
  id: number;
  role: "customer" | "assistant";
  content: string;
}

export interface ReasoningLog {
  id: number;
  title: string;
  detail: string;
  status: "complete" | "active" | "pending";
}

export interface BackendLog {
  step: string;
  detail: string;
}

export interface ChatResponse {
  answer: string;
  decision: Decision;
  logs: BackendLog[];
}