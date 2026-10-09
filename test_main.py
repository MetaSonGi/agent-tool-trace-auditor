import json,unittest
from pathlib import Path
from main import *
class Tests(unittest.TestCase):
 def sample(self):return json.loads(Path(__file__).with_name("sample-input.json").read_text())

 def test_missing(self):self.assertEqual({x["reason"] for x in run(self.sample())["violations"]},{"approval_missing","stale_or_unknown_state"})
 def test_valid(self):
  d=self.sample();d["trace"][2].update(approval_id="a1",observed_version=7);self.assertTrue(run(d)["allowed"]);self.assertFalse(run(d)["executed_actions"])
 def test_tool_citation(self):
  d=self.sample();d["trace"][0]["tool"]="shell";d["trace"][1]["citations"]=[];r={x["reason"] for x in run(d)["violations"]};self.assertTrue({"tool_not_allowed","citation_missing"}<=r)
 def test_order_duplicate(self):
  d=self.sample();d["trace"][1].update(step=1,event_id="e1");r={x["reason"] for x in run(d)["violations"]};self.assertTrue({"non_monotonic_step","duplicate_event_id"}<=r)

if __name__=="__main__":unittest.main()
