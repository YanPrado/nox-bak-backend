# Development Guide

## 1. Objetivo

Este documento define os critérios mínimos de desenvolvimento do projeto NOX BANK.

O objetivo é manter consistência na criação de módulos, organização do código, documentação e critérios de conclusão das funcionalidades.

---

## 2. Revisão de Arquitetura

Antes de iniciar um novo módulo, deve ser feita uma revisão rápida considerando:

- Qual problema o módulo resolve.
- Qual será o escopo inicial.
- Quais entidades serão necessárias.
- Quais tabelas serão impactadas.
- Quais módulos serão dependências.
- Se haverá necessidade de auditoria.
- Se haverá necessidade de eventos XES.
- Se há necessidade de nova ADR.

A revisão será feita antes da implementação de cada novo módulo.

---

## 3. Definition of Done

Uma funcionalidade ou módulo será considerado concluído quando os itens aplicáveis forem atendidos:

### Arquitetura

- [ ] Revisão de Arquitetura realizada.
- [ ] Escopo definido.
- [ ] Complexidade desnecessária evitada.
- [ ] ADR criada quando necessário.

### Banco de Dados

- [ ] Modelagem revisada.
- [ ] Relacionamentos conferidos.
- [ ] Migração Alembic criada quando aplicável.
- [ ] Banco atualizado.

### Backend

- [ ] Model criado.
- [ ] Schema criado.
- [ ] Repository criado.
- [ ] Service criado.
- [ ] Controller criado.
- [ ] Router criado.

### Segurança

- [ ] Validação de entrada implementada.
- [ ] Permissões RBAC aplicadas quando necessário.
- [ ] Informações sensíveis protegidas.

### Auditoria e XES

Quando aplicável:

- [ ] Audit Log implementado.
- [ ] Evento XES implementado.

### API

- [ ] Endpoint funcionando.
- [ ] Swagger atualizado.
- [ ] Retornos HTTP corretos.
- [ ] Tratamento de erros implementado.

### Testes

- [ ] Fluxo principal validado.
- [ ] Casos de erro testados.
- [ ] Integração com banco validada.

### Documentação

- [ ] Cabeçalho dos arquivos relevantes atualizado.
- [ ] Docstrings adicionadas quando necessário.
- [ ] Documentação geral atualizada quando aplicável.
- [ ] ADR criada quando aplicável.