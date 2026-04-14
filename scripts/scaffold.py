#!/usr/bin/env python3
"""Bootstrap a new analysis workspace with per-phase directories and CLAUDE.md files.

Usage:
    pixi run scaffold analyses/my_analysis --type measurement
    pixi run scaffold analyses/my_analysis --type search

Creates the full phase directory tree (phase0_acquire through phase7_final),
copies CLAUDE.md templates with placeholder substitution, initializes a git
repo, and prints next steps.
"""

import argparse
import subprocess
from pathlib import Path

HERE = Path(__file__).parent.parent  # apexAI root
TEMPLATES = HERE / "templates"

# ---------------------------------------------------------------------------
# Phase directories and template mapping
# ---------------------------------------------------------------------------

PHASES = [
    "phase0_acquire",
    "phase1_strategy",
    "phase2_exploration",
    "phase3_processing",
    "phase4_inference",
    "phase5_draft",
    "phase6_fulldata",
    "phase7_final",
]

PHASE_SUBDIRS = ["outputs", "outputs/figures", "src", "review", "logs"]

PHASE_TEMPLATE_MAP = {
    "phase0_acquire": "phase0.md",
    "phase1_strategy": "phase1.md",
    "phase2_exploration": "phase2.md",
    "phase3_processing": "phase3.md",
    "phase4_inference": "phase4.md",
    "phase5_draft": "phase5.md",
    "phase6_fulldata": "phase5.md",  # phases 5-7 share the documentation template
    "phase7_final": "phase5.md",
}


def _read_template(name: str) -> str:
    """Read a template file from templates/."""
    path = TEMPLATES / name
    if not path.exists():
        raise FileNotFoundError(f"Template not found: {path}")
    return path.read_text()


def _substitute(text: str, variables: dict) -> str:
    """Replace {{key}} placeholders with values from variables dict."""
    result = text
    for key, value in variables.items():
        result = result.replace("{{" + key + "}}", value)
    return result


def scaffold(analysis_dir: Path, analysis_type: str) -> None:
    """Create the analysis directory structure with CLAUDE.md files."""
    analysis_dir = analysis_dir.resolve()
    analysis_dir.mkdir(parents=True, exist_ok=True)

    variables = {
        "name": analysis_dir.name,
        "analysis_type": analysis_type,
    }

    # --- Root CLAUDE.md ---
    root_claude = analysis_dir / "CLAUDE.md"
    if not root_claude.exists():
        template = _read_template("root.md")
        root_claude.write_text(_substitute(template, variables))
        print(f"  wrote {root_claude}")

    # --- Per-phase directories and CLAUDE.md ---
    for phase_name in PHASES:
        phase_dir = analysis_dir / phase_name
        phase_dir.mkdir(exist_ok=True)
        for subdir in PHASE_SUBDIRS:
            (phase_dir / subdir).mkdir(parents=True, exist_ok=True)

        claude_path = phase_dir / "CLAUDE.md"
        template_name = PHASE_TEMPLATE_MAP.get(phase_name)
        if template_name and not claude_path.exists():
            template = _read_template(template_name)
            claude_path.write_text(_substitute(template, variables))
            print(f"  wrote {claude_path}")

    # --- Symlink conventions/ into the analysis ---
    conventions_link = analysis_dir / "conventions"
    conventions_src = HERE / "conventions"
    if not conventions_link.exists() and conventions_src.exists():
        conventions_link.symlink_to(conventions_src.resolve())
        print(f"  linked {conventions_link} -> {conventions_src}")

    # --- .analysis_config ---
    config_path = analysis_dir / ".analysis_config"
    if not config_path.exists():
        config_path.write_text(
            "# Analysis configuration.\n"
            "# Set data_dir to the path where your input ROOT files live.\n"
            "# Add extra allow= lines for additional paths (one per line).\n"
            "data_dir=\n"
            "# allow=/path/to/mc/samples\n"
            "# allow=/path/to/calibration\n"
        )
        print(f"  wrote {config_path}")

    # --- pixi.toml ---
    pixi_path = analysis_dir / "pixi.toml"
    if not pixi_path.exists():
        template = _read_template("pixi.toml")
        pixi_path.write_text(template.replace("{name}", variables["name"]))
        print(f"  wrote {pixi_path}")

    # --- Experiment log and retrieval log stubs ---
    for log_name in ["experiment_log.md", "retrieval_log.md"]:
        log_path = analysis_dir / log_name
        if not log_path.exists():
            title = log_name.replace("_", " ").replace(".md", "").title()
            log_path.write_text(f"# {title}\n\nAppend-only log. Do not edit prior entries.\n")
            print(f"  wrote {log_path}")

    # --- Git repo ---
    git_dir = analysis_dir / ".git"
    if not git_dir.exists():
        subprocess.run(
            ["git", "init"],
            cwd=analysis_dir,
            check=True,
            capture_output=True,
        )
        gitignore = analysis_dir / ".gitignore"
        if not gitignore.exists():
            gitignore.write_text(
                "# pixi\n"
                ".pixi/\n"
                "pixi.lock\n"
                "\n"
                "# Python\n"
                "__pycache__/\n"
                "*.pyc\n"
                "*.pyo\n"
                "\n"
                "# SLURM logs\n"
                ".slurm_*.out\n"
                "slurm-*.out\n"
                "\n"
                "# Editor\n"
                ".vscode/\n"
                "*.swp\n"
                "*~\n"
            )
            print(f"  wrote {gitignore}")
        print("  initialized git repo")

    # --- Print summary ---
    print(f"\nScaffolded {analysis_dir}/ ({analysis_type})")
    print(f"  8 phase directories: {PHASES[0]} ... {PHASES[-1]}")
    print(f"  each with: {', '.join(PHASE_SUBDIRS)}")
    print()
    print("Next steps:")
    print(f"  1. Edit .analysis_config -- set data_dir")
    print(f"  2. cd {analysis_dir} && pixi install")
    print(f"  3. claude   # starts the orchestrator agent")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Scaffold a new analysis workspace with per-phase CLAUDE.md files."
    )
    parser.add_argument("dir", type=Path, help="Analysis directory to create")
    parser.add_argument(
        "--type",
        choices=["measurement", "search"],
        required=True,
        dest="analysis_type",
        help="Analysis type (measurement or search)",
    )
    args = parser.parse_args()
    scaffold(args.dir, args.analysis_type)


if __name__ == "__main__":
    main()
