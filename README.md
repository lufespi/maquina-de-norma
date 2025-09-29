# 🖥️ Simulador de Máquina Norma

Este projeto é um **Simulador de Máquina Norma** desenvolvido em Python, com interface **GUI** usando Tkinter.

---

## 📌 Funcionalidades

✅ Leitura de programas monolíticos a partir de arquivos `.txt`.  
✅ Inicialização de registradores definidos pelo usuário.  
✅ Execução passo a passo com **trace detalhado** mostrando valores antes e depois de cada instrução.  
✅ Implementação das operações básicas: `zero_x`, `add_x`, `sub_x`.  
✅ **Macros implementadas:**  
- `MULT`: Multiplicação de dois registradores  
- `DIV`: Divisão com quociente e resto  
- `ENCODE` / `DECODE`: Codificação e decodificação via Par de Cantor  

✅ Interface gráfica moderna com:  
- Seleção de programas da pasta `programs/`  
- Entrada dinâmica de registradores com scroll  
- Botões arredondados e cores destacadas  
- Saída formatada para fácil leitura  

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

## 🧪 Exemplos de Programas

Exemplo de arquivo em `programs/exemplo.txt`:

```txt
1: se zero_b então vá_para 9 senão vá_para 2
2: faça add_a vá_para 3
3: faça sub_b vá_para 1
9: fim
```

---

## 🛠 Tecnologias Utilizadas

- **Python 3.11+**
- **Tkinter** para GUI
- **PIL/Pillow** (opcional, para exibir logotipo)
- Paradigma de programação modular

---

## 👨‍💻 Autores

- **Luis Fernando**  
- (Adicione os demais integrantes do grupo)

---

## 📄 Licença

Este projeto é de uso acadêmico, desenvolvido como parte da disciplina de **Computabilidade (UNISC)**.
