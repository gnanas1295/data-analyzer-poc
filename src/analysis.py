import pandas as pd
from .models import AnalysisRequest

def analyze_simulation_data(request: AnalysisRequest):
    df = pd.DataFrame([log.model_dump() for log in request.simulation_log])

    performance_score = 80  # Placeholder

    analysis_summary = {
        "performance_score": performance_score,
        "total_duration_seconds": df["timestamp"].max(),
        "average_speed": df["speed"].mean(),
        "critical_events": {
            "overspeed_incidents": len(df[df["speed"] > 300]),
            "unstable_approach_events": len(df[df["altitude"] < 1000])
        }
    }

    return analysis_summary
