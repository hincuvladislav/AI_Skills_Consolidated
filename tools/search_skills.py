#!/usr/bin/env python3
"""
Semantic search over the skills library (Qdrant collection "skills").

Usage:
    /Users/vladislavhincu/Projects/Agents/Agents/infrastructure/venv/bin/python \
        tools/search_skills.py "review a pull request for security issues" [-n 5]
"""

import argparse
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from qdrant_client import QdrantClient

AGENTS_ENV = Path("/Users/vladislavhincu/Projects/Agents/Agents/infrastructure/.env")
load_dotenv()
if not os.getenv("OPENAI_API_KEY") and AGENTS_ENV.exists():
    load_dotenv(AGENTS_ENV)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("query")
    ap.add_argument("-n", type=int, default=5)
    args = ap.parse_args()

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        sys.exit("OPENAI_API_KEY not found")
    from openai import OpenAI
    emb = OpenAI(api_key=api_key).embeddings.create(
        model="text-embedding-3-small", input=args.query
    ).data[0].embedding

    qc = QdrantClient(host=os.getenv("QDRANT_HOST", "localhost"),
                      port=int(os.getenv("QDRANT_PORT", 6357)))
    hits = qc.query_points("skills", query=emb, limit=args.n).points

    lib_root = Path(__file__).resolve().parent.parent
    for h in hits:
        p = h.payload
        print(f"[{h.score:.3f}] {p['skill']}  ({p['repo']}/{p['category']})")
        print(f"        {p['description'][:160]}")
        print(f"        -> {lib_root / p['path']}/SKILL.md")
        print()


if __name__ == "__main__":
    main()
