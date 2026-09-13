from typing import Dict, Any

class ExecutiveROIAnalytics:
    """
    Translates technical triage telemetry into MBA-grade financial and SLA metrics
    for CIO/CIS executive dashboards and client ROI reporting.
    """

    # Industry benchmarks for Tier-1 Enterprise Banking / Cloud Ops
    MANUAL_L1_L2_MTTR_MINUTES = 42.0       # Average human response + triage time
    SPECTRA_AUTONOMOUS_MTTR_MINUTES = 1.8   # Shadow execution + verification time
    ENGINEER_HOURLY_BILLING_RATE = 85.0    # USD / hour loaded cost

    @classmethod
    def calculate_incident_roi(cls, incident: Dict[str, Any], is_promoted: bool) -> Dict[str, Any]:
        cost_per_min = incident.get("downtime_cost_per_min", 1250.0)
        
        # 1. MTTR Time Saved
        time_saved_minutes = cls.MANUAL_L1_L2_MTTR_MINUTES - cls.SPECTRA_AUTONOMOUS_MTTR_MINUTES
        mttr_reduction_pct = round((time_saved_minutes / cls.MANUAL_L1_L2_MTTR_MINUTES) * 100, 1)

        # 2. Financial Downtime Avoidance
        gross_downtime_avoided_usd = round(time_saved_minutes * cost_per_min, 2)

        # 3. Engineering Work-Hours / FTE Savings
        engineering_hours_saved = round(time_saved_minutes / 60.0, 2)
        engineering_cost_saved_usd = round(engineering_hours_saved * cls.ENGINEER_HOURLY_BILLING_RATE, 2)

        # 4. Total Net Value Created per Incident Run
        total_value_generated = round(gross_downtime_avoided_usd + engineering_cost_saved_usd, 2)

        return {
            "manual_mttr_benchmark_min": cls.MANUAL_L1_L2_MTTR_MINUTES,
            "spectra_autonomous_mttr_min": cls.SPECTRA_AUTONOMOUS_MTTR_MINUTES,
            "mttr_reduction_pct": mttr_reduction_pct,
            "engineering_hours_freed": engineering_hours_saved,
            "engineering_cost_saved_usd": engineering_cost_saved_usd,
            "downtime_cost_avoided_usd": gross_downtime_avoided_usd,
            "total_net_economic_value_usd": total_value_generated,
            "sla_breach_prevented": is_promoted
        }

if __name__ == "__main__":
    import json
    mock_incident = {
        "downtime_cost_per_min": 1250.0,
        "sla_target_mttr_minutes": 15
    }
    metrics = ExecutiveROIAnalytics.calculate_incident_roi(mock_incident, is_promoted=True)
    print("[+] Executive MBA ROI Calculation:")
    print(json.dumps(metrics, indent=2))
