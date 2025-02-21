from datetime import datetime
from abc import ABC, abstractmethod

#Classes
class Conta:
    _agencia = "0001"

    def __init__(self, cliente, numero):
        self._cliente = cliente
        self._numero = numero
        self._saldo = 0
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(cliente, numero)

    @property
    def saldo(self) -> float:
        return self._saldo
    
    @property
    def cliente(self):
        return self._cliente

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def historico(self):
        return self._historico
    
    def sacar(self, valor) -> bool:
        if self._saldo < valor:
            print("Saldo insuficiente!")
            return False
        
        elif 0 >= valor:
            print("Valor invalido!")
            return False
        
        else:
            self._saldo -= valor
            print("Realizando saque...")
            return True
        
    def depositar(self, valor) -> bool:
        if valor <= 0:
            print("Valor Invalido!")
            return False
        else:
            self._saldo += valor
            print("Deposito realizado com sucesso!")
            return True
        
    def __str__(self):
        return f'''\
\tNumero da Conta: {self._numero}
\tAgencia: {self._agencia}
\tNome do Titular: {self.cliente.nome}
                  '''

class ContaCorrente(Conta):
    _LIMITE_SAQUES = 3
    
    def __init__(self, cliente, numero, limite=500):
        super().__init__(cliente, numero)
        self.limite = limite

    @property
    def limite_saques(self):
        return self._LIMITE_SAQUES

    def sacar(self, valor) -> bool:
        cont_saque = len([transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__])
        
        saque_excedido = cont_saque >= self.limite_saques

        if saque_excedido:
            print("Limite de saques diarios atingido!")
            return False

        limite_excedido = self.limite < valor
        
        if limite_excedido:
            print(f"Nao e possivel realizar saques acima do limite! O limite atual e de R${self.limite:.2f}")
            return False
        else: 
            return super().sacar(valor)
                 
class Cliente:
    def __init__(self, endereco):
        self._endereco = endereco
        self._contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self._contas.append(conta)

    @property
    def endereco(self):
        return self._endereco
    
    @property
    def contas(self):
        return self._contas
       
class PessoaFisica(Cliente):
    def __init__(self, endereco, cpf, nome, data_nascimento):
        super().__init__(endereco)
        self._cpf = cpf
        self._nome = nome
        self._data_nascimento = data_nascimento

    @property
    def cpf(self):
        return self._cpf

    @property
    def nome(self):
        return self._nome

    @property
    def data_nascimento(self):
        return self._data_nascimento
    
    def __str__(self):
        return f'''\
\t\t{self._nome}
\tCPF: {self._cpf}
\tData de Nascimento: {self._data_nascimento}
\tEndereco: {self._endereco}
        '''

class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    @classmethod
    @abstractmethod
    def registrar(self, conta):
        pass

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta: Conta):
        if conta.depositar(self.valor):
            conta.historico.adicionar_transacao(self)

    def __str__(self):
        return f"""\
\t{self.__class__.__name__}:
\t\t+R${self._valor}
    """
            
class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta: Conta):
        if conta.sacar(self.valor):
            conta.historico.adicionar_transacao(self) 

    def __str__(self):
        return f"""\
\t{self.__class__.__name__}:
\t\t-R${self._valor}
    """

class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes
        
    def adicionar_transacao(self, transacao):
        self._transacoes.append({"tipo": transacao.__class__.__name__, "valor": transacao.valor, "data": datetime.now().strftime("%d/%m/%Y %H:%M"),})
        
#Operacoes
def criar_usuario(usuarios): #Cliente do Banco
    cpf = input("Informe o CPF: ")
    for usuario in usuarios:
        if (usuario.cpf == cpf):
            print("Usuario ja possui cadastro!")
            pass
    
    nome = input("Insira o nome do titular: ")
    data_nascimento = input("Insira a data de nascimento: ")

    logradouro = input("Qual seu logradouro (Sem numero): ")
    numero = input("Agora informe o numero: ")
    bairro = input("Informe o bairro: ")
    cidade = input("Insira o nome da cidade: ")
    estado = input("E por ultimo informe a sigla do estado: ")

    endereco = f"{logradouro}, {numero} - {bairro} - {cidade}/{estado}"

    cliente = PessoaFisica(nome=nome, cpf=cpf, data_nascimento=data_nascimento, endereco=endereco)
    usuarios.append(cliente)
    print("Usuario cadastrado com sucesso!")

