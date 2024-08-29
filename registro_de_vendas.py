#!/usr/bin/env python
# coding: utf-8

# In[7]:


# Bibliotecas
import os
import sys
import re
import pandas as pd
import tkinter as tk
import datetime
from datetime import datetime, timedelta
from sys import _MEIPASS

global caminho_arquivo


# In[8]:
# Acessa os arquivos txt corretamente no exe
def get_resource_path(filename):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, filename)
    else:
        return os.path.join(os.path.dirname(__file__), filename)

# In[ ]:


# Classe do vendedor
class Vendedor:
    def __init__(self, nome, cpf, salario_bruto) -> None:
        self._nome = nome
        self._cpf = cpf
        self._salario_bruto = salario_bruto
        
        
    @property
    def nome(self):
        return self._nome
    
    @nome.setter
    def nome(self, valor):
        self._nome = valor
        
    @property
    def cpf(self):
        return self._cpf
    
    @cpf.setter
    def cpf(self, valor):
        self._cpf = valor
        
    @property
    def salario_bruto(self):
        return self._salario_bruto
    
    @salario_bruto.setter
    def salario_bruto(self, valor):
        self._salario_bruto = valor


# In[ ]:


class Vendedor_mes(Vendedor):
    def __init__(self, nome, cpf, salario_bruto, comissao_bruta, soma_vendas, desconto_ir, desconto_inss, dsr, total_bruto, total_liquido) -> None:
        super().__init__(nome, cpf, salario_bruto)
        self._soma_vendas = soma_vendas
        self._desconto_ir = desconto_ir
        self._desconto_inss = desconto_inss
        self._dsr = dsr
        self._total_bruto = total_bruto
        self._total_liquido = total_liquido
        self._comissao_bruta = comissao_bruta
        self._meta = 800000.00
        
        
        
    @property
    def comissao_bruta(self):
        return self._comissao_bruta
    
    @comissao_bruta.setter
    def comissao_bruta(self, valor):
        self._comissao_bruta = valor
        
    @property
    def desconto_ir(self):
        return self._desconto_ir
    
    @desconto_ir.setter
    def desconto_ir(self, valor):
        self._desconto_ir = valor
        
    @property
    def desconto_inss(self):
        return self._desconto_inss
        
    @desconto_inss.setter
    def desconto_inss(self, valor):
        self._desconto_inss = valor
        
    @property
    def dsr(self):
        return self._dsr
        
    @dsr.setter
    def dsr(self, valor):
        self._dsr = valor
    
    @property
    def total_bruto(self):
        return self._total_bruto
    
    @total_bruto.setter
    def total_bruto(self, valor):
        self._total_bruto = valor
        
    @property
    def total_liquido(self):
        return self._total_liquido
        
    @total_liquido.setter
    def total_liquido(self, valor):
        self._total_liquido = valor
        
    @property
    def meta(self):
        return self._meta
    
    @meta.setter
    def meta(self, valor):
        self._meta = valor
        
    @property
    def soma_vendas(self):
        return self._soma_vendas
    
    @soma_vendas.setter
    def soma_vendas(self, valor):
        self._soma_vendas = valor
    
    
        
        
    def calcular_desconto_ir(self):
        # Calcula o desconto de IR baseado no total bruto
        if self._total_bruto <= 2112.00:
            self._desconto_ir = 0.00
        elif self._total_bruto <= 2826.65:
            self._desconto_ir = self._total_bruto * 0.075
        elif self._total_bruto <= 3751.05:
            self._desconto_ir = self._total_bruto * 0.15
        elif self._total_bruto <= 4664.68:
            self._desconto_ir = self._total_bruto * 0.225
        else:
            self._desconto_ir = self._total_bruto * 0.275
            
            
    def calcular_desconto_inss(self):
        # Calcula o desconto de INSS baseado no total bruto
        if self._total_bruto <= 1412.00:
            self._desconto_inss = self._total_bruto * 0.075
        elif self._total_bruto <= 2666.68:
            self._desconto_inss = self._total_bruto * 0.09
        elif self._total_bruto <= 4000.03:
            self._desconto_inss = self._total_bruto * 0.12
        elif self._total_bruto <= 7786.02:
            self._desconto_inss = self._total_bruto * 0.14
        else:
            self._desconto_inss = 7786.02 * 0.14
            
    def calcular_comissao(self):
        if self._soma_vendas >= self.meta:
            self._comissao_bruta = 0.01 * self._soma_vendas # 1% de comissão se a meta for batida
            return self._comissao_bruta
        else:
            self._comissao_bruta = 0.0075 * self._soma_vendas # 0,75% de comissão se a meta não for batida   
            return self._comissao_bruta     
    

    def calcular_dsr(self, comissao_bruta, ano, mes, feriados):

        # Calcula o DSR (Descanso Semanal Remunerado) baseado na comissão bruta 
        # domingos, feriados do mês, dias úteis

        # Obter o primeiro e o último dia do mês
        primeiro_dia = datetime(ano, mes, 1)
        ultimo_dia = datetime(ano, mes + 1, 1) - timedelta(days=1) if mes < 12 else datetime(ano, 12, 31)

        # Contagem de dias úteis (segunda a sábado) e não úteis (domingos)
        dias_uteis = 0
        dias_nao_uteis = 0

        # Contar dias úteis e não úteis no mês
        for dia in range(primeiro_dia.day, ultimo_dia.day + 1):
            data_atual = datetime(ano, mes, dia)
            if data_atual.weekday() == 6: # Domingo 
                dias_nao_uteis += 1
            else:  # Dias úteis (segunda a sábado)
                dias_uteis += 1
                
        # Adiciona o número de feriados ao total de dias não úteis, usar função que calcula feriados
        dias_nao_uteis += feriados

        # Calculo do DSR
        dsr = (comissao_bruta * dias_nao_uteis) / dias_uteis
        return dsr
    


# In[ ]:


