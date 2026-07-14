import { useEffect, useRef, useState } from "react";

function normalizeVoiceTranscript(transcript: string): string {
  return transcript
    .replace(/\bat the rate of\b/gi, "@")
    .replace(/\bat sign\b/gi, "@")
    .replace(/\bat\b/gi, "@")
    .replace(/\bdot com\b/gi, ".com")
    .replace(/\bdot net\b/gi, ".net")
    .replace(/\bdot org\b/gi, ".org")
    .replace(/\bdot\b/gi, ".")
    .replace(/\bunderscore\b/gi, "_")
    .replace(/\bdash\b/gi, "-")
    .replace(/\s*@\s*/g, "@")
    .replace(/\s*\.\s*/g, ".")
    .replace(/\border\s+0(?=\d{4}\b)/gi, "order O")
    .replace(/\b0(?=\d{4}\b)/g, "O")
    .replace(/\s+/g, " ")
    .trim();
}

interface UseSpeechRecognitionOptions {
  onTranscript: (transcript: string) => void;
  onError?: (message: string) => void;
}

interface UseSpeechRecognitionResult {
  isSupported: boolean;
  isListening: boolean;
  startListening: () => void;
  stopListening: () => void;
}

export function useSpeechRecognition({
  onTranscript,
  onError,
}: UseSpeechRecognitionOptions): UseSpeechRecognitionResult {
  const recognitionRef = useRef<SpeechRecognition | null>(null);
  const [isListening, setIsListening] = useState(false);

  const RecognitionConstructor =
    window.SpeechRecognition ?? window.webkitSpeechRecognition;

  const isSupported = Boolean(RecognitionConstructor);

  useEffect(() => {
    if (!RecognitionConstructor) {
      return;
    }

    const recognition = new RecognitionConstructor();

    recognition.lang = "en-US";
    recognition.continuous = false;
    recognition.interimResults = true;

    recognition.onstart = () => {
      setIsListening(true);
    };

    recognition.onend = () => {
      setIsListening(false);
    };

    recognition.onerror = (event) => {
      setIsListening(false);

      const message =
        event.error === "not-allowed"
          ? "Microphone permission was denied."
          : `Speech recognition failed: ${event.error}`;

      onError?.(message);
    };

    recognition.onresult = (event) => {
      let transcript = "";

      for (let index = 0; index < event.results.length; index += 1) {
        transcript += event.results[index][0].transcript;
      }

      onTranscript(normalizeVoiceTranscript(transcript));
    };

    recognitionRef.current = recognition;

    return () => {
      recognition.abort();
      recognitionRef.current = null;
    };
  }, [RecognitionConstructor, onError, onTranscript]);

  function startListening() {
    if (!recognitionRef.current || isListening) {
      return;
    }

    recognitionRef.current.start();
  }

  function stopListening() {
    recognitionRef.current?.stop();
  }

  return {
    isSupported,
    isListening,
    startListening,
    stopListening,
  };
}