#!/usr/bin/env python3
"""Plot linter for apexAI analyses.

Scans plotting scripts for mechanical violations of standards/plotting.md.
Returns exit code 1 if any violations are found.

Usage:
    python lint_plots.py path/to/scripts/

Each violation is printed as:
    VIOLATION: <file>:<line> -- <rule description>
"""

import re
import sys
from pathlib import Path


def find_scripts(root: Path) -> list[Path]:
    """Find all Python files under the given path."""
    scripts = []
    for p in sorted(root.rglob("*.py")):
        if ".pixi" in str(p) or "__pycache__" in str(p):
            continue
        scripts.append(p)
    return scripts


def lint_file(path: Path) -> list[str]:
    """Return list of violation strings for a single file."""
    violations: list[str] = []
    text = path.read_text(errors="replace")
    lines = text.splitlines()

    def v(lineno: int, msg: str) -> None:
        violations.append(f"VIOLATION: {path}:{lineno} -- {msg}")

    # --- Category A: Banned patterns ---
    banned = [
        (r"\.set_title\(", "No set_title() -- captions go in the AN"),
        (r"fontsize\s*=\s*\d", "No absolute fontsize=N -- use stylesheet or relative strings"),
        (r"plt\.colorbar\(", "No plt.colorbar() -- use mh.hist2dplot or make_square_add_cbar"),
        (r"fig\.colorbar\([^)]*\bax\s*=", "No fig.colorbar(ax=) -- use cax= via make_square_add_cbar"),
        (r"ax\.bar\(", "No ax.bar() for histograms -- use mh.histplot()"),
        (r"ax\.step\(", "No ax.step() for histograms -- use mh.histplot()"),
        (r"ax\.text\(", "No ax.text() -- use mh.label.add_text()"),
        (r"ax\.annotate\(", "No ax.annotate() -- use mh.label.add_text()"),
        (r"tight_layout\(\)", "No tight_layout() -- use fig.savefig bbox_inches='tight'"),
    ]

    for i, line in enumerate(lines, 1):
        stripped = line.lstrip()
        if stripped.startswith("#"):
            continue
        for pattern, msg in banned:
            if re.search(pattern, line):
                v(i, msg)

    # --- Required: experiment label ---
    has_exp_label = any("exp_label" in line or "label.exp_label" in line for line in lines)
    has_savefig = any("savefig" in line for line in lines)
    if has_savefig and not has_exp_label:
        v(0, "Missing exp_label or label.exp_label -- required on every figure")

    # --- Required: savefig with bbox_inches ---
    for i, line in enumerate(lines, 1):
        if "savefig(" in line:
            context = line
            if i < len(lines):
                context += lines[i]  # check continuation line
            if "bbox_inches" not in context:
                v(i, "savefig without bbox_inches='tight'")

    # --- Required: both PDF and PNG output ---
    saves_pdf = any(".pdf" in line and "savefig" in line for line in lines)
    saves_png = any(".png" in line and "savefig" in line for line in lines)
    if has_savefig:
        if not saves_pdf:
            v(0, "Missing PDF save -- must save both .pdf and .png")
        if not saves_png:
            v(0, "Missing PNG save -- must save both .pdf and .png")

    # --- Error bar check: derived quantities need explicit yerr ---
    has_view_assign = False
    view_lines: list[int] = []
    for i, line in enumerate(lines, 1):
        if re.search(r"\.view\(\)\s*\[.*\]\s*[+]?=", line):
            has_view_assign = True
            view_lines.append(i)

    if has_view_assign:
        for i, line in enumerate(lines, 1):
            if 'histtype="errorbar"' in line or "histtype='errorbar'" in line:
                context = "\n".join(lines[max(0, i - 6) : i + 4])
                if "yerr=" not in context:
                    v(
                        i,
                        f'histtype="errorbar" on derived quantity without yerr= '
                        f"(view assignment at line(s) {view_lines}) -- "
                        "mplhep will apply sqrt(N), pass yerr= explicitly",
                    )

    # --- Missing hspace=0 for ratio plots ---
    has_sharex = any("sharex=True" in line for line in lines)
    has_hspace = any(re.search(r"hspace\s*=\s*0", line) for line in lines)
    if has_sharex and not has_hspace:
        v(0, "sharex=True without hspace=0 -- ratio panel will have a visible gap")

    # --- Figsize consistency check ---
    for i, line in enumerate(lines, 1):
        if "figsize" in line:
            m = re.search(r"figsize\s*=\s*\((\d+),\s*(\d+)\)", line)
            if m:
                w, h = int(m.group(1)), int(m.group(2))
                if w == h and w != 10:
                    v(i, f"figsize=({w}, {h}) -- single-panel must be (10, 10)")

    return violations


def main() -> int:
    if len(sys.argv) < 2:
        root = Path(".")
    else:
        root = Path(sys.argv[1])

    scripts = find_scripts(root)

    if not scripts:
        print(f"No Python scripts found under {root}")
        return 0

    all_violations: list[str] = []
    for script in scripts:
        all_violations.extend(lint_file(script))

    if all_violations:
        for violation in all_violations:
            print(violation)
        print(f"\n{len(all_violations)} violation(s) found in {len(scripts)} file(s).")
        return 1
    else:
        print(f"No plotting violations found in {len(scripts)} file(s).")
        return 0


if __name__ == "__main__":
    sys.exit(main())