# Classe venda
class Venda:
    def __init__(self, valor_venda, data) -> None:
        self._valor_venda = valor_venda
        self._data = data
        
    @property
    def valor_venda(self):
        return self._valor_venda
    
    @valor_venda.setter
    def valor_venda(self, valor):
        self._valor_venda = valor 
        
    @property
    def data(self):
        return self._data
    
    @data.setter
    def data(self, valor):
        self._data = valor 


# In[ ]:


def registrar_data_hora():
#Registra a data e hora atuais do pc em execussão no formato dd/mm/yyyy - hh:mm.
    agora = datetime.now()
    data_hora_formatada = agora.strftime('%d/%m/%Y - %H:%M')
    return data_hora_formatada

data_venda = registrar_data_hora()  # Variável que chama a função para obter a data e hora atuais dentro das outras funções


# In[ ]:


# Função para registrar a venda

def registrar_venda(vendedor, venda):
    # Registra uma venda no arquivo vendas.txt.
    caminho_arquivo = get_resource_path('vendas.txt')
    with open(caminho_arquivo, 'a') as arquivo:
        linha = f"{vendedor.nome.title()},{venda.valor_venda},{data_venda}\n"
        arquivo.write(linha)


# In[ ]:


# Buscar vendas

def buscar_vendas_por_data(data):
    #Busca e exibe vendas registradas em um mês específico no formato 'mm/yyyy'
    mes_ano = data
    caminho_arquivo = get_resource_path('vendas.txt')
    with open(caminho_arquivo, 'r') as arquivo:
        print(f"\nVendas registradas em {mes_ano}: \n")
        encontrou = False
        for linha in arquivo:
            nome, valor, data_venda = linha.strip().split(',')
            # Extrai o mês e o ano da data da venda
            mes_ano_venda = data_venda[3:10]
            if mes_ano == mes_ano_venda:
                print(f"Vendedor: {nome.title()}, Valor: {valor}, Data: {data_venda} \n")
                encontrou = True
        if not encontrou:
            print(f"Nenhuma venda encontrada para o mês/ano {mes_ano}.")
            
            

def buscar_vendas_por_funcionario(nome_vendedor):
    # Busca e exibe vendas registradas para um funcionário específico, permite a busca por nome completo ou parcial
    encontrou = False
    nome_vendedor = nome_vendedor.lower().strip()
    caminho_arquivo = get_resource_path('vendas.txt')
    with open(caminho_arquivo, 'r') as arquivo:
        print(f"\nVendas registradas para {nome_vendedor.title()}: \n")
        for linha in arquivo:
            nome, valor, data_venda = linha.strip().split(',')
            # Verifica se o nome_vendedor está contido
            if nome_vendedor in nome.lower():
                print(f"Vendedor: {nome.title()}, Valor: {valor}, Data: {data_venda} \n")
                encontrou = True
        if not encontrou:
            print(f"Nenhuma venda encontrada para o funcionário '{nome_vendedor.title()}'.")


def mostrar_todas_as_vendas():
    # Exibe todas as vendas registradas
    caminho_arquivo = get_resource_path('vendas.txt')
    with open(caminho_arquivo, 'r') as arquivo:
        print("\nTodas as vendas registradas: \n")
        for linha in arquivo:
            nome, valor, data_venda = linha.strip().split(',')
            print(f"Vendedor: {nome.title()}, Valor: {valor}, Data: {data_venda}\n")


# In[ ]:


def calcular_soma_vendas(parcial_nome_vendedor, mes_ano):
    # Calcula a soma de todas as vendas registradas para um vendedor específico
    soma_vendas = 0.0
    parcial_nome_vendedor = parcial_nome_vendedor.lower().strip()

    caminho_arquivo = get_resource_path('vendas.txt')
    with open(caminho_arquivo, 'r') as arquivo:
        for linha in arquivo:
            nome, valor, data_venda = linha.strip().split(',')
            nome = nome.lower().strip()
            data_venda = data_venda.strip()

            # Extrai o mês e o ano da data de venda
            mes_ano_venda = data_venda[3:10]  # Pega os caracteres de 3 a 10 para obter 'mm/yyyy'

            # Verifica se a parcial do nome do vendedor está contida no nome e se a data corresponde ao mês/ano
            if parcial_nome_vendedor in nome and mes_ano_venda == mes_ano:
                soma_vendas += float(valor)

    return soma_vendas


# In[ ]:


# Verifica se o CPF tem exatamente 11 dígitos e contém apenas números
def validar_cpf(cpf):
    if cpf.isdigit() and len(cpf) == 11:
        return True
    
    else:
        return False
    

# Formata o CPF para o formato xxx.xxx.xxx-xx
def formatar_cpf(cpf):
    return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"    
    

# Valida a data no formato dd/mm/yyyy ou mm/yyyy
def validar_data(data, formato='dd/mm/yyyy'):
    if formato == 'dd/mm/yyyy' and len(data) == 10:
        # Validação para formato dd/mm/yyyy
        if data[2] != '/' or data[5] != '/':
            return False
        dia, mes, ano = data[:2], data[3:5], data[6:]
    elif formato == 'mm/yyyy' and len(data) == 7:
        # Validação para formato mm/yyyy
        if data[2] != '/':
            return False
        dia, mes, ano = '01', data[:2], data[3:]
    else:
        return False

    if not (dia.isdigit() and mes.isdigit() and ano.isdigit()):
        return False
    
    dia = int(dia)
    mes = int(mes)
    ano = int(ano)

    if mes < 1 or mes > 12:
        return False
    if dia < 1 or dia > 31:
        return False

    return True

# In[ ]:


# valida se o nome do funcionário está registrado no arquivo vendedor.txt
def validar_nome_funcionario(nome):
    caminho_arquivo = get_resource_path('vendedor.txt')
    with open(caminho_arquivo, "r") as arquivo:
        for linha in arquivo:
            _, nome_registrado, _ = linha.strip().split(',')
            if nome.strip().title() in nome_registrado.strip().title():
                return True
    return False


