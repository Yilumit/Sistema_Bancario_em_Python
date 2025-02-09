def depositar(deposito ):
    global saldo 
    saldo_antigo = saldo
    saldo += deposito
    global extrato
    extrato += f"""
    Saldo anterior: {saldo_antigo}
    Deposito: +{deposito}
    Novo saldo: {saldo}
    """

    print("\nDeposito realizado com sucesso!")

def sacar(valor_saque):
    global saldo
    saldo_antigo = saldo
    saldo -= valor_saque
    global extrato
    extrato += f"""
    Saldo anterior: {saldo_antigo}
    Saque: -{valor_saque}
    Novo saldo: {saldo}
    """

    print("\nSaque realizado com sucesso!")

menu = """

[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair

=> """

saldo = 0
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3

while True:

    opcao = input(menu)

    if opcao == "d":
        deposito = 0 # valor a ser depositado
        while deposito <= 0:
            deposito = float(input("Insira o valor para ser depositado: "))
            if (deposito <= 0):
                print("O valor depositado deve ser positivo!")
        depositar(deposito)

    elif opcao == "s":
        if (numero_saques >= LIMITE_SAQUES):
            print("Voce excedeu o numero de saques diario!\nTente amanha.")
        else:       
            saque = float(input("Insira o valor que deseja sacar: "))
            if (saque > saldo):
                print("Voce nao possui saldo suficiente para realizar a transacao!")
            elif (saque > limite):
                print(f"Nao e possivel realizar saques a cima do limite! O limite atual e de R${limite:.2f}")
            else:
                sacar(saque)
                numero_saques += 1

    elif opcao == "e":
        if (not extrato):
            print("Nao houve transacoes desde a criacao da conta!")
        else:
            print()
            print(extrato)

    elif opcao == "q":
        break

    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")
