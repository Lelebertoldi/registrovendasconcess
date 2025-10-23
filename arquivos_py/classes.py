from datetime import datetime, timedelta

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