# In[ ]:

# Puxa o salario bruto do vendedor 
def salario_vendedor(vendedor_nome):
    vendedor_nome = vendedor_nome.title()
    
    caminho_arquivo = get_resource_path('vendedor.txt')
    with open(caminho_arquivo, 'r') as arquivo:
        for linha in arquivo:
            partes = linha.strip().split(',')
            if len(partes) >= 3:  # Verifica se há pelo menos três partes
                cpf = partes[0]
                nome = partes[1].strip()
                salario = partes[2].strip()
                if vendedor_nome in nome: # Comparar diretamente com o nome em formato title
                    return float(salario)
    
    return None # Retorna None se não encontrar o vendedor


# Filtra vendas registradas para um mês/ano específico no arquivo vendas
def filtrar_vendas(mes_ano):
    registros_filtrados = []
    
    caminho_arquivo = get_resource_path('vendas.txt')
    with open(caminho_arquivo, 'r') as arquivo:
        for linha in arquivo:
            nome, valor, data_venda = linha.strip().split(',')
            mes_ano_venda = data_venda[3:10] # Extrai o mês/ano da data da venda
            if mes_ano == mes_ano_venda:
                registros_filtrados.append((nome, float(valor), data_venda))
    
    return registros_filtrados

# Filtra vendas por mês/ano e vendedor no arquivo vendas
def filtrar_vendas_por_vendedor_mes(vendedor_nome, mes_ano):
    registros_filtrados = []
    
    caminho_arquivo = get_resource_path('vendas.txt')
    with open(caminho_arquivo, 'r') as arquivo:
        for linha in arquivo:
            nome, valor, data_venda = linha.strip().split(',')
            mes_ano_venda = data_venda[3:10]  # Extrai o mês/ano da data da venda
            if mes_ano == mes_ano_venda and nome.lower() == vendedor_nome.lower():
                registros_filtrados.append((nome, float(valor), data_venda))
    
    return registros_filtrados


# In[ ]:


# Cria arquivos Excel fora do .exe

def exportar_vendas_por_nome(nome_arquivo, nome_vendedor):
    # Adiciona a extensão do arquivo se não estiver presente
    if not nome_arquivo.lower().endswith('.xlsx'):
        nome_arquivo += '.xlsx'
        
    registros = []
    nome_vendedor = nome_vendedor.title()
    
    caminho_arquivo = get_resource_path('vendas.txt')
    with open(caminho_arquivo, 'r') as arquivo:
        for linha in arquivo:
            nome, valor, data_venda = linha.strip().split(',')
            if nome_vendedor in nome.split():
                registros.append((nome, float(valor), data_venda))
    
    df = pd.DataFrame(registros, columns=['Funcionário', 'Valor da venda', 'Data da Venda'])   
    df.to_excel(nome_arquivo, index=False)



def exportar_vendas_por_data(nome_arquivo, mes_ano):
    if not nome_arquivo.lower().endswith('.xlsx'):
        nome_arquivo += '.xlsx'
        
    registros = filtrar_vendas(mes_ano)
    
    df = pd.DataFrame(registros, columns=['Funcionário', 'Valor da venda', 'Data da Venda'])
    df.to_excel(nome_arquivo, index=False)


def exportar_todos_os_registros(nome_arquivo):
    if not nome_arquivo.lower().endswith('.xlsx'):
        nome_arquivo += '.xlsx'
        
    registros = []
    
    caminho_arquivo = get_resource_path('vendas.txt')
    with open(caminho_arquivo, 'r') as arquivo:
        for linha in arquivo:
            nome, valor, data_venda = linha.strip().split(',')
            registros.append((nome, float(valor), data_venda))
    
    df = pd.DataFrame(registros, columns=['Funcionário', 'Valor da venda', 'Data da Venda'])
    df.to_excel(nome_arquivo, index=False)


# In[ ]:

def gerenciar_feriados():
    feriados = set()
    
    # Lê os feriados existentes
    try:
        caminho_arquivo = get_resource_path('feriados.txt')
        with open(caminho_arquivo, 'r') as arquivo:
            for linha in arquivo:
                feriados.add(linha.strip())
    except FileNotFoundError:
        pass # Arquivo não existe, vamos criá-lo mais tarde

    while True:
        existe = input("Existe algum feriado no mês? (s/n): ").strip().lower()
        
        if existe == 's':
            data = input("Digite a data do feriado (dd/mm/yyyy): ").strip()

            if not validar_data(data):
                print("Data inválida. Tente novamente.")
                continue
            
            if data in feriados:
                print("A data já existe no registro.")
            else:
                feriados.add(data)
                print(f"Data {data} adicionada com sucesso.")

            mais_feriados = input("Deseja adicionar mais feriados? (s/n): ").strip().lower()
            if mais_feriados != 's':
                break
        
        elif existe == 'n':
            break
        
        else:
            print('Opção inválida. Por favor, escolha uma opção válida.')
        
    while True:
        apagar_data = input("Deseja apagar um feriado? (s/n): ").strip().lower()
        if apagar_data == 's':
            data_apagar = input("Digite a data a ser apagada (dd/mm/yyyy): ").strip()
            if data_apagar in feriados:
                feriados.remove(data_apagar)
                print(f"Data {data_apagar} removida com sucesso.")
            else:
                print("Data não encontrada no registro.")
        else:
            break

    # Grava os feriados no arquivo
    caminho_arquivo = get_resource_path('feriados.txt')
    with open(caminho_arquivo, 'w') as arquivo:
        for data in sorted(feriados):
            arquivo.write(data + '\n')

    print("Feriados atualizados com sucesso!")
    
