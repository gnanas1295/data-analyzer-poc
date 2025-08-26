import pandas as pd
import logging
from .models import AnalysisRequest

logger = logging.getLogger(__name__)


def analyze_simulation_data(request: AnalysisRequest):
    try:
        print("request:", request)
        df = pd.DataFrame([log.model_dump() for log in request.simulation_log])

        performance_score = 80  # Placeholder

        analysis_summary = {
            "performance_score": performance_score,
            "total_duration_seconds": df["timestamp"].max(),
            "average_speed": df["speed"].mean(),
            "critical_events": {
                "overspeed_incidents": len(df[df["speed"] > 300]),
                "unstable_approach_events": len(df[df["altitude"] < 1000]),
            },
        }

        # Only add cosmos metadata if config is available and valid
        try:
            from .config import get_cosmos_config

            cosmos_config = get_cosmos_config()
            if cosmos_config and cosmos_config.validate_config():
                analysis_summary["cosmos_config"] = {
                    "database": cosmos_config.database_name,
                    "container": cosmos_config.container_name,
                }

                # Try to save to cosmos and add save status to response
                try:
                    from .database import save_analysis_result

                    save_result = save_analysis_result(analysis_summary.copy())
                    analysis_summary["save_status"] = save_result
                except Exception as save_error:
                    logger.error(f"Failed to save analysis result: {save_error}")
                    analysis_summary["save_status"] = {
                        "saved": False,
                        "reason": str(save_error),
                    }

        except Exception as e:
            logger.warning(f"Cosmos DB config not available: {e}")
            # Continue without cosmos metadata

        return analysis_summary

    except Exception as e:
        logger.error(f"Error in analyze_simulation_data: {e}")
        # Return basic analysis even if there are errors
        return {
            "performance_score": 0,
            "total_duration_seconds": 0,
            "average_speed": 0,
            "critical_events": {
                "overspeed_incidents": 0,
                "unstable_approach_events": 0,
            },
            "error": "Analysis failed, returning default values",
        }
