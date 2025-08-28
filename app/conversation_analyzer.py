# app/conversation_analyzer.py
import re
from typing import List, Dict
from collections import defaultdict
from typing import List, Dict
from collections import defaultdict, OrderedDict

def analyze_transcript(lines):
    insights = {
        "SUMMARY": [],
        "FINAL_DECISIONS": [],
        "ACTION_ITEMS": [],
        "OBSTACLES": [],
        "AGREEMENTS": [],
        "FOLLOW_UP_PLANS": [],
        "TIME_MENTIONS": [],
        "REQUESTS": [],
        "ISSUES_DETECTED": [],
        "THIRD_PARTY_MENTIONS": [],
    }

    # Combine transcript into text for summary
    full_text = " ".join(lines).lower()
    if "call" in full_text:
        insights["SUMMARY"].append("The conversation is about setting up and testing calls.")
    if "application" in full_text or "install" in full_text:
        insights["SUMMARY"].append("User2 guided User1 through application setup.")
    if "okay" in full_text or "i'll do" in full_text:
        insights["SUMMARY"].append("User1 confirmed they will follow instructions.")

    # Pattern checks
    for line in lines:
        l = line.strip()

        # Decisions / action confirmations
        if re.search(r"\bi will\b|\bi'll\b|\bi am going to\b", l, re.I):
            insights["FINAL_DECISIONS"].append(l)
            insights["ACTION_ITEMS"].append(l)

        # Agreements
        if re.search(r"\bokay\b|\byeah\b|\bsure\b|\bthank you\b", l, re.I):
            insights["AGREEMENTS"].append(l)

        # Obstacles / Issues
        if "not" in l.lower() or "problem" in l.lower() or "can't" in l.lower():
            insights["OBSTACLES"].append(l)
            insights["ISSUES_DETECTED"].append(l)

        # Follow-up
        if re.search(r"\bi will\b|\bi'll\b|\blet me\b|\bwe will\b", l, re.I):
            insights["FOLLOW_UP_PLANS"].append(l)

        # Time mentions
        if re.search(r"yesterday|today|tomorrow|next week|in a minute", l, re.I):
            insights["TIME_MENTIONS"].append(l)

        # Requests
        if re.search(r"\bcan you\b|\bcould you\b|\bplease\b|\bi need\b", l, re.I):
            insights["REQUESTS"].append(l)

        # Third-party mentions
        if re.search(r"\b(anil|ashish|it person|advocate)\b", l, re.I):
            insights["THIRD_PARTY_MENTIONS"].append(l)

    return insights