# Retorna um número inteiro de quantos feriados existem no arquivo referente ao mês especificado para uso do DSR    
def contar_feriados(mes_ano):
    try:
        caminho_arquivo = get_resource_path('feriados.txt')
        with open(caminho_arquivo, 'r') as arquivo:
            numero_feriados = 0
            for linha in arquivo:
                data = linha.strip()
                if len(data) == 10 and data[2] == '/' and data[5] == '/':
                    dia, mes, ano = data.split('/')
                    if f"{mes}/{ano}" == mes_ano:
                        numero_feriados += 1
        
        print(f"Total de feriados em {mes_ano}: {numero_feriados}")
        return numero_feriados
    except FileNotFoundError:
        print("O arquivo 'feriados' não foi encontrado.")
        return 0
    

def calcular_relatorio_vendedor(vendedor_nome, mes_ano):
    # Calcula e retorna um relatório com as informações de vendas, salários, comissão e descontos para um vendedor específico em um mês/ano
    gerenciar_feriados() # Chama função para add feriados se necessário
    # Filtra vendas para o mês/ano especificado
    registros_filtrados = filtrar_vendas(mes_ano)
    # Filtra vendas para o vendedor específico
    vendas_vendedor = [
        (nome, valor, data_venda)
        for nome, valor, data_venda in registros_filtrados
        if vendedor_nome.lower() in nome.lower()
    ]

    if not vendas_vendedor:
        return f"Nenhuma venda encontrada para o vendedor '{vendedor_nome.title()}' no mês {mes_ano}."

    # Calcula soma das vendas
    soma_vendas = calcular_soma_vendas(vendedor_nome, mes_ano)
 
    # Cria uma instância de Vendedor_mes com os dados do vendedor
    vendedor = Vendedor_mes(
        nome=vendedor_nome.title(),
        cpf=None, # Não será utilizado
        salario_bruto=0,  # Inicialmente 0, será calculado abaixo
        comissao_bruta=0,  # Inicialmente 0, será calculado abaixo
        soma_vendas=soma_vendas,
        desconto_ir=0,  # Inicialmente 0, será calculado abaixo
        desconto_inss=0,  # Inicialmente 0, será calculado abaixo
        dsr=0,  # Inicialmente 0, será calculado abaixo
        total_bruto=0,  # Inicialmente 0, será calculado abaixo
        total_liquido=0  # Inicialmente 0, será calculado abaixo
    )
    
    # Lê o salário bruto do vendedor do arquivo 'vendedor.txt'
    vendedor.salario_bruto = salario_vendedor(vendedor_nome)
    
    # Calcula a comissão
    vendedor.comissao_bruta = vendedor.calcular_comissao()
    comissao = vendedor.comissao_bruta
    # Calcula o DSR
    ano = datetime.strptime(mes_ano, "%m/%Y").year
    mes = datetime.strptime(mes_ano, "%m/%Y").month
    feriados = contar_feriados(mes_ano)
    dsr = vendedor.calcular_dsr(comissao, ano, mes, feriados)
    vendedor.dsr = dsr
    # Calcula o salario bruto
    vendedor.total_bruto = vendedor.salario_bruto + vendedor.comissao_bruta + vendedor.dsr
    # Chama as funções para os cálculos dos descontos
    vendedor.calcular_desconto_ir()
    vendedor.calcular_desconto_inss()
    
    # Calcula o total líquido
    vendedor.total_liquido = vendedor.total_bruto - vendedor.desconto_ir - vendedor.desconto_inss
    
    # Verifica se o vendedor atingiu a meta de vendas
    meta_atendida = "Sim" if vendedor.soma_vendas >= vendedor.meta else "Não"
    
    
    # Retorna o relatório em dict
    relatorio = {
        'nome': vendedor.nome,
        'mes_ano': mes_ano,
        'soma_vendas': vendedor.soma_vendas,
        'salario_bruto': vendedor.salario_bruto,
        'comissao_bruta': vendedor.comissao_bruta,
        'dsr': vendedor.dsr,
        'desconto_ir': vendedor.desconto_ir,
        'desconto_inss': vendedor.desconto_inss,
        'total_bruto': vendedor.total_bruto,
        'total_liquido': vendedor.total_liquido,
        'meta_atendida': meta_atendida
    }
    
    return relatorio

# Função para registrar o relatório no arquivo vendedor_mes.txt
def registrar_relatorio_vendedor():
    vendas_por_vendedor_mes = {}

    # Lê o arquivo de vendas e organiza as vendas por vendedor e mês
    caminho_arquivo = get_resource_path('vendas.txt')
    with open(caminho_arquivo, 'r') as vendas_file:
        for linha in vendas_file:
            nome, valor, data_venda = linha.strip().split(',')
            mes_ano = data_venda[3:10]  # Extrai o mês/ano da data da venda

            # Usa o dicionário para organizar vendas por vendedor e por mês/ano
            if (nome, mes_ano) not in vendas_por_vendedor_mes:
                vendas_por_vendedor_mes[(nome, mes_ano)] = []
            vendas_por_vendedor_mes[(nome, mes_ano)].append((nome, valor, data_venda))

    # Lê os registros existentes de vendedor_mes.txt e os armazena em um dicionário para facilitar a atualização
    registros_existentes = {}
    try:
        caminho_arquivo = get_resource_path('vendedor_mes.txt')
        with open(caminho_arquivo, 'r') as relatorio_file:
            for linha in relatorio_file:
                dados = linha.strip().split(',')
                vendedor_existente, mes_ano_existente = dados[0], dados[1]
                registros_existentes[(vendedor_existente, mes_ano_existente)] = linha.strip()
    except FileNotFoundError:
        # Arquivo não encontrado, não há registros existentes para atualizar
        pass

    # Abre o arquivo para escrita, o que vai apagar seu conteúdo, e reescreve com atualizações
    caminho_arquivo = get_resource_path('vendedor_mes.txt')
    with open(caminho_arquivo, 'w') as relatorio_file:
        for (vendedor_nome, mes_ano), _ in vendas_por_vendedor_mes.items():
            relatorio = calcular_relatorio_vendedor(vendedor_nome, mes_ano)
            
            if isinstance(relatorio, str):  # Se o relatorio retornar uma string, significa que não há vendas
                continue
            
            # Converte o relatório em uma linha de texto
            relatorio_linha = ",".join([
                relatorio['nome'], 
                mes_ano, 
                f"{relatorio['soma_vendas']:.2f}", 
                f"{relatorio['salario_bruto']:.2f}", 
                f"{relatorio['comissao_bruta']:.2f}", 
                f"{relatorio['dsr']:.2f}", 
                f"{relatorio['desconto_ir']:.2f}", 
                f"{relatorio['desconto_inss']:.2f}", 
                f"{relatorio['total_bruto']:.2f}", 
                f"{relatorio['total_liquido']:.2f}", 
                relatorio['meta_atendida']
            ])

            # Atualiza ou adiciona a linha no arquivo de relatório
            registros_existentes[(vendedor_nome, mes_ano)] = relatorio_linha

        # Escreve todas as linhas atualizadas de volta no arquivo
        for linha_atualizada in registros_existentes.values():
            relatorio_file.write(linha_atualizada + '\n')


