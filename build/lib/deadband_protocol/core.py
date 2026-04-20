"""Core deadband engine — P0 blocks danger, P1 finds safe channels, P2 optimizes."""
import re
from typing import Optional


class DeadbandResult:
    __slots__ = ("passed", "p0_violations", "safe_channel", "channel_confidence")
    
    def __init__(self, passed: bool, p0_violations: list = None,
                 safe_channel: str = None, channel_confidence: float = 0.0):
        self.passed = passed
        self.p0_violations = p0_violations or []
        self.safe_channel = safe_channel
        self.channel_confidence = channel_confidence


class Deadband:
    """
    Navigate by knowing where the rocks are NOT.
    
    P0: Block dangerous patterns
    P1: Identify safe channel
    P2: Optimize within the safe channel
    """
    
    DEFAULT_DANGEROUS = [
        r"rm\s+-rf", r"DROP\s+TABLE", r"DELETE\s+FROM",
        r"chmod\s+777", r"eval\s*\(", r"sudo\s+rm",
        r"__import__\(", r"os\.system\(", r"subprocess\.(call|run)\(",
        r">\s*/dev/sda", r"mkfs\.", r"dd\s+if=",
        r"shutdown\s+now", r"curl\s+.*\|\s*sh",
        r"wget\s+.*\|\s*sh",
    ]
    
    def __init__(self, dangerous_patterns=None, custom_blocklist=None):
        self.patterns = [re.compile(p, re.IGNORECASE) for p in (dangerous_patterns or self.DEFAULT_DANGEROUS)]
        self.blocklist = set(w.lower() for w in (custom_blocklist or []))
    
    def check(self, text, channels=None):
        violations = []
        for pat in self.patterns:
            m = pat.search(text)
            if m:
                violations.append(m.group())
        text_lower = text.lower()
        for word in self.blocklist:
            if word in text_lower:
                violations.append(word)
        if violations:
            return DeadbandResult(passed=False, p0_violations=violations)
        if channels:
            channel, confidence = channels.route(text)
            return DeadbandResult(passed=True, safe_channel=channel, channel_confidence=confidence)
        return DeadbandResult(passed=True, safe_channel="general", channel_confidence=0.5)
    
    def filter(self, text):
        for pat in self.patterns:
            text = pat.sub("[BLOCKED]", text)
        return text
    
    def add_pattern(self, pattern):
        self.patterns.append(re.compile(pattern, re.IGNORECASE))
    
    def add_blocklist(self, word):
        self.blocklist.add(word.lower())
