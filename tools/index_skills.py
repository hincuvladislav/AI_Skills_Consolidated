#!/usr/bin/env python3
"""
Index the consolidated skills library into Qdrant (collection: "skills").

Indexes every canonical SKILL.md under vendor/ with payload metadata
(skill name, source repo, category, path, description) for semantic lookup
from any project on this machine.

Runs on the Agents project venv (has qdrant-client, openai, python-dotenv):
    /Users/vladislavhincu/Projects/Agents/Agents/infrastructure/venv/bin/python \
        tools/index_skills.py [--recreate]

Env (defaults match the Agents Qdrant instance):
    QDRANT_HOST=localhost  QDRANT_PORT=6357  OPENAI_API_KEY=...
    (falls back to the Agents infrastructure .env for the API key)
"""

import argparse
import hashlib
import os
import re
import sys
import uuid
from pathlib import Path

from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams

LIB_ROOT = Path(__file__).resolve().parent.parent
AGENTS_ENV = Path("/Users/vladislavhincu/Projects/Agents/Agents/infrastructure/.env")

load_dotenv()
if not os.getenv("OPENAI_API_KEY") and AGENTS_ENV.exists():
    load_dotenv(AGENTS_ENV)

QDRANT_HOST = os.getenv("QDRANT_HOST", "localhost")
QDRANT_PORT = int(os.getenv("QDRANT_PORT", 6357))
COLLECTION = "skills"
MODEL = "text-embedding-3-small"
DIM = 1536
MAX_CHARS = 18000  # ~ well under the 8k-token embedding limit per chunk


def parse_frontmatter(text: str):
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.S)
    name = desc = ""
    if m:
        for line in m.group(1).splitlines():
            if line.startswith("name:"):
                name = line.split(":", 1)[1].strip().strip("\"'")
            elif line.startswith("description:"):
                desc = line.split(":", 1)[1].strip().strip("\"'")
    return name, desc


def chunks_for(text: str):
    if len(text) <= MAX_CHARS:
        return [text]
    out, cur, size = [], [], 0
    for para in text.split("\n\n"):
        if size + len(para) > MAX_CHARS and cur:
            out.append("\n\n".join(cur))
            cur, size = [], 0
        cur.append(para)
        size += len(para) + 2
    if cur:
        out.append("\n\n".join(cur))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--recreate", action="store_true", help="drop & recreate the collection")
    args = ap.parse_args()

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        sys.exit("OPENAI_API_KEY not found (checked env + Agents infrastructure .env)")
    from openai import OpenAI
    oai = OpenAI(api_key=api_key)

    qc = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)
    existing = {c.name for c in qc.get_collections().collections}
    if args.recreate and COLLECTION in existing:
        qc.delete_collection(COLLECTION)
        existing.discard(COLLECTION)
    if COLLECTION not in existing:
        qc.create_collection(
            COLLECTION,
            vectors_config=VectorParams(size=DIM, distance=Distance.COSINE),
        )
        print(f"Created collection '{COLLECTION}'")

    import json as _json
    src_by_path = {}
    idx_file = LIB_ROOT / "skills-index.json"
    if idx_file.exists():
        for e in _json.loads(idx_file.read_text()):
            src_by_path[e["path"]] = e.get("source", "")
    skill_files = sorted((LIB_ROOT / "skills").rglob("SKILL.md"))
    print(f"Indexing {len(skill_files)} SKILL.md files ...")

    points, indexed = [], 0
    for f in skill_files:
        rel = f.relative_to(LIB_ROOT)
        parts = rel.parts  # skills / <category> / <unit> / ...
        category = parts[1]
        unit_path = "/".join(parts[:3])
        repo = src_by_path.get(unit_path, "")
        text = f.read_text(errors="replace")
        name, desc = parse_frontmatter(text)
        skill_dir = str(rel.parent)
        for i, chunk in enumerate(chunks_for(text)):
            emb = oai.embeddings.create(model=MODEL, input=chunk).data[0].embedding
            pid = str(uuid.UUID(hashlib.md5(f"{rel}#{i}".encode()).hexdigest()))
            points.append(PointStruct(
                id=pid,
                vector=emb,
                payload={
                    "skill": name or f.parent.name,
                    "description": desc,
                    "repo": repo,
                    "category": category,
                    "path": skill_dir,
                    "chunk": i,
                    "content": chunk[:2000],
                },
            ))
            if len(points) >= 64:
                qc.upsert(COLLECTION, points=points)
                points = []
        indexed += 1
        if indexed % 50 == 0:
            print(f"  {indexed}/{len(skill_files)}")
    if points:
        qc.upsert(COLLECTION, points=points)

    info = qc.get_collection(COLLECTION)
    print(f"Done: {indexed} skills indexed, {info.points_count} vectors in '{COLLECTION}'")


if __name__ == "__main__":
    main()
