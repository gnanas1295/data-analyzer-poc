from pydantic import BaseModel
from typing import List

class SimulationLog(BaseModel):
    timestamp: float
    altitude: int
    speed: int
    event: str

class AnalysisRequest(BaseModel):
    trainee_id: str
    simulation_log: List[SimulationLog]
