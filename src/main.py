from fastapi import FastAPI, Depends
from .models import AnalysisRequest
from .analysis import analyze_simulation_data
from .database import get_container
import datetime
from azure.cosmos.container import ContainerProxy

app = FastAPI()


@app.get("/")
def read_root():
    return {"status": "ok", "service": "VRAI Simulation Data Analyzer API"}


@app.post("/analyze")
def analyze_data(
    request: AnalysisRequest, container: ContainerProxy = Depends(get_container)
):
    # Call the analysis function instead of saving directly
    response_data = analyze_simulation_data(request)
    return {
        "trainee_id": request.trainee_id,
        "simulation_timestamp_utc": datetime.datetime.now(datetime.UTC).isoformat(),
        "input_data": {
            "simulation_log": [log.model_dump() for log in request.simulation_log]
        },
        "analysis_summary": response_data,
    }

    saved_data = save_analysis_result(response_data, container)

    return saved_data
