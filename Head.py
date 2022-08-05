import re
import random as rand
from discord import Embed


class Filtro:
    def __init__(self,msg=str):
        self.__mensagem = msg.strip()
        self.__filtro1 = re.compile(r"^[dD]+[0-9]+")
        self.__filtro2 = re.compile(r"^[0-9]+[dD]+[0-9]+")
        self.__filtro3 = re.compile(r"^[0-9]+\#[0-9]+[dD]+[0-9]+")
        self.__filtros = [self.__filtro1,self.__filtro2,self.__filtro3]
        self.__get_numbers = re.sub(pattern=r"[a-z-A-z #]+",repl=" ",string= f"{self.__findComand()}")
        self.__numeros = {f"num{z+1}":int(x) for z,x in enumerate(self.__get_numbers.strip().split(" ")) if x not in (""," ") and z <=3}
        self.__no_comands_msg = f"{msg}".replace(f"{self.__findComand()}","")
    @property
    def mensagem(self):
        return self.__mensagem
    @property
    def numeros(self):
        return self.__numeros
    @property
    def no_comands_mensssage(self):
        return self.__no_comands_msg
    @property
    def filtros(self):
        return self.__filtros
    
    def __findComand(self):
        for n in self.filtros:
            comando = re.findall(pattern=n,string=f"{self.mensagem}")
            if comando:
                return comando[0]
        return False

class Brain(Filtro):
    def __init__(self,message):
        super().__init__(msg=message)
        self.__sinais = re.compile(r"[\-\+\*\/]+[0-9]+")

    @property
    def resto_msg(self):
        return self.no_comands_mensssage
    

    def Cprop(self,n1=int,n2=int):
        q1 = n1//4
        if n2 == 1:
            return 0xFE0400
        elif n2 == n1:
            return 0x3FF300
        elif n2 != 1 and n2 <= q1:
            return 0xB22222
        elif n2 > q1 and n2 < q1*2:
            return 0xFF8C00
        elif n2 >= q1*2 and n2 < q1*3:
            return 0x3CB371
        elif n2 >= q1*3 and n2 != n1:
            return 0x006400
        else:
            return 0x000000

    def roll(self):
        try:
            if "num3" in self.numeros:
                resultado = []
                extremidades = []
                for x in range(self.numeros["num1"]):
                    dados= []
                    for n in range(self.numeros["num2"]):
                        dados.append(rand.randint(1,self.numeros["num3"]))
                    acertos = [x for x in dados if x==self.numeros["num3"]]
                    erros = [x for x in dados if x ==1]
                    extremidades.append((len(acertos),len(erros)))
                    resultado.append(dados)
                    #
                tamanho= len(resultado)
                dados_por_roll = self.numeros["num2"]
                return {"tipo":3,"tamanho":tamanho, "resultado": resultado,"DPorRoll":dados_por_roll,"extremidades":extremidades}
            
            elif "num2" in self.numeros:
                dados = []
                for n in range(self.numeros["num1"]):
                        dados.append(rand.randint(1,self.numeros["num2"]))
                tamanho = len(dados)
                acertos = [x for x in dados if x==self.numeros["num2"]]
                erros = [x for x in dados if x ==1]
                if self.numeros["num1"] == 1:
                    return {"tipo":1,"tamanho":tamanho, "dado": dados[0],"sinais":False,
                    "cor":self.Cprop(n1=self.numeros["num2"],n2=dados[0]),"erros":len(erros),"acertos":len(acertos)}
                return {"tipo":2,"tamanho":tamanho, "resultado": dados,"erros":len(erros),"acertos":len(acertos)}
            
            elif "num1" in self.numeros:
                dado = rand.randint(1,self.numeros["num1"])
                return {"sinais":False,"cor":self.Cprop(n1=self.numeros["num1"],n2=dado),"tipo":1,"dado": dado}
            
            else:
                return False
        except Exception as log:
            with open("log.txt","w") as file:
                file.write(f"{log}")

    def main(self):
        try:
            sinais = re.findall(self.__sinais,self.resto_msg)
            roll = self.roll()
            if roll:
                if sinais:
                    if  roll["tipo"] ==1:
                        if not isinstance(roll["dado"],list):
                            conta = f"{roll['dado']}{self.resto_msg}"
                            return {"tipo":roll["tipo"],"sinais":True,"cor":roll['cor'],"conta":conta,
                                    "resultado":eval(conta),"dado":roll["dado"]}
                        else:
                            conta = f"{roll['dado']}{self.resto_msg}"
                            return {"tipo":roll["tipo"],"sinais":True,"cor":roll['cor'],"conta":conta,
                                    "resultado":eval(conta),"dado":roll["dado"]}

                    elif roll["tipo"] in (2,3):
                        return roll
                    else:
                        return False            
                else:
                    if  roll["tipo"] in (1,2,3):
                        return roll
                    else:
                        return False
            else:
                return False
        except Exception as log:
            with open("log.txt","w") as file:
                file.write(f"{log}")
