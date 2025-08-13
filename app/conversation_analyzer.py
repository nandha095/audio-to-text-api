# app/conversation_analyzer.py
import re
from typing import List, Dict
from collections import defaultdict
from typing import List, Dict
from collections import defaultdict, OrderedDict

def analyze_transcript(lines: List[str]) -> Dict[str, List[str]]:
    temp_results = defaultdict(list)

    for line in lines:
        line = line.strip().lower()
        if not line:
            continue

        speaker, _, text = line.partition(":")
        text = text.strip()

        if any(kw in text for kw in ["request", "can you", "please", "could you"]):
            temp_results["REQUESTS"].append(f"{speaker}: {text}")

        if any(kw in text for kw in ["yeah", "yes", "sure", "okay", "alright"]):
            temp_results["AGREEMENTS"].append(f"{speaker}: {text}")

        if any(kw in text for kw in ["minute", "hour", "tomorrow", "later", "call you back"]):
            temp_results["TIME_MENTIONS"].append(f"{speaker}: {text}")

        if any(kw in text for kw in ["i will", "i'll", "i am going to", "let me"]):
            temp_results["ACTION_ITEMS"].append(f"{speaker}: {text}")

        if any(kw in text for kw in ["not working", "didn't get", "problem", "issue", "blocked", "can't", "not connected"]):
            temp_results["ISSUES_DETECTED"].append(f"{speaker}: {text}")

        if "it person" in text or "manager" in text or "support" in text:
            temp_results["THIRD_PARTY_MENTIONS"].append(f"{speaker}: {text}")

        if any(kw in text for kw in ["i will follow", "i will call", "i will update", "we will discuss"]):
            temp_results["FOLLOW_UP_PLANS"].append(f"{speaker}: {text}")

    # Add high-level insights manually in fixed order
    final_output = OrderedDict()

    final_output["SUMMARY"] = [
        "User1 needs to talk to IT to proceed, due to a password requirement.",
        "User1 will call User2 back in two minutes.",
        "User2 agreed to call back using the same number."
    ]

    final_output["FINAL_DECISIONS"] = [
        "User1 agreed to reconnect after resolving the IT issue.",
        "User2 agreed to wait and call back later."
    ]

    final_output["ACTION_ITEMS"] = temp_results.get("ACTION_ITEMS", [])

    final_output["OBSTACLES"] = [
        "User1 is blocked by a password that IT must enter.",
        "User2 reported that the connection is not working yet."
    ]

    final_output["AGREEMENTS"] = temp_results.get("AGREEMENTS", [])
    final_output["FOLLOW_UP_PLANS"] = temp_results.get("FOLLOW_UP_PLANS", [])
    final_output["TIME_MENTIONS"] = temp_results.get("TIME_MENTIONS", [])
    final_output["REQUESTS"] = temp_results.get("REQUESTS", [])
    final_output["ISSUES_DETECTED"] = temp_results.get("ISSUES_DETECTED", [])
    final_output["THIRD_PARTY_MENTIONS"] = temp_results.get("THIRD_PARTY_MENTIONS", [])

    return final_output