def formatar_registro(dados):
    # Formata uma linha de registro para quando imprimir na tela
    vendedor_nome = dados[0]
    mes_ano = dados[1]
    soma_vendas = f"{float(dados[2]):.2f}"
    salario_bruto = f"{float(dados[3]):.2f}"
    comissao_bruta = f"{float(dados[4]):.2f}"
    dsr = f"{float(dados[5]):.2f}"
    desconto_ir = f"{float(dados[6]):.2f}"
    desconto_inss = f"{float(dados[7]):.2f}"
    total_bruto = f"{float(dados[8]):.2f}"
    total_liquido = f"{float(dados[9]):.2f}"
    meta_atendida = dados[10]

    return {
        "Vendedor": vendedor_nome,
        "Mês/Ano": mes_ano,
        "Soma de Vendas": soma_vendas,
        "Salário Bruto": salario_bruto,
        "Comissão Bruta": comissao_bruta,
        "DSR": dsr,
        "Desconto IR": desconto_ir,
        "Desconto INSS": desconto_inss,
        "Total Bruto": total_bruto,
        "Total Líquido": total_liquido,
        "Meta Atingida": meta_atendida
    }
   
# Mostra todos os registros no arquivo vendedor_mes.txt
def mostrar_todos():
    caminho_arquivo = get_resource_path('vendedor_mes.txt')
    with open(caminho_arquivo, 'r') as arquivo:
        registros = [formatar_registro(linha.strip().split(',')) for linha in arquivo]
    return registros

def filtrar_por_nome(nome):
    # Filtra registros no arquivo vendedor_mes.txt por nome de funcionário
    caminho_arquivo = get_resource_path('vendedor_mes.txt')
    with open(caminho_arquivo, 'r') as arquivo:
        registros = [formatar_registro(linha.strip().split(',')) for linha in arquivo if nome.lower() in linha.split(',')[0].lower()]
    return registros

# Funções para exportar registros para um arquivo .xlsx no caminho a ser especificado
def exportar_para_excel(registros, nome_arquivo):
    df = pd.DataFrame(registros)
    caminho_completo = os.path.join(nome_arquivo)
    df.to_excel(caminho_completo, index=False)
    print(f"Arquivo exportado com sucesso para: {caminho_completo}")

def exportar_por_funcionario(nome):
    registros = filtrar_por_nome(nome)
    if registros:
        nome_arquivo = f"{nome}_relatorio.xlsx"
        exportar_para_excel(registros, nome_arquivo)
    else:
        print("\nNenhum registro encontrado para o nome fornecido.")

def exportar_todos():
    registros = mostrar_todos()
    if registros:
        nome_arquivo = "todos_registros.xlsx"
        exportar_para_excel(registros, nome_arquivo)
    else:
        print("\nNão há registros para exportar.")


# In[ ]:


# Menus

menu_inicial = """Selecione a opção desejada:
                    
                    [1] Registrar nova venda
                    [2] Verificar vendas realizadas
                    [3] Importar registros
                    [4] Menu de funcionários
                    [5] Sair
                    
                    """
                    
verificar_vendas = """Selecione a opção desejada:
                        
                        [1] Buscar vendas por data
                        [2] Buscar vendas por funcionário
                        [3] Mostrar todas as vendas registradas
                        [4] Voltar ao menu anterior
                        
                        """
                        
menu_funcionarios = """Selecione a opção desejada:
                        
                        [1] Registrar novo funcionário
                        [2] Verificar registro de funcionários
                        [3] Apagar registros de funcionário
                        [4] Verificar cálculos dos funcionários
                        [5] Voltar ao menu anterior
                        
                        """                        
                        
importar_registros = """Selecione a opção desejada:

                        [1] Importar registro detalhado de vendas por funcionário
                        [2] Importar registro detalhado de vendas por data
                        [3] Importar todos os registros detalhados de vendas
                        [4] Importar cálculo mensal de funcionário
                        [5] Importar todos os cálculos mensais dos funcionários
                        [6] Apagar registros
                        [7] Voltar ao menu anterior

                        """
                        
apagar_registros = """Selecione a opção desejada:
                        
                        [1] Apagar registros de venda por funcionário  
                        [2] Apagar registros de venda por data
                        [3] Apagar todos os registros de vendas
                        [4] Apagar todos os registros de cálculos mensais dos funcionários
                        [5] Voltar ao menu anterior
                        
                        ** ATENÇÃO, APAGAR UM REGISTRO É IRREVERSÍVEL, USE COM CAUTELA**
                        
                        """


# In[ ]:

