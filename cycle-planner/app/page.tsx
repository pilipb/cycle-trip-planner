"use client";

import { useState, useRef, useEffect } from "react";
import dynamic from "next/dynamic";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { sendChatMessageStream, sendChatAnswer } from "@/lib/api";
import type { RouteGeoJSON } from "@/lib/api";

const RouteMap = dynamic(() => import("@/components/RouteMap"), { ssr: false });

type PendingQuestion = {
  tool_call_id: string;
  question: string;
  options: string[];
};

type Message = {
  role: "user" | "assistant";
  content: string;
  thinking?: string;
  route_geojson?: RouteGeoJSON | null;
  pending_question?: PendingQuestion;
};

function generateSessionId(): string {
  return crypto.randomUUID();
}

function QuestionAnswerUI({
  pendingQuestion,
  onAnswer,
  disabled,
}: {
  pendingQuestion: PendingQuestion;
  onAnswer: (toolCallId: string, value: string) => void;
  disabled: boolean;
}) {
  const [freeText, setFreeText] = useState("");
  const hasOptions = pendingQuestion.options.length > 0;

  if (hasOptions) {
    return (
      <div className="mt-3 space-y-2">
        <p className="text-sm font-medium text-zinc-700 dark:text-zinc-300">
          {pendingQuestion.question}
        </p>
        <div className="flex flex-wrap gap-2">
          {pendingQuestion.options.map((opt) => (
            <button
              key={opt}
              type="button"
              disabled={disabled}
              onClick={() => onAnswer(pendingQuestion.tool_call_id, opt)}
              className="rounded-lg border border-zinc-300 bg-white px-3 py-2 text-sm font-medium text-zinc-700 transition hover:bg-zinc-50 disabled:opacity-50 dark:border-zinc-600 dark:bg-zinc-800 dark:text-zinc-300 dark:hover:bg-zinc-700"
            >
              {opt}
            </button>
          ))}
        </div>
      </div>
    );
  }

  return (
    <div className="mt-3 space-y-2">
      <p className="text-sm font-medium text-zinc-700 dark:text-zinc-300">
        {pendingQuestion.question}
      </p>
      <form
        onSubmit={(e) => {
          e.preventDefault();
          const v = freeText.trim();
          if (v && !disabled) {
            onAnswer(pendingQuestion.tool_call_id, v);
            setFreeText("");
          }
        }}
        className="flex gap-2"
      >
        <input
          type="text"
          value={freeText}
          onChange={(e) => setFreeText(e.target.value)}
          placeholder="Type your answer..."
          disabled={disabled}
          className="flex-1 rounded-lg border border-zinc-300 bg-white px-3 py-2 text-sm text-zinc-900 placeholder-zinc-500 focus:border-zinc-500 focus:outline-none focus:ring-1 focus:ring-zinc-500 disabled:opacity-50 dark:border-zinc-600 dark:bg-zinc-800 dark:text-zinc-100 dark:placeholder-zinc-400"
        />
        <button
          type="submit"
          disabled={disabled || !freeText.trim()}
          className="rounded-lg bg-zinc-900 px-4 py-2 text-sm font-medium text-white transition hover:bg-zinc-800 disabled:opacity-50 dark:bg-zinc-100 dark:text-zinc-900 dark:hover:bg-zinc-200"
        >
          Submit
        </button>
      </form>
    </div>
  );
}

