FROM python:3.11-slim

# Define variáveis de ambiente essenciais
# PYTHONUNBUFFERED: Garante que os logs apareçam imediatamente no console do Render
# PYTHONDONTWRITEBYTECODE: Evita a criação de arquivos .pyc inúteis no container
# POETRY_VERSION: Fixa a versão para evitar quebras em atualizações futuras
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    POETRY_VERSION=1.8.3

# Define o diretório de trabalho
WORKDIR /app

# Instala dependências do sistema
# Adiciona 'curl' caso precise baixar algo e mantem gcc/libpq-dev para o Postgres
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Instala o Poetry numa versão específica
RUN pip install "poetry==$POETRY_VERSION"

# Copia APENAS os arquivos de dependência primeiro (para usar o cache do Docker)
COPY pyproject.toml poetry.lock ./

# Configura Poetry e instala dependências
RUN poetry config virtualenvs.create false \
    && poetry install --no-root --no-interaction --no-ansi

# Copia o restante do código da aplicação
COPY . .

# Expõe a porta
EXPOSE 8000

# Comando de inicialização
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]