def main():
    while True:       

        opcao = input(menu_inicial)
        
        if opcao == '1':
            # Registrar nova venda
            nome_vendedor = input("Digite o nome do vendedor: ").strip().title()
            # Verifica se o nome do vendedor é válido
            if not validar_nome_funcionario(nome_vendedor):
                print("Nome de vendedor inválido. O vendedor deve estar registrado.")
                continue
            valor_venda = input("Digite o valor da venda (formato xxxx,xx): R$ ").strip()
            # Verifica se o valor está no formato correto usando regex
            if not re.match(r"^\d+,\d{2}$", valor_venda):
                print("Erro: O valor da venda deve estar no formato xxxx,xx. Tente novamente.")
                continue
            try:
                valor_float = float(valor_venda.replace(',', '.'))
            except ValueError:
                print("Valor da venda inválido. Use o formato xxxx,xx.")
                return
            # Formata a data e hora da venda
            data_venda = registrar_data_hora()
            # Registra a venda no arquivo vendas.txt
            caminho_arquivo = get_resource_path("vendas.txt")
            with open(caminho_arquivo, "a") as arquivo:
                arquivo.write(f"{nome_vendedor},{valor_float:.2f},{data_venda}\n")
            print("Venda registrada com sucesso.")
        
        
        elif opcao == '2':
            # Verificar vendas realizadas
            verificar = input(verificar_vendas)
            
            if verificar == "1": 
                # Buscar vendas por data
                data = input("Digite o mês e ano para a busca (mm/yyyy): ").strip()
                if validar_data(data, formato='mm/yyyy'):
                    buscar_vendas_por_data(data)
                else:
                    print("Formato de data inválido. Por favor, insira no formato mm/yyyy.")
                    
            elif verificar == "2":
                # Buscar vendas por funcionário
                nome_vendedor = input("Digite o nome do funcionário para a busca: ").strip()
                buscar_vendas_por_funcionario(nome_vendedor)
                
            elif verificar == "3":
                # Mostrar todas as vendas registradas
                mostrar_todas_as_vendas()
                
            elif verificar == "4":
                # Voltar ao menu anterior
                print("Voltando ao menu anterior...")
                break
            
            else:
                print("Opção inválida. Por favor, escolha uma opção válida.")
        
        
        elif opcao == '3':
            # Importar registros de vendas
            importarregistro = input(importar_registros)
            
            if importarregistro == '1':  # Importar registro detalhado de vendas por funcionário
                nome_vendedor = input("Digite o nome do vendedor: ").strip().title()
                caminho_arquivo = input("Digite o caminho da pasta onde deseja salvar o arquivo: ").strip()
                if not os.path.exists(caminho_arquivo):
                    print("A pasta especificada não existe. Tente novamente.")
                    continue
                nome_arquivo = os.path.join(caminho_arquivo, f'{nome_vendedor}_vendas.xlsx')
                exportar_vendas_por_nome(nome_arquivo, nome_vendedor)
                print(f"Registros de vendas para o vendedor '{nome_vendedor}' foram importados para {caminho_arquivo}.")

            elif importarregistro == '2':  # Importar registro detalhado de vendas por data
                mes_ano = input("Digite o mês e ano no formato MM/YYYY: ").strip()
                caminho_arquivo = input("Digite o caminho da pasta onde deseja salvar o arquivo: ").strip()
                if not os.path.exists(caminho_arquivo):
                    print("A pasta especificada não existe. Tente novamente.")
                    continue
                nome_arquivo = os.path.join(caminho_arquivo, f'{mes_ano}_vendas.xlsx')
                exportar_vendas_por_data(nome_arquivo, mes_ano)
                print(f"Registros de vendas para o mês {mes_ano} foram importados para {caminho_arquivo}.")

            elif importarregistro == '3':  # Importar todos os registros detalhados de vendas
                caminho_arquivo = input("Digite o caminho da pasta onde deseja salvar o arquivo: ").strip()
                if not os.path.exists(caminho_arquivo):
                    print("A pasta especificada não existe. Tente novamente.")
                    continue
                nome_arquivo = os.path.join(caminho_arquivo, f'geral_vendas.xlsx')
                exportar_todos_os_registros(nome_arquivo)
                print(f"Todos os registros de vendas foram importados para {caminho_arquivo}.")

            elif importarregistro == '4': # Importar cálculo mensal de funcionário
                nome = input("Digite o nome do funcionário para exportar: ").title()
                caminho_arquivo = input("Digite o caminho da pasta onde deseja salvar o arquivo: ").strip()
                if not os.path.exists(caminho_arquivo):
                    print("A pasta especificada não existe. Tente novamente.")
                    continue
                exportar_por_funcionario(nome)
                print(f"Todos os registros de vendas foram importados para {caminho_arquivo}.")
                      
            elif importarregistro == '5': # Importar todos os cálculos mensais dos funcionários
                registrar_relatorio_vendedor()
                caminho_arquivo = input("Digite o caminho da pasta onde deseja salvar o arquivo: ")
                if not os.path.exists(caminho_arquivo):
                    print("A pasta especificada não existe. Tente novamente.")
                    continue
                exportar_todos()
                print(f"Todos os registros de vendas foram importados para {caminho_arquivo}.")
               
            elif importarregistro == '6': # Apagar registros
                apagar = input(apagar_registros)
                if apagar == '1': # Apagar registros de venda por funcionário
                    nome_funcionario = input("Digite o nome do funcionário para ter os registros apagados: ").title()
                    registros_vendedor = []
                    registros_restantes = []
                
                    # Lê o arquivo de vendas e filtra os registros do funcionário
                    caminho_arquivo = get_resource_path('vendas.txt')
                    with open(caminho_arquivo, 'r') as arquivo:
                        for linha in arquivo:
                            nome, valor, data_venda = linha.strip().split(',')
                            if nome_funcionario.lower() in nome.lower():
                                registros_vendedor.append((nome, valor, data_venda))
                            else:
                                registros_restantes.append(linha.strip())
                
                    if registros_vendedor:
                        print("\nRegistros encontrados para o funcionário '{}':".format(nome_funcionario))
                        for registro in registros_vendedor:
                            print(f"Vendedor: {registro[0]}, Valor: {registro[1]}, Data: {registro[2]}")
                
                        confirmacao = input("\nDeseja realmente apagar esses registros? (s/n): ").strip().lower()
                
                        if confirmacao == 's':
                            # Sobrescreve o arquivo de vendas com os registros restantes
                            caminho_arquivo = get_resource_path('vendas.txt')
                            with open(caminho_arquivo, 'w') as arquivo:
                                for registro in registros_restantes:
                                    arquivo.write(registro + '\n')
                            print("Registros apagados com sucesso.")
                        else:
                            print("Operação cancelada. Nenhum registro foi apagado.")
                    else:
                        print(f"\nNenhum registro encontrado para o funcionário '{nome_funcionario}'.")

                    
                elif apagar == '2': # Apagar registros de venda por data
                    # Filtra vendas para o mês/ano especificado
                    data_input = input("Digite a data para filtrar os registros a serem apagados (formato MM/YYYY): ")
                    if not validar_data(data_input, formato='mm/yyyy'):
                        print("Data inválida. Por favor, insira no formato MM/YYYY.")
                        continue
                    mes_ano = data_input
                    registros_vendidos = filtrar_vendas(mes_ano)
                    registros_restantes = []
                
                    if registros_vendidos:
                        print("\nRegistros encontrados para o mês/ano '{}':".format(mes_ano))
                        for registro in registros_vendidos:
                            print(f"Vendedor: {registro[0]}, Valor: {registro[1]:.2f}, Data: {registro[2]}")
                
                        confirmacao = input("\nDeseja realmente apagar esses registros? (s/n): ").strip().lower()
                
                        if confirmacao == 's':
                            # Recria a lista de registros restantes, excluindo os registros filtrados
                            caminho_arquivo = get_resource_path('vendas.txt')
                            with open(caminho_arquivo, 'r') as arquivo:
                                for linha in arquivo:
                                    nome, valor, data_venda = linha.strip().split(',')
                                    mes_ano_venda = data_venda[3:10]
                                    if mes_ano != mes_ano_venda:
                                        registros_restantes.append(linha.strip())
                
                            # Sobrescreve o arquivo de vendas com os registros restantes
                            caminho_arquivo = get_resource_path('vendas.txt')
                            with open(caminho_arquivo, 'w') as arquivo:
                                for registro in registros_restantes:
                                    arquivo.write(registro + '\n')
                
                            print("Registros apagados com sucesso.")
                        else:
                            print("Operação cancelada. Nenhum registro foi apagado.")
                    else:
                        print(f"\nNenhum registro encontrado para o mês/ano '{mes_ano}'.")
                      
                
                elif apagar == '3': # Apagar todos os registros de vendas
                    confirmacao = input("\nDeseja realmente apagar todos os registros de vendas? (s/n): ").strip().lower()

                    if confirmacao == 's':
                        # Limpa o arquivo de vendas
                        caminho_arquivo = get_resource_path('vendas.txt')
                        open(caminho_arquivo, 'w').close()  # Apaga todo o conteúdo do arquivo

                        print("Todos os registros foram apagados com sucesso.")
                    else:
                        print("Operação cancelada. Nenhum registro foi apagado.")  
   
                    
                elif apagar == '4': # Apagar todos os registros de cálculos mensais dos funcionários
                    confirmacao = input("\nDeseja realmente apagar todos os registros de cálculos mensais dos funcionários? (s/n): ").strip().lower()

                    if confirmacao == 's':
                        # Limpa o arquivo de cálculos mensais dos funcionários
                        caminho_arquivo = get_resource_path('vendedor_mes.txt')
                        open(caminho_arquivo, 'w').close()  # Apaga todo o conteúdo do arquivo

                        print("Todos os registros foram apagados com sucesso.")
                    else:
                        print("Operação cancelada. Nenhum registro foi apagado.")

    
                elif apagar == '5': # Voltar ao menu anterior
                    break
                    
                    
                else:
                    print('Opção inválida. Por favor, escolha uma opção válida.')
                    
            
            elif importarregistro == '7': # Voltar ao menu anterior
                break
                       
            else:
                print('Opção inválida. Por favor, escolha uma opção válida.')
                   
        
        elif opcao == '4':
            # Menu de funcionários
            menufuncionario = input(menu_funcionarios)
            
            if menufuncionario == '1': # Registrar novo funcionário
                # Solicita o CPF do funcionário e garante que apenas números sejam inseridos
                cpf = input("Digite o CPF do funcionário (apenas números): ").strip()
                if not validar_cpf(cpf):
                    print("CPF inválido! O CPF deve conter exatamente 11 dígitos numéricos.")
                    continue
                # Formata o CPF
                cpf_formatado = formatar_cpf(cpf)
                # Verifica se o CPF já está cadastrado
                try:
                    caminho_arquivo = get_resource_path("vendedor.txt")
                    with open(caminho_arquivo, "r") as arquivo:
                        registros = arquivo.readlines()
                        cpf_existente = any(cpf_formatado in linha for linha in registros)
            
                        if cpf_existente:
                            print("Funcionário já está cadastrado.")
                            continue
                except FileNotFoundError:
                # Se o arquivo não existir, segue para o cadastro
                    pass
    
                # Solicita o nome do funcionário
                nome = input("Digite o nome do funcionário: ").strip().title()
    
                # Solicita o salário bruto do funcionário
                while True:
                    salario_bruto_str = input("Digite o salário bruto do funcionário (formato xxxx,xx): R$ ").strip()
                    # Verifica se o salário está no formato correto usando regex
                    if not re.match(r"^\d+,\d{2}$", salario_bruto_str):
                        print("Erro: O salário bruto deve estar no formato xxxx,xx. Tente novamente.")
                        continue

                    try:
                        # Substitui a vírgula por ponto e converte para float
                        salario_bruto = float(salario_bruto_str.replace(",", "."))
                        break
                    except ValueError:
                        print("Valor de salário inválido! Use o formato xxxx,xx e digite um valor numérico.")
    
                # Exibe as informações e pede confirmação
                print(f"\nConfirme os dados do funcionário:")
                print(f"CPF: {cpf_formatado}")
                print(f"Nome: {nome}")
                print(f"Salário Bruto: R$ {salario_bruto:.2f}\n")
    
                confirmar = input("As informações estão corretas? (s/n): ").strip().lower()
                if confirmar == 's':
                    # Grava as informações no arquivo vendedor.txt
                    caminho_arquivo = get_resource_path("vendedor.txt")
                    with open(caminho_arquivo, "a") as arquivo:
                        arquivo.write(f"{cpf_formatado},{nome},{salario_bruto:.2f}\n")
                    print("Funcionário cadastrado com sucesso!\n")
                else:
                    print("Cadastro cancelado. Por favor, insira os dados novamente.\n")
        
                
            elif menufuncionario == '2': # Verificar registro de funcionários
                # Solicita o CPF do funcionário e garante que apenas números sejam inseridos
                cpf = input("Digite o CPF do funcionário (apenas números): ").strip()
                if not validar_cpf(cpf):
                    print("CPF inválido! O CPF deve conter exatamente 11 dígitos numéricos.")
                    continue
                # Formata o CPF
                cpf_formatado = formatar_cpf(cpf)
                # Verifica se o CPF já está cadastrado
                try:
                    caminho_arquivo = get_resource_path("vendedor.txt")
                    with open(caminho_arquivo, "r") as arquivo:
                        registros = arquivo.readlines()
                        cpf_existente = any(cpf_formatado in linha for linha in registros)
            
                        if cpf_existente:
                            # Encontrar a linha específica com o CPF
                            for linha in registros:
                                if cpf_formatado in linha:
                                    dados = linha.strip().split(",")                                    
                                    cpf_registrado = dados[0]
                                    nome_registrado = dados[1]
                                    salario_registrado = dados[2]
                                    print(f"\nCPF: {cpf_registrado}")
                                    print(f"Nome: {nome_registrado}")
                                    print(f"Salário Bruto: {salario_registrado}\n")
                                    break
                        if not cpf_existente:
                            print("Funcionário não cadastrado.")
                            continue
                except FileNotFoundError:
                    print("Arquivo de registros não encontrado.")
                    break                
            
                    
            elif menufuncionario == '3':  # Apagar registro de funcionário
                # Solicita o CPF do funcionário e garante que apenas números sejam inseridos
                cpf = input("""ATENÇÃO, ESSA AÇÃO IRÁ APAGAR TODOS OS REGISTROS EXISTENTES DESTE FUNCIONÁRIO IRREVERSIVELMENTE\n
                            Digite o CPF do funcionário (apenas números): """).strip()
                if not validar_cpf(cpf):
                    print("CPF inválido! O CPF deve conter exatamente 11 dígitos numéricos.")
                    continue
                # Formata o CPF
                cpf_formatado = formatar_cpf(cpf)
                # Verifica se o CPF já está cadastrado e obtém o nome associado
                try:
                    caminho_arquivo = get_resource_path("vendedor.txt")
                    with open(caminho_arquivo, "r") as arquivo:
                        registros = arquivo.readlines()
                        cpf_existente = any(cpf_formatado in linha for linha in registros)

                        if cpf_existente:
                            for linha in registros:
                                if cpf_formatado in linha:
                                    dados = linha.strip().split(",")
                                    nome_registrado = dados[1]
                                    break

                            # Remove todas as linhas contendo o nome nos arquivos
                            caminho_arquivo1 = get_resource_path("vendedor.txt")
                            caminho_arquivo2 = get_resource_path("vendas.txt")
                            caminho_arquivo3 = get_resource_path("vendedor_mes.txt")
                            for arquivo_nome in [caminho_arquivo1, caminho_arquivo2, caminho_arquivo3]:
                                try:
                                    with open(arquivo_nome, "r") as arquivo:
                                        linhas = arquivo.readlines()

                                    with open(arquivo_nome, "w") as arquivo:
                                        for linha in linhas:
                                            if nome_registrado not in linha:
                                                arquivo.write(linha)

                                except FileNotFoundError:
                                    print(f"Arquivo {arquivo_nome} não encontrado. Pulando remoção.")

                            print(f"Funcionário {nome_registrado} e seus registros foram removidos.")

                        else:
                            print("Funcionário não cadastrado.")
                            continue

                except FileNotFoundError:
                    print("Arquivo de vendedores não encontrado. Não foi possível realizar a operação.")
                    break


            elif menufuncionario == '4': # Verificar cálculos dos funcionário
                registrar_relatorio_vendedor()
                registros = mostrar_todos()
                if registros:
                    print("\nTodos os registros:\n")
                    for registro in registros:
                        for chave, valor in registro.items():
                            print(f"{chave}: {valor}")
                        print()  # Linha em branco para separar os registros
                else:
                    print("\nNão há registros para mostrar.")
                
                     
            elif menufuncionario == '5': # Voltar ao menu anterior
                break
                
            else:
                print('Opção inválida. Por favor, escolha uma opção válida.')
                       
        
        elif opcao == '5':
            # Sair
            break
        
        
        else:
            print('Opção inválida. Por favor, escolha uma opção válida.')


    root = tk.Tk()
    root.title("Triumph | Floripa")
    root.geometry("300x200")  # Ajuste o tamanho da janela 

    # Adiciona um widget Label para mostrar alguma informação
    label = tk.Label(root, text="Feche a janela para sair.\n Projeto criado por Letícia Bertoldi.\n https://github.com/Lelebertoldi\n https://www.linkedin.com/in/lelebertoldi/")
    label.pack(padx=15, pady=15)

    root.mainloop()

if __name__ == "__main__":
    main()

