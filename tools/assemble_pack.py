"""Assemble a pack draft: inject the canonical Safety Core block.

Usage: python3 tools/assemble_pack.py <draft.md> <out.md>
The draft contains the literal line {{SAFETY_CORE}} where the block goes.
Everything else passes through unchanged. Keeps embedded cores byte-identical
to core/SAFETY-CORE.md by construction.
"""
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def assemble(draft_path: str, out_path: str) -> None:
    with open(os.path.join(REPO, "core", "SAFETY-CORE.md"), encoding="utf-8") as f:
        core = f.read().rstrip("\n")
    with open(draft_path, encoding="utf-8") as f:
        draft = f.read()
    if "{{SAFETY_CORE}}" not in draft:
        raise SystemExit("draft has no {{SAFETY_CORE}} marker")
    block = "<!-- SAFETY-CORE-BEGIN -->\n" + core + "\n<!-- SAFETY-CORE-END -->"
    out = draft.replace("{{SAFETY_CORE}}", block)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(out)
    print(f"assembled {out_path}")


if __name__ == "__main__":
    assemble(sys.argv[1], sys.argv[2])
