# Observação, o código está lotado de comentários para uma melhor explicação de cada função dentro dele.

import re
import cmath


# Calculadora de Números Complexos (modo texto no terminal).
# Esse código serve pra interpretar expressões matemáticas que envolvem números complexos (tipo 1+2i), com operadores: +, -, *, /, ** (potência), √ (raiz), e conj() (conjugado).
# Ele também constrói uma "árvore de expressão", o que significa que ele entende a ordem correta das operações (tipo primeiro * depois +) e ainda permite o uso de variáveis.

# ======================================================================================================================

# Inicio: CLASSE No — Representa um "nó" da árvore de expressão.
# Cada nó é basicamente uma caixinha que guarda:
# - um valor (tipo '+', '-', 'x', 3+2i etc)
# - o filho esquerdo e o filho direito (dependendo da operação)
# Isso é usado pra montar a árvore da expressão e depois percorrê-la.
class No:
    def __init__(self, valor, esquerdo=None, direito=None):
        self.valor = valor
        self.esquerdo = esquerdo
        self.direito = direito

    def __repr__(self):
        if self.esquerdo and self.direito:
            return f"({self.valor} {self.esquerdo} {self.direito})"
        elif self.esquerdo:
            return f"({self.valor} {self.esquerdo})"
        return str(self.valor)


# CLASSE ExpressaoComplexa — Lê a expressão e monta a árvore.
# Aqui acontece toda a da interpretação. Ela pega o texto que o usuário digitou e transforma em uma estrutura de árvore pra depois calcular certinho.
class ExpressaoComplexa:
    def __init__(self, expr):
        self.expr = expr.replace(" ", "") # tira espaços da expressão
        self.tokens = self.tokenizar(self.expr) # separa a expressão em partes
        self.pos = 0 # controla onde estamos na lista de tokens
        self.arvore = self.parse_expressao()  # monta a árvore de fato

    def tokenizar(self, expr):
        # separa a expressão em pedaços (números, operadores, etc)
        padrao = r'(\*\*|[+\-*/()√]|conj|[A-Za-z_]\w*|\d+(?:\.\d+)?|i)'
        tokens = re.findall(padrao, expr)
        return [t for t in tokens if t.strip()]

    def olhar(self):
       # "Olhar" o próximo token SEM consumir (sem avançar)
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def consumir(self):
        # "Consumir" o token atual e avançar pro próximo
        token = self.olhar()
        self.pos += 1
        return token

    # A partir daqui vêm as funções que constroem a árvore respeitando a hierarquia das operações (ordem de precedência)
    def parse_expressao(self):
         # expressão = termo (+ ou - termo)
        no = self.parse_termo()
        while self.olhar() in ('+', '-'):
            op = self.consumir()
            direito = self.parse_termo()
            no = No(op, no, direito)
        return no

    def parse_termo(self):
         # termo = fator (* ou / ou ** fator)
        no = self.parse_fator()
        while self.olhar() in ('*', '/', '**'):
            op = self.consumir()
            direito = self.parse_fator()
            no = No(op, no, direito)
        return no


    def parse_fator(self):
        # Aqui ele trata os casos básicos: número, variável, (), conj(), √
        token = self.olhar()
        if token is None:
            raise ValueError("Erro: expressão incompleta.")

       # Se for um parêntese abrindo, entra recursivamente
        if token == '(':
            self.consumir()
            no = self.parse_expressao() # analisa o que tem dentro dos parênteses
            if self.olhar() != ')':
                raise ValueError("Erro: Falta ')' no final da expressão.")
            self.consumir()
             # se tiver potência depois de parêntese, tipo (2+3)**2
            if self.olhar() == '**':
                self.consumir()
                expoente = self.parse_fator()
                no = No('**', no, expoente)
            return no

        # Raiz quadrada
        elif token == '√':
            self.consumir()
            interno = self.parse_fator()
            return No('√', interno)

        # Conjugado
        elif token == 'conj':
            self.consumir()
            if self.olhar() != '(':
                raise ValueError("Erro: esperado '(' após 'conj'.")
            self.consumir()
            interno = self.parse_expressao()
            if self.olhar() != ')':
                raise ValueError("Erro: Falta ')' no final de conj().")
            self.consumir()
            return No('conj', interno)

       # Se for número, variável ou 'i'
        elif re.match(r'\d', token) or token == 'i' or re.match(r'[A-Za-z_]\w*', token):
            self.consumir()
            if token == 'i':
                return No(complex(0, 1))
            # Caso tipo "2i" (número seguido de 'i')
            if self.olhar() == 'i':
                self.consumir()
                return No(complex(0, float(token)))
            try:
                # Tenta converter pra número complexo com parte real
                return No(complex(float(token), 0))
            except:
                # Se não for número, deve ser variável (ex: x)
                return No(token)

        else:
            raise ValueError(f"Erro: token inesperado '{token}'.")


