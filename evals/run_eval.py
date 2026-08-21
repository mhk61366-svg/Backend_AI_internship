import json
import requests

cases = json.load(open("evals/cases.json"))
correct = 0
failures = []

for case in cases:
    res = requests.post("http://127.0.0.1:8000/llm", json={"text": case["input"]})
    got = res.json().get("category")
    if got == case["expected_category"]:
        correct += 1
    else:
        failures.append((case["input"], case["expected_category"], got))

print(f"{correct}/{len(cases)} correct")
for text, expected, got in failures:
    print(f"FAIL: '{text}' expected={expected} got={got}")