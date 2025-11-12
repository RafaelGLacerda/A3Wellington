import re
import cmath

# ===========================================================
# Calculadora de Números Complexos (modo texto)
# Feita pra interpretar expressões com +, -, *, /, **, √, conj()
# Também monta uma árvore da expressão e pede valores de variáveis.
# ===========================================================

# Cada nó da árvore representa uma operação ou número
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


# Classe que transforma a expressão digitada numa árvore
class ExpressaoComplexa:
    def __init__(self, expr):
        self.expr = expr.replace(" ", "")  # tira espaços
        self.tokens = self.tokenizar(self.expr)
        self.pos = 0
        self.arvore = self.parse_expressao()

    def tokenizar(self, expr):
        # separa a expressão em pedaços (números, operadores, etc)
        padrao = r'(\*\*|[+\-*/()√]|conj|[A-Za-z_]\w*|\d+(?:\.\d+)?|i)'
        tokens = re.findall(padrao, expr)
        return [t for t in tokens if t.strip()]

    def olhar(self):
        # olha o próximo token sem consumir
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def consumir(self):
        # lê e avança o ponteiro
        token = self.olhar()
        self.pos += 1
        return token

    # monta a árvore levando em conta a ordem das operações
    def parse_expressao(self):
        no = self.parse_termo()
        while self.olhar() in ('+', '-'):
            op = self.consumir()
            direito = self.parse_termo()
            no = No(op, no, direito)
        return no

    def parse_termo(self):
        no = self.parse_fator()
        while self.olhar() in ('*', '/', '**'):
            op = self.consumir()
            direito = self.parse_fator()
            no = No(op, no, direito)
        return no

    # aqui ele interpreta cada parte, tipo (1+2i), √x, conj(x), etc
    def parse_fator(self):
        token = self.olhar()
        if token is None:
            raise ValueError("Erro: expressão incompleta.")

        # caso seja parênteses
        if token == '(':
            self.consumir()
            no = self.parse_expressao()
            if self.olhar() != ')':
                raise ValueError("Erro: Falta ')' no final da expressão.")
            self.consumir()
            # caso tenha potência depois do parêntese
            if self.olhar() == '**':
                self.consumir()
                expoente = self.parse_fator()
                no = No('**', no, expoente)
            return no

        # raiz quadrada
        elif token == '√':
            self.consumir()
            interno = self.parse_fator()
            return No('√', interno)

        # conjugado
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

        # variável, número ou imaginário
        elif re.match(r'\d', token) or token == 'i' or re.match(r'[A-Za-z_]\w*', token):
            self.consumir()
            if token == 'i':
                return No(complex(0, 1))
            # verifica se é número seguido de 'i' (tipo 2i)
            if self.olhar() == 'i':
                self.consumir()
                return No(complex(0, float(token)))
            try:
                return No(complex(float(token), 0))
            except:
                return No(token)

        else:
            raise ValueError(f"Erro: token inesperado '{token}'.")


# Classe principal da calculadora
class CalculadoraComplexa:
    def __init__(self, expr):
        self.expr = ExpressaoComplexa(expr)
        self.vars = {}

    # função que realmente faz o cálculo da árvore
    def avaliar(self, no):
        if isinstance(no.valor, complex):
            return no.valor

        # se for variável, pede o valor
        if isinstance(no.valor, str) and re.match(r'^[A-Za-z_]\w*$', no.valor):
            if no.valor not in self.vars:
                val = input(f"Digite o valor da variável {no.valor} (ex: 3+2i): ")
                self.vars[no.valor] = self.parse_complexo(val)
            return self.vars[no.valor]

        # funções especiais
        if no.valor == '√':
            return cmath.sqrt(self.avaliar(no.esquerdo))
        if no.valor == 'conj':
            v = self.avaliar(no.esquerdo)
            return complex(v.real, -v.imag)

        # operações básicas
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
        texto = texto.replace('i', 'j')
        return complex(texto)

    def executar(self):
        return self.avaliar(self.expr.arvore)



# Parte principal - interação com o usuário
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
            continue

        expr2 = input("Expressão 2 (deixe vazio se não quiser comparar): ").strip()

        try:
            calc1 = CalculadoraComplexa(expr1)
            res1 = calc1.executar()
            print(f"\nÁrvore 1: {calc1.expr.arvore}")
            print(f"Resultado 1: {res1}")
            if expr2:
                calc2 = CalculadoraComplexa(expr2)
                res2 = calc2.executar()
                print(f"\nÁrvore 2: {calc2.expr.arvore}")
                print(f"Resultado 2: {res2}")
                if abs(res1 - res2) < 1e-9:
                    print("As expressões são EQUIVALENTES.")
                else:
                    print("As expressões são DIFERENTES.")
        except Exception as e:
            print(f"Erro na expressão: {e}")
        print()


if __name__ == "__main__":
    main()
