# Especificações para o Frontend - Sistema de Receitas Públicas

## Visão Geral

O sistema de receitas agora funciona como um Instagram de receitas, onde:
- ✅ Todos os usuários podem visualizar TODAS as receitas públicas
- ✅ Cada usuário pode ver suas próprias receitas em uma aba "Minhas Receitas"
- ✅ Cada usuário pode visualizar o perfil de outro usuário e suas receitas

## Endpoints Disponíveis

### 1. **Listar Todas as Receitas Públicas** (Público)
```
GET /recipes
```
**Autenticação:** Não requerida
**Resposta:** Array de receitas públicas

**Exemplo de uso:**
```javascript
fetch('http://localhost:8000/recipes')
  .then(res => res.json())
  .then(data => console.log(data))
```

---

### 2. **Minhas Receitas** (Autenticado)
```
GET /recipes/me/my-recipes
```
**Autenticação:** REQUERIDA (Bearer Token)
**Headers:**
```
Authorization: Bearer <seu_token_jwt>
```
**Resposta:** Array contendo apenas as receitas do usuário logado

**Exemplo de uso:**
```javascript
fetch('http://localhost:8000/recipes/me/my-recipes', {
  headers: {
    'Authorization': `Bearer ${token}`
  }
})
  .then(res => res.json())
  .then(data => console.log(data))
```

**Quando usar no Frontend:**
- Aba "Minhas Receitas" no perfil do usuário logado
- Mostrar apenas as receitas criadas pelo usuário
- Permitir edição/exclusão apenas dessas receitas

---

### 3. **Receitas de um Usuário Específico** (Público)
```
GET /recipes/user/{user_id}
```
**Autenticação:** Não requerida
**Parâmetros:**
- `user_id`: ID do usuário (number)

**Resposta:** Array contendo todas as receitas daquele usuário

**Exemplo de uso:**
```javascript
fetch('http://localhost:8000/recipes/user/123')
  .then(res => res.json())
  .then(data => console.log(data))
```

**Quando usar no Frontend:**
- Perfil público de outro usuário
- Mostrar todas as receitas daquele usuário
- Link para visualizar perfil: `/user/{user_id}` ou `/profile/{user_id}`

---

### 4. **Receita Específica** (Público)
```
GET /recipes/{recipe_id}
```
**Autenticação:** Não requerida
**Parâmetros:**
- `recipe_id`: ID da receita (number)

**Resposta:** Detalhes da receita

---

### 5. **Criar Receita** (Autenticado)
```
POST /recipes
```
**Autenticação:** REQUERIDA (Bearer Token)
**Body:**
```json
{
  "title": "Bolo de Chocolate",
  "description": "Um bolo delicioso",
  "instructions": "Misture os ingredientes...",
  "category": "Doces",
  "time_minutes": 30,
  "image_url": "https://...",
  "meal_type": "snack"
}
```

---

## Estrutura de Dados de Receita

Cada receita retornada tem a seguinte estrutura:
```json
{
  "id": 1,
  "title": "Bolo de Chocolate",
  "description": "Um bolo delicioso",
  "instructions": "Misture os ingredientes...",
  "category": "Doces",
  "time_minutes": 30,
  "image_url": "https://example.com/image.jpg",
  "meal_type": "snack"
}
```

**Observação:** O campo `owner_id` não é retornado na resposta pública, mas as receitas estão associadas ao usuário que as criou.

---

## Fluxo de UI Sugerido

### **Página Principal**
1. Exibir feed com TODAS as receitas (`GET /recipes`)
2. Cards com foto, título, descrição, tempo de preparo
3. Ao clicar em uma receita → detalhes (`GET /recipes/{recipe_id}`)
4. Ao clicar no nome do autor → perfil do usuário com suas receitas

### **Perfil do Usuário Logado**
1. **Aba "Minhas Receitas"** → `GET /recipes/me/my-recipes`
   - Mostrar botões de editar/deletar
   - Permitir adicionar nova receita
2. **Aba "Seguidores"** ou **Info do Perfil**
   - Mostrar informações pessoais
   - Exibir contador: "5 receitas"

### **Perfil de Outro Usuário**
1. Exibir informações do usuário
2. Listar receitas do usuário → `GET /recipes/user/{user_id}`
3. Cards das receitas (sem opções de editar/deletar)
4. Opção de seguir (se implementado futuramente)

---

## Ordem de Prioridade para Implementação no Frontend

1. **[Alta]** Implementar `/recipes/me/my-recipes` com aba "Minhas Receitas"
2. **[Alta]** Implementar `/recipes/user/{user_id}` para perfil de outros usuários
3. **[Média]** Adicionar link de autor nas receitas do feed
4. **[Média]** Diferenciar quais receitas o usuário pode editar/deletar
5. **[Baixa]** Sistema de seguir usuários (futura feature)
6. **[Baixa]** Favoritar receitas (futura feature)

---

## Notas Técnicas

- ✅ As receitas são **totalmente públicas** - qualquer pessoa pode ver qualquer receita
- ✅ Controle de edição/exclusão é feito no backend (apenas owner pode editar)
- ✅ Token JWT é necessário para criar/editar/deletar receitas
- ✅ Usar `Bearer <token>` no header `Authorization`
