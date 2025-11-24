# Calculadora Científica de Números Complexos

**Faculdade:** UNIFACS – Universidade Salvador  
**Curso:** Ciência da Computação  
**Disciplina:** Estrutura de Dados e Análise de Algoritmos  
**Professor:** Wellington Lacerda  
**Data:** 18/11/2025  
**GitHub do Projeto:** https://github.com/RafaelGLacerda/A3Wellington

---

## Relatório
Acesse o relatório completo do projeto no link abaixo:  
https://drive.google.com/file/d/1l4rtNaQ3pyl_gpSbj0jz3lBl_hyBIuNJ/view?usp=sharing

---

## Integrantes do Grupo 

| Nome Completo | RA | Função no grupo |
|----------------|----|----------------|
| Rafael Pereira Grigorio de Lacerda | 1272526033 | Lógica do codigo, Readme e Testes |
| Ana Priscilla Silva Oliveira | 1272411739 | Lógica do codigo e Testes |
| Witan Mendes Paixão Nascimento de Jesus | 12724123796 | Lógica do codigo e Relatorio |
| Fillype da Silva Araujo | 12724145904 | Lógica do codigo e Relatorio |

---

## Sobre o Projeto
Este código implementa uma calculadora de números complexos que interpreta expressões digitadas pelo usuário, constrói a árvore sintática correspondente e calcula o resultado.

A expressão é lida caractere por caractere, transformada em tokens e organizada em uma árvore em notação LISP, respeitando a ordem correta das operações. A avaliação dessa árvore permite realizar soma, subtração, multiplicação, divisão, potência, raiz quadrada, conjugado e operações com variáveis.

O programa também permite comparar duas expressões para verificar se produzem o mesmo valor e identifica erros comuns, como sintaxe inválida, divisão por zero ou parênteses faltando. Tudo funciona diretamente no terminal e sem uso de bibliotecas externas.

---

## Requisitos

- Python **3.8+**
- Nenhuma. Todas as funcionalidades matemáticas e estruturais foram implementadas manualmente

---

## Como Executar️

1. Baixe o arquivo `CalculadoraComplexa.py`  
2. No terminal ou prompt de comando, vá até a pasta onde o arquivo está salvo.  
3. Execute o comando:

   ```bash
   python CalculadoraComplexa.py

---

## Exemplos de Funcionamento

### 🔹 Exemplo 1 — Soma
Expressão 1: (3+2i) + (1+4i)  
**Saída:**  
Árvore 1: (+ (+ (3+0j) 2j) (+ (1+0j) 4j))    
Resultado 1: 4+6i

---

### 🔹 Exemplo 2 — Subtração
Expressão 1: (5+3i) - (2+7i)  
**Saída:**  
Árvore 1: (- (+ (5+0j) 3j) (+ (2+0j) 7j))   
Resultado 1: 3-4i

---

### 🔹 Exemplo 3 — Multiplicação
Expressão 1: (3+2i)\*(1-4i)  
**Saída:**  
Árvore 1: (\* (+ (3+0j) 2j) (- (1+0j) 4j))     
Resultado 1: 11-10i

---

### 🔹 Exemplo 4 — Divisão
Expressão 1: (2+3i)/(1-i)  
**Saída:**  
Árvore 1: (/ (+ (2+0j) 3j) (- (1+0j) 1j))      
Resultado 1: -0.5+2.5i

---

### 🔹 Exemplo 5 — Potência
Expressão 1: (1+i)\*\*3  
**Saída:**  
Árvore 1: (\*\* (+ (1+0j) 1j) (3+0j))    
Resultado 1: -2+2i

---

### 🔹 Exemplo 6 — Raiz quadrada
Expressão 1: √(3+4i)  
**Saída:**  
Árvore 1: (√ (+ (3+0j) 4j))    
Resultado 1: (2+1i)

---

### 🔹 Exemplo 7 — Conjugado
Expressão 1: conj(5-2i)  
**Saída:**  
Árvore 1: (conj (- (5+0j) 2j))      
Resultado 1: 5+2i

---

### 🔹 Exemplo 8 — Expressão com variável
Expressão 1: x\*\*2 + conj(x)  
O programa perguntará:  
Digite o valor de x (ex: 3+2i):  
**Se o usuário digitar `3+2i`:**   
**Saída:**   
Árvore 1: (+ (\*\* x 2) (conj x))       
Resultado 1: 8 + 10i

---

### 🔹 Exemplo 9 — Comparação de duas expressões equivalentes
Expressão 1: (1+i)\*\*2  
Expressão 2: 1 + 2i + i\*\*2  
**Saída:**  
Árvore 1: (\*\* (+ (1+0j) 1j) (2+0j))         
Resultado 1: 2i            
Árvore 2: (+ (+ (1+0j) 2j) (\*\* 1j (2+0j)))             
Resultado 2: 2i  
As expressões são EQUIVALENTES.

---

### 🔹 Exemplo 10 — Detecção de erro
Expressão 1: 1 /(1-1)  
**Saída:**       
Resultado 1: Erro: Divisão por zero.

