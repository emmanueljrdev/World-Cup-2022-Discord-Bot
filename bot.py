# This example requires the 'message_content' intent. 
from urllib import response
from wsgiref import headers
from table2ascii import table2ascii
import requests
import os
import json
import discord
import PIL
from dotenv import load_dotenv
import extcolors
import sqlite3
con = sqlite3.connect("tutorial.db")
cur = con.cursor()
load_dotenv()  # take environment variables from .env.

# Code of your application, which uses environment variables (e.g. from `os.environ` or
# `os.getenv`) as if they came from the actual environment.

intents = discord.Intents.default()
intents.message_content = True

def get_country_embed(pais):
    pais.lower()
    pais_raw = requests.get(
        f"https://restcountries.com/v3.1/name/{pais}")
    data_pais = pais_raw.json()
    clima_raw = requests.get(
        f"https://api.openweathermap.org/data/2.5/weather?lat={data_pais[0]['latlng'][0]}&lon={data_pais[0]['latlng'][1]}&appid={'2cd4b906451c18a0484baf589f40dc4f'}&lang=es")
    data_clima = clima_raw.json()
    nombre_pais = data_pais[0]['name']['common']
    capital = data_pais[0]['capital'][0]
    region = data_pais[0]['region']
    population = data_pais[0]['population']
    weather = data_clima['weather'][0]['description']
    flag = data_pais[0]['flags']['png']
    image = PIL.Image.open(requests.get(flag, stream=True).raw)

    colors = extcolors.extract_from_image(image)
    color1 = colors[0][0][0][0]
    color2 = colors[0][0][0][1]
    color3 = colors[0][0][0][2]
    embed = discord.Embed(
        title=pais.capitalize(),
        description="Información del país",
        color=discord.Colour.from_rgb(color1, color2, color3)
    )

    embed.add_field(name="Capital", value=capital, inline=True)
    embed.add_field(name="Población",
                    value=f" {'{:,}'.format(population)}", inline=True)
    embed.add_field(name="Region", value=region, inline=True)
    embed.set_thumbnail(url=flag)
    embed.add_field(name="Clima", value=weather)
    embed.set_image(url=f"http://openweathermap.org/img/wn/{data_clima['weather'][0]['icon']}@2x.png")
            
    return embed

def get_team(team_name, equipos):
    for equipo in equipos:
        if equipo["name_en"] == team_name:
            return equipo

def get_match(team_name, partidos):
        # new_array = []
        filter_partidos = []

        
        for partido in partidos:
            if partido["home_team_en"] == team_name or partido["away_team_en"] == team_name:
                if partido["time_elapsed"] == 'notstarted': 
                    filter_partidos.append(partido)
        
        return filter_partidos
       

def get_standings(team_name, standings):
    for standing in standings:
        if standing["group"] == team_name or standing['teams'][0]['name_en'] == team_name or standing['teams'][1]['name_en'] == team_name or standing['teams'][2]['name_en'] == team_name or standing['teams'][3]['name_en'] == team_name:
            return standing['teams']
            

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')


@client.event
async def on_message(message):
    if message.author == client.user:
        return
