from fastapi import FastAPI, Form, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import Optional, Union
from logic import FarmHealthLogic

app = FastAPI()
templates = Jinja2Templates(directory="templates")

class HealthInputs(BaseModel):
    total_revenue: float
    total_expenses: float
    current_assets: float
    current_liabilities: float
    long_term_liabilities: float
    total_assets: float
    owner_equity: float
    land_area_ha: float
    commodity_dependence: float
    irrigation_access: bool
    avg_rainfall_last_5_years: float
    insurance_coverage: bool
    yield_per_ha: float
    labor_hours: float
    machinery_costs: float
    fertilizer_costs: float

@app.post("/api/health")
async def calculate_health(
    request: Request,
    # Optional Form params for fallback if JSON not present
    total_revenue: Optional[float] = Form(None),
    total_expenses: Optional[float] = Form(None),
    current_assets: Optional[float] = Form(None),
    current_liabilities: Optional[float] = Form(None),
    long_term_liabilities: Optional[float] = Form(None),
    total_assets: Optional[float] = Form(None),
    owner_equity: Optional[float] = Form(None),
    land_area_ha: Optional[float] = Form(None),
    commodity_dependence: Optional[float] = Form(None),
    irrigation_access: Optional[str] = Form(None),
    avg_rainfall_last_5_years: Optional[float] = Form(None),
    insurance_coverage: Optional[str] = Form(None),
    yield_per_ha: Optional[float] = Form(None),
    labor_hours: Optional[float] = Form(None),
    machinery_costs: Optional[float] = Form(None),
    fertilizer_costs: Optional[float] = Form(None),
):
    try:
        # Try to get JSON body
        data = await request.json()
        inputs = HealthInputs(**data)
    except Exception:
        # If JSON parsing fails, fallback to form data
        # Check that all form fields are provided
        form_values = [
            total_revenue, total_expenses, current_assets, current_liabilities,
            long_term_liabilities, total_assets, owner_equity, land_area_ha,
            commodity_dependence, irrigation_access, avg_rainfall_last_5_years,
            insurance_coverage, yield_per_ha, labor_hours, machinery_costs,
            fertilizer_costs
        ]
        if any(v is None for v in form_values):
            raise HTTPException(status_code=422, detail="Missing form fields")

        # Convert irrigation_access and insurance_coverage to bool
        irrigation_access_bool = irrigation_access.lower() == "true"
        insurance_coverage_bool = insurance_coverage.lower() == "true"

        inputs = HealthInputs(
            total_revenue=total_revenue,
            total_expenses=total_expenses,
            current_assets=current_assets,
            current_liabilities=current_liabilities,
            long_term_liabilities=long_term_liabilities,
            total_assets=total_assets,
            owner_equity=owner_equity,
            land_area_ha=land_area_ha,
            commodity_dependence=commodity_dependence,
            irrigation_access=irrigation_access_bool,
            avg_rainfall_last_5_years=avg_rainfall_last_5_years,
            insurance_coverage=insurance_coverage_bool,
            yield_per_ha=yield_per_ha,
            labor_hours=labor_hours,
            machinery_costs=machinery_costs,
            fertilizer_costs=fertilizer_costs,
        )

    logic = FarmHealthLogic(inputs)
    result = logic.compute_scores()
    return JSONResponse(result)
