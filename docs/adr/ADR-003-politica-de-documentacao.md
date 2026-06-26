# ADR-003 — Política de Documentação

## Status

Aceito

## Contexto

O NOX BANK será um projeto de longo prazo, com múltiplos módulos, regras de negócio, autenticação, autorização, auditoria e mineração de processos.

Era necessário definir uma política de documentação que evitasse excesso de arquivos desatualizados, mas mantivesse clareza técnica para manutenção e apresentação do projeto.

## Decisão

A documentação será dividida em três níveis:

1. README.md
   Apresentação geral do projeto, tecnologias utilizadas, instruções de execução e visão resumida da arquitetura.

2. docs/
   Documentação técnica de alto nível, incluindo arquitetura geral, banco de dados, módulos, API, auditoria e XES.

3. Documentação no código
   Cada arquivo relevante deve conter comentários ou docstrings explicando sua responsabilidade, fluxo, o que pode fazer e o que não deve fazer.

As ADRs serão usadas apenas para registrar decisões arquiteturais relevantes.

## Diretrizes

A documentação no código deve explicar o motivo das decisões e a responsabilidade dos componentes.

Não devem ser criados comentários óbvios que apenas repetem o que o código já demonstra.

Exemplo ruim:

```python
# cria usuário
user = User(...)
```

Exemplo aceitável:

```python
"""
A senha deve chegar ao repository já criptografada.

Motivo:
A criptografia é uma regra de negócio e pertence ao Service.
"""
```

## Consequências

### Positivas

* Reduz risco de documentação desatualizada.
* Facilita entendimento direto durante leitura do código.
* Mantém documentação de alto nível separada da implementação.
* Registra decisões importantes sem poluir o repositório.

### Negativas

* Exige disciplina para manter docstrings úteis.
* Pode aumentar levemente o tamanho dos arquivos.
