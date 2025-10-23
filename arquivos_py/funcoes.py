# Bibliotecas
import os
import sys
import pandas as pd
import datetime
from datetime import datetime
import classes

# Acessa os arquivos txt
def get_resource_path(filename, permanent=False):
    if hasattr(sys, '_MEIPASS') and not permanent:
        # Quando empacotado com PyInstaller
        return os.path.join(sys._MEIPASS, filename)
    else:
        # Quando em desenvolvimento ou em um script .py
        #diretorio = os.path.dirname(os.path.abspath(__file__))  # Diretório do script .py
        #return os.path.join(diretorio, filename)
    
        # Diretório onde o script está localizado, ou onde o executável está localizado
        diretorio = os.path.dirname(sys.executable)  # Diretório do executável
        #print(f"Diretório do executável: {diretorio}")  # Adicionado para depuração
        return os.path.join(diretorio, filename)


def inicializar_arquivos():
    # Lista dos nomes dos arquivos necessários
    arquivos = ['vendas.txt', 'feriados.txt', 'vendedor.txt', 'vendedor_mes.txt']
    
    for arquivo in arquivos:
        # Caminho do arquivo no diretório do executável
        caminho_arquivo = get_resource_path(arquivo, permanent=True)
        
        # Verifica se o arquivo existe, se não, cria um arquivo vazio
        if not os.path.exists(caminho_arquivo):
            try:
                with open(caminho_arquivo, 'w') as f:
                    pass  # Cria o arquivo vazio
                print(f"Arquivo criado: {caminho_arquivo}")
            except PermissionError as e:
                print(f"Erro ao criar o arquivo {caminho_arquivo}: {e}")


caminho_arquivo_vendas = get_resource_path('vendas.txt', permanent=True)
caminho_arquivo_feriados = get_resource_path('feriados.txt', permanent=True)
caminho_arquivo_vendedor = get_resource_path('vendedor.txt', permanent=True)
caminho_arquivo_vendedor_mes = get_resource_path('vendedor_mes.txt', permanent=True)


def registrar_data_hora():
#Registra a data e hora atuais do pc em execussão no formato dd/mm/yyyy - hh:mm.
    agora = datetime.now()
    data_hora_formatada = agora.strftime('%d/%m/%Y - %H:%M')
    return data_hora_formatada


data_venda = registrar_data_hora()  # Variável que chama a função para obter a data e hora atuais dentro das outras funções


# Função para registrar a venda
def registrar_venda(vendedor, venda):
    # Registra uma venda no arquivo vendas.txt.
    with open(caminho_arquivo_vendas, 'a') as arquivo:
        if os.path.getsize(caminho_arquivo_vendas) > 0:
            arquivo.write('\n')  # Adiciona nova linha apenas se o arquivo não estiver vazio
        linha = f"{vendedor.nome.title()},{venda.valor_venda},{data_venda}"
        arquivo.write(linha)


# Buscar vendas

def buscar_vendas_por_data(data):
    #Busca e exibe vendas registradas em um mês específico no formato 'mm/yyyy'
    mes_ano = data
    with open(caminho_arquivo_vendas, 'r') as arquivo:
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
    with open(caminho_arquivo_vendas, 'r') as arquivo:
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
    with open(caminho_arquivo_vendas, 'r') as arquivo:
        print("\nTodas as vendas registradas: \n")
        for linha in arquivo:
            nome, valor, data_venda = linha.strip().split(',')
            print(f"Vendedor: {nome.title()}, Valor: {valor}, Data: {data_venda}\n")


def calcular_soma_vendas(parcial_nome_vendedor, mes_ano):
    # Calcula a soma de todas as vendas registradas para um vendedor específico
    soma_vendas = 0.0
    parcial_nome_vendedor = parcial_nome_vendedor.lower().strip()

    with open(caminho_arquivo_vendas, 'r') as arquivo:
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