# CLASSE CalculadoraComplexa — Executa os cálculos da árvore.
# Essa parte realmente "avalia" a árvore, ou seja, faz as contas. Ela percorre os nós, resolve as operações, e retorna o resultado.
class CalculadoraComplexa:
    def __init__(self, expr):
        self.expr = ExpressaoComplexa(expr) # cria a árvore a partir da expressão
        self.vars = {} # dicionário pra guardar valores das variáveis

    
    def avaliar(self, no):
         # Caso base: se o valor do nó já é um número complexo
        if isinstance(no.valor, complex):
            return no.valor

        # se for variável, pede o valor para o usuario
        if isinstance(no.valor, str) and re.match(r'^[A-Za-z_]\w*$', no.valor):
            if no.valor not in self.vars:
                val = input(f"Digite o valor da variável {no.valor} (ex: 3+2i): ")
                self.vars[no.valor] = self.parse_complexo(val)
            return self.vars[no.valor]

       # Aqui funções especiais - raiz quadrada e conjugado
        if no.valor == '√':
            return cmath.sqrt(self.avaliar(no.esquerdo))
        if no.valor == 'conj':
            v = self.avaliar(no.esquerdo)
            return complex(v.real, -v.imag)

        # Aqui faz as operações normais - (+, -, *, /, **)
        esquerdo = self.avaliar(no.esquerdo)
        direito = self.avaliar(no.direito)

        if no.valor == '+':
            return esquerdo + direito
        elif no.valor == '-':
            return esquerdo - direito
        elif no.valor == '*':
            return esquerdo * direito
        elif no.valor == '/':
            if direito == 0:
                raise ZeroDivisionError("Divisão por zero.")
            return esquerdo / direito
        elif no.valor == '**':
            return esquerdo ** direito
        else:
            raise ValueError(f"Operador inválido: {no.valor}")

    def parse_complexo(self, texto):
        # Substitui 'i' por 'j' pra compatibilizar com o Python (que usa j)
        texto = texto.replace('i', 'j')
        return complex(texto)

    def executar(self):
        # Chama o avaliador na árvore principal e retorna o resultado
        return self.avaliar(self.expr.arvore)



# FUNÇÃO PRINCIPAL (main)
# Aqui é onde o usuário interage com o programa. Ele pode digitar expressões, comparar duas expressões e sair.
def main():
    print("=== Calculadora de Números Complexos (modo texto) ===")
    print("Use operadores: +, -, *, /, **")
    print("Funções: conj(expr), √(expr)")
    print("Use i para o imaginário. Exemplo: (1+2i)*(3-4i)")
    print("Digite 'sair' para encerrar.\n")

    while True:
        expr1 = input("Expressão 1: ").strip()
        if expr1.lower() == 'sair': 
            break
        if not expr1:
            continue # se o usuário só apertar Enter, ignora

        expr2 = input("Expressão 2 (deixe vazio se não quiser comparar): ").strip()

        try:
            # Cria e avalia a primeira expressão
            calc1 = CalculadoraComplexa(expr1)
            res1 = calc1.executar()
            print(f"\nÁrvore 1: {calc1.expr.arvore}")
            print(f"Resultado 1: {res1}")

            # Se o usuário digitou uma segunda expressão, compara
            if expr2:
                calc2 = CalculadoraComplexa(expr2)
                res2 = calc2.executar()
                print(f"\nÁrvore 2: {calc2.expr.arvore}")
                print(f"Resultado 2: {res2}")

                # Verifica se os resultados são praticamente iguais
                if abs(res1 - res2) < 1e-9:
                    print("As expressões são EQUIVALENTES.")
                else:
                    print("As expressões são DIFERENTES.")
                    
        except Exception as e:
            # Se der erro em qualquer parte, mostra mensagem
            print(f"Erro na expressão: {e}")
        print()

# Só executa o programa se o arquivo for rodado diretamente
if __name__ == "__main__":
    main()
