#!/usr/bin/env python3
"""Install the self-learning skill templates into another project.

The installer keeps the historical Codex/Claude defaults, but the core
operation is agent-neutral: copy shared skills into one or more configured
agent skill directories, then optionally install learning hooks for each
agent runtime.
"""

from __future__ import annotations

import argparse
import json
import shutil
from dataclasses import dataclass
from pathlib import Path


TEMPLATE_ROOT = Path(__file__).resolve().parent
PROFILE_ROOT = TEMPLATE_ROOT.parent.parent / "profiles"
SKILLS = ("digest", "maintain-learnings")


@dataclass(frozen=True)
class AgentProfile:
    name: str
    skills_dir: str
    hooks_dir: str | None = None
    hook_config: str | None = None
    hook_template: str | None = None
    include_openai_yaml: bool = False
    rules_file: str = "AGENTS.md"


def parse_flat_yaml(path: Path) -> dict[str, str]:
    """Read the scalar-only profile format without adding a YAML dependency."""
    values: dict[str, str] = {}
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        key, value = line.split(":", 1)
        values[key.strip()] = value.strip().strip('"\'')
    return values


def load_builtin_profiles() -> dict[str, AgentProfile]:
    profiles: dict[str, AgentProfile] = {}
    for path in sorted(PROFILE_ROOT.glob("*.yaml")):
        values = parse_flat_yaml(path)
        name = values.get("name", path.stem)
        profiles[name] = AgentProfile(
            name=name,
            skills_dir=values["skills_dir"],
            hooks_dir=values.get("hooks_dir") or None,
            hook_config=values.get("hook_config") or None,
            hook_template=values.get("hook_template") or None,
            include_openai_yaml=values.get("include_openai_yaml", "false").lower() == "true",
            rules_file=values.get("entry_file", "AGENTS.md"),
        )
    if profiles:
        return profiles
    return {
        "codex": AgentProfile(
            "codex",
            ".agents/skills",
            ".codex/hooks",
            ".codex/hooks.json",
            "codex-hooks.json.template",
            True,
            "AGENTS.md",
        ),
        "claude": AgentProfile(
            "claude",
            ".claude/skills",
            ".claude/hooks",
            ".claude/settings.json",
            "claude-settings.json.template",
            False,
            "CLAUDE.md",
        ),
        "generic": AgentProfile("generic", ".agent/skills", ".agent/hooks", rules_file="AGENTS.md"),
    }


BUILTIN_PROFILES = load_builtin_profiles()


def load_profile_file(path: str | Path) -> AgentProfile:
    profile_path = Path(path).resolve()
    values = parse_flat_yaml(profile_path)
    name = values.get("name", profile_path.stem)
    if "skills_dir" not in values:
        raise argparse.ArgumentTypeError(f"profile is missing skills_dir: {profile_path}")
    return AgentProfile(
        name=name,
        skills_dir=values["skills_dir"],
        hooks_dir=values.get("hooks_dir") or None,
        hook_config=values.get("hook_config") or None,
        hook_template=values.get("hook_template") or None,
        include_openai_yaml=values.get("include_openai_yaml", "false").lower() == "true",
        rules_file=values.get("entry_file", "AGENTS.md"),
    )


def copytree(source: Path, target: Path, overwrite: bool) -> bool:
    if target.exists():
        if not overwrite:
            print(f"[SKIP] exists: {target}")
            return False
        shutil.rmtree(target)
    shutil.copytree(source, target)
    print(f"[OK] copied: {target}")
    return True


def copyfile(source: Path, target: Path, overwrite: bool) -> None:
    if target.exists() and not overwrite:
        print(f"[SKIP] exists: {target}")
        return
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)
    print(f"[OK] copied: {target}")


