"""Offline launcher regressions: aliases share code, not config or state."""
import json
import os
from pathlib import Path
import subprocess
import shutil
import tempfile
import unittest

SOURCE = Path(__file__).resolve().parents[1] / 'toolreview'

class AliasTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.project = self.root / 'project'; self.project.mkdir()
        self.env = {'PATH': os.environ['PATH'], 'HOME': str(self.root),
                    'XDG_CONFIG_HOME': str(self.root / 'config'),
                    'XDG_CACHE_HOME': str(self.root / 'cache')}
        self.aliases = []
        for name in ('toolreview', 'toolreview-experimental'):
            alias = self.root / name; alias.symlink_to(SOURCE); self.aliases.append(alias)
            config = self.root / 'config' / name / 'config.toml'
            config.parent.mkdir(parents=True)
            config.write_text('[resolver]\nmodel = ' + json.dumps(name + '-model') + '\n')
    def run_alias(self, alias, *args):
        return subprocess.run([str(alias), *args], cwd=self.project, env=self.env,
                              text=True, capture_output=True, check=True, timeout=10).stdout
    def test_aliases_keep_config_cache_and_state_separate(self):
        versions = []
        for alias in self.aliases:
            name = alias.name
            cfg = self.run_alias(alias, 'config')
            self.assertIn('resolver.model = ' + json.dumps(name + '-model'), cfg)
            self.assertTrue((self.root / 'cache' / 'toolreview' / name).is_dir())
            # An unreadable event reports the selected state namespace.
            event = json.dumps({'cwd': str(self.project)})
            p = subprocess.run([str(alias), 'hook'], input=event, cwd=self.project,
                               env=self.env, text=True, capture_output=True, timeout=10)
            self.assertEqual(p.returncode, 2)
            self.assertIn('no .' + name + '/', p.stderr)
            versions.append(self.run_alias(alias, 'version'))
        self.assertEqual(versions[0], versions[1])
    def test_different_checkout_versions_remain_independent(self):
        # Disposable snapshots model worktree files without editing the installed code.
        checkouts = []
        for index, alias in enumerate(self.aliases):
            checkout = self.root / ('checkout-' + str(index)); checkout.mkdir()
            script = checkout / 'toolreview'; shutil.copy2(SOURCE, script)
            alias.unlink(); alias.symlink_to(script); checkouts.append(script)
        stable_before = self.run_alias(self.aliases[0], 'version')
        experiment_before = self.run_alias(self.aliases[1], 'version')
        checkouts[1].write_bytes(checkouts[1].read_bytes() + b'\n# experimental test revision\n')
        self.assertEqual(self.run_alias(self.aliases[0], 'version'), stable_before)
        self.assertNotEqual(self.run_alias(self.aliases[1], 'version'), experiment_before)
        self.assertIn('toolreview-experimental-model', self.run_alias(self.aliases[1], 'config'))

    def test_both_aliases_can_read_one_private_config(self):
        private = self.root / 'private.toml'; private.write_text('[resolver]\nmodel = "shared-private"\n')
        for alias in self.aliases:
            config = self.root / 'config' / alias.name / 'config.toml'
            config.unlink(); config.symlink_to(private)
            self.assertIn('resolver.model = "shared-private"', self.run_alias(alias, 'config'))
        override = self.root / 'override.toml'; override.write_text('[resolver]\nmodel = "override"\n')
        self.env['TOOLREVIEW_CONFIG'] = str(override)
        self.assertIn('resolver.model = "override"', self.run_alias(self.aliases[1], 'config'))

if __name__ == '__main__':
    unittest.main()
