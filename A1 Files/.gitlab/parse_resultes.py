#!/usr/bin/env python3
import os
import re
import sys
from pathlib import Path

MIN_SCORE = float(os.environ.get("MIN_SCORE", "0"))  # default 0

p = Path(sys.argv[1])
text = p.read_text(encoding="utf-8", errors="ignore")

# ---- count ok / FAIL / ERROR lines ----
ok_cnt = len(re.findall(r"\.\.\.\s+ok\s*$", text, flags=re.MULTILINE))
fail_cnt = len(re.findall(r"\.\.\.\s+FAIL\s*$", text, flags=re.MULTILINE))
err_cnt = len(re.findall(r"\.\.\.\s+ERROR\s*$", text, flags=re.MULTILINE))

# ---- Ran xx tests & FAILED(...) ----
ran = re.search(r"^Ran\s+(\d+)\s+tests?\s+in\s+([0-9.]+)s", text, flags=re.MULTILINE)
ran_tests = int(ran.group(1)) if ran else None
ran_time = float(ran.group(2)) if ran else None

failed_line = re.search(r"^FAILED\s*\(([^)]+)\)", text, flags=re.MULTILINE)
failed_detail = failed_line.group(1) if failed_line else ""

# ---- traceback exists ----
has_traceback = "Traceback (most recent call last):" in text

# ---- parse Grades ----
def find_pair(label: str):
    m = re.search(
        rf"^{re.escape(label)}:\s*([0-9]*\.?[0-9]+)\s*/\s*([0-9]*\.?[0-9]+)\s*$",
        text, flags=re.MULTILINE
    )
    if not m:
        return None
    return float(m.group(1)), float(m.group(2))

total = find_pair("TOTAL")
if total is None:
    print("? TOTAL not found; check results.txt format.")
    Path("grade.env").write_text("PARSE_OK=0\n", encoding="utf-8")
    sys.exit(2)

total_score, total_max = total

items = {}
for m in re.finditer(
    r"^([A-Z0-9_]+):\s*([0-9]*\.?[0-9]+)\s*/\s*([0-9]*\.?[0-9]+)\s*$",
    text, flags=re.MULTILINE
):
    items[m.group(1)] = (float(m.group(2)), float(m.group(3)))

# ---- helper: extract first ERROR/FAIL detail block from unittest output ----
def extract_first_problem_block(text: str, prefer: str = "ERROR", max_chars: int = 12000):
    """
    Unittest typically prints sections like:
    ======================================================================
    ERROR: test_xxx (ClassName)
    ----------------------------------------------------------------------
    Traceback ...
    ...
    ======================================================================
    FAIL: test_yyy (ClassName)
    ----------------------------------------------------------------------
    AssertionError ...
    ...
    ----------------------------------------------------------------------
    Ran ...
    """
    # find all headings
    headings = list(re.finditer(r"^(ERROR|FAIL):\s+(.+)$", text, flags=re.MULTILINE))
    if not headings:
        return None

    # choose first ERROR if prefer=ERROR, else first FAIL, else first heading
    chosen = None
    if prefer == "ERROR":
        for h in headings:
            if h.group(1) == "ERROR":
                chosen = h
                break
    if chosen is None:
        for h in headings:
            if h.group(1) == "FAIL":
                chosen = h
                break
    if chosen is None:
        chosen = headings[0]

    start = chosen.start()

    # end at next heading or at "Ran xx tests" or end-of-file
    next_starts = [h.start() for h in headings if h.start() > start]
    ran_pos = text.find("\nRan ")
    candidates = []
    if next_starts:
        candidates.append(min(next_starts))
    if ran_pos != -1 and ran_pos > start:
        candidates.append(ran_pos)
    end = min(candidates) if candidates else len(text)

    block = text[start:end].strip()
    if len(block) > max_chars:
        block = block[:max_chars] + "\n... [TRUNCATED] ..."
    return block

problem_block = extract_first_problem_block(text, prefer="ERROR")

# ---- write grade.env ----
env = []
env.append("PARSE_OK=1")
env.append(f"OK_COUNT={ok_cnt}")
env.append(f"FAIL_COUNT={fail_cnt}")
env.append(f"ERROR_COUNT={err_cnt}")
env.append(f"TOTAL_SCORE={total_score}")
env.append(f"TOTAL_MAX={total_max}")
env.append(f"TOTAL_PCT={0 if total_max == 0 else total_score/total_max:.6f}")
env.append(f"HAS_TRACEBACK={1 if has_traceback else 0}")
if ran_tests is not None:
    env.append(f"RAN_TESTS={ran_tests}")
if ran_time is not None:
    env.append(f"RAN_TIME_SEC={ran_time}")
Path("grade.env").write_text("\n".join(env) + "\n", encoding="utf-8")

# ---- print summary ----
print("==================== AUTOGRADER SUMMARY ====================")
if ran_tests is not None and ran_time is not None:
    print(f"Ran: {ran_tests} tests in {ran_time:.3f}s")
print(f"Result counts: ok={ok_cnt}, FAIL={fail_cnt}, ERROR={err_cnt}")
if failed_detail:
    print(f"FAILED detail: {failed_detail}")
print(f"Traceback: {'YES' if has_traceback else 'NO'}")

print("\n[Grades]")
for k in sorted(items.keys()):
    v, mx = items[k]
    print(f"- {k}: {v}/{mx}")

print("\nTOTAL:", f"{total_score}/{total_max} ({(total_score/total_max*100 if total_max else 0):.2f}%)")

# ---- fail conditions ----
reasons = []
if err_cnt > 0:
    reasons.append(f"ERROR_COUNT={err_cnt}")
if has_traceback:
    reasons.append("Traceback detected")
if total_score < MIN_SCORE:
    reasons.append(f"TOTAL {total_score} < MIN_SCORE {MIN_SCORE}")

if reasons:
    # dump detail so job log shows where it failed
    if problem_block:
        Path("error_detail.txt").write_text(problem_block + "\n", encoding="utf-8")
        print("\n==================== FIRST PROBLEM DETAIL ====================")
        print(problem_block)
        print("==============================================================")
        print("\n(Wrote error_detail.txt for artifacts)")
    else:
        print("\n(no ERROR/FAIL detail block found in results.txt)")

    print("\n? JOB FAILED:", "; ".join(reasons))
    sys.exit(1)

print("\n? JOB PASSED")
sys.exit(0)