def install_skills(target_root: Path, profile: AgentProfile, overwrite: bool) -> None:
    skills_root = target_root / profile.skills_dir
    skills_root.mkdir(parents=True, exist_ok=True)
    for skill in SKILLS:
        source = TEMPLATE_ROOT / "skills" / skill
        target = skills_root / skill
        copied = copytree(source, target, overwrite)
        if copied and not profile.include_openai_yaml:
            agents_dir = target / "agents"
            if agents_dir.exists():
                shutil.rmtree(agents_dir)
                print(f"[OK] removed OpenAI UI metadata from: {agents_dir}")


def install_learnings(target_root: Path) -> None:
    learnings_root = target_root / ".learnings"
    learnings_root.mkdir(parents=True, exist_ok=True)
    (learnings_root / "archive").mkdir(parents=True, exist_ok=True)
    for name in ("LEARNINGS.md", "ERRORS.md", "RULES.md"):
        copyfile(TEMPLATE_ROOT / "learnings" / name, learnings_root / name, overwrite=False)


def hook_identity(hook: object) -> str | None:
    if not isinstance(hook, dict):
        return None
    command = hook.get("command")
    if not isinstance(command, str):
        return None
    if "read_learnings.py" in command:
        return "read_learnings.py"
    if "read-learnings.sh" in command:
        return "read-learnings.sh"
    return command


def merge_hook_config(existing: dict, desired: dict) -> dict:
    """Merge only this template's hook while preserving unrelated settings."""
    merged = dict(existing)
    for key, value in desired.items():
        if key != "hooks":
            merged.setdefault(key, value)

    merged_hooks = merged.setdefault("hooks", {})
    if not isinstance(merged_hooks, dict):
        raise SystemExit("existing hook config has a non-object 'hooks' value")

    for event, desired_entries in desired.get("hooks", {}).items():
        existing_entries = merged_hooks.setdefault(event, [])
        if not isinstance(existing_entries, list):
            raise SystemExit(f"existing hook config event is not a list: {event}")
        for desired_entry in desired_entries:
            matcher = desired_entry.get("matcher", "")
            target_entry = next(
                (
                    entry
                    for entry in existing_entries
                    if isinstance(entry, dict) and entry.get("matcher", "") == matcher and isinstance(entry.get("hooks"), list)
                ),
                None,
            )
            if target_entry is None:
                existing_entries.append(desired_entry)
                continue

            existing_hook_list = target_entry["hooks"]
            for desired_hook in desired_entry.get("hooks", []):
                identity = hook_identity(desired_hook)
                match_index = next(
                    (index for index, hook in enumerate(existing_hook_list) if hook_identity(hook) == identity),
                    None,
                )
                if match_index is None:
                    existing_hook_list.append(desired_hook)
                else:
                    existing_hook_list[match_index] = desired_hook
    return merged


def install_hooks(target_root: Path, profile: AgentProfile, overwrite: bool, python_command: str) -> None:
    if not profile.hooks_dir:
        return

    hook_root = target_root / profile.hooks_dir
    copyfile(TEMPLATE_ROOT / "hooks" / "read-learnings.sh", hook_root / "read-learnings.sh", overwrite)
    copyfile(TEMPLATE_ROOT / "hooks" / "read_learnings.py", hook_root / "read_learnings.py", overwrite)

    if not profile.hook_config or not profile.hook_template:
        print(f"[NEXT] Configure {profile.name} to run: {python_command} {profile.hooks_dir}/read_learnings.py")
        return

    template_path = Path(profile.hook_template)
    if not template_path.is_absolute():
        template_path = TEMPLATE_ROOT / "hooks" / profile.hook_template
    content = template_path.read_text(encoding="utf-8")
    content = content.replace("{{PYTHON}}", python_command)
    content = content.replace("{{HOOK_SCRIPT}}", f"{profile.hooks_dir}/read_learnings.py")
    desired = json.loads(content)

    config_path = target_root / profile.hook_config
    existing = json.loads(config_path.read_text(encoding="utf-8")) if config_path.exists() else {}
    merged = merge_hook_config(existing, desired)
    copyfile_from_text(json.dumps(merged, ensure_ascii=False, indent=2) + "\n", config_path)


