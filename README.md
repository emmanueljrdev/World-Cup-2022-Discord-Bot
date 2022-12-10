# World Cup 2022 Discord Bot en Pyrhon

## Bot de discord con motivo del Mundial de Qatar 2022 realizado con el lenguaje Python para el curso de EDTecnica.


Sigamos la instalación para un correcto uso:
---
### Características:

#### Comandos del bot:


`!help` Te mostrará toda la información necesaria acerca de los comandos que se encuentran disponibles para el uso común.

`!registro` Te crea un usuario en la API del mundial y te registra en la base de datos local. Usando el comando `!help` en el bot encontrarás la sintaxis de cómo registrarte.

`!iniciar` Con este comando el bot da inicio a sus funciones siguientes. Si el registro fue satisfactorio deberás obtener un mensaje que diga: ***_Iniciaste sesion_***.

`!equipo` Coloca este comando seguido de el equipo del cual quieras obtener información; es **importante que el nombre del equipo que vayas a colocar este en inglés**.

`!partidos` Al igual que el comando anterior ingresa este seguido del **nombre del equipo en inglés** para así obtener información de los proximos encuentrso de tus equipos favoritos.

`!grupo` Busca tambien por grupos y así obtendrás los puntajes de un grupo determinado dentro de este mundial.

**NOTA: Toda la sintaxis de los comandos está especificada usando el comando de `!help`**

***

### Herramientas necearias para instalar el bot:

#### Windows:

*	Instala Python en su versión 3.10.8 (***es necesario que sea la versión antes mencionada para que el bot pueda funcionar, versiones posteriores no son soportadas aún***); ( https://www.python.org/downloads/)
*	Como editor de código usaremos Visual Studio Code; existen muchas alternativas, sin embargo, el código está hecho en este editor.
*	Lugo de haber instalado Visual Studio Code, es necesario instalar la extensión de SQLITE, la cual nos ayudará a ver y crear la base de datos.
*	Es necesario instalar todas las dependencias que se encuentran al inicio del código, tales como `json`, `PIL` , entre otros.
*	Descarga Git para Windows, este te permitirá clonar el código más adelante; descárgalo a través de su web oficial: ( https://gitforwindows.org/).

#### Descargar el código:

1.	Crea una carpeta y ábrela con Visual Studio Code.
2.	En el terminal de VSCODE copia el siguiente comando:

`git clone https://github.com/Storgaro/python-bot`

Posteriormente da enter en _SI_ y espera a que la descarga de todos los archivos termine. ***Es necesario que deje su terminal abierto y siga con los siguientes pasos***

#### Configuración del Bot 

1.	En tu buscador de preferencia dirígete a la página de [Discord developer]( https://discord.com/developers/applications.).
2.	Clickea en el botón de **New Application**

![imagen9final](https://user-images.githubusercontent.com/8563780/162317136-4373626f-9f7a-4d7f-880c-60e470c64d69.png)

3.	Posteriormente coloca el nombre que gustes a tu **Servidor de Discord**
4.	En el menu de la izquierda selecciona la pestaña de Bot.

![imagen10final](https://user-images.githubusercontent.com/8563780/162320423-275012d1-dc06-4c10-b954-b3cd86322c2c.png)

5.	Daremos click donde dice **Add Bot**

![imagen11final](https://user-images.githubusercontent.com/8563780/162321199-e5b00e88-4720-45c4-86c1-0da4bf47ebf1.png)

6.	En este apartado daremos nombre al Bot y daremos click en el botón de **Reset Token**.

![imagen12final](https://user-images.githubusercontent.com/8563780/162322546-7119e7b5-fe30-42e2-9369-4f695f87d3d7.png)

7.	Copiaremos el nuevo **Token** dado por el Bot y lo reservaremos para más adelante.

#### Creando el URL para añadir el bot al servidor:

1.	Nos dirigimos al menú del lado izquierdo y presionaremos la opción **OAuth2**; Copiaremos el **Cient ID** y lo reservaremos para más adelante.

![imagen13final](https://user-images.githubusercontent.com/8563780/162323888-77958a62-0aab-403a-9f56-1688b30ccdef.png)

![imagen14final](https://user-images.githubusercontent.com/8563780/162325239-fde9fef0-9e1f-4a39-b92e-a297c73991a7.png)


2.	Daremos click al **URL GENERTOR** y seleccionaremos las opciones de **bot** y **applications.commands**

![imagen15final](https://user-images.githubusercontent.com/8563780/162325504-68045770-e28e-404c-a441-b9192f0a55a5.png)

3.	Posteriormente marcaremos las casillas de los permisos, en estos seleccionaremos los mostrados a continuación.

![imagen16final](https://github.com/Storgaro/imagenes/blob/main/images.md/imagen16final.png)

4.	Copiaremos el **URL** que nos da al final y lo pegaremos en el navegador. Este traerá un menú de Discord y nos preguntará a que servidor queremos añadir el bot. Aquí seleccionaremos el servidor que creamos hace un momento y daremos **Confirmar**.


![imagen17final](https://github.com/Storgaro/imagenes/blob/main/images.md/imagen17final.png)

Por último, ya tenemos el bot dentro de nuestro servidor y ahora procederemos a activar sus funciones.

#### Configurando el bot:

Primero, deberá completar su archivo **env**. (***El bot viene con un archivo example.env, el cual deberá renombrar a env***). Aquí deberá agregar su **token del bot y la ID de cliente para el bot**.
_Consulte el archivo ejemplo.env para obtener más información._

#### Instalar las dependenciaas necesarias:

En su terminal escruba el siguiente código:

`pip install (Seguido del nombre de la dependencia que le haga falta)`

(**Las dependencias necesarias se encuentran en los IMPORT al inicio del código**).

### Poner a funcionar el Bot:

En su terminal escriba el siguiente comando:

`py (seguido del nombre de su archivo .py)`

Posteriormente presione **Enter** y disfrute de todas las opciones y comandos que este bot le ofrece.
