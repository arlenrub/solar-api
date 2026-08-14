# SolarTech API ☀️

API desenvolvida com **FastAPI** para simular economia de energia, payback simples e retorno sobre investimento de sistemas solares fotovoltaicos. O serviço funciona como motor de cálculos do projeto [Solar Tech Digital](https://github.com/arlenrub/solar-tech-digital-web).

## Funcionalidades

- Cálculo de economia mensal e anual estimada
- Cálculo de payback simples
- Estimativa de ROI para um horizonte de 20 anos
- Validação dos dados de entrada com Pydantic
- Endpoints de verificação de saúde da API
- Compatibilidade com o frontend do Solar Tech Digital
- Empacotamento com Docker

## Tecnologias

- Python
- FastAPI
- Pydantic
- Uvicorn
- Docker

## Endpoints principais

### GET /api/v1/health

Verifica se o serviço está disponível.

### POST /api/v1/simulate/savings

Recebe a potência instalada e a tarifa de energia. A geração mensal e o custo de instalação podem ser informados ou estimados automaticamente pelo MVP.

Exemplo de requisição:

    {
      "potencia_kwp": 5.0,
      "tarifa_kwh": 0.85
    }

### POST /simular

Endpoint legado mantido para compatibilidade com integrações anteriores.

## Executando localmente

    git clone https://github.com/arlenrub/solar-api.git
    cd solar-api
    python -m venv .venv
    .venv\Scripts\activate
    pip install -r requirements.txt
    uvicorn main:app --reload

A documentação interativa ficará disponível em http://127.0.0.1:8000/docs.

## Executando com Docker

    docker build -t solartech-api .
    docker run -p 8000:8000 solartech-api

## Observações técnicas

- Os resultados são estimativas para apoio a simulações e não representam garantia financeira ou de geração de energia.
- As premissas padrão de geração e custo devem ser ajustadas conforme região, equipamento, tarifa e condições reais do projeto.
- A configuração atual de CORS inclui liberação ampla para o MVP. Em produção, deve ser limitada aos domínios autorizados.
- O cálculo implementa payback simples e não substitui uma análise financeira completa com inflação, degradação dos módulos, manutenção e variação tarifária.

## Autor

Desenvolvido por [Arlen Vasconcelos](https://github.com/arlenrub).