# valida se o nome do funcionário está registrado no arquivo vendedor.txt
def validar_nome_funcionario(nome):
    with open(caminho_arquivo_vendedor, "r") as arquivo:
        for linha in arquivo:
            _, nome_registrado, _ = linha.strip().split(',')
            if nome.strip().title() in nome_registrado.strip().title():
                return True
    return False


# Puxa o salario bruto do vendedor 
def salario_vendedor(vendedor_nome):
    vendedor_nome = vendedor_nome.title()

    with open(caminho_arquivo_vendedor, 'r') as arquivo:
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
    
    with open(caminho_arquivo_vendas, 'r') as arquivo:
        for linha in arquivo:
            nome, valor, data_venda = linha.strip().split(',')
            mes_ano_venda = data_venda[3:10] # Extrai o mês/ano da data da venda
            if mes_ano == mes_ano_venda:
                registros_filtrados.append((nome, float(valor), data_venda))
    
    return registros_filtrados

# Filtra vendas por mês/ano e vendedor no arquivo vendas
def filtrar_vendas_por_vendedor_mes(vendedor_nome, mes_ano):
    registros_filtrados = []
    
    with open(caminho_arquivo_vendas, 'r') as arquivo:
        for linha in arquivo:
            nome, valor, data_venda = linha.strip().split(',')
            mes_ano_venda = data_venda[3:10]  # Extrai o mês/ano da data da venda
            if mes_ano == mes_ano_venda and nome.lower() == vendedor_nome.lower():
                registros_filtrados.append((nome, float(valor), data_venda))
    
    return registros_filtrados


# Cria arquivos Excel fora do .exe

def exportar_vendas_por_nome(nome_arquivo, nome_vendedor):
    # Adiciona a extensão do arquivo se não estiver presente
    if not nome_arquivo.lower().endswith('.xlsx'):
        nome_arquivo += '.xlsx'
        
    registros = []
    nome_vendedor = nome_vendedor.title()
    
    with open(caminho_arquivo_vendas, 'r') as arquivo:
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
    
    with open(caminho_arquivo_vendas, 'r') as arquivo:
        for linha in arquivo:
            nome, valor, data_venda = linha.strip().split(',')
            registros.append((nome, float(valor), data_venda))
    
    df = pd.DataFrame(registros, columns=['Funcionário', 'Valor da venda', 'Data da Venda'])
    df.to_excel(nome_arquivo, index=False)


def gerenciar_feriados():
    feriados = set()
    
    # Lê os feriados existentes
    try:
        with open(caminho_arquivo_feriados, 'r') as arquivo:
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
    with open(caminho_arquivo_feriados, 'w') as arquivo:
        for data in sorted(feriados):
            arquivo.write(data + '\n')

    print("Feriados atualizados com sucesso!")
    
# Retorna um número inteiro de quantos feriados existem no arquivo referente ao mês especificado para uso do DSR    
def contar_feriados(mes_ano):
    try:
        with open(caminho_arquivo_feriados, 'r') as arquivo:
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
    vendedor = classes.Vendedor_mes(
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
    with open(caminho_arquivo_vendas, 'r') as vendas_file:
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
        with open(caminho_arquivo_vendedor_mes, 'r') as relatorio_file:
            for linha in relatorio_file:
                dados = linha.strip().split(',')
                vendedor_existente, mes_ano_existente = dados[0], dados[1]
                registros_existentes[(vendedor_existente, mes_ano_existente)] = linha.strip()
    except FileNotFoundError:
        # Arquivo não encontrado, não há registros existentes para atualizar
        pass

    # Abre o arquivo para escrita, o que vai apagar seu conteúdo, e reescreve com atualizações
    with open(caminho_arquivo_vendedor_mes, 'w') as relatorio_file:
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
    with open(caminho_arquivo_vendedor_mes, 'r') as arquivo:
        registros = [formatar_registro(linha.strip().split(',')) for linha in arquivo]
    return registros

def filtrar_por_nome(nome):
    # Filtra registros no arquivo vendedor_mes.txt por nome de funcionário
    with open(caminho_arquivo_vendedor_mes, 'r') as arquivo:
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


