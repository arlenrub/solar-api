from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from calculadora import (
    calcular_economia_mensal,
    calcular_economia_anual,
    calcular_payback_simples,
    calcular_roi
)

app = FastAPI(
    title="SolarTech API",
    description="Motor de cálculos de Payback, ROI e economia de energia solar fotovoltaica.",
    version="1.0.0"
)

class SimulacaoSolar(BaseModel):
    potencia_kwp: float = Field(
        ..., 
        gt=0, 
        description="Potência instalada em kWp", 
        json_schema_extra={"example": 5.0}
    )
    geracao_kwh_mes: float = Field(
        ..., 
        gt=0, 
        description="Geração mensal estimada em kWh", 
        json_schema_extra={"example": 600.0}
    )
    tarifa_energia: float = Field(
        ..., 
        gt=0, 
        description="Tarifa de energia em R$/kWh", 
        json_schema_extra={"example": 0.85}
    )
    custo_instalacao: float = Field(
        ..., 
        gt=0, 
        description="Custo total de instalação em R$", 
        json_schema_extra={"example": 15000.0}
    )

class ResultadoSimulacao(BaseModel):
    economia_mensal: float = Field(
        ..., 
        description="Economia mensal estimada em R$"
    )
    economia_anual: float = Field(
        ..., 
        description="Economia anual estimada em R$"
    )
    payback_anos: float = Field(
        ..., 
        description="Tempo de payback simples em anos"
    )
    roi_porcentagem: float = Field(
        ..., 
        description="Retorno sobre investimento (ROI) de 20 anos em %"
    )

@app.get("/")
def health_check():
    return {
        "status": "API SolarTech ativa e a funcionar",
        "service": "Calculation Engine",
        "health": "OK"
    }

@app.post("/simular", response_model=ResultadoSimulacao)
def simular_projeto(dados: SimulacaoSolar):
    try:
        economia_mensal = calcular_economia_mensal(dados.geracao_kwh_mes, dados.tarifa_energia)
        economia_anual = calcular_economia_anual(economia_mensal)
        payback = calcular_payback_simples(dados.custo_instalacao, economia_anual)
        roi = calcular_roi(dados.custo_instalacao, economia_anual)
        
        return ResultadoSimulacao(
            economia_mensal=economia_mensal,
            economia_anual=economia_anual,
            payback_anos=payback,
            roi_porcentagem=roi
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