# Comandos Principales
   
    if message.content.lower().startswith('!registro'):
        try:
            # mensaje = message.content.startswith('!registro')
            # mensaje.lower()
            response_message = await message.channel.send('Cargando...')
            id = message.author.id;
            name = message.content.split(" ")[1]
            email = message.content.split(" ")[2]
            password = message.content.split(" ")[3]
            confirm_pass = message.content.split(" ")[4]
            
            cur.execute("""
                    INSERT INTO users (discord_id, name, email, password) VALUES(?, ?, ?, ?)
            """, (id, name, email, password)) 
            con.commit()

            user = {
                "name": name,
                "email": email,
                "password": password,
                "passwordConfirm": confirm_pass
            }
            json_body = json.dumps(user)
            print(json_body)

            headers = {
                "Content-Type": "application/json"
            }
            response = requests.post("http://api.cup2022.ir/api/v1/user", data=json_body, headers=headers)
            print(response.json())
            error = response.json()
            await response_message.delete()
            if str(error["message"]).__contains__("duplicate"):
                return await message.channel.send(f"<@{id}>, el usuario ya existe")
            elif str(error["message"]).__contains__("minimum allowed length"):
                return await message.channel.send(f"<@{id}>, la contraseña debe tener un **MINIMO** de 8 caracteres")
            elif str(error["message"]).__contains__("valid email"):
                return await message.channel.send(f"<@{id}>, el email es inválido")
            await message.channel.send(f"¡Registro satisfactorio! <@{id}>")
        except sqlite3.IntegrityError:
            await response_message.delete()
            await message.channel.send(f" <@{id}>, el usuario ya existe en la base de datos")
        except IndexError:
            await response_message.delete()
            await message.channel.send(f"<@{id}>, parece que has escrito mal el comando. Intenta hacerlo de la siguiente manera: ***!registro 'nombre de usuario' 'e-mail' 'contraseña' 'confirmar contraseña'*** (no agregues espacios de más)")
        
    if message.content.lower().startswith('!help'):
        response_message = await message.channel.send('Cargando...')
        embed = discord.Embed(
        title="Comandos",
        description="Estos son los comandos que se encuentran disponibles en el bot",
        )

        embed.add_field(name="!registro", value="Sirve para registrarte y poder utilizar los demás comandos. Su sintaxis es: ***!registro 'nombre de usuario' 'e-mail' 'contraseña' 'confirmar contraseña'***." , inline=False)
        embed.add_field(name="!iniciar", value="Funciona para iniciar sesión. Su sintaxis es: ***!iniciar (sin ningún espacio extra)***", inline=False)
        embed.add_field(name="!equipo", value="Te mostrará la información de un equipo del mundial. Su sintaxis es: ****!equipo 'pais'***", inline=False)
        embed.add_field(name="!grupo", value="Te mostrará el grupo seleccionado. Su sintaxis es: ****!grupo 'pais'*** o ***!grupo 'letra del grupo'***", inline=False)
        embed.add_field(name="!partidos", value="Te mostrará el partido siguiente de un equipo. Su sintaxis es: ****!partidos 'pais'*** Nota: La API tarda en registrar los siguientes partidos de un equipo en fase eliminatoria.", inline=False)
        await response_message.delete()
        await message.channel.send(embed=embed)

    if message.content.lower().startswith('!borrar'):
        try:
            
            response_message = await message.channel.send('Cargando...')
            id = message.author.id;
            # Buscar
            res = cur.execute("""
                    SELECT * FROM users WHERE discord_id = ?
            """, [id]) 

            user = res.fetchone()[0]
            # Eliminar
            cur.execute("""
                    DELETE FROM users WHERE discord_id = ?
            """, [id]) 
            con.commit()
            await response_message.delete()
            await message.channel.send(f"¡Usuario eliminado! <@{id}>")
        except:
            await response_message.delete()
            await message.channel.send(f" <@{id}>, el usuario no existe")

    if message.content.lower().startswith('!iniciar'):
        try:
            response_message = await message.channel.send('Cargando...')
            id = message.author.id

            res = cur.execute("""
                SELECT email, password FROM users 
                WHERE discord_id = ?
            """,[id])

            data = res.fetchone()
            credentials = {
                "email": data[0],
                "password": data[1]
            }
            json_body = json.dumps(credentials)
            print(json_body)

            headers = {
                "Content-Type": "application/json"
            }

            response = requests.post("http://api.cup2022.ir/api/v1/user/login", data=json_body, headers=headers).json()
            token = response["data"]["token"]
            print(token)
            cur.execute("""
                        UPDATE users 
                        SET token = ? 
                        WHERE discord_id = ?
                """, [token, id])

            con.commit()

            await response_message.delete()

            await message.channel.send(f" <@{id}>, iniciaste sesión")
        except TypeError:
            await response_message.delete()
            await message.channel.send(f" <@{id}>, parece que no tienes un usuario creado. Escribe !help para ver la sintaxis del comando !registro")

    if message.content.lower().startswith('!equipo'):
        try:
            response_message = await message.channel.send('Cargando...')
            id = message.author.id
            pais = str(message.content.split(' ')[1]).capitalize()
            equipo = message.content.split(' ')[1]
            res = cur.execute("""
                SELECT token FROM users
                WHERE discord_id = ?
            """, [id])
            token = res.fetchone()[0]
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"
            }

            response = requests.get("http://api.cup2022.ir/api/v1/team", headers=headers).json()
            equipos = response["data"]

            informacion_equipo = get_team(pais, equipos)
            print(informacion_equipo)

            group = informacion_equipo['groups']
            flag = informacion_equipo['flag']

            image = PIL.Image.open(requests.get(flag, stream=True).raw)

            colors = extcolors.extract_from_image(image)
            color1 = colors[0][0][0][0]
            color2 = colors[0][0][0][1]
            color3 = colors[0][0][0][2]

            embed = discord.Embed(
            title=pais.capitalize(),
            description=f"Grupo {group}",
            color=discord.Colour.from_rgb(color1, color2, color3)
            )

            

            embed.set_thumbnail(url=flag)
            await response_message.delete()
            await message.channel.send(embed=embed)

            if message.content.split(' ')[1] == '':
                await message.channel.send(f"<@{id}>, parece que has escrito mal el comando. Intenta hacerlo de la siguiente manera: ***!equipo*** ***pais*** (no agregues espacios de más)")
            elif informacion_equipo == None:
                await message.channel.send(f"<@{id}>, el país que intentaste buscar no clasificó al mundial :(")
        except KeyError: 
            await response_message.delete()
            await message.channel.send(f"Oh oh, <@{id}> parece que no has iniciado sesión. Escribe ***!iniciar*** para logearte ")
        except TypeError: 
            await response_message.delete()
            await message.channel.send(f"<@{id}>, el país que intentaste buscar no clasificó al mundial :(")
        except IndexError:
            await response_message.delete()
            await message.channel.send(f"<@{id}>, parece que has escrito mal el comando. Intenta hacerlo de la siguiente manera: ***!equipo*** ***pais*** (no agregues espacios de más)")
        except:
            await response_message.delete()
            await message.channel.send(f"<@{id}>, ha ocurrido un error. Verifica que estés ingresando el comando de la siguiente manera: ***!equipo*** ***pais*** (no agregues espacios de más) ")

    if message.content.lower().startswith('!partidos'):
        try:
            response_message = await message.channel.send('Cargando...')
            id = message.author.id
            pais = str(message.content.split(' ')[1]).capitalize()
            partido = message.content.split(' ')[1]
            # print(partido)
            res = cur.execute("""
                SELECT token FROM users
                WHERE discord_id = ?
            """, [id])
            token = res.fetchone()[0]
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"
            }

            response = requests.get("http://api.cup2022.ir/api/v1/match", headers=headers).json()
            partidos = response["data"]

            info_partidos = get_match(pais, partidos)

            group = info_partidos[0]['group']
            home = info_partidos[0]['home_team_en']
            away = info_partidos[0]['away_team_en']
            date = info_partidos[0]['local_date']
            flag = info_partidos[0]['home_flag'] 

            image = PIL.Image.open(requests.get(flag, stream=True).raw)

            colors = extcolors.extract_from_image(image)
            color1 = colors[0][0][0][0]
            color2 = colors[0][0][0][1]
            color3 = colors[0][0][0][2]

            embed = discord.Embed(
            title=f"{home} vs {away}",
            description=f"{group}",
            color=discord.Colour.from_rgb(color1, color2, color3)
            )

            embed.add_field(name="Local", value=home, inline=True)
            embed.add_field(name="Visitante", value=away, inline=True)
            embed.add_field(name="Fecha", value=date, inline=True)
            embed.set_thumbnail(url=flag)
            await response_message.delete()
            await message.channel.send(embed=embed)
            

        except IndexError:
            await response_message.delete()
            if message.content[1] == '':
                await message.channel.send(f"Oh oh <@{id}>, parece que escribiste mal el comando. Recuerda que se escribe ***!partidos pais*** ")
            else:
                await message.channel.send(f"Lo sentimos <@{id}>, el país que intentaste buscar no clasificó al mundial o no clasificó a la siguiente ronda :(")
        except KeyError: 
            await response_message.delete()
            await message.channel.send(f"Oh oh, <@{id}> parece que no has iniciado sesión. Escribe ***!iniciar*** para logearte ")
        except:
            await response_message.delete()
            await message.channel.send(f"Oh oh, <@{id}> parece que ha ocurrido un error")

    if message.content.lower().startswith('!grupo'):
        try:
            response_message = await message.channel.send('Cargando...')
            id = message.author.id
            pais = str(message.content.split(' ')[1]).capitalize()
            standing = message.content.split(' ')[1]
            res = cur.execute("""
                SELECT token FROM users
                WHERE discord_id = ?
            """, [id])
            token = res.fetchone()[0]

            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"
            }

            response = requests.get("http://api.cup2022.ir/api/v1/standings", headers=headers).json()
            standings = response["data"]
            info_standings = get_standings(pais, standings)
            def sort_standings(e):
                return e['pts']

            info_standings.sort(key=sort_standings, reverse=True)
            print(info_standings)

            output = table2ascii(
            header=["Equipos", "PJ", "PG", "PE", "PP", "PTS"],
            body=[
            [info_standings[0]['name_en'], info_standings[0]['mp'], info_standings[0]['w'], info_standings[0]['d'], info_standings[0]['l'], info_standings[0]['pts']], 
            [info_standings[1]['name_en'], info_standings[1]['mp'], info_standings[1]['w'], info_standings[1]['d'], info_standings[1]['l'], info_standings[1]['pts']],
            [info_standings[2]['name_en'], info_standings[2]['mp'], info_standings[2]['w'], info_standings[2]['d'], info_standings[2]['l'], info_standings[2]['pts']],
            [info_standings[3]['name_en'], info_standings[3]['mp'], info_standings[3]['w'], info_standings[3]['d'], info_standings[3]['l'], info_standings[3]['pts']]
            ]
            )
            await response_message.delete()
            await message.channel.send(f"```\n{output}\n```")

            if message.content.split(' ')[1] == '':
                await message.channel.send(f"<@{id}>, parece que has escrito mal el comando. Intenta hacerlo de la siguiente manera: ***!equipo*** ***pais*** (no agregues espacios de más)")
            elif info_standings == None:
                await message.channel.send(f"Lo sentimos <@{id}>, el país que intentaste buscar no clasificó al mundial :(. PD: Recuerda que debes escribir el nombre del país en inglés :)")

        except IndexError:
            await response_message.delete()
            await message.channel.send(f"Lo sentimos <@{id}>, el país que intentaste buscar no clasificó al mundial o no clasificó a la siguiente ronda :(")
        except KeyError: 
            await response_message.delete()
            await message.channel.send(f"Oh oh, <@{id}> parece que no has iniciado sesión. Escribe ***!iniciar*** para logearte ")
        except:
            await response_message.delete()
            await message.channel.send(f"Oh oh, <@{id}> parece que ha ocurrido un error")
    
