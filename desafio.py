from datetime import datetime

def criar_usuario(usuarios): #Cliente do Banco
    cpf = input("Informe o CPF: ")
    for usuario in usuarios:
        if (usuario["cpf"] == cpf):
            print("Usuario ja possui cadastro!")
            return
    
    nome = input("Insira o nome do titular: ")
    data_nascimento = input("Insira a data de nascimento: ")

    logradouro = input("Qual seu logradouro (Sem numero): ")
    numero = input("Agora informe o numero:")
    bairro = input("Informe o bairro: ")
    cidade = input("Insira o nome da cidade:")
    estado = input("E por ultimo informe a sigla do estado: ")
    
    # endereco = f"{input("Qual seu logradouro (Sem numero): ")}, {input("Agora informe o numero:")} - {input("Informe o bairro: ")} - {input("Insira a cidade:")}/{input("E por ultimo informe a sigla do estado: ")}"
    # endereco = {'logradouro': logradouro, 'numero': numero, 'bairro': bairro, 'cidade': cidade, 'estado': estado}

    endereco = f"{logradouro}, {numero} - {bairro} - {cidade}/{estado}"

    usuarios.append({'nome': nome, 'cpf': cpf, 'nascimento': data_nascimento, 'endereco': endereco})
    print("Usuario cadastrado com sucesso!")

def criar_conta_corrente(contas, cpf, agencia, numero_conta):
    contas.append({'numero': numero_conta, 'cpf_titular': cpf, 'agencia': agencia, 'saldo': 0.001, 'extrato': f"Conta criada em {datetime.now()}", 'saques': 0})

    print(f"""Conta criada com sucesso em {datetime.now()}
    Numero: {numero_conta}
    Agencia: {agencia}
    """)
    return numero_conta + 1

def listar_contas(contas):
    if (not contas):
        print("Nao existem contas criadas!")
    else:
        print("CONTAS CRIADAS".center(30, "="))
        for conta in contas:
            print(f'''
            Numero da Conta: {conta["numero"]}
            Agencia: {conta["agencia"]}
            CPF do Titular: {conta["cpf_titular"]}
                  ''')

def listar_usuarios(usuarios):
    if (not usuarios):
        print("Nao existem usuarios cadastrados!")
    else:
        print("USUARIOS CADASTRADOS".center(30, "="))
        for usuario in usuarios:
            print(f'''
                {usuario["nome"]}
            CPF: {usuario["cpf"]}
            Data de Nascimento: {usuario["nascimento"]}
            Endereco: {usuario["endereco"]}
                  ''')
    
def exibir_extrato(saldo, /, *, extrato):
    print("EXTRATO".center(21, "="))
    print(extrato)
    print(f"Saldo atual: R$ {saldo:.2f}")

def depositar(saldo, deposito, extrato, / ):
    saldo += deposito

    data_saque = datetime.now().date()
    hora_saque = datetime.now().time()

    extrato += f"""
    Deposito:
        +R${deposito:.2f}
    Informacoes de deposito:
        Data: {data_saque} Hora: {hora_saque}
    Novo saldo: R${saldo:.2f}
    """

    print("\nDeposito realizado com sucesso!")
    print(f"Deposito no valor de R$ {deposito:.2f} realizado em {data_saque.strftime("%d/%m/%Y")} as {hora_saque}")

    return saldo, extrato

def sacar(*, saldo, valor_saque, extrato, numero_saques, limite_saques):
    if (numero_saques >= limite_saques):
        print("Voce excedeu o numero de saques diario!\nTente amanha.")
        return None, None
    else:       
        if (valor_saque > saldo):
            print("Voce nao possui saldo suficiente para realizar a transacao!") 
            return None, None
        else:
            saldo -= valor_saque

            data_saque = datetime.now().date()
            hora_saque = datetime.now().time()

            extrato += f"""
            Saque: 
                -R$ {valor_saque:.2f} 
            Informacoes de saque:
                Data: {data_saque} Hora: {hora_saque}
            Novo saldo: R$ {saldo:.2f}
            """

            print("\nSaque realizado com sucesso!")
            print(f"Saque no valor de R$ {valor_saque:.2f} realizado em {data_saque.strftime("%d/%m/%Y")} as {hora_saque}")

            return saldo, extrato