def copyfile_from_text(content: str, target: Path) -> None:
    if target.exists() and target.read_text(encoding="utf-8") == content:
        print(f"[SKIP] unchanged: {target}")
        return
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")
    print(f"[OK] wrote: {target}")


def parse_custom_agent(spec: str) -> AgentProfile:
    parts = spec.split(":")
    if len(parts) < 2:
        raise argparse.ArgumentTypeError(
            "--custom-agent must look like NAME:SKILLS_DIR[:HOOKS_DIR[:HOOK_CONFIG[:HOOK_TEMPLATE]]]"
        )
    name, skills_dir, *rest = parts
    if not name or not skills_dir:
        raise argparse.ArgumentTypeError("custom agent name and skills dir are required")
    hooks_dir = rest[0] if len(rest) > 0 and rest[0] else None
    hook_config = rest[1] if len(rest) > 1 and rest[1] else None
    hook_template = rest[2] if len(rest) > 2 and rest[2] else None
    return AgentProfile(name=name, skills_dir=skills_dir, hooks_dir=hooks_dir, hook_config=hook_config, hook_template=hook_template)


def selected_profiles(args: argparse.Namespace) -> list[AgentProfile]:
    names = list(args.profile or [])

    if not names and not args.profile_file and not args.custom_agent:
        if not args.no_codex:
            names.append("codex")
        if not args.no_claude:
            names.append("claude")

    if args.no_codex:
        names = [name for name in names if name != "codex"]
    if args.no_claude:
        names = [name for name in names if name != "claude"]

    profiles = [BUILTIN_PROFILES[name] for name in names]
    profiles.extend(args.profile_file or [])
    profiles.extend(args.custom_agent or [])
    return profiles


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", default=".", help="Target project root.")
    parser.add_argument(
        "--profile",
        action="append",
        choices=sorted(BUILTIN_PROFILES),
        help="Install a built-in agent profile. Repeatable. Defaults to codex + claude for compatibility.",
    )
    parser.add_argument(
        "--custom-agent",
        action="append",
        type=parse_custom_agent,
        metavar="NAME:SKILLS_DIR[:HOOKS_DIR[:HOOK_CONFIG[:HOOK_TEMPLATE]]]",
        help="Install into an arbitrary agent profile.",
    )
    parser.add_argument(
        "--profile-file",
        action="append",
        type=load_profile_file,
        metavar="PATH",
        help="Install a scalar YAML profile file. Repeatable and preferred for paths containing colons.",
    )
    parser.add_argument("--no-codex", action="store_true", help="Compatibility flag: do not install the codex profile.")
    parser.add_argument("--no-claude", action="store_true", help="Compatibility flag: do not install the claude profile.")
    parser.add_argument("--no-hooks", action="store_true", help="Do not install read-learnings hooks.")
    parser.add_argument("--python-command", default="python3", help="Python command written into generated hook configs.")
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Replace managed skill and hook script files. Learning records and unrelated hook settings are always preserved.",
    )
    args = parser.parse_args()

    target_root = Path(args.target).resolve()
    if not target_root.exists():
        parser.error(f"target does not exist: {target_root}")

    profiles = selected_profiles(args)
    if not profiles:
        parser.error("no agent profiles selected")

    for profile in profiles:
        print(f"\n== Installing profile: {profile.name} ==")
        install_skills(target_root, profile, overwrite=args.overwrite)

    install_learnings(target_root)
    if not args.no_hooks:
        for profile in profiles:
            install_hooks(target_root, profile, overwrite=args.overwrite, python_command=args.python_command)
    print("")
    rules_files = ", ".join(sorted({profile.rules_file for profile in profiles}))
    print(f"[NEXT] Merge templates/self-learning/AGENTS.snippet.md into the target project instruction file(s): {rules_files}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
