# APS - Definição de Linguagem de Programação

---

## Objetivo

Criação de uma linguagem voltada para confeiteiros, com o objetivo de organizar pedidos de forma metódica e gerar um plano de execução para as encomendas recebidas. A partir das receitas associadas a cada pedido, a linguagem permite:

- resumir as quantidades de ingredientes necessárias;
- listar os passos de produção, como tempo de forno, resfriamento e decoração;
- ajustar automaticamente as quantidades de ingredientes com base na proporção entre porções que uma receita rende e porções solicitadas;
- estimar o tempo total de produção de cada pedido;
- comparar o tempo total de produção do pedido com o tempo disponível (informado no input).

---

## Testes

A pasta de testes contém alguns exemplos de arquivos que podem ser submetidos. Como fica evidente, o sistema permite na entrada uma encomenda com até 10 pedidos que, por sua vez, podem conter até 20 ingredientes e 10 etapas para produção.

A saída envolve os resumos das informações relevantes para o plano de execução, como tempo total, ingredientes e quantidades necessários, entre outros.

---

## Como usar

Após clonar o repositório, é necessário abrir um terminal (recomendado o uso de Ubuntu ou terminal WSL) que permita o uso comando `make`. Em seguida, rode o programa da seguinte forma:

```./encomenda < arquivo_input.txt```

Substitua `arquivo_input.txt` pelo nome do arquivo desejado. Exemplo:

```./encomenda < testes/teste1_pedido_unico.txt```

Essa execução gerará o arquivo na linguagem `go`, que pode ser compilado através do uso do `compilador_para_go.py`, desenvolvido ao longo do semestre na disciplina Lógica da Computação. Para compilar o arquivo, utilize o seguinte comando no terminal:

```python compilador_para_go.py output.go```

Em que o arquivo `output.go` é o gerado anteriormente pelo executável `encomenda`. A saída será um arquivo `.asm` que pode ser montado e executado.

LEMBRETE: Use a versão do `python` compatível com o seu sistema para a compilação.
