# Automação de testes de API com Pytest + Requests

Projeto demonstrativo de QA para a API pública [DummyJSON](https://dummyjson.com), elaborado para mostrar como testes automatizados verificam autenticação e protegem o contrato da API.

## O que está coberto

- `POST /auth/login`: valida o status HTTP, o usuário retornado e a presença dos identificadores e tokens.
- `GET /auth/me`: reutiliza o token recebido no login como Bearer token e valida o status e os dados essenciais do usuário autenticado.
- `GET /products` e `GET /products/{id}`: validam coleção, campos essenciais e consulta por identificador.
- Paginação e busca de produtos: verificam os parâmetros enviados e a estrutura do resultado.
- `POST /products/add`: valida a representação de produto que a API retorna ao simular uma criação.

O `ApiClient` centraliza URL-base, timeout e sessão HTTP. As fixtures do Pytest criam e encerram o cliente por teste e mantêm as credenciais configuráveis. Cada teste realiza sua própria autenticação, evitando dependência de ordem ou compartilhamento de estado entre testes.

O endpoint de inclusão da DummyJSON simula a criação e devolve um objeto de resposta; ele não persiste o produto no servidor. Por isso o teste valida o contrato da resposta, sem esperar encontrar o produto em uma consulta posterior.

## Requisitos

- Python 3.10 ou superior
- Acesso à internet durante a execução dos testes

## Como executar

No terminal, dentro da pasta do projeto:

```bash
python -m venv .venv
```

Ative o ambiente virtual:

```bash
# Windows PowerShell
.venv\Scripts\Activate.ps1

# macOS/Linux
source .venv/bin/activate
```

Instale as dependências e execute os testes:

```bash
python -m pip install -r requirements.txt
python -m pytest -v
```

No Windows, também é possível chamar diretamente o Python do ambiente virtual:

```powershell
.\.venv\Scripts\python.exe -m pytest -v
```

Para executar somente o primeiro cenário (login):

```powershell
.\.venv\Scripts\python.exe -m pytest -v tests/test_auth.py::test_login_returns_access_token
```

As credenciais públicas de demonstração da DummyJSON são usadas por padrão. Para configurar outras credenciais de teste ou outro ambiente, defina as variáveis antes de executar:

```powershell
# Windows PowerShell
$env:DUMMYJSON_USERNAME="usuario-de-teste"
$env:DUMMYJSON_PASSWORD="senha-de-teste"
$env:DUMMYJSON_BASE_URL="https://dummyjson.com"
$env:REQUEST_TIMEOUT="10"
python -m pytest -v
```

```bash
# macOS/Linux
export DUMMYJSON_USERNAME="usuario-de-teste"
export DUMMYJSON_PASSWORD="senha-de-teste"
export DUMMYJSON_BASE_URL="https://dummyjson.com"
export REQUEST_TIMEOUT="10"
python -m pytest -v
```

Não use credenciais pessoais, tokens reais ou dados sensíveis no repositório. O arquivo `.env.example` documenta as variáveis disponíveis; o projeto lê variáveis do ambiente do processo e não carrega arquivos `.env` automaticamente.

## Estrutura

```text
api/
  client.py       # Cliente HTTP reutilizável
tests/
  conftest.py     # Fixtures e configuração dos testes
  test_auth.py    # Cenários de login e endpoint autenticado
  test_products.py # Cenários de consulta, busca, paginação e criação simulada
pytest.ini        # Descoberta e execução dos testes
requirements.txt  # Dependências do projeto
.github/workflows/tests.yml # Execução automatizada no GitHub Actions
```

## Como isso ajuda a empresa

- Encontra regressões no fluxo de autenticação sem depender de uma interface gráfica.
- Reaproveita cliente, configuração e fixtures para novos endpoints.
- Facilita execução repetida no computador do time e em pipeline CI/CD.
- Mantém verificações focadas no contrato: status, campos essenciais e autenticação.

Em um pipeline, a etapa de qualidade pode instalar `requirements.txt` e executar `python -m pytest -v`. Em um ambiente real, credenciais e URL devem vir do gerenciador de segredos e da configuração do ambiente da CI; não devem ser gravadas no código.

## Limitações conhecidas

DummyJSON é uma API pública de demonstração, dependente de internet e sujeita a disponibilidade e mudanças externas. Ela não representa um serviço de produção nem garante persistência de dados de negócio. Para uma solução empresarial, os mesmos padrões devem apontar para um ambiente de teste controlado, com dados isolados e contratos definidos pela própria equipe.
