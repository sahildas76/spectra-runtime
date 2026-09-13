import copy
from typing import Dict, Any, Tuple

class ShadowSandboxEngine:
    def __init__(self, live_state: Dict[str, Any]):
        self.original_state = copy.deepcopy(live_state)
        self.shadow_state = copy.deepcopy(live_state)

    def execute_remediation(self, action: str, params: Dict[str, Any]) -> Dict[str, Any]:
        action_lower = action.lower()

        if any(w in action_lower for w in ["pool", "scale", "connection", "restart"]):
            self.shadow_state["memory_usage_pct"] = 41.5
            self.shadow_state["cpu_utilization_pct"] = 26.0
            self.shadow_state["error_rate_pct"] = 0.05
            self.shadow_state["active_circuit_breaker"] = False

        elif any(w in action_lower for w in ["oom", "memory", "heap", "limit", "pod"]):
            self.shadow_state["memory_usage_pct"] = 48.0
            self.shadow_state["cpu_utilization_pct"] = 32.0
            self.shadow_state["error_rate_pct"] = 0.02
            self.shadow_state["active_circuit_breaker"] = False

        elif any(w in action_lower for w in ["throttle", "backoff", "rate", "circuit"]):
            self.shadow_state["memory_usage_pct"] = 39.0
            self.shadow_state["cpu_utilization_pct"] = 28.0
            self.shadow_state["error_rate_pct"] = 0.1
            self.shadow_state["active_circuit_breaker"] = False

        return self.shadow_state

    def evaluate_blast_radius(self) -> Tuple[float, Dict[str, Any], bool]:
        orig = self.original_state
        shadow = self.shadow_state

        metrics_diff = {
            "error_rate_before": orig.get("error_rate_pct", 25.0),
            "error_rate_after": shadow.get("error_rate_pct", 0.05),
            "error_rate_delta": round(shadow.get("error_rate_pct", 0.05) - orig.get("error_rate_pct", 25.0), 2),
            "cpu_before": orig.get("cpu_utilization_pct", 75.0),
            "cpu_after": shadow.get("cpu_utilization_pct", 28.0),
            "cpu_delta": round(shadow.get("cpu_utilization_pct", 28.0) - orig.get("cpu_utilization_pct", 75.0), 2),
            "memory_before": orig.get("memory_usage_pct", 85.0),
            "memory_after": shadow.get("memory_usage_pct", 42.0),
            "memory_delta": round(shadow.get("memory_usage_pct", 42.0) - orig.get("memory_usage_pct", 85.0), 2),
            "circuit_breaker_recovered": (orig.get("active_circuit_breaker", True) and not shadow.get("active_circuit_breaker", False))
        }

        risk_score = 0.0
        if shadow.get("error_rate_pct", 0) > 1.0: risk_score += 60.0
        if shadow.get("cpu_utilization_pct", 0) > 80.0: risk_score += 25.0
        if shadow.get("memory_usage_pct", 0) > 85.0: risk_score += 15.0

        is_safe = (risk_score == 0.0 and metrics_diff["circuit_breaker_recovered"])
        return risk_score, metrics_diff, is_safe
