class FarmHealthLogic:
    def __init__(self, inputs):
        self.inputs = inputs
        self.net_income = inputs.total_revenue - inputs.total_expenses

        if not (1 <= self.inputs.yield_per_ha <= 50000):
            raise ValueError(
                f"yield_per_ha value {self.inputs.yield_per_ha} seems unrealistic for kg/ha. "
                "Please ensure it is entered in kilograms per hectare (kg/ha)."
            )

    def compute_metrics(self):
        liquidity = self.inputs.current_assets / (self.inputs.current_liabilities + 1e-5)
        debt_asset = (self.inputs.current_liabilities + self.inputs.long_term_liabilities) / (self.inputs.total_assets + 1e-5)
        profit_margin = self.net_income / (self.inputs.total_revenue + 1e-5)
        rainfall_score = min(self.inputs.avg_rainfall_last_5_years / 100, 10)
        commodity_dependence_score = min(max((1 - self.inputs.commodity_dependence) * 10, 0), 10)
        yield_efficiency = self.inputs.yield_per_ha / (self.inputs.labor_hours + 1)
        cost_per_ha = (self.inputs.machinery_costs + self.inputs.fertilizer_costs) / (self.inputs.land_area_ha + 1e-5)

        # Exclude yield_score and cost_score here (they only affect productivity score, not metrics display)
        return {
            "liquidity": liquidity,
            "debt_asset": debt_asset,
            "profit_margin": profit_margin,
            "rainfall_score": rainfall_score,
            "commodity_dependence_score": commodity_dependence_score,
            "yield_efficiency_(kg/labor hour)": yield_efficiency,
            "cost_per_ha_($)": cost_per_ha,
        }

    def _financial_score(self):
        liquidity = self.inputs.current_assets / (self.inputs.current_liabilities + 1e-5)
        debt_asset = (self.inputs.current_liabilities + self.inputs.long_term_liabilities) / (self.inputs.total_assets + 1e-5)
        profit_margin = self.net_income / (self.inputs.total_revenue + 1e-5)

        score = 0
        score += min(max(liquidity / 2.0 * 10, 0), 10)
        score += min(max((1 - debt_asset) * 15, 0), 15)
        score += min(max(profit_margin * 10, 0), 10)
        return round(score)

    def _risk_score(self):
        score = 0
        if self.inputs.irrigation_access:
            score += 5
        if self.inputs.insurance_coverage:
            score += 5
        rainfall_score = min(self.inputs.avg_rainfall_last_5_years / 100, 10)
        score += rainfall_score
        score += min(max((1 - self.inputs.commodity_dependence) * 10, 0), 10)
        return round(score)

    def _productivity_score(self):
        yield_efficiency = self.inputs.yield_per_ha / (self.inputs.labor_hours + 1)
        cost_per_ha = (self.inputs.machinery_costs + self.inputs.fertilizer_costs) / (self.inputs.land_area_ha + 1e-5)
        rev_per_ha = self.inputs.total_revenue/self.inputs.land_area_ha
        cost_score = max(0, cost_per_ha/rev_per_ha*10)
        yield_score = min(yield_efficiency * 2, 10)
        return round(cost_score + yield_score)

    def compute_scores(self):
        raw_financial = self._financial_score()  # max 35
        raw_risk = self._risk_score()            # max 30
        raw_productivity = self._productivity_score()  # max 20

        financial_pct = round((raw_financial / 35) * 100, 2)
        risk_pct = round((raw_risk / 30) * 100, 2)
        productivity_pct = round((raw_productivity / 20) * 100, 2)
        total_raw = raw_financial + raw_risk + raw_productivity
        total_pct = round((total_raw) / 85 * 100, 2)

        metrics = self.compute_metrics()

        return {
            "raw_scores": {
                "financial": raw_financial,
                "risk": raw_risk,
                "productivity": raw_productivity,
                "total": total_raw,
            },
            "financial_score": financial_pct,  # underscore fixed here
            "risk_score": risk_pct,
            "productivity_score": productivity_pct,
            "total_score": total_pct,
            "metrics": metrics,
        }
