import unittest

from quant_skillkit.hermes_adapter import build_hermes_manifest


class HermesAdapterTests(unittest.TestCase):
    def test_manifest_contains_tools_endpoint(self) -> None:
        manifest = build_hermes_manifest("http://localhost:9999")
        self.assertEqual(manifest["tools_endpoint"], "http://localhost:9999/tools")
        self.assertTrue(any(tool["name"] == "quant.strategy.backtest" for tool in manifest["tools"]))


if __name__ == "__main__":
    unittest.main()
