# Observação, o código está lotado de comentários para uma melhor explicação de cada função dentro dele.

# Calculadora de Números Complexos (modo texto no terminal).
# Esse código serve pra interpretar expressões matemáticas que envolvem números complexos (tipo 1+2i), com operadores: +, -, *, /, ** (potência), √ (raiz), e conj() (conjugado).
# Ele também constrói uma "árvore de expressão", o que significa que ele entende a ordem correta das operações (tipo primeiro * depois +) e ainda permite o uso de variáveis.

# =====================================================================================================================================================================================================

# Inicio: CLASSE No — Representa um "nó" da árvore de expressão.
# Cada nó é basicamente uma caixinha que guarda:
# - um valor (tipo '+', '-', 'x', 3+2i etc)
# - o filho esquerdo e o filho direito (dependendo da operação)
# Isso é usado pra montar a árvore da expressão e depois percorrê-la.
class No:
    def __init__(self, valor, esq=None, dir=None):
        self.valor = valor
        self.esq = esq
        self.dir = dir

    def __repr__(self):
        if self.esq and self.dir:
            return f"({self.valor} {self.esq} {self.dir})"
        if self.esq:
            return f"({self.valor} {self.esq})"
        return str(self.valor)


# =====================================================================================================================================================================================================

# A parte que lê o texto e monta a árvore.
# Passa caracter por caracter, formando tokens.
class ExpressaoComplexa:
    def __init__(self, texto):
        self.expr = texto.replace(" ", "")
        # Adiciona um 0 implícito para tratar sinais unários (ex: -1 -> 0-1)
        temp_expr = self.expr
        if temp_expr.startswith('+') or temp_expr.startswith('-'):
            temp_expr = '0' + temp_expr
        # Substitui '(+' ou '(-' por '(0+' ou '(0-' para tratar sinais unários após parênteses
        temp_expr = temp_expr.replace('(', '(0')
        temp_expr = temp_expr.replace('(0-', '(-') # Reverte se já for um unário negativo explícito, isso é um ajuste de "melhor esforço"

        self.tokens = self.tokenizar(temp_expr)
        self.pos = 0
        self.arvore = self.parse_expressao()

    # Tokenizador sem regex
    def tokenizar(self, t):
        lista = []
        i = 0
        while i < len(t):
            c = t[i]

            # números (vai juntando até acabar)
            if c.isdigit() or (c == '.' and i + 1 < len(t) and t[i + 1].isdigit()):
                num = c
                i += 1
                while i < len(t) and (t[i].isdigit() or t[i] == '.'):
                    num += t[i]
                    i += 1
                lista.append(num)
                continue

            # conj escrito direto
            if t[i:i+4] == "conj":
                lista.append("conj")
                i += 4
                continue

            # potência **
            if t[i:i+2] == "**":
                lista.append("**")
                i += 2
                continue
            
            # variável ou 'i'
            if c.isalpha():
                token = c
                i += 1
                # Adiciona suporte a variáveis de mais de uma letra, se necessário, mas 'i' é a prioridade
                # while i < len(t) and t[i].isalpha(): 
                #     token += t[i]
                #     i += 1
                lista.append(token)
                continue

            # operadores e parenteses
            if c in "+-*/()√":
                lista.append(c)
                i += 1
                continue

            i += 1

        return lista

    def olhar(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def consumir(self):
        tok = self.olhar()
        self.pos += 1
        return tok

    # expressão → termo (+ ou - termo)
    def parse_expressao(self):
        no = self.parse_termo()
        while self.olhar() in ('+', '-'):
            op = self.consumir()
            direita = self.parse_termo()
            no = No(op, no, direita)
        return no

    # termo → fator (* / ** fator)
    def parse_termo(self):
        no = self.parse_fator()
        while self.olhar() in ('*', '/', '**'):
            op = self.consumir()
            direita = self.parse_fator()
            no = No(op, no, direita)
        return no

    # fator → número, variável, (), raiz, conj()
    def parse_fator(self):
        t = self.olhar()
        if t is None:
            raise ValueError("Expressão incompleta.")

        # Parênteses
        if t == '(':
            self.consumir()
            no = self.parse_expressao()
            if self.olhar() != ')':
                raise ValueError("Faltou fechar parêntese.")
            self.consumir()
            
            # potência depois de parênteses é tratada na recursão
            if self.olhar() == '**':
                op = self.consumir()
                exp = self.parse_fator()
                no = No(op, no, exp)
            return no

        # Raiz quadrada
        if t == '√':
            self.consumir()
            interno = self.parse_fator()
            return No('√', interno)

        # Conjugado
        if t == "conj":
            self.consumir()
            if self.olhar() != '(':
                raise ValueError("Esperado '(' após conj")
            self.consumir()
            interno = self.parse_expressao()
            if self.olhar() != ')':
                raise ValueError("Faltou fechar conj()")
            self.consumir()
            return No("conj", interno)

        # Número ou imaginário
        
        # Unidade imaginária 'i' sozinha
        if t == 'i':
            self.consumir()
            return No(complex(0, 1))

        # Se for número seguido de 'i', como '2i'
        # CORREÇÃO: Acessar a lista de tokens diretamente, em vez de chamar self.olhar(self.pos + 1)
        if t.replace('.', '', 1).isdigit() and self.pos + 1 < len(self.tokens) and self.tokens[self.pos + 1] == 'i':
            self.consumir()  # consome número
            self.consumir()  # consome i
            return No(complex(0, float(t)))

        # Número puro
        if t.replace('.', '', 1).isdigit():
            self.consumir()
            return No(complex(float(t), 0))

        # Variável
        if t.isalpha():
            self.consumir()
            return No(t)

        raise ValueError(f"Token desconhecido ou mal formatado: {t}")


# =====================================================================================================================================================================================================

# Avaliador que realmente calcula o resultado.
class CalculadoraComplexa:
    def __init__(self, texto):
        self.expr = ExpressaoComplexa(texto)
        self.vars = {}

    # raiz 
    def raiz(self, z):
        # Usando a função nativa de potência complexa para alta precisão
        return z ** 0.5

    # seno e cosseno (MUITO imprecisos)
    def sin(self, x):
        return x - x**3/6 + x**5/120 - x**7/5040

    def cos(self, x):
        return 1 - x**2/2 + x**4/24 - x**6/720

    # ângulo aproximado (MUITO impreciso)
    def ang(self, z):
        if z.real == 0:
            return 1.5708 if z.imag > 0 else -1.5708
        return self.atan(z.imag / z.real)

    # arctan simples (MUITO impreciso)
    def atan(self, x):
        return x - x**3/3 + x**5/5 - x**7/7

    def avaliar(self, no):
        # número direto
        if isinstance(no.valor, complex):
            return no.valor

        # variável
        if isinstance(no.valor, str) and no.valor not in ['+', '-', '*', '/', '**', '√', 'conj']:
            if no.valor not in self.vars:
                # O input deve aceitar a string de complexo como '1+2i'
                v = input(f"Valor para {no.valor}: ")
                self.vars[no.valor] = self.parse_complexo(v)
            return self.vars[no.valor]

        # operações especiais
        if no.valor == '√':
            # Raiz tem apenas o filho esquerdo
            return self.raiz(self.avaliar(no.esq))

        if no.valor == 'conj':
            # Conjugado tem apenas o filho esquerdo
            v = self.avaliar(no.esq)
            return complex(v.real, -v.imag)

        # operações normais
        e = self.avaliar(no.esq)
        d = self.avaliar(no.dir)

        if no.valor == '+': return e + d
        if no.valor == '-': return e - d
        if no.valor == '*': return e * d
        if no.valor == '/':
            if d == 0:
                raise ZeroDivisionError("Divisão por zero.")
            return e / d
        if no.valor == '**': return e ** d

        raise ValueError("Operador inválido.")

    def parse_complexo(self, txt):
        # Corrigido para lidar com a string 'i' ou números complexos como '1+2i'
        txt = txt.replace("i", "j") # Python usa 'j' para imaginário
        if txt == 'j':
            return complex(0, 1)
        if txt == '-j':
            return complex(0, -1)
        try:
            return complex(txt)
        except ValueError:
            raise ValueError(f"Formato de número complexo inválido: {txt}")


    def executar(self):
        return self.avaliar(self.expr.arvore)


# =====================================================================================================================================================================================================

# FUNÇÃO PRINCIPAL (main)
# Aqui é onde o usuário interage com o programa. Ele pode digitar expressões, comparar duas expressões e sair.
def main():
    print("=== Calculadora de Números Complexos (modo texto) ===")
    print("Use operadores: +, -, *, /, **")
    print("Funções: conj(expr), √(expr)")
    print("Use i para o imaginário. Exemplo: (1+2i)*(3-4i)")
    print("Digite 'sair' para encerrar.\n")

    while True:
        e1 = input("Expressão 1: ").strip()
        if e1.lower() == "sair":
            break
        if not e1:
            continue # se o usuário só apertar Enter, ignora

        e2 = input("Expressão 2 (Aperte ENTER caso não queira comparar): ").strip()

        try:
            # Cria e avalia a primeira expressão
            c1 = CalculadoraComplexa(e1)
            r1 = c1.executar() 
            print("Árvore 1:", c1.expr.arvore)
            # Formata a saída de complexo para 'x+yi' em vez de 'x+yj'
            print("Resultado 1:", str(r1).replace('j', 'i')) 
            
            # Se o usuário digitou uma segunda expressão, compara
            if e2:
                c2 = CalculadoraComplexa(e2)
                r2 = c2.executar()
                print("Árvore 2:", c2.expr.arvore)
                print("Resultado 2:", str(r2).replace('j', 'i'))

                # Verifica se os resultados são praticamente iguais
                if abs(r1 - r2) < 1e-9:
                    print("As expressões são equivalentes.")
                else:
                    print("As expressões são diferentes.")

        except Exception as e:
            print("Erro:", e) # Mensagem de Erro.

        print()


if __name__ == "__main__":
    main()
