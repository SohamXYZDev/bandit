#
# Copyright 2026 PyCQA
#
# SPDX-License-Identifier: Apache-2.0
import io
import unittest

from bandit.core import config
from bandit.core import manager
from bandit.core import node_visitor
from bandit.core import test_set
from bandit.plugins import yaml_load


class YamlLoadTests(unittest.TestCase):
    def setUp(self):
        self.b_conf = config.BanditConfig()
        self.mgr = manager.BanditManager(self.b_conf, "file")
        self.mgr.b_ts = test_set.BanditTestSet(
            config=self.b_conf, profile={"include": {"B506"}}
        )

    def _scan(self, code):
        visitor = node_visitor.BanditNodeVisitor(
            "tests/unit/plugins/test_yaml_load.py",
            io.BytesIO(code.encode("utf-8")),
            self.mgr.b_ma,
            self.mgr.b_ts,
            False,
            {},
            self.mgr.metrics,
        )
        visitor.process(code)
        return visitor.tester.results

    def test_safe_loaders_defined(self):
        self.assertEqual(
            ("BaseLoader", "CBaseLoader", "SafeLoader", "CSafeLoader"),
            yaml_load.SAFE_LOADERS,
        )

    def test_safe_baseloader_keyword(self):
        code = "import yaml\nyaml.load('{}', Loader=yaml.BaseLoader)"
        results = self._scan(code)
        self.assertEqual([], results)

    def test_safe_cbaseloader_keyword(self):
        code = "import yaml\nyaml.load('{}', Loader=yaml.CBaseLoader)"
        results = self._scan(code)
        self.assertEqual([], results)

    def test_safe_baseloader_imported_keyword(self):
        code = (
            "import yaml\n"
            "from yaml import BaseLoader\n"
            "yaml.load('{}', Loader=BaseLoader)"
        )
        results = self._scan(code)
        self.assertEqual([], results)

    def test_safe_cbaseloader_imported_keyword(self):
        code = (
            "import yaml\n"
            "from yaml import CBaseLoader\n"
            "yaml.load('{}', Loader=CBaseLoader)"
        )
        results = self._scan(code)
        self.assertEqual([], results)

    def test_safe_safeloader_keyword(self):
        code = "import yaml\nyaml.load('{}', Loader=yaml.SafeLoader)"
        results = self._scan(code)
        self.assertEqual([], results)

    def test_safe_csafeloader_keyword(self):
        code = "import yaml\nyaml.load('{}', Loader=yaml.CSafeLoader)"
        results = self._scan(code)
        self.assertEqual([], results)

    def test_safe_baseloader_positional(self):
        code = "import yaml\nyaml.load('{}', yaml.BaseLoader)"
        results = self._scan(code)
        self.assertEqual([], results)

    def test_safe_cbaseloader_positional(self):
        code = "import yaml\nyaml.load('{}', yaml.CBaseLoader)"
        results = self._scan(code)
        self.assertEqual([], results)

    def test_safe_safeloader_positional(self):
        code = "import yaml\nyaml.load('{}', yaml.SafeLoader)"
        results = self._scan(code)
        self.assertEqual([], results)

    def test_safe_csafeloader_positional(self):
        code = "import yaml\nyaml.load('{}', yaml.CSafeLoader)"
        results = self._scan(code)
        self.assertEqual([], results)

    def test_from_yaml_import_baseloader_call(self):
        code = (
            "from yaml import load, BaseLoader\n"
            "load('{}', Loader=BaseLoader)"
        )
        results = self._scan(code)
        self.assertEqual([], results)

    def test_unsafe_loader_keyword(self):
        code = "import yaml\nyaml.load('{}', Loader=yaml.Loader)"
        results = self._scan(code)
        self.assertEqual(1, len(results))
        self.assertEqual("B506", results[0].test_id)

    def test_unsafe_unsafeloader_keyword(self):
        code = "import yaml\nyaml.load('{}', Loader=yaml.UnsafeLoader)"
        results = self._scan(code)
        self.assertEqual(1, len(results))
        self.assertEqual("B506", results[0].test_id)

    def test_unsafe_no_loader(self):
        code = "import yaml\nyaml.load('{}')"
        results = self._scan(code)
        self.assertEqual(1, len(results))
        self.assertEqual("B506", results[0].test_id)

    def test_unsafe_loader_positional(self):
        code = "import yaml\nyaml.load('{}', yaml.Loader)"
        results = self._scan(code)
        self.assertEqual(1, len(results))
        self.assertEqual("B506", results[0].test_id)

    def test_unsafe_unsafeloader_positional(self):
        code = "import yaml\nyaml.load('{}', yaml.UnsafeLoader)"
        results = self._scan(code)
        self.assertEqual(1, len(results))
        self.assertEqual("B506", results[0].test_id)
