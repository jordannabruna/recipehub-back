# RecipeHub Backend - Docker Setup

Este projeto está totalmente dockerizado com PostgreSQL incluído.

## 🚀 Como Rodar com Docker

### **Pré-requisitos:**
- Docker instalado
- Docker Compose instalado

### **1. Executar a Aplicação Completa:**

```bash
docker-compose up -d
```

Isso irá:
- ✅ Criar e rodar o banco de dados PostgreSQL na porta `5432`
- ✅ Criar e rodar o backend FastAPI na porta `8000`
- ✅ Inicializar o banco de dados automaticamente com roles (admin, user)

### **2. Verificar se está rodando:**

```bash
docker-compose ps
```

Você verá algo como:
```
NAME                   STATUS
recipehub-backend      Up 2 minutes
recipehub-db           Up 2 minutes
```

### **3. Acessar a API:**

- 🌐 **API Base:** `http://localhost:8000`
- 📚 **Documentação:** `http://localhost:8000/docs`
- 🔧 **ReDoc:** `http://localhost:8000/redoc`

### **4. Parar a Aplicação:**

```bash
docker-compose down
```

Se quiser remover também os volumes (banco de dados):
```bash
docker-compose down -v
```

## 📝 Variáveis de Ambiente

As variáveis estão no arquivo `.env`:

```env
POSTGRES_USER=postgresql
POSTGRES_PASSWORD=12345678
POSTGRES_DB=recipe_hub
APP_PROFILE=PROD
```

Você pode editá-las conforme necessário.

## 🔍 Logs

Ver logs do backend:
```bash
docker-compose logs -f backend
```

Ver logs do banco de dados:
```bash
docker-compose logs -f db
```

## 📦 Build da Imagem

Se fez mudanças no código e quer rebuildar:

```bash
docker-compose build --no-cache
docker-compose up -d
```

## 🗄️ Acessar o Banco Diretamente

```bash
docker-compose exec db psql -U postgresql -d recipe_hub
```

## ✅ Testar Endpoint de Criação de Usuário

```bash
curl -X POST "http://localhost:8000/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Jordanna",
    "email": "jordanabruna90@gmail.com",
    "password": "senha123"
  }'
```

## 🚀 Deploy no Render com Docker

Se quiser fazer deploy no Render usando Docker:

1. Conecte seu repositório GitHub ao Render
2. Configure o serviço como **Web Service**
3. Selecione **Docker** como ambiente
4. Adicione as variáveis de ambiente no Render dashboard:
   - `POSTGRES_USER`
   - `POSTGRES_PASSWORD`
   - `POSTGRES_HOST`
   - `POSTGRES_DB`
   - `APP_PROFILE=PROD`

O Render vai usar automaticamente o `Dockerfile` para fazer build e deploy!

---

**Desenvolvido com ❤️ usando FastAPI + PostgreSQL + Docker**
