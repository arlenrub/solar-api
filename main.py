from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional
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

# Configuração do Middleware de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://solartechdigital.techguiadigital.com",  # Subdomínio da API (Cloudflare)
        "https://solartechdigital.vercel.app",           # Projeto na Vercel
        "http://localhost:3000",                          # Ambiente local de desenvolvimento
        "*",                                              # MVP: libera para todas as origens
    ],
    allow_credentials=True,
    allow_methods=["*"],   # Permite todos os verbos HTTP (GET, POST, etc.)
    allow_headers=["*"],   # Permite todos os cabeçalhos
)

# ─── Models ───────────────────────────────────────────────────────────────────

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
    economia_mensal: float = Field(..., description="Economia mensal estimada em R$")
    economia_anual: float = Field(..., description="Economia anual estimada em R$")
    payback_anos: float = Field(..., description="Tempo de payback simples em anos")
    roi_porcentagem: float = Field(..., description="Retorno sobre investimento (ROI) de 20 anos em %")

# Modelo simplificado para o endpoint v1 (frontend envia só potencia_kwp + tarifa_kwh)
class SimulacaoSimplificada(BaseModel):
    potencia_kwp: float = Field(..., gt=0, description="Potência instalada em kWp", json_schema_extra={"example": 5.0})
    tarifa_kwh: float = Field(..., gt=0, description="Tarifa de energia em R$/kWh", json_schema_extra={"example": 0.85})
    geracao_kwh_mes: Optional[float] = Field(None, description="Geração mensal em kWh (calculada automaticamente se não informada)")
    custo_instalacao: Optional[float] = Field(None, description="Custo de instalação em R$ (calculado automaticamente se não informado)")

# ─── Rotas legadas (mantidas para compatibilidade) ────────────────────────────

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

# ─── Rotas v1 (usadas pelo frontend Next.js) ──────────────────────────────────

@app.get("/api/v1/health")
def health_v1():
    return {"status": "ok", "service": "SolarTechDigital API"}

@app.post("/api/v1/simulate/savings")
def simulate_savings(dados: SimulacaoSimplificada):
    try:
        # Valores padrão calculados se não informados
        # Estimativa: 1 kWp gera ~120 kWh/mês (média nordeste Brasil)
        geracao = dados.geracao_kwh_mes if dados.geracao_kwh_mes else dados.potencia_kwp * 120
        # Estimativa: R$ 3.000 por kWp instalado
        custo = dados.custo_instalacao if dados.custo_instalacao else dados.potencia_kwp * 3000

        economia_mensal = calcular_economia_mensal(geracao, dados.tarifa_kwh)
        economia_anual = calcular_economia_anual(economia_mensal)
        payback = calcular_payback_simples(custo, economia_anual)
        roi = calcular_roi(custo, economia_anual)

        return {
            "economia_mes_reais": round(economia_mensal, 2),
            "economia_anual_reais": round(economia_anual, 2),
            "payback_anos": round(payback, 2),
            "roi_porcentagem": round(roi, 2),
            "geracao_kwh_mes": round(geracao, 2),
            "custo_instalacao": round(custo, 2),
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
