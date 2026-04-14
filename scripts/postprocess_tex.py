#!/usr/bin/env python3
"""LaTeX post-processor for pandoc output.

Applies deterministic structural fixes that pandoc cannot produce natively.
Stdlib only -- no pip dependencies.

Usage:
    python postprocess_tex.py input.tex output.tex
"""

import re
import sys
from pathlib import Path


def fix_title_math(lines: list[str]) -> int:
    r"""Replace \textbackslash and literal sqrt(s) with proper LaTeX in \title."""
    count = 0
    for i, line in enumerate(lines):
        if "\\title{" not in line:
            continue
        new = re.sub(r"sqrt\(s\)", r"$\\sqrt{s}$", line)
        new = re.sub(r"\\\$\\sqrt\{s\}\\\$", r"$\\sqrt{s}$", new)
        new = re.sub(r"\$\\sqrt\{s\}\$", r"$\\sqrt{s}$", new)
        new = new.replace("\\textbackslash{}", "\\")
        if new != line:
            lines[i] = new
            count += 1
    return count


def fix_escaped_math(lines: list[str]) -> int:
    r"""Fix escaped standalone math: \$\pm\$ -> $\pm$, and similar."""
    count = 0
    replacements = [
        (r"\\\$\\pm\\\$", r"$\\pm$"),
        (r"\\\$\xb1\\\$", r"$\\pm$"),
        (r"\\\$<\\\$", r"$<$"),
        (r"\\\$>\\\$", r"$>$"),
        (r"\\\$\\sim\\\$", r"$\\sim$"),
    ]
    for i, line in enumerate(lines):
        new = line
        for pat, repl in replacements:
            new = re.sub(pat, repl, new)
        if new != line:
            lines[i] = new
            count += 1
    return count


def fix_longtable_short(lines: list[str]) -> int:
    """Convert longtables with fewer than 15 data rows to table+tabular."""
    text = "".join(lines)
    count = 0
    pat = re.compile(
        r"(\\begin\{longtable\}(?:\[[^\]]*\])?)(\{[^}]*\})(.*?)(\\end\{longtable\})",
        re.DOTALL,
    )

    def convert(m: re.Match) -> str:
        nonlocal count
        col_spec = m.group(2)
        body = m.group(3)
        data_rows = [
            r for r in body.split("\n")
            if "\\\\" in r
            and "\\toprule" not in r
            and "\\midrule" not in r
            and "\\bottomrule" not in r
            and "\\endhead" not in r
        ]
        if len(data_rows) >= 15:
            return m.group(0)
        cleaned = re.sub(r"\\end(head|foot|lastfoot)\s*\n?", "", body)
        count += 1
        return (
            "\\begin{table}[htbp]\n\\centering\n\\small\n"
            f"\\begin{{tabular}}{col_spec}\n{cleaned.strip()}\n"
            "\\end{tabular}\n\\end{table}"
        )

    new_text = pat.sub(convert, text)
    if count:
        lines.clear()
        lines.extend(new_text.splitlines(keepends=True))
        if lines and not lines[-1].endswith("\n"):
            lines[-1] += "\n"
    return count


def fix_margins(lines: list[str]) -> int:
    """Ensure geometry package with 0.75in margins."""
    target = "\\usepackage[margin=0.75in]{geometry}\n"
    for i, line in enumerate(lines):
        if "\\usepackage" in line and "geometry" in line:
            if line.strip() == target.strip():
                return 0
            lines[i] = target
            return 1
    for i, line in enumerate(lines):
        if line.strip().startswith("\\documentclass"):
            lines.insert(i + 1, target)
            return 1
    return 0


def fix_abstract(lines: list[str]) -> int:
    """Convert \\section{Abstract} to \\begin{abstract}...\\end{abstract}."""
    start = end = None
    for i, line in enumerate(lines):
        if re.search(r"\\section\{Abstract\}", line):
            start = i
            if start > 0 and "hypertarget{abstract}" in lines[start - 1]:
                start -= 1
            break
    if start is None:
        return 0
    for i in range(start + 1, len(lines)):
        if re.search(r"\\(section|chapter)\b", lines[i]) and i > start + 1:
            end = i
            break
    if end is None:
        return 0
    content = [l for l in lines[start + 1 : end] if l.strip()]
    del lines[start:end]
    block = ["\\begin{abstract}\n"] + content + ["\\end{abstract}\n\n"]
    insert = None
    for i, line in enumerate(lines):
        if "\\tableofcontents" in line:
            insert = i
            break
        if "\\maketitle" in line:
            insert = i + 1
            break
    if insert is None:
        for i, line in enumerate(lines):
            if "\\begin{document}" in line:
                insert = i + 1
                break
    if insert is not None:
        for j, bl in enumerate(block):
            lines.insert(insert + j, bl)
    return 1


def fix_references(lines: list[str]) -> int:
    """Convert \\section{References} to unnumbered \\section*{References}."""
    for i, line in enumerate(lines):
        if re.search(r"\\section\{References\}", line):
            lines[i] = "\\section*{References}\\addcontentsline{toc}{section}{References}\n"
            return 1
    return 0


def fix_table_spacing(lines: list[str]) -> int:
    """Insert \\vspace{1em} before \\begin{longtable}."""
    count = 0
    offset = 0
    indices = [i for i, line in enumerate(lines) if "\\begin{longtable}" in line]
    for idx in indices:
        pos = idx + offset
        if pos > 0 and "\\vspace" in lines[pos - 1]:
            continue
        lines.insert(pos, "\\vspace{1em}\n")
        offset += 1
        count += 1
    return count