export default function Home() {
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [streamingMessage, setStreamingMessage] = useState<{
    thinking: string;
    content: string;
    status?: string;
  } | null>(null);
  const streamingRef = useRef({ thinking: "", content: "", status: "" });
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  useEffect(() => scrollToBottom(), [messages, streamingMessage]);

  const hasPendingQuestion = messages.some(
    (m) => m.role === "assistant" && m.pending_question
  );

  const startNewChat = () => {
    setSessionId(generateSessionId());
    setMessages([]);
    setInput("");
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const text = input.trim();
    if (!text || loading) return;

    setInput("");
    setMessages((m) => [...m, { role: "user", content: text }]);
    setLoading(true);
    streamingRef.current = { thinking: "", content: "", status: "" };
    setStreamingMessage({ thinking: "", content: "" });

    try {
      const done = await sendChatMessageStream(text, sessionId, (chunk) => {
        if (chunk.type === "thinking") {
          streamingRef.current.thinking += chunk.delta;
          setStreamingMessage((s) =>
            s ? { ...s, thinking: s.thinking + chunk.delta } : s
          );
        } else if (chunk.type === "text") {
          streamingRef.current.content += chunk.delta;
          setStreamingMessage((s) =>
            s ? { ...s, content: s.content + chunk.delta } : s
          );
        } else if (chunk.type === "status") {
          streamingRef.current.status = chunk.message;
          setStreamingMessage((s) =>
            s ? { ...s, status: chunk.message } : { thinking: "", content: "", status: chunk.message }
          );
        } else if (chunk.type === "question") {
          setMessages((m) => [
            ...m,
            {
              role: "assistant",
              content: streamingRef.current.content,
              thinking: streamingRef.current.thinking || undefined,
              pending_question: {
                tool_call_id: chunk.tool_call_id,
                question: chunk.question,
                options: chunk.options,
              },
            },
          ]);
          setStreamingMessage(null);
        }
      });
      setSessionId(done.session_id);
      if (done.waiting_for_input) {
        setLoading(false);
        setStreamingMessage(null);
      } else {
        setMessages((m) => [
          ...m,
          {
            role: "assistant",
            content: streamingRef.current.content,
            thinking: streamingRef.current.thinking || undefined,
            route_geojson: done.route_geojson ?? undefined,
          },
        ]);
        setLoading(false);
        setStreamingMessage(null);
      }
    } catch (err) {
      setMessages((m) => [
        ...m,
        {
          role: "assistant",
          content: `Error: ${err instanceof Error ? err.message : "Failed to get response"}`,
        },
      ]);
      setLoading(false);
      setStreamingMessage(null);
    }
  };

  const handleAnswerQuestion = async (
    toolCallId: string,
    value: string
  ) => {
    if (!sessionId || loading) return;
    setLoading(true);
    streamingRef.current = { thinking: "", content: "", status: "" };
    setStreamingMessage({ thinking: "", content: "" });

    try {
      const done = await sendChatAnswer(
        sessionId,
        toolCallId,
        value,
        (chunk) => {
          if (chunk.type === "thinking") {
            streamingRef.current.thinking += chunk.delta;
            setStreamingMessage((s) =>
              s ? { ...s, thinking: s.thinking + chunk.delta } : s
            );
          } else if (chunk.type === "text") {
            streamingRef.current.content += chunk.delta;
            setStreamingMessage((s) =>
              s ? { ...s, content: s.content + chunk.delta } : s
            );
          } else if (chunk.type === "status") {
            streamingRef.current.status = chunk.message;
            setStreamingMessage((s) =>
              s ? { ...s, status: chunk.message } : { thinking: "", content: "", status: chunk.message }
            );
          } else if (chunk.type === "question") {
            setMessages((m) => {
              const prev = m[m.length - 1];
              const base = prev?.role === "assistant"
                ? { ...prev, content: prev.content + streamingRef.current.content, pending_question: undefined }
                : null;
              const newMsgs = base ? [...m.slice(0, -1), base] : m;
              return [
                ...newMsgs,
                {
                  role: "assistant" as const,
                  content: "",
                  pending_question: {
                    tool_call_id: chunk.tool_call_id,
                    question: chunk.question,
                    options: chunk.options,
                  },
                },
              ];
            });
            streamingRef.current = { thinking: "", content: "" };
          }
        }
      );
      setSessionId(done.session_id);
      if (done.waiting_for_input) {
        setLoading(false);
        setStreamingMessage(null);
      } else {
        setMessages((m) => {
          const prev = m[m.length - 1];
          if (prev?.role === "assistant" && prev.pending_question) {
            return [
              ...m.slice(0, -1),
              {
                ...prev,
                content: prev.content + streamingRef.current.content,
                thinking: prev.thinking || streamingRef.current.thinking || undefined,
                route_geojson: done.route_geojson ?? prev.route_geojson,
                pending_question: undefined,
              },
            ];
          }
          return [
            ...m,
            {
              role: "assistant" as const,
              content: streamingRef.current.content,
              thinking: streamingRef.current.thinking || undefined,
              route_geojson: done.route_geojson ?? undefined,
            },
          ];
        });
        setLoading(false);
        setStreamingMessage(null);
      }
    } catch (err) {
      setMessages((m) => [
        ...m,
        {
          role: "assistant",
          content: `Error: ${err instanceof Error ? err.message : "Failed to get response"}`,
        },
      ]);
      setLoading(false);
      setStreamingMessage(null);
    }
  };

  return (
    <div className="flex h-screen flex-col bg-zinc-50 dark:bg-zinc-950">
      <header className="flex shrink-0 items-center justify-between border-b border-zinc-200 bg-white px-4 py-3 dark:border-zinc-800 dark:bg-zinc-900">
        <h1 className="text-lg font-semibold text-zinc-900 dark:text-zinc-100">
          Cycle Trip Planner
        </h1>
        <button
          onClick={startNewChat}
          className="rounded-lg border border-zinc-300 bg-white px-3 py-1.5 text-sm font-medium text-zinc-700 transition hover:bg-zinc-50 dark:border-zinc-600 dark:bg-zinc-800 dark:text-zinc-300 dark:hover:bg-zinc-700"
        >
          New chat
        </button>
      </header>

      <div className="flex-1 overflow-y-auto px-4 py-6">
        <div className="mx-auto max-w-2xl">
          {messages.length === 0 ? (
            <div className="flex flex-col items-center justify-center py-16 text-center">
              <p className="text-zinc-500 dark:text-zinc-400">
                Start a conversation to plan your cycling trip.
              </p>
              <p className="mt-2 text-sm text-zinc-400 dark:text-zinc-500">
                Ask about routes, weather, accommodation, and more.
              </p>
            </div>
          ) : (
            <div className="space-y-6">
              {messages.map((msg, i) => (
                <div
                  key={i}
                  className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}
                >
                  <div
                    className={`max-w-[85%] rounded-2xl px-4 py-2.5 ${
                      msg.role === "user"
                        ? "bg-zinc-900 text-white dark:bg-zinc-100 dark:text-zinc-900"
                        : "bg-white text-zinc-900 shadow-sm dark:bg-zinc-800 dark:text-zinc-100"
                    }`}
                  >
                    {msg.role === "user" ? (
                      <p className="whitespace-pre-wrap text-sm leading-relaxed">{msg.content}</p>
                    ) : (
                      <div className="space-y-3">
                        {msg.thinking ? (
                          <details className="group">
                            <summary className="cursor-pointer list-none text-xs text-zinc-500 dark:text-zinc-400 before:mr-1 before:inline-block before:content-['']">
                              <span className="italic">Thinking</span>
                            </summary>
                            <pre className="mt-1 whitespace-pre-wrap rounded bg-zinc-100 p-2 text-xs text-zinc-600 dark:bg-zinc-700 dark:text-zinc-300">
                              {msg.thinking}
                            </pre>
                          </details>
                        ) : null}
                        {msg.route_geojson?.features?.length ? (
                          <RouteMap geojson={msg.route_geojson} />
                        ) : null}
                        <div className="prose prose-sm dark:prose-invert max-w-none prose-p:my-1 prose-ul:my-2 prose-ol:my-2 prose-li:my-0 prose-pre:my-2 prose-pre:text-xs prose-code:bg-zinc-200 prose-code:dark:bg-zinc-700 prose-code:px-1 prose-code:rounded">
                          <ReactMarkdown remarkPlugins={[remarkGfm]}>{msg.content}</ReactMarkdown>
                        </div>
                        {msg.pending_question ? (
                          <QuestionAnswerUI
                            pendingQuestion={msg.pending_question}
                            onAnswer={handleAnswerQuestion}
                            disabled={loading}
                          />
                        ) : null}
                      </div>
                    )}
                  </div>
                </div>
              ))}
              {loading && streamingMessage && (
                <div className="flex justify-start">
                  <div className="max-w-[85%] space-y-3 rounded-2xl bg-white px-4 py-2.5 shadow-sm dark:bg-zinc-800 dark:text-zinc-100">
                    {streamingMessage.thinking ? (
                      <details open className="group">
                        <summary className="cursor-pointer list-none text-xs text-zinc-500 dark:text-zinc-400 before:mr-1 before:inline-block before:content-['']">
                          <span className="italic">Thinking...</span>
                        </summary>
                        <pre className="mt-1 max-h-40 overflow-y-auto whitespace-pre-wrap rounded bg-zinc-100 p-2 text-xs text-zinc-600 dark:bg-zinc-700 dark:text-zinc-300">
                          {streamingMessage.thinking}
                        </pre>
                      </details>
                    ) : null}
                    {streamingMessage.status ? (
                      <p className="text-xs text-zinc-500 dark:text-zinc-400 italic">
                        {streamingMessage.status}
                      </p>
                    ) : null}
                    <div className="prose prose-sm dark:prose-invert max-w-none prose-p:my-1 prose-ul:my-2 prose-ol:my-2 prose-li:my-0 prose-pre:my-2 prose-pre:text-xs prose-code:bg-zinc-200 prose-code:dark:bg-zinc-700 prose-code:px-1 prose-code:rounded">
                      <ReactMarkdown remarkPlugins={[remarkGfm]}>
                        {streamingMessage.content || "…"}
                      </ReactMarkdown>
                    </div>
                  </div>
                </div>
              )}
              <div ref={messagesEndRef} />
            </div>
          )}
        </div>
      </div>

      <form onSubmit={handleSubmit} className="shrink-0 border-t border-zinc-200 bg-white p-4 dark:border-zinc-800 dark:bg-zinc-900">
        <div className="mx-auto flex max-w-2xl gap-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder={
              hasPendingQuestion
                ? "Answer the question above first..."
                : "Ask about your cycling trip..."
            }
            disabled={loading || hasPendingQuestion}
            className="flex-1 rounded-xl border border-zinc-300 bg-zinc-50 px-4 py-3 text-zinc-900 placeholder-zinc-500 focus:border-zinc-500 focus:outline-none focus:ring-1 focus:ring-zinc-500 disabled:opacity-50 dark:border-zinc-600 dark:bg-zinc-800 dark:text-zinc-100 dark:placeholder-zinc-400"
          />
          <button
            type="submit"
            disabled={loading || hasPendingQuestion || !input.trim()}
            className="rounded-xl bg-zinc-900 px-5 py-3 font-medium text-white transition hover:bg-zinc-800 disabled:opacity-50 dark:bg-zinc-100 dark:text-zinc-900 dark:hover:bg-zinc-200"
          >
            Send
          </button>
        </div>
      </form>
    </div>
  );
}
