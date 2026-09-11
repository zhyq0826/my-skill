import importlib.util
import json
import re
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('installer', ROOT / 'scripts/install.py')
installer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(installer)


class InstallTests(unittest.TestCase):
    def test_native_paths(self):
        for client, folder in [('cursor', '.cursor'), ('codex', '.agents'), ('claude', '.claude')]:
            self.assertEqual(installer.destination(client), Path.home() / folder / 'skills')
            with tempfile.TemporaryDirectory() as temp:
                self.assertEqual(installer.destination(client, temp), Path(temp).resolve() / folder / 'skills')

    def test_dry_run_and_full_copy(self):
        with tempfile.TemporaryDirectory() as temp:
            dest = Path(temp) / 'skills'
            names = ['axiom-scene-register', 'report-writing']
            installer.install(names, dest)
            self.assertFalse(dest.exists())
            installer.install(names, dest, apply=True)
            for name in names:
                for source in (ROOT / 'skills' / name).rglob('*'):
                    if source.is_file():
                        self.assertEqual(source.read_bytes(), (dest / name / source.relative_to(ROOT / 'skills' / name)).read_bytes())

    def test_conflict_leaves_existing_and_new_untouched(self):
        with tempfile.TemporaryDirectory() as temp:
            dest = Path(temp)
            old = dest / 'report-writing'
            old.mkdir()
            (old / 'SKILL.md').write_text('local edits')
            with self.assertRaises(FileExistsError):
                installer.install(['interview-notes', 'report-writing'], dest, True)
            self.assertFalse((dest / 'interview-notes').exists())
            self.assertEqual((old / 'SKILL.md').read_text(), 'local edits')

    def test_broken_symlink_is_not_replaced(self):
        with tempfile.TemporaryDirectory() as temp:
            dest = Path(temp)
            (dest / 'report-writing').symlink_to(dest / 'missing')
            with self.assertRaises(FileExistsError):
                installer.install(['report-writing'], dest, True)

    def test_catalog_and_portable_content(self):
        catalog = json.loads((ROOT / 'catalog.json').read_text())
        names = [item['name'] for item in catalog]
        self.assertEqual(len(names), len(set(names)))
        self.assertEqual(set(names), {p.name for p in (ROOT / 'skills').iterdir() if p.is_dir()})
        for name in names:
            source = ROOT / 'skills' / name
            self.assertTrue((source / 'agents/openai.yaml').is_file())
            body = (source / 'SKILL.md').read_text()
            self.assertRegex(body, r'\A---\nname:')
            for file in source.rglob('*'):
                self.assertFalse(file.is_symlink())
                if file.is_file():
                    text = file.read_text()
                    self.assertNotIn('/Users/', text)
                    for link in re.findall(r'\]\(([^)]+\.md)\)', text):
                        if '://' not in link:
                            self.assertTrue((file.parent / link).is_file(), str(file) + ': ' + link)


if __name__ == '__main__':
    unittest.main()