def fix_figure_placement(lines: list[str]) -> int:
    """Add [htbp] to bare \\begin{figure}."""
    count = 0
    for i, line in enumerate(lines):
        if line.rstrip("\n") == "\\begin{figure}":
            lines[i] = "\\begin{figure}[htbp]\n"
            count += 1
    return count


def fix_float_barriers(lines: list[str]) -> int:
    """Insert \\FloatBarrier before each \\section{ (not \\section*{)."""
    count = 0
    offset = 0
    indices = [
        i for i, line in enumerate(lines)
        if re.search(r"\\section\{", line) and not re.search(r"\\section\*\{", line)
    ]
    for idx in indices:
        pos = idx + offset
        if pos > 0 and "\\FloatBarrier" in lines[pos - 1]:
            continue
        lines.insert(pos, "\\FloatBarrier\n")
        offset += 1
        count += 1
    return count


def fix_needspace(lines: list[str]) -> int:
    """Insert \\needspace{4\\baselineskip} before section headings."""
    count = 0
    offset = 0
    indices = [i for i, line in enumerate(lines) if re.search(r"\\(sub)?section[\{*]", line)]
    for idx in indices:
        pos = idx + offset
        if pos > 0 and "\\needspace" in lines[pos - 1]:
            continue
        lines.insert(pos, "\\needspace{4\\baselineskip}\n")
        offset += 1
        count += 1
    return count


def fix_duplicate_headers(lines: list[str]) -> int:
    """Remove duplicate table header blocks (two \\toprule within 5 lines)."""
    count = 0
    i = 0
    while i < len(lines):
        if "\\toprule" in lines[i]:
            for j in range(i + 1, min(i + 6, len(lines))):
                if "\\toprule" in lines[j]:
                    end = j + 1
                    while end < len(lines):
                        if "\\midrule" in lines[end] or "\\endhead" in lines[end]:
                            end += 1
                            break
                        end += 1
                    del lines[j:end]
                    count += 1
                    break
        i += 1
    return count


def fix_duplicate_labels(lines: list[str]) -> int:
    """Remove consecutive duplicate \\label{...}\\label{...}."""
    text = "".join(lines)
    new_text, n = re.subn(r"(\\label\{([^}]+)\})(\s*\\label\{\2\})+", r"\1", text)
    if n > 0:
        lines.clear()
        lines.extend(new_text.splitlines(keepends=True))
    return n


def fix_appendix(lines: list[str]) -> int:
    """Insert \\clearpage and \\appendix before appendix markers."""
    for i, line in enumerate(lines):
        if re.search(r"%%\s*Appendices", line) or re.search(r"<!--\s*Appendices", line):
            if i + 1 < len(lines) and "\\appendix" in lines[i + 1]:
                return 0
            lines.insert(i + 1, "\\appendix\n")
            lines.insert(i + 1, "\\clearpage\n")
            return 1
    return 0


def fix_clearpage(lines: list[str]) -> int:
    """Insert \\clearpage before \\appendix and \\section*{References}."""
    count = 0
    offset = 0
    targets = []
    for i, line in enumerate(lines):
        if line.strip() == "\\appendix":
            targets.append(i)
        elif re.search(r"\\section\*\{References\}", line):
            targets.append(i)
    for idx in targets:
        pos = idx + offset
        if pos > 0 and "\\clearpage" in lines[pos - 1]:
            continue
        lines.insert(pos, "\\clearpage\n")
        offset += 1
        count += 1
    return count


def postprocess(input_path: str, output_path: str) -> None:
    """Read input .tex, apply all fixes in order, write output .tex."""
    text = Path(input_path).read_text()
    lines = text.splitlines(keepends=True)
    if lines and not lines[-1].endswith("\n"):
        lines[-1] += "\n"

    fixes = []
    fix_functions = [
        ("title-math", fix_title_math),
        ("escaped-math", fix_escaped_math),
        ("margins", fix_margins),
        ("abstract", fix_abstract),
        ("references", fix_references),
        ("table-spacing", fix_table_spacing),
        ("longtable-short", fix_longtable_short),
        ("figure-placement", fix_figure_placement),
        ("float-barriers", fix_float_barriers),
        ("needspace", fix_needspace),
        ("dup-headers", fix_duplicate_headers),
        ("dup-labels", fix_duplicate_labels),
        ("appendix", fix_appendix),
        ("clearpage", fix_clearpage),
    ]

    for name, fn in fix_functions:
        n = fn(lines)
        if n:
            fixes.append(f"{n} {name}" if isinstance(n, int) and n > 1 else name)

    Path(output_path).write_text("".join(lines))

    if fixes:
        print(f"postprocess_tex: {len(fixes)} fixes applied ({', '.join(fixes)})")
    else:
        print("postprocess_tex: no fixes needed")


def main() -> None:
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} input.tex output.tex", file=sys.stderr)
        sys.exit(1)
    input_path, output_path = sys.argv[1], sys.argv[2]
    if not Path(input_path).exists():
        print(f"Error: {input_path} not found", file=sys.stderr)
        sys.exit(1)
    postprocess(input_path, output_path)


if __name__ == "__main__":
    main()
