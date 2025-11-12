# 🧮 Calculadora Científica de Números Complexos (Linha de Comando)

Projeto desenvolvido como parte da atividade prática de **Programação**.

Este programa realiza **operações matemáticas com números complexos**, constrói a **árvore sintática** da expressão (em formato LISP), e compara se duas expressões são **equivalentes**.

---

## 👥 Integrantes do Grupo

| Nome Completo | RA | Função no grupo |
|----------------|----|----------------|
| Rafael Pereira Grigorio de Lacerda | 1272526033 | Lógica do codigo e testes |
| Ana Priscilla | (RA) | Conhecimento Matematico e testes |
| Witan de Jesus | (RA) | Lógica do codigo e Relatorio (Readme) |
| Fillyoe Araujo | (RA) | Ajuda no codigo e Relatorio (Readme) |

---

## 🧠 Funcionalidades

✅ Representa números complexos no formato **a + bi** ou **a - bi**  
✅ Aceita operadores: `+`, `-`, `*`, `/`, `**` (potência)  
✅ Funções: `conj(expr)` (conjugado) e `sqrt(expr)` (raiz quadrada)  
✅ Permite **variáveis** (ex: `x`, `y`) — o programa pede o valor na hora da execução  
✅ Mostra a **árvore da expressão em notação LISP**  
✅ Verifica se **duas expressões são equivalentes** numericamente  
✅ Detecta **erros** de sintaxe, divisão por zero e valores inválidos  
✅ Feito totalmente em **Python**, sem necessidade de interface gráfica  

---

## ⚙️ Requisitos

- Python **3.8+**
- Nenhuma biblioteca externa é necessária (apenas `cmath` e `re`)

---

## ▶️ Como Executar

1. Baixe o arquivo `CalculadoraComplexa.py`  
2. No terminal ou prompt de comando, vá até a pasta onde o arquivo está salvo.  
3. Execute o comando:

   ```bash
   python calculadora_complexa.py

---

## 💡 Exemplos de Funcionamento

### 🔹 Exemplo 1 — Soma de complexos
Expressão 1: (3+2i) + (1+4i)  
**Saída:**  
Árvore 1: (+ (3+2i) (1+4i))  
Resultado 1: 4+6i

---

### 🔹 Exemplo 2 — Subtração de complexos
Expressão 1: (5+3i) - (2+7i)  
**Saída:**  
Árvore 1: (- (5+3i) (2+7i))  
Resultado 1: 3-4i

---

### 🔹 Exemplo 3 — Multiplicação de complexos
Expressão 1: (3+2i)*(1-4i)  
**Saída:**  
Árvore 1: (* (3+2i) (1-4i))  
Resultado 1: 11-10i

---

### 🔹 Exemplo 4 — Divisão de complexos
Expressão 1: (2+3i)/(1-i)  
**Saída:**  
Árvore 1: (/ (2+3i) (1-i))  
Resultado 1: 0.5+2.5i

---

### 🔹 Exemplo 5 — Potência de número complexo
Expressão 1: (1+i)**3  
**Saída:**  
Árvore 1: (** (1+i) 3)  
Resultado 1: -2+2i

---

### 🔹 Exemplo 6 — Raiz quadrada de número complexo
Expressão 1: √(3+4i)  
**Saída:**  
Árvore 1: (√ (3+4i))  
Resultado 1: 2+1i

---

### 🔹 Exemplo 7 — Conjugado de número complexo
Expressão 1: conj(5-2i)  
**Saída:**  
Árvore 1: (conj (5-2i))  
Resultado 1: 5+2i

---

### 🔹 Exemplo 8 — Expressão com variável
Expressão 1: x**2 + conj(x)  
> O programa perguntará:  
Digite o valor de x (ex: 3+2i):  
**Se o usuário digitar `3+2i`:**  
Árvore 1: (+ (** x 2) (conj x))  
Resultado 1: 10+10i

---

### 🔹 Exemplo 9 — Comparação de duas expressões equivalentes
Expressão 1: (1+i)**2  
Expressão 2: 1 + 2i + i**2  
**Saída:**  
Árvore 1: (** (1+i) 2)  
Árvore 2: (+ (+ 1 (* 2i)) (** i 2))  
Resultado 1: 2i  
Resultado 2: 2i  
As expressões são EQUIVALENTES.

---

### 🔹 Exemplo 10 — Detecção de erro
Expressão 1: (3+2i)/(1-1i-1)  
**Saída:**  
Erro: Expressão inválida ou divisão por zero.

---

### 🔹 Exemplo 11 — Exibição da árvore em notação LISP
Expressão 1: (2+i)*(1-i)  
**Saída:**  
Árvore: (* (2+i) (1-i))  
Resultado: 3+i  

