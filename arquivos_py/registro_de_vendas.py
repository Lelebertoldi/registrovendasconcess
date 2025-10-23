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
import shutil
import classes
import funcoes

# Detecta o caminho de execução (funciona no .py e no .exe, para MEIPASS não dar erro no .py)
if hasattr(sys, '_MEIPASS'):
    base_path = sys._MEIPASS
else:
    base_path = os.path.abspath(".")

#global caminho_arquivo

# In[ ]:

# Chama a função para garantir que os arquivos existam ao iniciar o programa
funcoes.inicializar_arquivos() 


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
            if not funcoes.validar_nome_funcionario(nome_vendedor):
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
            data_venda = funcoes.registrar_data_hora()
            # Registra a venda no arquivo vendas.txt
            with open(funcoes.caminho_arquivo_vendas, "a") as arquivo:
                if os.path.getsize(funcoes.caminho_arquivo_vendas) > 0:
                    arquivo.write('\n')  # Adiciona nova linha apenas se o arquivo não estiver vazio
                arquivo.write(f"{nome_vendedor},{valor_float:.2f},{data_venda}")
            print("Venda registrada com sucesso.")
        
        
        elif opcao == '2':
            # Verificar vendas realizadas
            verificar = input(verificar_vendas)
            
            if verificar == "1": 
                # Buscar vendas por data
                data = input("Digite o mês e ano para a busca (mm/yyyy): ").strip()
                if funcoes.validar_data(data, formato='mm/yyyy'):
                    funcoes.buscar_vendas_por_data(data)
                    continue
                else:
                    print("Formato de data inválido. Por favor, insira no formato mm/yyyy.")
                    
            elif verificar == "2":
                # Buscar vendas por funcionário
                nome_vendedor = input("Digite o nome do funcionário para a busca: ").strip()
                funcoes.buscar_vendas_por_funcionario(nome_vendedor)
                continue
                
            elif verificar == "3":
                # Mostrar todas as vendas registradas
                funcoes.mostrar_todas_as_vendas()
                continue
                
            elif verificar == "4":
                # Voltar ao menu anterior
                print("Voltando ao menu anterior...")
                continue
            
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
                funcoes.exportar_vendas_por_nome(nome_arquivo, nome_vendedor)
                print(f"Registros de vendas para o vendedor '{nome_vendedor}' foram importados para {caminho_arquivo}.")

            elif importarregistro == '2':  # Importar registro detalhado de vendas por data
                mes_ano = input("Digite o mês e ano no formato MM/YYYY: ").strip()
                caminho_arquivo = input("Digite o caminho da pasta onde deseja salvar o arquivo: ").strip()
                if not os.path.exists(caminho_arquivo):
                    print("A pasta especificada não existe. Tente novamente.")
                    continue
                nome_arquivo = os.path.join(caminho_arquivo, f'{mes_ano}_vendas.xlsx')
                funcoes.exportar_vendas_por_data(nome_arquivo, mes_ano)
                print(f"Registros de vendas para o mês {mes_ano} foram importados para {caminho_arquivo}.")

            elif importarregistro == '3':  # Importar todos os registros detalhados de vendas
                caminho_arquivo = input("Digite o caminho da pasta onde deseja salvar o arquivo: ").strip()
                if not os.path.exists(caminho_arquivo):
                    print("A pasta especificada não existe. Tente novamente.")
                    continue
                nome_arquivo = os.path.join(caminho_arquivo, f'geral_vendas.xlsx')
                funcoes.exportar_todos_os_registros(nome_arquivo)
                print(f"Todos os registros de vendas foram importados para {caminho_arquivo}.")

            elif importarregistro == '4': # Importar cálculo mensal de funcionário
                nome = input("Digite o nome do funcionário para exportar: ").title()
                caminho_arquivo = input("Digite o caminho da pasta onde deseja salvar o arquivo: ").strip()
                if not os.path.exists(caminho_arquivo):
                    print("A pasta especificada não existe. Tente novamente.")
                    continue
                funcoes.exportar_por_funcionario(nome)
                print(f"Todos os registros de vendas foram importados para {caminho_arquivo}.")
                      
            elif importarregistro == '5': # Importar todos os cálculos mensais dos funcionários
                funcoes.registrar_relatorio_vendedor()
                caminho_arquivo = input("Digite o caminho da pasta onde deseja salvar o arquivo: ")
                if not os.path.exists(caminho_arquivo):
                    print("A pasta especificada não existe. Tente novamente.")
                    continue
                funcoes.exportar_todos()
                print(f"Todos os registros de vendas foram importados para {caminho_arquivo}.")
               
            elif importarregistro == '6': # Apagar registros
                apagar = input(apagar_registros)
                if apagar == '1': # Apagar registros de venda por funcionário
                    nome_funcionario = input("Digite o nome do funcionário para ter os registros apagados: ").title()
                    registros_vendedor = []
                    registros_restantes = []
                
                    # Lê o arquivo de vendas e filtra os registros do funcionário
                    with open(funcoes.caminho_arquivo_vendas, 'r') as arquivo:
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
                            with open(funcoes.caminho_arquivo_vendas, 'w') as arquivo:
                                for registro in registros_restantes:
                                    arquivo.write(registro + "\n")
                            print("Registros apagados com sucesso.")
                        else:
                            print("Operação cancelada. Nenhum registro foi apagado.")
                    else:
                        print(f"\nNenhum registro encontrado para o funcionário '{nome_funcionario}'.")

                    
                elif apagar == '2': # Apagar registros de venda por data
                    # Filtra vendas para o mês/ano especificado
                    data_input = input("Digite a data para filtrar os registros a serem apagados (formato MM/YYYY): ")
                    if not funcoes.validar_data(data_input, formato='mm/yyyy'):
                        print("Data inválida. Por favor, insira no formato MM/YYYY.")
                        continue
                    mes_ano = data_input
                    registros_vendidos = funcoes.filtrar_vendas(mes_ano)
                    registros_restantes = []
                
                    if registros_vendidos:
                        print("\nRegistros encontrados para o mês/ano '{}':".format(mes_ano))
                        for registro in registros_vendidos:
                            print(f"Vendedor: {registro[0]}, Valor: {registro[1]:.2f}, Data: {registro[2]}")
                
                        confirmacao = input("\nDeseja realmente apagar esses registros? (s/n): ").strip().lower()
                
                        if confirmacao == 's':
                            # Recria a lista de registros restantes, excluindo os registros filtrados
                            with open(funcoes.caminho_arquivo_vendas, 'r') as arquivo:
                                for linha in arquivo:
                                    nome, valor, data_venda = linha.strip().split(',')
                                    mes_ano_venda = data_venda[3:10]
                                    if mes_ano != mes_ano_venda:
                                        registros_restantes.append(linha.strip())
                
                            # Sobrescreve o arquivo de vendas com os registros restantes
                            with open(funcoes.caminho_arquivo_vendas, 'w') as arquivo:
                                for registro in registros_restantes:
                                    arquivo.write(registro + "\n")
                
                            print("Registros apagados com sucesso.")
                        else:
                            print("Operação cancelada. Nenhum registro foi apagado.")
                    else:
                        print(f"\nNenhum registro encontrado para o mês/ano '{mes_ano}'.")
                      
                
                elif apagar == '3': # Apagar todos os registros de vendas
                    confirmacao = input("\nDeseja realmente apagar todos os registros de vendas? (s/n): ").strip().lower()

                    if confirmacao == 's':
                        # Limpa o arquivo de vendas
                        open(funcoes.caminho_arquivo_vendas, 'w').close()  # Apaga todo o conteúdo do arquivo

                        print("Todos os registros foram apagados com sucesso.")
                    else:
                        print("Operação cancelada. Nenhum registro foi apagado.")  
   
                    
                elif apagar == '4': # Apagar todos os registros de cálculos mensais dos funcionários
                    confirmacao = input("\nDeseja realmente apagar todos os registros de cálculos mensais dos funcionários? (s/n): ").strip().lower()

                    if confirmacao == 's':
                        # Limpa o arquivo de cálculos mensais dos funcionários
                        open(funcoes.caminho_arquivo_vendedor_mes, 'w').close()  # Apaga todo o conteúdo do arquivo

                        print("Todos os registros foram apagados com sucesso.")
                    else:
                        print("Operação cancelada. Nenhum registro foi apagado.")

    
                elif apagar == '5': # Voltar ao menu anterior
                    continue
                    
                    
                else:
                    print('Opção inválida. Por favor, escolha uma opção válida.')
                    
            
            elif importarregistro == '7': # Voltar ao menu anterior
                continue
                       
            else:
                print('Opção inválida. Por favor, escolha uma opção válida.')
                   
        
        elif opcao == '4':
            # Menu de funcionários
            menufuncionario = input(menu_funcionarios)
            
            if menufuncionario == '1': # Registrar novo funcionário
                # Solicita o CPF do funcionário e garante que apenas números sejam inseridos
                cpf = input("Digite o CPF do funcionário (apenas números): ").strip()
                if not funcoes.validar_cpf(cpf):
                    print("CPF inválido! O CPF deve conter exatamente 11 dígitos numéricos.")
                    continue
                # Formata o CPF
                cpf_formatado = funcoes.formatar_cpf(cpf)
                # Verifica se o CPF já está cadastrado
                try:
                    with open(funcoes.caminho_arquivo_vendedor, "r") as arquivo:
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
                    with open(funcoes.caminho_arquivo_vendedor, "a") as arquivo:
                        if os.path.getsize(funcoes.caminho_arquivo_vendedor) > 0:
                            arquivo.write('\n')  # Adiciona nova linha apenas se o arquivo não estiver vazio
                        arquivo.write(f"{cpf_formatado},{nome},{salario_bruto:.2f}")
                    print("Funcionário cadastrado com sucesso!\n")
                else:
                    print("Cadastro cancelado. Por favor, insira os dados novamente.\n")
        
                
            elif menufuncionario == '2': # Verificar registro de funcionários
                # Solicita o CPF do funcionário e garante que apenas números sejam inseridos
                cpf = input("Digite o CPF do funcionário (apenas números): ").strip()
                if not funcoes.validar_cpf(cpf):
                    print("CPF inválido! O CPF deve conter exatamente 11 dígitos numéricos.")
                    continue
                # Formata o CPF
                cpf_formatado = funcoes.formatar_cpf(cpf)
                # Verifica se o CPF já está cadastrado
                try:
                    with open(funcoes.caminho_arquivo_vendedor, "r") as arquivo:
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
                if not funcoes.validar_cpf(cpf):
                    print("CPF inválido! O CPF deve conter exatamente 11 dígitos numéricos.")
                    continue
                # Formata o CPF
                cpf_formatado = funcoes.formatar_cpf(cpf)
                # Verifica se o CPF já está cadastrado e obtém o nome associado
                try:
                    with open(funcoes.caminho_arquivo_vendedor, "r") as arquivo:
                        registros = arquivo.readlines()
                        cpf_existente = any(cpf_formatado in linha for linha in registros)

                        if cpf_existente:
                            for linha in registros:
                                if cpf_formatado in linha:
                                    dados = linha.strip().split(",")
                                    nome_registrado = dados[1]
                                    break

                            # Remove todas as linhas contendo o nome nos arquivos
                            for arquivo_nome in [funcoes.caminho_arquivo_vendedor, funcoes.caminho_arquivo_vendas, funcoes.caminho_arquivo_vendedor_mes]:
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
                funcoes.registrar_relatorio_vendedor()
                registros = funcoes.mostrar_todos()
                if registros:
                    print("\nTodos os registros:\n")
                    for registro in registros:
                        for chave, valor in registro.items():
                            print(f"{chave}: {valor}")
                        print()  # Linha em branco para separar os registros
                else:
                    print("\nNão há registros para mostrar.")
                
                     
            elif menufuncionario == '5': # Voltar ao menu anterior
                continue
                
            else:
                print('Opção inválida. Por favor, escolha uma opção válida.')
                       
        
        elif opcao == '5':
            # Sair
            break
        
        
        else:
            print('Opção inválida. Por favor, escolha uma opção válida.')



    # Parte para funcionar apenas no arquivo .exe, remover # das linhas abaixo para criar o .exe e colocar para rodar no vscode

    #root = tk.Tk()
    #oot.title("Triumph | Floripa")
    #root.geometry("300x200")  # Ajuste o tamanho da janela 

    # Adiciona um widget Label para mostrar alguma informação
    #label = tk.Label(root, text="Feche a janela para sair.\n Projeto criado por Letícia Bertoldi.\n https://github.com/Lelebertoldi\n https://www.linkedin.com/in/lelebertoldi/")
    #label.pack(padx=15, pady=15)

    #root.mainloop()

if __name__ == "__main__":
    main()


# %%
#