import json, sys

sys.stdout.reconfigure(encoding="utf-8")
run_file = sys.argv[1]
data = json.load(open(run_file, encoding="utf-8"))
s = data["summary"]
print(f"PASS: {s['passed_cases']} / {s['total_cases']}  accuracy={s['case_accuracy']:.4f}")
print()

fail_list = []
for r in data["results"]:
    passed = r["result"]["passed"]
    ft = r["result"].get("failure_type") or ""
    mm = r["result"].get("observed_mismatch") or ""
    exp = [t["name"] for t in r.get("expect", {}).get("tool_calls", [])]
    act = [t["name"] for t in r["result"].get("actual_tool_calls", [])]
    status = "PASS" if passed else "FAIL"
    rid = r["id"]
    print(f"{status}  {rid:42} | expect={exp} | got={act} | fail={ft} | mismatch={mm}")
    if not passed:
        fail_list.append(r)

print()
print("=== FAIL DETAILS ===")
for r in fail_list:
    rid = r["id"]
    ft = r["result"].get("failure_type") or ""
    mm = r["result"].get("observed_mismatch") or ""
    failures = r["result"].get("failures", [])
    exp_calls = r.get("expect", {}).get("tool_calls", [])
    act_calls = r["result"].get("actual_tool_calls", [])
    print(f"\n--- {rid} ---")
    print(f"  failure_type: {ft}, mismatch: {mm}")
    print(f"  expected: {json.dumps(exp_calls)}")
    print(f"  actual:   {json.dumps(act_calls)}")
    if failures:
        print(f"  failures: {failures[:2]}")
