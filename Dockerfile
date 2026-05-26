# Usa uma imagem oficial leve do Python
FROM python:3.11-slim

# Define variáveis de ambiente úteis
# PYTHONUNBUFFERED=1: Garante que os logs do Python sejam exibidos imediatamente no console
# PYTHONDONTWRITEBYTECODE=1: Evita que o Python escreva arquivos .pyc no container
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia primeiro o arquivo de dependências para aproveitar o cache de camadas do Docker
COPY requirements.txt .

# Instala as dependências do projeto sem salvar cache do pip (reduz tamanho da imagem)
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código da API para o diretório de trabalho
COPY . .

# Expõe a porta que a aplicação vai escutar
EXPOSE 8000

# Comando para iniciar o servidor Uvicorn escutando em todas as interfaces de rede na porta 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
