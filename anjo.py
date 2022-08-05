from Head import Brain
import discord
from dotenv import load_dotenv
import os
import json

#le json
def leitor_json(nome=str):
    with open(f"{nome}", "r") as arquivoJson:
        jsonLido = json.load(arquivoJson)
    return jsonLido

setupJ = leitor_json("setup.json")

#embeds
class EmbedC():
    def __init__(self,titulo=str,cor=0xFFFFFF,conteudo=str):
        self.generico = discord.Embed(
        title = titulo,
        color = cor,
        description = conteudo
        )
    def setar_author(self,m):
        self.generico.set_author (name = m.author.name, icon_url = m.author.avatar_url)
    def add_field(self,nome=str,valor=str,na_linha = False):
        self.generico.add_field(name = f"{nome}",value= f"{valor}",inline=na_linha)
    @property
    def retorna(self):
        return self.generico


###############################
ajuda = discord.Embed(
title = "Help:",
color = 0x48C9B0,
description = setupJ["olaMSG"])
ajuda.add_field(name = "Sinais Matemáticos:",value = setupJ["msg1"], inline=False)
ajuda.add_field(name = "Dados Normais:",value = setupJ["msg2"], inline=False)
ajuda.add_field(name = "Dados Multiplos:",value = setupJ["msg3"], inline=False)
ajuda.add_field(name = "Calculadora Comum:",value = setupJ["msg4"],inline=False)
ajuda.add_field(name = "Multiplos Dados Multiplos",value = setupJ["msg5"], inline=False)
ajuda.add_field(name="Fazendo Operações com Dados",value=setupJ["msg6"],inline=False)
    


client = discord.Client()

@client.event
async def on_ready():
    print(f"Logado como : {client.user}")
    print(f"Seja bem vindo {client.user}")
    print(15*"-_-")
    return "OK!"


@client.event
async def on_message(message):
    msg = message.content
    send = message.channel
    mension = message.author.mention
    main = Brain(msg).main()
    try:
    #        verifica se o autor e um client user  
        if message.author == client.user:
            return
            #calculadora
        if msg.startswith(".help"):
            return await send.send(embed=ajuda)
        elif msg.startswith("<") and "+" in msg or msg.startswith("<") and "-"in msg or msg.startswith("<") and "*" in msg or msg.startswith("<") and "/" in msg:
            return await send.send(f"{mension}: ``` 🧠{msg.replace('<',' ')} = {eval(str(msg.replace('<',' ')))}```")
            #Multiplos Dados Multiplos
        if main != False:
            if main["tipo"] == 1:
                if main["dado"] <= 100000000000:
                    if main["sinais"] == True:
                        sinais_dado = EmbedC(f"{msg}",main['cor'],f'{main["conta"]}={main["resultado"]}')
                        sinais_dado.setar_author(m=message)
                        return await send.send(embed=sinais_dado.retorna)

                    dado = EmbedC(f"{msg}",main['cor'],main['dado'])
                    dado.setar_author(m=message)
                    return await send.send(embed=dado.retorna)
                else:
                    return await send.send("```MESSAGE ERRO:\nMessage return is too big```")
            elif main["tipo"] == 2:
                if main["tamanho"] <= 250:
                    resultado = EmbedC(
                    f"{msg}\n{main['tamanho']} Dados rolados | Acertos criticos:{main['acertos']} | Erros criticos:{main['erros']}",
                    cor=0x8B008B,conteudo = f"```{main['resultado']} = {sum(main['resultado'])}```".replace("[","").replace("]","")
                    )
                    resultado.setar_author(m=message)
                    return await send.send(embed=resultado.retorna)
                else:
                    return await send.send("```MESSAGE ERRO:\nMessage return is too big ```")
            elif main["tipo"] == 3:
                if main["tamanho"] <= 15:
                    resultados = EmbedC(titulo=f"Rolls: {main['tamanho']}",cor=0xDA70D6,conteudo="")
                    resultados.setar_author(m=message)
                    for x , n  in enumerate(main["resultado"]):
                        z = main["extremidades"]
                        resultados.add_field(nome=f"{x+1}: Acertos Criticos {z[x][0]} | Erros Criticos {z[x][1]}",
                        valor=f"```{n} = {sum(n)}```\n**Dados rolados : {main['DPorRoll']}**".replace("[","").replace("]",""))
                    return await send.send(embed=resultados.retorna)
                else:
                    return await send.send("```MESSAGE ERRO:\nMessage return is too big ```")
            else:
                pass
    except Exception as log:
        return await send.send(f"FATAL ERROR:\n{log}\n ``` Send this error to : >> Ojama Tatico#6821 <<```")

if __name__ =="__main__":
    load_dotenv()
    client.run(os.getenv("TOKEN"))
