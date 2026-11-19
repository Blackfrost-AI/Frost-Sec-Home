"""Token budget counting for Frost-Sec-Home packs.

count_tokens(path) -> {"prose": int, "code": int, "total": int}
Uses a real tokenizer (tiktoken cl100k_base) — words x 1.4 is banned by the
prompt standard because code blocks run ~2.5 tokens/word.
"""
import re

import tiktoken

_ENC = tiktoken.get_encoding("cl100k_base")
_FENCE = re.compile(r"^```", re.M)


def count_text(text: str) -> dict:
    parts = _FENCE.split(text)
    # alternating: prose, code, prose, code... (fence markers removed)
    prose = "".join(parts[0::2])
    code = "".join(parts[1::2])
    p = len(_ENC.encode(prose))
    c = len(_ENC.encode(code))
    return {"prose": p, "code": c, "total": p + c}


def count_tokens(path: str) -> dict:
    with open(path, encoding="utf-8") as f:
        return count_text(f.read())


if __name__ == "__main__":
    import sys

    for path in sys.argv[1:]:
        print(path, count_tokens(path))
