from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
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
async def calculate_health(inputs: HealthInputs):
    logic = FarmHealthLogic(inputs)
    result = logic.compute_scores()
    return result

@app.get("/", response_class=HTMLResponse)
async def form_get(request: Request):
    return templates.TemplateResponse("health_form.html", {"request": request})

@app.post("/submit", response_class=HTMLResponse)
async def form_post(
    request: Request,
    total_revenue: float = Form(...),
    total_expenses: float = Form(...),
    current_assets: float = Form(...),
    current_liabilities: float = Form(...),
    long_term_liabilities: float = Form(...),
    total_assets: float = Form(...),
    owner_equity: float = Form(...),
    land_area_ha: float = Form(...),
    commodity_dependence: float = Form(...),
    irrigation_access: str = Form(...),
    avg_rainfall_last_5_years: float = Form(...),
    insurance_coverage: str = Form(...),
    yield_per_ha: float = Form(...),
    labor_hours: float = Form(...),
    machinery_costs: float = Form(...),
    fertilizer_costs: float = Form(...),
):
    irrigation_access_bool = irrigation_access.lower() == "true"
    insurance_coverage_bool = insurance_coverage.lower() == "true"

    net_income = total_revenue - total_expenses

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
    scores = logic.compute_scores()

    inputs_dict = inputs.dict()
    inputs_dict["net_income"] = net_income

    return templates.TemplateResponse(
        "health_result.html",
        {
            "request": request,
            "inputs_json": inputs_dict,
            "scores": scores,
        }
    )
