"""Inspect setup declarations without invoking packaging or importing ROS."""

import ast
import runpy
import sys
import unittest
import xml.etree.ElementTree as ET
from types import ModuleType
from unittest.mock import patch

from offline_support import ROOT, TREES


def package_metadata(path):
    result = {}
    setuptools = ModuleType("setuptools")
    setuptools.setup = lambda **kwargs: result.update(kwargs)
    setuptools.find_packages = lambda **kwargs: [path.parent.name]
    with patch.dict(sys.modules, {"setuptools": setuptools}):
        runpy.run_path(str(path))
    return result


class PackagingTests(unittest.TestCase):
    def test_every_python_package_installs_existing_ament_marker(self):
        for tree in TREES:
            for setup in sorted((ROOT / tree).rglob("setup.py")):
                with self.subTest(package=str(setup.relative_to(ROOT))):
                    metadata = package_metadata(setup)
                    expected = f"resource/{metadata['name']}"
                    installed = dict(metadata["data_files"])
                    self.assertIn(expected, installed.get(
                        "share/ament_index/resource_index/packages", []))
                    self.assertTrue((setup.parent / expected).is_file())

    def test_console_entry_points_resolve_to_source_functions(self):
        for tree in TREES:
            for setup in sorted((ROOT / tree).rglob("setup.py")):
                metadata = package_metadata(setup)
                for entry in metadata["entry_points"]["console_scripts"]:
                    with self.subTest(package=str(setup), entry=entry):
                        module, function = entry.split("=", 1)[1].strip().split(":")
                        source = setup.parent / (module.replace(".", "/") + ".py")
                        parsed = ast.parse(source.read_text())
                        self.assertIn(function, [n.name for n in parsed.body
                                                if isinstance(n, ast.FunctionDef)])

    def test_package_names_agree_with_setup(self):
        for tree in TREES:
            for setup in sorted((ROOT / tree).rglob("setup.py")):
                with self.subTest(package=str(setup)):
                    name = ET.parse(setup.parent / "package.xml").findtext("name")
                    self.assertEqual(name, package_metadata(setup)["name"])


if __name__ == "__main__":
    unittest.main()
