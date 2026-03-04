#!/usr/bin/env python3
"""Interactive terminal REPL for the Cycle Trip Planner agent."""
from __future__ import annotations

import sys
import uuid

from dotenv import load_dotenv

load_dotenv()

from src.agent.session import run_turn  # noqa: E402 — load_dotenv must run first


def main() -> None:
    session_id = str(uuid.uuid4())

    print("\n🚴 Cycle Trip Planner")
    print("Type your trip request, or 'quit' to exit.\n")

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye! Happy cycling!")
            sys.exit(0)

        if not user_input:
            continue

        if user_input.lower() in {"quit", "exit", "q"}:
            print("Goodbye! Happy cycling!")
            sys.exit(0)

        try:
            reply, tools_used, _, _ = run_turn(session_id, user_input)
        except Exception as exc:
            print(f"[Error: {exc}]")
            continue

        if tools_used:
            print(f"[tools: {', '.join(tools_used)}]\n")

        print(f"Agent: {reply}\n")


if __name__ == "__main__":
    main()
