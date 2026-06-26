# ADR-002 — Utilização de Enums

## Status

Aceito

## Contexto

O sistema possui informações que representam estados fixos e outras que representam dados de negócio.

Era necessário decidir quais informações seriam representadas por Enums.

## Decisão

Enums serão utilizados apenas para estados internos da aplicação.

Exemplo:

* UserStatus
* TransactionStatus
* AccountStatus

Perfis (Roles) e Permissões permanecerão armazenados exclusivamente no banco de dados.

## Motivo

Perfis e permissões poderão ser administrados pela interface do sistema, sem necessidade de alterar o código ou realizar novo deploy.

Estados da aplicação representam comportamentos internos e tendem a ser estáveis, sendo adequados para Enums.

## Consequências

### Positivas

* Evita erros de digitação.
* Facilita autocompletar na IDE.
* Mantém o sistema flexível para administração de perfis e permissões.

### Negativas

* Novos estados exigirão alteração de código, porém essa mudança é esperada e controlada.
