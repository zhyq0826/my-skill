#!/usr/bin/env python3
"""Preview or copy selected skills into a client's native skills directory."""
import argparse
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIRECTORIES = {'cursor': '.cursor/skills', 'codex': '.agents/skills', 'claude': '.claude/skills'}


def destination(client, project=None, dest=None):
    if dest:
        return Path(dest).expanduser().resolve()
    base = Path(project).expanduser().resolve() if project else Path.home()
    return base / DIRECTORIES[client]


def install(names, target, apply=False, client='codex'):
    if client not in DIRECTORIES:
        raise ValueError(f'Unknown client: {client}')
    catalog = json.loads((ROOT / 'catalog.json').read_text(encoding='utf-8'))
    explicit_only = {item['name'] for item in catalog if item.get('explicit_only')}
    sources = [ROOT / 'skills' / name for name in names]
    # Preflight the entire selection so a conflict does not leave a partial install.
    for source in sources:
        if not (source / 'SKILL.md').is_file():
            raise ValueError(f'Missing SKILL.md: {source.name}')
        if target == source or source in target.parents:
            raise ValueError('Destination must not be inside a source skill')
        result = target / source.name
        if result.exists() or result.is_symlink():
            raise FileExistsError(f'Existing skill; compare and back up before installing: {result}')
    for source in sources:
        print(f'{"COPY" if apply else "PLAN"} {source.name} -> {target / source.name}')
    if not apply:
        return
    target.mkdir(parents=True, exist_ok=True)
    for source in sources:
        shutil.copytree(source, target / source.name)
        if client in ('cursor', 'claude') and source.name in explicit_only:
            entry = target / source.name / 'SKILL.md'
            body = entry.read_text(encoding='utf-8')
            # Keep one canonical skill; add the client's native invocation flag.
            entry.write_text(body.replace('\n---\n', '\ndisable-model-invocation: true\n---\n', 1), encoding='utf-8')


def main():
    catalog = json.loads((ROOT / 'catalog.json').read_text(encoding='utf-8'))
    available = [item['name'] for item in catalog]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--client', choices=DIRECTORIES)
    location = parser.add_mutually_exclusive_group()
    location.add_argument('--project', help='Install into this project instead of the user directory')
    location.add_argument('--dest', help='Explicit skills directory (useful for isolated testing)')
    parser.add_argument('--skills', nargs='+', choices=available)
    parser.add_argument('--apply', action='store_true', help='Write files; otherwise preview only')
    parser.add_argument('--list', action='store_true')
    args = parser.parse_args()
    if args.list:
        for item in catalog:
            print(f"{item['name']:26} {item['category']} · {item['title']}")
        return
    if not args.client:
        parser.error('--client is required unless --list is used')
    if args.project and not Path(args.project).expanduser().is_dir():
        parser.error('--project must be an existing directory')
    try:
        install(list(dict.fromkeys(args.skills or available)), destination(args.client, args.project, args.dest), args.apply, client=args.client)
    except (ValueError, OSError) as error:
        parser.exit(1, f'{error}\n')


if __name__ == '__main__':
    main()
