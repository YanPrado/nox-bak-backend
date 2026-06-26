# ADR-001 — Estrutura do Projeto

## Status

Aceito

## Contexto

O NOX BANK será um projeto de longo prazo, composto por diversos módulos como autenticação, clientes, contas, transações, investimentos, crédito, auditoria e mineração de processos (XES).

Era necessário definir uma organização que permitisse crescimento sem comprometer a legibilidade do código.

## Decisão

O backend será organizado por módulos (domínios), e não por camadas globais.

Estrutura:

* auth
* clients
* accounts
* transactions
* audit
* xes

Cada módulo conterá seus próprios arquivos:

* models.py
* schemas.py
* repositories.py
* services.py
* controllers.py
* routers.py

Os componentes compartilhados permanecerão fora dos módulos:

* config
* database
* core
* utils

## Consequências

### Positivas

* Alto desacoplamento entre módulos.
* Facilidade para localizar arquivos relacionados.
* Escalabilidade para dezenas de módulos.
* Redução da complexidade conforme o projeto cresce.

### Negativas

* Pequena duplicação de estrutura entre módulos.
* Exige disciplina para manter responsabilidades bem definidas.
