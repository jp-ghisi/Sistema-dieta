'''BIBLIOTECAS'''
import sqlite3

'''CLASSES'''
#Criando usuário
class Usuario:
    def __init__(self, nome, idade, peso, altura, objetivo, nivel_ativo):
        self.nome = nome
        self._idade = idade
        self._peso = peso
        self._altura = altura
        self.objetivo = objetivo
        self.nivel_ativo = nivel_ativo
    
    def calcular_gasto_energetico_total(self):
        return self.calcular_metabolismo_basal() * self.nivel_ativo
    
    #Funções importantes pra caso o usuário queira mudar no futuro valores específicos da sua conta
    def set_idade(self, idade):
        if idade > 0 and idade < 99:
            self._idade = idade
        else:
            print("Valor inválido!")
    
    def set_peso(self, peso):
        if peso > 0:
            self._peso = peso
        else:
            print("Valor inválido!")

    def set_altura(self, altura):
        if altura > 0:
            self._altura = altura
        else:
            print("Valor inválido!")
    

class Homem(Usuario):
    def calcular_metabolismo_basal(self):
        return 66.5 + (13.75 * self._peso) + (5.0 * self._altura) - (6.8 * self._idade) #Fórmula do Google
    
class Mulher(Usuario):
    def calcular_metabolismo_basal(self):
        return 665.1 + (9.563 * self._peso) + (1.850 * self._altura) - (4.676 * self._idade) #Fórmula do Google

#Criando alimento
class Alimento:
    def __init__(self, nome_alimento, gramas, cal, proteina, carbo, gordura):
        self.nome_alimento = nome_alimento
        self.gramas = gramas
        self.cal = cal
        self.proteina = proteina
        self.carbo = carbo
        self.gordura = gordura
    
    def registrar_alimento(self, dia):
        #Inserir no banco de dados
        cursor.execute(
            """INSERT INTO alimentos_dia (nome_alimento, gramas, cal, proteina, carbo, gordura, dia) \
            VALUES(?, ?, ?, ?, ?, ?, ?)""",
            (self.nome_alimento, self.gramas, self.cal, self.proteina, self.carbo, self.gordura, dia)
            )

        #Atualizando banco de dados
        conn.commit()
            
'''FUNÇÕES'''

def linha():
    print("*-*"*15)

def mensagem_erro():
    print("Você ainda não registrou nenhum alimento!")

def exibir_historico(contagem_dias=None):
    try:
        cursor.execute("""
                        SELECT
                            nome_alimento,
                            SUM(gramas),
                            SUM(cal),
                            SUM(proteina),
                            SUM(carbo),
                            SUM(gordura)
                        FROM alimentos_dia
                        WHERE (? IS NULL OR dia = ?)
                        GROUP BY nome_alimento
                    """, (contagem_dias, contagem_dias))

        alimentos = cursor.fetchall()

        if not alimentos:
            mensagem_erro()
        else:
            for alimento in alimentos:
                print(f"{alimento[0]} -> {alimento[1]}g ({alimento[2]}cal) | {alimento[3]}g de proteina\
| {alimento[4]}g de carboidratos | {alimento[5]}g de gordura")
    

    except sqlite3.OperationalError:
        mensagem_erro()

def calculo_calorias(contagem_dias):
    try:
        cursor.execute("""
                        SELECT
                            SUM(cal)
                            FROM alimentos_dia
                            WHERE (dia = ?)
                        """, (contagem_dias,))

        resultado = cursor.fetchone() #Retorna (X,)

        if resultado[0] is None:
            return 0
        
        return resultado[0]

    
    except sqlite3.OperationalError:
        return 0

def cadastro_usuario():
    nome = input("Qual o seu nome? ")
    idade = int(input("Qual a sua idade? "))
    genero = input("Qual o seu gênero? [M/F] ").upper()[0]
    peso = float(input("Qual o seu peso (kg)? "))
    altura = float(input("Qual a sua altura (cm)? "))
    print("Qual o seu objetivo?")
    print("[1] Perda de peso\n[2] Manutenção\n[3] Ganho de massa")
    resp_objetivo = int(input("Resposta: "))
    objetivo = ""
    match resp_objetivo:
        case 1:
            objetivo = "Perda de peso".lower()
        case 2:
            objetivo = "Manutenção".lower()
        case 3:
            objetivo = "Ganho de massa".lower()

    print("Você se considera:")
    print("[1] Sedentário\n[2] Levemente ativo\n[3] Moderado\n[4] Muito ativo\n[5] Extremamente ativo")
    resp_ativo = int(input("Resposta: "))
    nivel_ativo = 0

    match resp_ativo:
        case 1:
            nivel_ativo = 1.2 #Valor vindo de pesquisa no Google
        case 2:
            nivel_ativo = 1.375 #Valor vindo de pesquisa no Google
        case 3:
            nivel_ativo = 1.55 #Valor vindo de pesquisa no Google
        case 4:
            nivel_ativo = 1.725 #Valor vindo de pesquisa no Google
        case 5:
            nivel_ativo = 1.9 #Valor vindo de pesquisa no Google
    linha()
    print("Cadastro finalizado!")

    if genero == 'M':
        return Homem(nome, idade, peso, altura, objetivo, nivel_ativo)
    else:
        return Mulher(nome, idade, peso, altura, objetivo, nivel_ativo)
    
