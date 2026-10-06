import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest


SOURCE = Path(__file__).resolve().parents[1]
CHEZMOI = shutil.which("chezmoi")
NAMES = ("zshrc", "zprofile", "gitconfig")


class LocalEntrypointsTest(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.config = self.root / "chezmoi.toml"
        self.config.write_text(
            '[data]\nname = "Test User"\nemail = "test@example.org"\n'
            'useOhMyZsh = false\nautoInstallZsh = false\ncavemanAgents = []\n'
        )
        self.command = [
            CHEZMOI, "--source", str(SOURCE), "--destination", str(self.root),
            "--config", str(self.config), "--persistent-state", str(self.root / "state.db"),
        ]

    def run_command(self, command, **kwargs):
        return subprocess.run(command, capture_output=True, text=True, timeout=20, **kwargs)

    def apply(self):
        targets = [self.root / f".{name}{suffix}" for name in NAMES for suffix in ("", ".remote")]
        targets.append(self.root / "15-migrate-local-entrypoints.sh")
        return self.run_command(self.command + ["apply", "--include", "files,scripts"] + list(map(str, targets)))

    def seed(self, revision):
        originals = {}
        for name in NAMES:
            template = subprocess.check_output(
                ["git", "-C", str(SOURCE), "show", f"{revision}:dot_{name}.tmpl"], text=True
            )
            result = self.run_command(self.command + ["execute-template"], input=template)
            self.assertEqual(result.returncode, 0, result.stderr)
            addition = '\n# installer addition\n' if name != "gitconfig" else '\n[alias]\n    local-test = status\n'
            originals[name] = result.stdout + addition
            (self.root / f".{name}").write_text(originals[name])
            local = '# local override\n' if name != "gitconfig" else '[user]\n    email = local@example.org\n'
            (self.root / f".{name}.local").write_text(local)
        return originals

    def check_migration(self, revision):
        originals = self.seed(revision)
        result = self.apply()
        self.assertEqual(result.returncode, 0, result.stderr)
        backup = self.root / ".local/state/chezmoi/local-entrypoints-backup"
        migrated = {}
        for name in NAMES:
            self.assertEqual((backup / f".{name}").read_text(), originals[name])
            self.assertTrue((backup / f".{name}.local").exists())
            self.assertFalse((self.root / f".{name}.local").exists())
            migrated[name] = (self.root / f".{name}").read_text()
            self.assertEqual(migrated[name].count(f".{name}.remote"), 1)
        self.assertIn("# installer addition", migrated["zshrc"])
        self.assertIn("# local override", migrated["zshrc"])
        self.assertIn("PNPM_HOME", migrated["zprofile"])
        self.assertIn("ROS_LOCALHOST_ONLY", migrated["zprofile"])
        self.assertNotIn("PNPM_HOME", (self.root / ".zprofile.remote").read_text())
        self.assertNotIn("nvm", (self.root / ".zshrc.remote").read_text())
        if revision == "1ef8c4e":
            self.assertIn('source "$NVM_DIR/nvm.sh"', migrated["zshrc"])
            self.assertIn("apps-bin-path.sh", migrated["zprofile"])
        env = dict(os.environ, HOME=str(self.root), GIT_CONFIG_GLOBAL=str(self.root / ".gitconfig"))
        result = self.run_command(["git", "config", "--global", "user.email"], env=env)
        self.assertEqual(result.stdout.strip(), "local@example.org")
        result = self.run_command(["git", "config", "--global", "--includes", "pull.ff"], env=env)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.strip(), "only")
        result = self.run_command(["git", "config", "--global", "user.name", "Changed Locally"], env=env)
        self.assertEqual(result.returncode, 0, result.stderr)
        migrated["gitconfig"] = (self.root / ".gitconfig").read_text()
        result = self.apply()
        self.assertEqual(result.returncode, 0, result.stderr)
        script = self.run_command(self.command + ["execute-template"], input=(SOURCE / "run_once_after_15-migrate-local-entrypoints.sh.tmpl").read_text())
        result = self.run_command(["sh"], input=script.stdout)
        self.assertEqual(result.returncode, 0, result.stderr)
        for name in NAMES:
            self.assertEqual((self.root / f".{name}").read_text(), migrated[name])

    def test_current_layout(self):
        self.check_migration("1ef8c4e")

    def test_previous_layout(self):
        self.check_migration("00ee7cd")

    def test_fresh_install_preserves_later_additions(self):
        result = self.apply()
        self.assertEqual(result.returncode, 0, result.stderr)
        expected = {}
        for name in NAMES:
            path = self.root / f".{name}"
            expected[name] = path.read_text() + "\n# added locally\n"
            path.write_text(expected[name])
        result = self.apply()
        self.assertEqual(result.returncode, 0, result.stderr)
        for name in NAMES:
            self.assertEqual((self.root / f".{name}").read_text(), expected[name])
        self.assertNotIn("nvm", expected["zshrc"])

    def test_unknown_layout_leaves_all_entrypoints_intact(self):
        originals = self.seed("1ef8c4e")
        originals["gitconfig"] = "[user]\n    name = Unknown Layout\n"
        (self.root / ".gitconfig").write_text(originals["gitconfig"])
        result = self.apply()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("No entry points were changed", result.stderr)
        for name in NAMES:
            self.assertEqual((self.root / f".{name}").read_text(), originals[name])
            self.assertTrue((self.root / f".{name}.local").exists())


if __name__ == "__main__":
    unittest.main()