def criar_conta_corrente(numero_conta, cliente: Cliente):
    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    cliente.adicionar_conta(conta)

    print(f"""Conta criada com sucesso em {datetime.now()}
    Numero: {numero_conta}
    Agencia: {conta.agencia}
    """)

def listar_contas(cliente : Cliente):
    if (not cliente.contas):
        print("Nao existem contas criadas!")
    else:
        print("CONTAS CRIADAS".center(30, "="))
        for conta in cliente.contas:
            print(conta)

def listar_usuarios(usuarios):
    if (not usuarios):
        print("Nao existem usuarios cadastrados!")
    else:
        print("\tUSUARIOS CADASTRADOS".center(30, "="))
        for usuario in usuarios:
            print(usuario)
    
def exibir_extrato(*, conta: Conta):
    print("EXTRATO".center(21, "="))
    transacoes = conta.historico.transacoes
    if not transacoes:
        print("Nao houve transacoes registradas nesta conta!")
    else:
        for transacao in transacoes:
            print(f'''{transacao["tipo"]}
\tR${transacao["valor"]:.2f}
Informacoes de deposito:
\tData: {transacao["data"]}
''')
    
    print(f"Saldo atual: R$ {conta.saldo:.2f}")

def depositar(cliente: Cliente, conta: Conta, deposito, / ):
    depositar = Deposito(deposito)
    cliente.realizar_transacao(conta=conta, transacao=depositar)

def sacar(*, cliente: Cliente, conta: Conta, saque):
    sacar = Saque(saque)
    cliente.realizar_transacao(conta=conta, transacao=sacar)

def procurar_cpf(usuarios, cpf):
    for indice, usuario in enumerate(usuarios):
        if (cpf == usuario.cpf):
           return indice
        
    else:
        print("Usuario nao encontrado!")
        return 

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

usuarios = []
numero_conta = 1
while True:

    opcao = input(menu)

    #Depositar
    if opcao == "d":
        if (not usuarios):
            print("Nao existem usuarios cadastrados!")
        else:
            cpf_procurado = input("Informe o CPF do usuario: ")
            indice = procurar_cpf(usuarios, cpf_procurado)
            if indice != None: 
                numero_conta = int(input("Informe o numero da conta: "))

                conta_encontrada = False
                for conta in usuarios[indice].contas:
                    if (numero_conta == conta.numero):
                        conta_encontrada = True
                        deposito = float(input("Insira o valor para ser depositado: "))
                        
                        depositar(usuarios[indice], conta, deposito)
                
                if (not conta_encontrada):
                    print("Conta nao encontrada!")

    #Sacar
    elif opcao == "s":
        if (not usuarios):
            print("Nao existem usuarios cadastrados!")
        else: 
            cpf_procurado = input("Informe o CPF do usuario: ")
            indice = procurar_cpf(usuarios, cpf_procurado)
            if indice != None:  
                numero_conta = int(input("Informe o numero da conta: "))

                conta_encontrada = False
                for conta in usuarios[indice].contas:
                    if (numero_conta == conta.numero):
                        conta_encontrada = True
                        saque = float(input("Insira o valor que deseja sacar: "))
                        sacar(cliente=usuarios[indice], conta=conta, saque=saque)

                if (not conta_encontrada):
                    print("Conta nao encontrada!")

    #Exibir Extrato
    elif opcao == "e":
        if (not usuarios):
            print("Nao existem usuarios cadastrados!")
        else:
            cpf_procurado = input("Informe o CPF do usuario: ")
            indice = procurar_cpf(usuarios, cpf_procurado)
            if indice != None:
                numero_conta = int(input("Informe o numero da conta: "))

                conta_encontrada = False
                for conta in usuarios[indice].contas:
                    if (numero_conta == conta.numero):
                        conta_encontrada = True
                        exibir_extrato(conta=conta)
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
            indice = procurar_cpf(usuarios, cpf_procurado)
            if indice != None:
                criar_conta_corrente(numero_conta=numero_conta, cliente=usuarios[indice])
                numero_conta += 1
    
    #Listar Contas
    elif opcao == "lc":
        if (not usuarios):
            print("Nao existem contas ativas!")
        else:
            cpf_procurado = input("Informe o CPF do usuario: ")
            indice = procurar_cpf(usuarios, cpf_procurado)
            if indice != None:
                listar_contas(usuarios[indice])

    #Sair   
    elif opcao == "q":
        break

    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")
