# Electrical Circuit Engine

Interpretador de circuitos com contatos NO/NC, lógica AND/OR, temporização TON, retenção por estado anterior e exclusão de bobinas simultâneas.

## Executar

Requisitos: Node.js 24.

```sh
npm test
node src/cli.mjs examples/seal-in.json examples/inputs.json > resultado.json
```

## Funcionamento

A configuração limita profundidade, tags e bobinas. O relógio não pode regredir. Erros de entrada não alteram temporizadores já confirmados. Testes exercitam retenção, atraso e intertravamento.

## Persistência de resultados

O arquivo de operações está em [vercel-home-telemetry-api.vercel.app](https://vercel-home-telemetry-api.vercel.app/laboratory.html?project=eletrical-comands-and-teory). As migrações Supabase estão no [repositório da API](https://github.com/brunnojob/vercel-home-telemetry-api/tree/main/supabase/migrations).

```sh
python cloud/sync.py enqueue resultado.json --project eletrical-comands-and-teory
python cloud/sync.py sync
```

Defina `BRUNNODEV_ACCESS_TOKEN` com sua sessão. A fila SQLite conserva os relatórios até confirmação do servidor; o mesmo conteúdo não gera registros duplicados. Tokens não são gravados no código.
