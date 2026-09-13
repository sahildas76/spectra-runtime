import time
import copy
from typing import Dict, Any

class EnterpriseEnvironmentSimulator:
    def __init__(self):
        self.live_state = {
            "cluster_id": "PROD-US-EAST-04",
            "service_name": "Core-Gateway",
            "db_connection_pool": {"max": 100, "active": 22, "status": "HEALTHY"},
            "memory_usage_pct": 38.5,
            "cpu_utilization_pct": 24.1,
            "error_rate_pct": 0.02,
            "active_circuit_breaker": False,
            "financial_downtime_cost_per_minute": 1250.0
        }

    def inject_incident(self, incident_type: str = "db_pool_exhaustion") -> Dict[str, Any]:
        ts = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

        if incident_type == "k8s_oom_kill":
            self.live_state["memory_usage_pct"] = 98.6
            self.live_state["cpu_utilization_pct"] = 91.2
            self.live_state["error_rate_pct"] = 62.4
            self.live_state["active_circuit_breaker"] = True
            return {
                "incident_id": f"INC-OOM-{int(time.time())}",
                "severity": "P1-CRITICAL",
                "service": "Microservice-Worker-Fleet",
                "affected_cluster": "K8S-CLUSTER-EU-01",
                "timestamp": ts,
                "error_log": "[FATAL] Container worker-pod-89a killed: OOMKilled (Exit Code 137). Memory cgroup limit exceeded (512MiB). Thread stack leak detected.",
                "downtime_cost_per_min": 1400.0,
                "raw_system_telemetry": copy.deepcopy(self.live_state)
            }

        elif incident_type == "api_throttling":
            self.live_state["memory_usage_pct"] = 44.0
            self.live_state["cpu_utilization_pct"] = 79.5
            self.live_state["error_rate_pct"] = 38.1
            self.live_state["active_circuit_breaker"] = True
            return {
                "incident_id": f"INC-THROTTLE-{int(time.time())}",
                "severity": "P2-HIGH",
                "service": "Payment-ThirdParty-Adapter",
                "affected_cluster": "PAYMENT-GW-US-02",
                "timestamp": ts,
                "error_log": "[WARN] HTTP 429 Too Many Requests received from downstream Stripe Core. Rate limit: 200 req/sec exceeded. Retry-After header: 30s.",
                "downtime_cost_per_min": 850.0,
                "raw_system_telemetry": copy.deepcopy(self.live_state)
            }

        # Default: db_pool_exhaustion
        self.live_state["db_connection_pool"]["active"] = 100
        self.live_state["db_connection_pool"]["status"] = "EXHAUSTED"
        self.live_state["memory_usage_pct"] = 92.4
        self.live_state["cpu_utilization_pct"] = 88.7
        self.live_state["error_rate_pct"] = 44.8
        self.live_state["active_circuit_breaker"] = True
        return {
            "incident_id": f"INC-DB-{int(time.time())}",
            "severity": "P1-CRITICAL",
            "service": "Core-Transaction-Gateway",
            "affected_cluster": "PROD-US-EAST-04",
            "timestamp": ts,
            "error_log": "[FATAL] org.postgresql.util.PSQLException: Connection pool exhausted! Active: 100/100. Unable to allocate connection for worker-thread-4481. HTTP 503 spike.",
            "downtime_cost_per_min": 1250.0,
            "raw_system_telemetry": copy.deepcopy(self.live_state)
        }

    def get_state(self) -> Dict[str, Any]:
        return copy.deepcopy(self.live_state)
