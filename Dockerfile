FROM python:3.11-slim

# Define variáveis de ambiente essenciais
# PYTHONUNBUFFERED: Garante que os logs apareçam imediatamente no console do Render
# PYTHONDONTWRITEBYTECODE: Evita a criação de arquivos .pyc inúteis no container
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Define o diretório de trabalho
WORKDIR /app

# Instala dependências do sistema
# gcc e libpq-dev para o PostgreSQL
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copia o arquivo de dependências
COPY pyproject.toml ./

# Instala dependências usando pip
RUN pip install --upgrade pip && \
    pip install fastapi uvicorn sqlalchemy email-validator python-multipart passlib[bcrypt] python-jose bcrypt psycopg2-binary

# Copia o restante do código da aplicação
COPY . .

# Expõe a porta
EXPOSE 8000

# Comando de inicialização
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]