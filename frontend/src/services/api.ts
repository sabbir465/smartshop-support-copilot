import axios from "axios";
import type { ChatResponse } from "../types/models";

const api = axios.create({
  baseURL:
    import.meta.env.VITE_API_BASE_URL ?? "http://127.0.0.1:8000",
  headers: {
    "Content-Type": "application/json",
  },
  timeout: 30000,
});

export async function sendChatMessage(
  message: string,
): Promise<ChatResponse> {
  const response = await api.post<ChatResponse>("/chat", {
    message,
  });

  return response.data;
}