# def procurar_cpf(usuarios, cpf_procurado):
#     for indice, usuario in enumerate(usuarios):
#         if (cpf_procurado == usuario["cpf"]):
#            return indice
        
#     else:
#         print("Usuario nao encontrado!")
#         return 

menu = """

[c] Cadastrar Usuario
[l] Listar Usuarios
[cc]Criar Conta
[lc]Listar Contas
[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair

=> """

limite = 500
LIMITE_SAQUES = 3
AGENCIA = "0001"
usuarios = []
contas = []
numero_conta = 1

while True:

    opcao = input(menu)

    #Depositar
    if opcao == "d":
        if (not contas):
            print("Nao existem contas cadastradas!")
        else:  
            numero_conta = int(input("Informe o numero da conta: "))

            conta_encontrada = False
            for conta in contas:
                if (numero_conta == conta["numero"]):
                    conta_encontrada = True
                    deposito = 0 # valor a ser depositado

                    while deposito <= 0 and deposito != "q":
                        deposito = float(input("Insira o valor para ser depositado: "))
                        if (deposito <= 0):
                            print("O valor depositado deve ser positivo!")
                    if deposito == "q":
                        break
                    else:
                        saldo, extrato = depositar(conta["saldo"], deposito, conta["extrato"])
                        if (saldo == None or extrato == None):
                            break
                        else:
                            conta["saldo"] = saldo
                            conta["extrato"] = extrato
                            break
            if (not conta_encontrada):
                print("Conta nao encontrada!")

    #Sacar
    elif opcao == "s":
        if (not contas):
            print("Nao existem contas cadastradas!")
        else:  
            numero_conta = int(input("Informe o numero da conta: "))

            conta_encontrada = False
            for conta in contas:
                if (numero_conta == conta["numero"]):
                    conta_encontrada = True
                    saque = 0
                    while saque <= 0 and saque != "q":
                        saque = float(input("Insira o valor que deseja sacar: "))

                        if (saque <= 0):
                            print("Valor digitado invalido!")

                    if saque == "q":
                        break
                    elif (saque > limite):
                        print(f"Nao e possivel realizar saques a cima do limite! O limite atual e de R${limite:.2f}")
                        break
                    else:
                        saldo, extrato = sacar(saldo=conta["saldo"], valor_saque=saque, extrato=conta["extrato"], limite_saques=LIMITE_SAQUES, numero_saques=conta["saques"])
                        conta["saldo"] = saldo
                        conta["extrato"] = extrato
                        conta["saques"] += 1
                        break
            if (not conta_encontrada):
                print("Conta nao encontrada!")

    #Exibir Extrato
    elif opcao == "e":
        if (not contas):
            print("Nao existem contas cadastradas!")
        else:
            numero_conta = int(input("Informe o numero da conta: "))

            conta_encontrada = False
            for conta in contas:
                print(conta["numero"])
                if (numero_conta == conta["numero"]):
                    conta_encontrada = True
                    exibir_extrato(saldo, extrato=conta["extrato"])
                    break
            if (not conta_encontrada):
                print("Conta nao encontrada!")

    #Criar Usuario
    elif opcao == "c":
        criar_usuario(usuarios)

    #Listar Usuarios
    elif opcao == "l":
        if (not usuarios):
            print("Nao existem usuarios cadastrados!")
        else:
            listar_usuarios(usuarios)
            
    #Criar Conta
    elif opcao == "cc":
        if (not usuarios):
            print("Nao existem usuarios cadastrados!")
        else:
            cpf_procurado = input("Informe o CPF do usuario: ")
            # TODO: Melhorar chamada de funcao e saida do for
            for usuario in usuarios:
                if (cpf_procurado == usuario["cpf"]):
                    numero_conta = criar_conta_corrente(contas=contas, cpf=cpf_procurado, agencia=AGENCIA, numero_conta=numero_conta) 
                    break
            else:
                print("Usuario nao encontrado!")
    
    #Listar Contas
    elif opcao == "lc":
        if (not contas):
            print("Nao existem contas ativas!")
        else:
            listar_contas(contas)

    #Sair   
    elif opcao == "q":
        break

    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")