# Comandos secundarios

    if message.content.lower().startswith('!calc'):
        operacion = message.content.split(' ')[1]

        def calc():
            try:
                if operacion.__contains__("+"):
                    num1 = float(operacion.split("+")[0])
                    num2 = float(operacion.split("+")[1])
                    return num1 + num2
                elif operacion.__contains__("-"):
                    num1 = float(operacion.split("-")[0])
                    num2 = float(operacion.split("-")[1])
                    return num1 - num2
                elif operacion.__contains__("*"):
                    num1 = float(operacion.split("*")[0])
                    num2 = float(operacion.split("*")[1])
                    return num1 * num2
                elif operacion.__contains__("/"):
                    num1 = float(operacion.split("/")[0])
                    num2 = float(operacion.split("/")[1])
                    return num1 / num2
                else:
                    return "Datos invalidos"
            except ValueError:
                return "Numeros invalidos"

        resultado = calc()

        if isinstance(resultado, str):
            await message.channel.send(resultado)
        else:
            await message.channel.send(f"""
            El resultado es: {calc()}
            """)

    if message.content.lower().startswith('!pais'):
        try:
            response_message = await message.channel.send('Cargando...')
            pais = str(message.content.split(' ')[1])
            embed = get_country_embed(pais)
            await response_message.delete()
            await message.channel.send(embed=embed)
        except IndexError:
            res = cur.execute("""
                SELECT country FROM users 
                WHERE discord_id = ?
            """, ([message.author.id]))
            country = res.fetchone()[0]
            print(country)
            embed = get_country_embed(country)

            await response_message.delete()
            await message.channel.send(embed=embed)
        except:
            await response_message.delete()
            await message.channel.send("Pais no existe")
client.run(os.environ['TOKEN'])
