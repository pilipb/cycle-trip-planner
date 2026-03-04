#!/usr/bin/env python3
"""Interactive terminal REPL for the Cycle Trip Planner agent."""
from __future__ import annotations

import sys
import uuid

from dotenv import load_dotenv

load_dotenv()

from src.agent.session import (
    get_pending_tool_call_id,
    run_turn,
    run_turn_resume,
)  # noqa: E402 — load_dotenv must run first


def _is_pending_question(reply: str | dict) -> bool:
    return isinstance(reply, dict) and "tool_call_id" in reply and "question" in reply


def main() -> None:
    session_id = str(uuid.uuid4())

    print("\n🚴 Cycle Trip Planner")
    print("Type your trip request, or 'quit' to exit.\n")

    while True:
        try:
            prompt = "You: "
            if get_pending_tool_call_id(session_id):
                prompt = "Answer: "
            user_input = input(prompt).strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye! Happy cycling!")
            sys.exit(0)

        if not user_input:
            continue

        if user_input.lower() in {"quit", "exit", "q"}:
            print("Goodbye! Happy cycling!")
            sys.exit(0)

        try:
            pending_id = get_pending_tool_call_id(session_id)
            if pending_id:
                reply, tools_used, _, _ = run_turn_resume(session_id, pending_id, user_input)
            else:
                reply, tools_used, _, _ = run_turn(session_id, user_input)
        except Exception as exc:
            print(f"[Error: {exc}]")
            continue

        if tools_used:
            print(f"[tools: {', '.join(tools_used)}]\n")

        if _is_pending_question(reply):
            q = reply["question"]
            opts = reply.get("options", [])
            print(f"Agent: {q}")
            if opts:
                print(f"  Options: {', '.join(opts)}")
            print()
        else:
            print(f"Agent: {reply}\n")


if __name__ == "__main__":
    main()