'''PROGRAMA PRINCIPAL'''
#Introdução ao sistema
linha()
print("Bem-vindo ao sistema nutricional!")
print("Precisamos de algumas informações pro seu cadastro...")
linha()

#Variáveis relacionadas ao funcionamento do programa
contagem_dias = 1
dia = 1
qnt_cal_max = 0 #Relativo ao objetivo do usuário

#Usando a biblioteca sqlite 
conn = sqlite3.connect("alimentos.db")
cursor = conn.cursor()

#Criando banco de dados
cursor.execute(""" 
    CREATE TABLE IF NOT EXISTS alimentos_dia (
        nome_alimento TEXT,
        gramas REAL,
        cal REAL,
        proteina REAL,
        carbo REAL,
        gordura REAL,
        dia INTEGER
    )
    """)

#Construindo o objeto que guarda os dados da pessoa
usuario = cadastro_usuario()

#Calculando TMB e GET
tmb = usuario.calcular_metabolismo_basal()
get = usuario.calcular_gasto_energetico_total()
    
#Calculando objetivos e as calorias para alcançá-los
#Valor 200 utilizado como controle, porém pode variar entre 200-300
if usuario.objetivo == 'perda de peso':
    qnt_cal_max = get - 200
elif usuario.objetivo == 'manutenção':
    qnt_cal_max = get
else:
    qnt_cal_max = get + 200

#Início do programa
print(f"Olá, {usuario.nome}.\nSua taxa metabólica basal é: {tmb:.2f}.\nSeu gasto energético é: {get:.2f}\nSua meta de calorias diária é: {qnt_cal_max:.2f}.")
linha()

while True:
    print("Selecione uma opção: \n[1] Cadastrar um alimento\n[2] Acessar resumo diário\n[3] Acessar histórico" \
    "\n[4] Avançar dia \n[5] Visualizar meta de calorias\n[6] Reiniciar histórico\n[7] Encerrar programa")
    resp_op = int(input("Resposta: "))
    linha()
    match resp_op:
        case 1:
            nome_alimento = input("Qual alimento você comeu? ").lower()
            gramas = float(input("Quanto você comeu? (g) "))
            cal = float(input("Quantas calorias por porção? (cal) "))
            proteina = float(input("Quanto de proteína? (g) "))
            carboidratos = float(input("Quanto de carboidrato? (g) "))
            gordura = float(input("Quanto de gordura? (g) "))
            linha()

            alimento = Alimento(nome_alimento, gramas, cal, proteina, carboidratos, gordura)
            alimento.registrar_alimento(dia)
    
        case 2: 
            exibir_historico(contagem_dias)
            linha()

        case 3:
            exibir_historico()
            linha()

        case 4:
            contagem_dias += 1
            dia += 1
            total_calorias = 0
            print("Você avançou um dia.")
            linha()

        case 5:
            total_calorias = calculo_calorias(contagem_dias)
            if total_calorias > 0:
                if total_calorias < qnt_cal_max:
                    print(f"Falta ainda {qnt_cal_max - total_calorias} calorias pra atingir o objetivo!")
                else:
                    print(f"Você atingiu o objetivo!")
                    if total_calorias > qnt_cal_max:
                        print(f"Você ultrapassou a meta em {total_calorias - qnt_cal_max}")
                linha()
            else:
                mensagem_erro()
                linha()

        case 6:
            try:
                cursor.execute("DELETE FROM alimentos_dia")
                conn.commit()
                print("Histórico reiniciado.")
            except sqlite3.OperationalError:
                mensagem_erro()
            linha()
            
        case 7:
            print("Fim do programa. Até logo!")
            conn.close()
            break
