# 🖥️ Simulador de Máquina Norma

Este projeto é um **Simulador de Máquina Norma** desenvolvido em Python, com interface **GUI** usando Tkinter.

---

## ✨ Principais funcionalidades

- Leitura de **programas monolíticos rotulados** (`1: ...`, `2: ...`, etc.).  
- **Registradores** nomeados `a..z` com valores inteiros **não-negativos** (saturação em 0).  
- **Operações primitivas**:  
  - `se zero_x então vá_para N senão vá_para M`  
  - `faça add_x vá_para N`  
  - `faça sub_x vá_para N` (sem valores negativos)  
  - `fim` (parada)
- **Macros** de alto nível (expandidas pelo parser):  
  - `IGUAL a b c` → coloca **1 em `c` se `a == b`**, senão **0**.  
  - `MENOR a b c` → copia o **mínimo entre `a` e `b` para `c`**.  
  - `MAIOR a b c d` → copia o **máximo entre `a` e `b` para `d`** usando `c` como auxiliar.
- **Trace executável**: lista das instruções executadas, rótulos visitados, valores antes/depois.  
- **Exportação de traço** (CLI) para a pasta `runs/` com timestamp.  
- Interface **GUI** com Tkinter para edição/execução visual.

> As macros estão em `src/macros.py`; o parser expande chamadas do tipo `faça MACRO (...) vá_para N`.

---

## 📂 Estrutura do Projeto

```plaintext
trabalho-maquina-norma-python/
│
├── main.py              # Ponto de entrada
├── ui/
│   ├── gui.py           # Interface gráfica (Tkinter)
│   └── cli.py           # (Opcional) Interface de console
│
├── src/
│   ├── parser.py        # Parser dos programas monolíticos
│   ├── virtual_machine.py # Implementação da Máquina Norma
│   └── macros.py        # Biblioteca de macros (MULT, DIV, ENCODE, DECODE)
│
├── programs/            # Programas de teste (.txt)
│   ├── exemplo.txt
│   ├── divisao.txt
│   └── multiplicacao.txt
│
└── README.md
```

---

## 🚀 Como Executar

1. **Instale o Python 3.11+**
```bash
python --version
```

2. **Clone o repositório e instale dependências**
```bash
git clone <seu-repo.git>
cd trabalho-maquina-norma-python
pip install -r requirements.txt
```

3. **Execute o simulador**
```bash
python main.py
```

4. **Escolha o modo**
- `1` → CLI (console)
- `2` → GUI (interface gráfica)

---

## 🧾 Sintaxe dos programas (Norma)

Cada linha tem um **rótulo numérico** seguido de uma instrução:

```text
1: se zero_b então vá_para 9 senão vá_para 2
2: faça add_a vá_para 3
3: faça add_a vá_para 4
4: faça sub_b vá_para 1
9: fim
```

Chamadas de **macro**:

```text
1: faça IGUAL a b c vá_para 100
100: fim

1: faça MENOR a b c vá_para 100
100: fim

1: faça MAIOR a b c d vá_para 100
100: fim
```

> **Dicas**
> - Use apenas letras `a..z` para nome de registradores.  
> - `sub_x` não deixa o registrador negativo (satura em 0).  
> - O programa sempre inicia no **menor rótulo** definido.

---

## 🧩 Estendendo com novas macros

1. Abra `src/macros.py` e adicione uma função `macro_<nome>(...)` que **retorne a sequência de instruções expandidas**.  
2. Registre no dicionário `MACROS = { "NOME": macro_nome, ... }`.  
3. No programa `.txt`, chame: `faça NOME (args) vá_para RÓTULO`.

O **parser** (`src/parser.py`) cuida da expansão antes da execução.

---

## 🧪 Exemplos incluídos

- `programs/igualdade.txt` → usa `IGUAL a b c` para colocar 1 em `c` se `a == b`.  
- `programs/maior.txt` → usa `MAIOR a b c d` para escrever o máximo em `d`.  
- `programs/menor.txt` → usa `MENOR a b c` para escrever o mínimo em `c`.  
- `programs/exemplo_basico.txt` → programa simples com `add/sub` e teste de zero.

---

## ⚠️ Limitações e validações

- **Inteiros não-negativos** apenas; decremento satura em 0.  
- **Passos máximos** padrão: `100000` (evita laços infinitos).  
- Nomes de registradores são **normalizados para minúsculo**.  
- Erros comuns são tratados com mensagens amigáveis (ex.: divisão por zero — caso implementada por macros futuras).

---

## 👥 Autores

- **Luis Fernando Souza Pinto**  
- **Kaue Muller**  
- **Bernardo Bencke**  
- **Leonardo Bencke**

---

---

## 📄 Licença

Este projeto é de uso acadêmico, desenvolvido como parte da disciplina de **Computabilidade (UNISC)**.
