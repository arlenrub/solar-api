def calcular_economia_mensal(geracao_kwh_mes: float, tarifa_energia: float) -> float:
    """
    Calcula a economia financeira gerada no mês.
    Fórmula: Geração Mensal (kWh) * Tarifa de Energia (R$/kWh)
    """
    if geracao_kwh_mes < 0 or tarifa_energia < 0:
        raise ValueError("Os valores de geração e tarifa devem ser positivos.")
    return round(geracao_kwh_mes * tarifa_energia, 2)


def calcular_economia_anual(economia_mensal: float) -> float:
    """
    Calcula a economia financeira anual gerada.
    Fórmula: Economia Mensal * 12
    """
    if economia_mensal < 0:
        raise ValueError("A economia mensal deve ser positiva.")
    return round(economia_mensal * 12, 2)


def calcular_payback_simples(custo_instalacao: float, economia_anual: float) -> float:
    """
    Calcula o payback simples em anos.
    Fórmula: Custo Total da Instalação / Economia Anual
    """
    if custo_instalacao < 0:
        raise ValueError("O custo de instalação deve ser positivo.")
    if economia_anual <= 0:
        return 0.0
    return round(custo_instalacao / economia_anual, 2)


def calcular_roi(custo_instalacao: float, economia_anual: float, anos: int = 20) -> float:
    """
    Calcula o Retorno sobre o Investimento (ROI) estimado para um ciclo de anos (padrão 20 anos) em porcentagem.
    Fórmula: ((Ganho Total - Custo da Instalação) / Custo da Instalação) * 100
    Onde Ganho Total é Economia Anual * Anos.
    """
    if custo_instalacao <= 0:
        return 0.0
    if economia_anual < 0:
        raise ValueError("A economia anual deve ser positiva.")
    
    ganho_total = economia_anual * anos
    roi = ((ganho_total - custo_instalacao) / custo_instalacao) * 100
    return round(roi, 2)
