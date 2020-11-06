import random


def primo(n):  # verifica se o número é primo
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while (i * i) <= n:
        if (n % i) == 0 or (n % (i + 2)) == 0:
            return False
        i += 6
    return True


def gerar_numero():  # gera um número primo aleatório
    while True:
        numero = random.randint(0, 100)
        if primo(numero):
            return numero


def totiente(p, q):  # calcula o totiente de n
    x = (p - 1) * (q - 1)
    return x


def gerar_e(num):
    while True:
        e = random.randint(2, num)
        if mdc(num, e) == 1:
            return e


def mdc(num1, num2):
    resto = 1
    while num2 != 0:
        resto = num1 % num2
        num1 = num2
        num2 = resto
    return num1


def cifrar_mensagem(msg, e, n):
    mensagem_criptografada = []
    for i in msg:
        letra = ord(i)
        cifra = (letra ** e) % n
        mensagem_criptografada.append(cifra)
    return mensagem_criptografada


def mod(a, b):  # mod function
    if a < b:
        return a
    else:
        c = a % b
        return c


def gerar_chaves():
    p = gerar_numero()
    q = gerar_numero()
    n = p * q
    t = totiente(p, q)
    e = gerar_e(t)

    chave_publica = [n, e]
    d = 0
    while mod(d*e, t) != 1:
        d += 1
    chave_privada = [n, d]
    return [chave_publica, chave_privada]


def descriptar_mensagem(msg, d, n):
    mensagem = ""
    for i in msg:
        letra = (int(i) ** d) % n
        letra = chr(letra)
        mensagem += letra
    return mensagem
