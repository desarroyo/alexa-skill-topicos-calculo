# -*- coding: utf-8 -*-

import logging
import json
import random
import math
import re

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import (
    AbstractRequestHandler, AbstractExceptionHandler,
    AbstractRequestInterceptor, AbstractResponseInterceptor)
from ask_sdk_core.utils import is_request_type, is_intent_name, viewport
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model.ui import SimpleCard
from ask_sdk_model import Response
from ask_sdk_model.interfaces.alexa.presentation.apl import (
    RenderDocumentDirective, ExecuteCommandsDirective, SpeakItemCommand,
    AutoPageCommand, HighlightMode)

from typing import Dict, Any


TOPICOS_NOMBRE = ["aceleración","alfa","álgebra","ángulo","área","beta","binomio","bisectriz","biyectiva","cartesiano","cateto","cilindro","circunferencia","cociente","coeficiente","constante","continuidad","cosecante","coseno","cotangente","curva","decágono","decaedro","decímetro","delta","denominador","determinante","diferencia","diferencial","dividendo","divisor","dominio","elipse","eneágono","épsilon","equilátero","escaleno","exponencial","exponente","factorial","factorización","fracción","función","geometría","hectómetro","heptaedro","hipérbola","hipotenusa","icosaedro","indeterminación","infinito","integral","intervalo","inyectiva","límite","logaritmo","matriz","mixto","múltiplo","numerable","numerador","obtusángulo","ordenada","ortoedro","óvalo","parábola","pentadecágono","pentágono","perímetro","perpendicular","pi","pirámide","polígono","polinomio","porcentaje","potencia","primos","producto","q","quebrado","radián","radio","raíz","rango","reales","recíproco","rectángulo","secante","seno","sobreyectiva","subconjunto","suma","tangente","teorema","trapecio","trigonometría","trinomio","variable","vector","razón de cambio","derivada"]

TOPICOS = [ "Cambio de la velocidad en el tiempo. Siempre que la velocidad de un cuerpo cambia al transcurrir el tiempo, ya sea porque cambia su magnitud o su dirección o ambas cosas a la vez, se puede afirmar que existe aceleración.",
 "Es la primera letra del alfabeto griego. En cálculo o ecuaciones diferenciales representa a números infinitesimales, en geometría y trigonometría representa a ángulos y en física es una constante.",
 "Es una rama de la matemática que emplea números, letras y signos.  Cada letra o signo representa simbólicamente un número u otra entidad matemática.",
 "Un ángulo es la parte del plano comprendida entre dos semirrectas que tienen el mismo punto de origen o vértice.",
 "Es una medida de la extensión de una superficie, expresada en unidades de medida denominadas “Unidades de Superficie”. Equivale a 100 metros cuadrados. Para la geometría, un área es la superficie comprendida dentro de un perímetro, que se expresa en unidades de medidas que son conocidas como superficiales. Cuando alguno de los signos representa un valor desconocido se llama incógnita.",
 "Es la segunda letra del alfabeto griego. En cálculo o ecuaciones diferenciales representa a números infinitesimales, en geometría y trigonometría representa a ángulos y en física es una constante.",
 "Un binomio consta únicamente de dos términos unidos por los signos “+” o “-“ ",
 "La bisectriz de un ángulo es el lugar geométrico de los puntos que equidistan de los lados de un ángulo.",
 "Es la función que al mismo tiempo es inyectiva y sobreyectiva a la vez, es decir si todos los elementos del conjunto de salida tienen una imagen distinta en el conjunto de llegada, y a cada elemento del conjunto de llegada le corresponde un elemento del conjunto de salida.",
 "Es el plano que está formado por dos rectas numéricas, una horizontal y otra vertical que se cortan en un punto. Tiene como finalidad describir la posición de puntos, los cuales se representan por sus coordenadas o pares ordenados.",
 "Un cateto es cualquiera de los dos lados menores de un triángulo rectángulo, los que conforman el ángulo recto.",
 "Cuerpo geométrico que se obtiene por la rotación de un rectángulo en torno a uno de sus lados.",
 "Una circunferencia es el lugar geométrico de los puntos de un plano que equidistan de otro punto fijo y coplanario llamado centro en una cantidad constante llamada radio.",
 "Es el resultado que se obtiene al dividir una cantidad por otra, y que expresa cuantas veces está contenido el divisor en el dividendo.",
 "Constante o número que multiplica a una variable en una expresión algebraica.",
 "Una constante es una cantidad que tiene un valor fijo en un determinado cálculo, proceso o ecuación. Esto quiere decir que la constante es un valor permanente que no puede modificarse.",
 "Una función continua es aquella para la cual intuitivamente, para puntos cercanos del dominio se producen pequeñas variaciones en los valores de la función. Si la función no es continua se dice que es discontinua.",
 "Es la razón trigonométrica inversa del seno.",
 "En trigonometría el coseno de un ángulo en un triángulo rectángulo, e define como la razón entre el cateto adyacente a ese ángulo y la hipotenusa.",
 "Es la razón trigonométrica inversa de la tangente.",
 "Es una línea continua de una dimensión, que varía de dirección paulatinamente.",
 "Es un polígono que consta de diez lados.",
 "Poliedro de diez caras.",
 "Medida de longitud equivalente a la décima parte del metro.",
 "La diferencia entre dos valores próximos de una magnitud y varias funciones y operadores.",
 "Indica las partes iguales en que se divide la unidad en una fracción.",
 "En Matemáticas se define el determinante como una forma multilineal alternada de un cuerpo. Esta definición indica una serie de propiedades matemáticas y generaliza el concepto de determinante haciéndolo aplicable en numerosos campos. Sin embargo, el concepto de determinante o de volumen orientado fue introducido para estudiar el número de soluciones de los sistemas de ecuaciones lineales.",
 "Es el resultado de la resta o sustracción. La resta consiste en quitar una cierta cantidad de una cifra, la cantidad resultante es la diferencia.",
 "Se refiere a un cambio en la linearización de una función.",
 "Es el nombre matemático del primer término de la división.",
 "Es el término matemático del segundo término de la división.",
 "El dominio de una función es el conjunto de existencia de ella misma, es decir, los valores para los cuales la función está definida. El conjunto de todos los posibles valores de ingreso que la función acepta.",
 "Es el lugar geométrico de todos los puntos de un plano, tales que la suma de las distancias a otros dos puntos fijos llamados focos es constante.",
 "Es un polígono de nueve lados.",
 "Es la quinta letra del alfabeto griego. Suele designar a cantidades que tienden hacia cero, en particular en el estudio de los límites y de la continuidad.",
 "Triángulo cuyos lados y ángulos son de igual medida.",
 "Es el triángulo que tiene sus tres lados desiguales.",
 "Es la función donde e es el número de Euler. Esta función tiene por dominio de definición el conjunto de  los números reales, y tiene la particularidad de que su derivada es la misma función. ",
 "Se refiere al número de veces que se debe multiplicar por sí misma la base de una potencia.",
 "Producto obtenido al multiplicar un número pósitivo dado, por todos los enteros positivos inferiores a ese número.",
 "La factorización de un polinomio es el mecanismo que permite expresar a ese polinomio como el producto de dos o más polinomios.",
 "Representación de un número que consta de un valor llamado numerador (representado en la parte superior) y otro llamado denominador (representado en la inferior).",
 "Es una asociación que se establece entre los elementos de un conjunto A y los de un conjunto B, de manera que a cada elemento del conjunto A se le asocia un solo elemento del conjunto B",
 "Es una rama de las matemáticas que se ocupa del estudio  de medidas, propiedades y relaciones entre puntos, líneas, ángulos, superficies y sólidos.",
 "Medida de longitud equivalente a 100 metros.",
 "Poliedro de siete caras.",
 "Una hipérbola es el lugar geométrico de los puntos de un plano tales que el valor absoluto de la diferencia de sus distancias a dos puntos fijos, llamados focos, es igual a la distancia entre los vértices, la cual es una constante positiva.",
 "Es el lado de mayor longitud de un triángulo rectángulo, y el lado opuesto al ángulo recto. La medida de la hipotenusa puede ser hallada mediante el teorema de Pitágoras, si se conoce la longitud de los otros dos lados denominados catetos.",
 "Poliedro de veinte caras.",
 "Se refiere a que la aplicación de las propiedades de los límites no son válidas, sin embargo no significa que el límite no exista o no se pueda determinar.",
 "Cantidad sin límite, la misma puede ser numerable o no numerable. Es un signo en forma de ocho tendido que sirve para expresar un valor mayor que cualquier cantidad asignable.",
 "La integral es la operación inversa respecto de la derivada. La integral calcula el área debajo de una curva.",
 "Se llama intervalo al conjunto de números reales comprendidos entre otros dos dados; a y b que se llaman extremos del intervalo. Es un conjunto comprendido entre dos valores.",
 "Es la función donde a cada elemento del dominio le corresponde una imagen distinta en el codominio. En términos matemáticos una función es inyectiva si a cada valor del conjunto X (dominio) le corresponde un valor distinto en el conjunto Y (imagen).",
 "El límite describe la tendencia de una sucesión o una función, a medida que los parámetros de esa función se acercan a determinado valor.",
 "El logaritmo de un número en una base determinada, es el exponente al cual hay que elevar la base para obtener dicho número.",
 "Una matriz es un arreglo, en filas y columnas, de números que son llamados coeficientes.",
 "Es el número compuesto de un número entero y una fracción.",
 "Un múltiplo de un número es otro número que lo contiene un número entero de veces. En otras palabras, un múltiplo de n es un número tal que, dividido por n, da por resultado un número entero.",
 "Es el conjunto con el que se puede establecer una correspondencia biyectiva con el conjunto de los números naturales.",
 "Indica las partes iguales que se toman de la unidad en una fracción.",
 "Triángulo que tiene un ángulo obtuso.",
 "Segunda componente del par ordenado (x,y) que determinan un punto del plano en un sistema de coordenadas cartesianas.",
 "Paralelepípedo cuyas bases son rectángulos y sus aristas laterales perpendiculares a las básicas.",
 "Curva cerrada con dos ejes de simetría perpendiculares entre sí y compuesta de varios arcos de circunferencia tangentes entre sí.",
 "Se define como el lugar geométrico de los puntos de un plano que equidistan de una recta (eje o directriz) y un punto fijo llamado foco.",
 "Polígono de quince lados",
 "Es un polígono que consta de cinco lados y cinco vértices.",
 "Se refiere a la longitud de una curva cerrada.",
 "Rectas que se cortan formando ángulos rectos.",
 "Número irracional que corresponde a la razón entre la longitud de la circunferencia y su diámetro.",
 "Cuerpo geométrico que tiene como base un polígono cualquiera y como caras laterales triángulos con un vértice común.",
 "es una figura plana compuesta por una secuencia finita de segmentos rectos consecutivos no alineados. Estos segmentos son llamados lados, y los puntos en que se interceptan se llaman vértices. El interior del polígono es llamado cuerpo.",
 "expresión algebraica compuesta de dos o más términos llamados monomios unidos por los signos más o menos.",
 "Es una razón cuyo consecuente es 100.",
 "Una potencia es la manera abreviada en la que escribimos una multiplicación en la que todos sus factores son iguales.",
 "Son aquellos números que tienen la capacidad de poseer únicamente dos divisores, el mismo número y el 1, que es divisor de todo número. ",
 "Es el resultado que se obtiene de multiplicar dos o más cantidades.",
 "Símbolo con el que se representa el conjunto de los números racionales.",
 "Término con el que también se designa una fracción.",
 "Unidad de medida de ángulos que equivale a un ángulo que con el vértice en el centro de la circunferencia subtiende un arco de longitud igual al radio de esta circunferencia.",
 "Segmento que une el centro con un punto cualquiera de la circunferencia.",
 "Cantidad que ha de multiplicarse por sí misma una o más veces para obtener un número determinado.",
 "Es el conjunto de todos los valores de salida de una función.",
 "Es el conjunto de números resultante de la unión de los racionales con los irracionales.",
 "Corresponde al valor inverso de un número, de manera tal que al efectuar el producto entre ambos, resulta 1.",
 "Un rectángulo es un polígono de cuatro lados, en donde cada ángulo es un ángulo recto, es decir de 90 grados.",
 "Es la razón trigonométrica inversa del coseno.",
 "En trigonometría el seno de un ángulo en un triángulo rectángulo, se define como la razón entre el cateto opuesto y la hipotenusa.",
 "Una función es sobreyectiva si cada elemento del codominio tiene preimagen en el dominio, de la función. ",
 "Conjunto que forma parte de otro conjunto dado.",
 "Consiste en añadir dos números o más para obtener una cantidad total.",
 "En trigonometría la tangente de un ángulo en un triángulo rectángulo se define como la razón entre el cateto opuesto y el adyacente.",
 "Se llama Teorema a toda afirmación matemática importante que es demostrada de manera rigurosa, irrefutable. Un teorema es una afirmación que puede ser demostrada dentro de un sistema formal. Demostrar teoremas es un asunto central en la matemática.",
 "Cuadrilátero con un par de lados paralelos.",
 "La trigonometría es una rama de la matemática, cuyo significado etimológico es la medición de los triángulos.",
 "Expresión algebraica de tres términos.",
 "Una variable es la expresión simbólica representativa de un elemento no especificado, cuyo valor puede ser modificado.",
 "Un vector es todo segmento de recta dirigido en el espacio. Cada vector posee unas características que son; origen, módulo, dirección, sentido.",
 "Se refiere a la medida en la cual una variable se modifica con relación a otra. Se trata de la magnitud que compara dos variables a partir de sus unidades de cambio. En caso de que las variables no estén relacionadas, tendrán una razón de cambio igual a cero.",
 "La derivada de una función es una medida de la rapidez con la que cambia el valor de dicha función según cambie el valor de su variable independiente."]


SKILL_NAME = "Tópicos de Calculo"
HELP_MESSAGE = ('''<speak> 
    <p>Si deseas una definición, puedes pedirme: <s>"Alexa, abre tópicos de cálculo y dime un tópico"<break time=\"500ms\"/> </s> </p> 
    <p>Si deseas un tópico en específico, puedes decirme: <s>"¿Cuál es la definición de ...?"<break time=\"500ms\"/> </s> </p> 
    <p>Si deseas realizar una derivada, puedes preguntarme: <s>"¿Cuál es la derivada de ...?"<break time=\"500ms\"/> </s> </p> 
    ¿Qué deseas realizar?
    </speak>''')
HELP_REPROMPT = (HELP_MESSAGE)
STOP_MESSAGE = "Gracias por usar esta skill. ¡Adiós! "
EXCEPTION_MESSAGE = "No entendí muy bien, ¿Qué deseas realizar?"

sb = SkillBuilder()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def apl_img_title_text(title, text):
    return {
    "json" :"apl_img_title_text.json",
                    "datasources" : {
                    "bodyTemplate1Data": {
                        "type": "object",
                        "objectId": "bt1Sample",
                        "backgroundImage": {
                            "contentDescription": None,
                            "smallSourceUrl": None,
                            "largeSourceUrl": None,
                            "sources": [
                                {
                                    "url": "https://observatoriotecnologico.org.mx/assets/img/alexa/calculo.jpg",
                                    "size": "small",
                                    "widthPixels": 0,
                                    "heightPixels": 0
                                },
                                {
                                    "url": "https://observatoriotecnologico.org.mx/assets/img/alexa/calculo.jpg",
                                    "size": "large",
                                    "widthPixels": 0,
                                    "heightPixels": 0
                                }
                            ]
                        },
                        "title": title,
                        "textContent": {
                            "primaryText": {
                                "type": "PlainText",
                                "text": text
                            }
                        },
                        "logoUrl": "https://observatoriotecnologico.org.mx/assets/img/alexa/calculo_icon.png"
                    }
                }
            }

def _load_apl_document(file_path):
    # type: (str) -> Dict[str, Any]
    """Load the apl json document at the path into a dict object."""
    with open(file_path) as f:
        return json.load(f)

# Built-in Intent Handlers
class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In LaunchRequest")

        speech = "<speak>Bienvenido a la Skill de Tópicos de Cálculo, si deseas la definición de un tópico de cálculo, solo pídemelo <break time=\"500ms\"/>o puedes pedirme uno al azar, también puedo hacer derivadas básicas. Si necesitas ayuda, solo dí: 'Ayuda'. ¿Qué deseas realizar? </speak>"

        apl = apl_img_title_text("Bienvenido", "Bienvenido a la Skill de Tópicos de Cálculo, si deseas la definición de un tópico de cálculo, solo pídemelo, o puedes pedirme uno al azar, también puedo hacer derivadas básicas.\n\nSi necesitas ayuda, solo dí: 'Ayuda'\n\n. ¿Qué deseas realizar?")

        if viewport.get_viewport_profile(handler_input.request_envelope) == viewport.ViewportProfile.HUB_LANDSCAPE_LARGE or viewport.get_viewport_profile(handler_input.request_envelope) == viewport.ViewportProfile.HUB_LANDSCAPE_MEDIUM or viewport.get_viewport_profile(handler_input.request_envelope) == viewport.ViewportProfile.HUB_ROUND_SMALL or viewport.get_viewport_profile(handler_input.request_envelope) == viewport.ViewportProfile.TV_LANDSCAPE_XLARGE or viewport.get_viewport_profile(handler_input.request_envelope) == viewport.ViewportProfile.MOBILE_LANDSCAPE_SMALL:
            handler_input.response_builder.speak(speech).add_directive(
                RenderDocumentDirective(document=_load_apl_document(apl["json"]),datasources=apl["datasources"])
            ).set_should_end_session(False)
        else:
            handler_input.response_builder.speak(speech).set_card(SimpleCard(SKILL_NAME, re.sub('<[^<]+>', "",speech))).set_should_end_session(False)
        #handler_input.response_builder.speak(speech).ask(speech).set_card(
        #    SimpleCard(SKILL_NAME, speech))
        return handler_input.response_builder.response



class TopicoAleatorioIntentHandler(AbstractRequestHandler):
    """Handler for Device Information Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("topico_aleatorio")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("Topico Aleatiorio")

        speech = "No tengo la definición"+ ". ¿Qué más deseas realizar?"
    
        session_attributes = {}
        card_title = "Tópico de Cálculo"
        card_content = "No tengo la definición"
        try:
            id= random.randint(1,len(TOPICOS))
            speech = "'"+TOPICOS_NOMBRE[id].capitalize() +"': "+TOPICOS[id] + ". ¿Qué más deseas realizar?"
            card_content = "'"+TOPICOS_NOMBRE[id].capitalize() +"': "+TOPICOS[id]
        
        except:
            print("An exception occurred")

            
        apl = apl_img_title_text(card_title, card_content)
        
        if viewport.get_viewport_profile(handler_input.request_envelope) == viewport.ViewportProfile.HUB_LANDSCAPE_LARGE or viewport.get_viewport_profile(handler_input.request_envelope) == viewport.ViewportProfile.HUB_LANDSCAPE_MEDIUM or viewport.get_viewport_profile(handler_input.request_envelope) == viewport.ViewportProfile.HUB_ROUND_SMALL or viewport.get_viewport_profile(handler_input.request_envelope) == viewport.ViewportProfile.TV_LANDSCAPE_XLARGE or viewport.get_viewport_profile(handler_input.request_envelope) == viewport.ViewportProfile.MOBILE_LANDSCAPE_SMALL:
            handler_input.response_builder.speak(speech).add_directive(
            RenderDocumentDirective(document=_load_apl_document(apl["json"]),datasources=apl["datasources"])
            ).set_should_end_session(False)
        else:
            handler_input.response_builder.speak(speech).set_card(SimpleCard(SKILL_NAME, re.sub('<[^<]+>', "",speech))).set_should_end_session(False)
            
        

        return handler_input.response_builder.response
        
        
        
class TopicoIntentHandler(AbstractRequestHandler):
    """Handler for Device Information Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("topico")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("Topico")

        card_title = "Tópico de Cálculo"
    
        topico = ''
        topico_id = -1
        topico_nombre = ''
        speech = "No tengo la definición" + ". ¿Qué más deseas realizar?"
        card_content = "No tengo la definición"
        
        
        
        #speech = "Definición de {} es {}".format(topico,"")
        #session_attributes = {}
        attribute_manager = handler_input.attributes_manager
        session_attr = attribute_manager.session_attributes
        
        
        try:
            #topico = str(intent_r['intent']['slots']['topico_text']['value']) if 'topico_text' in intent_r['intent']['slots'] else ''
            #topico_id = int(intent_r['intent']['slots']['topico_text']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['id']) if 'values' in intent_r['intent']['slots']['topico_text']['resolutions']['resolutionsPerAuthority'][0] else -1
            #topico_nombre = str(intent_r['intent']['slots']['topico_text']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['name']) if 'values' in intent_r['intent']['slots']['topico_text']['resolutions']['resolutionsPerAuthority'][0] else -1
            
            slots = handler_input.request_envelope.request.intent.slots
            
            topico = str(slots["topico_text"].value) if 'topico_text' in slots else ''
            session_attr["topico_text"] = topico
            
            try:
                topico_id = int(slots['topico_text'].resolutions.resolutions_per_authority[0].values[0].value.id)# if 'values' in slots['topico_text'].resolutions.resolutions_per_authority[0] else -1
            except:
                topico_id = -1
            session_attr["id"] = topico_id
            
            try:
                topico_nombre = str(slots['topico_text'].resolutions.resolutions_per_authority[0].values[0].value.name)# if 'values' in slots['topico_text'].resolutions.resolutions_per_authority[0] else ""
            except:
                topico_nombre = ''
            session_attr["name"] = topico_nombre
            
            
            card_content = "" 
            if topico_id > -1:
                speech = "'"+topico_nombre.capitalize()+"': "+TOPICOS[topico_id] + ". ¿Qué más deseas realizar?"
                card_content = "'"+topico_nombre.capitalize()+"': "+TOPICOS[topico_id]
            else:
                speech = "No tengo la definición de " + topico + ". ¿Qué más deseas realizar?"
                card_content = "No tengo la definición de " + topico 
                
            
        except:
            print("An exception occurred")

            
        apl = apl_img_title_text(card_title, card_content)

        if viewport.get_viewport_profile(handler_input.request_envelope) == viewport.ViewportProfile.HUB_LANDSCAPE_LARGE or viewport.get_viewport_profile(handler_input.request_envelope) == viewport.ViewportProfile.HUB_LANDSCAPE_MEDIUM or viewport.get_viewport_profile(handler_input.request_envelope) == viewport.ViewportProfile.HUB_ROUND_SMALL or viewport.get_viewport_profile(handler_input.request_envelope) == viewport.ViewportProfile.TV_LANDSCAPE_XLARGE or viewport.get_viewport_profile(handler_input.request_envelope) == viewport.ViewportProfile.MOBILE_LANDSCAPE_SMALL:
            handler_input.response_builder.speak(speech).add_directive(
            RenderDocumentDirective(document=_load_apl_document(apl["json"]),datasources=apl["datasources"])
            ).set_should_end_session(False)
        else:
            handler_input.response_builder.speak(speech).set_card(SimpleCard(SKILL_NAME, re.sub('<[^<]+>', "",speech))).set_should_end_session(False)
        

        return handler_input.response_builder.response
        
        

class DerivadaIntentHandler(AbstractRequestHandler):
    """Handler for Device Information Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("derivada")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("Derivada")

        card_title = "Cálcular derivada a la n"
        
        x_valor = None
        x_exponente = None
        x_exponente_numero = None
        variable = ""
        
        slots = handler_input.request_envelope.request.intent.slots
        
        try:
            #variable = str(intent_r['intent']['slots']['variable']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['name']) if 'values' in intent_r['intent']['slots']['variable']['resolutions']['resolutionsPerAuthority'][0] else ""
            variable = str(slots['variable'].resolutions.resolutions_per_authority[0].values[0].value.name)
            
        except:
            variable = ""
            
        try:
            #x_valor = int(intent_r['intent']['slots']['x_valor']['value']) if 'value' in intent_r['intent']['slots']['x_valor'] else None
            x_valor = int(slots["x_valor"].value)# if 'value' in intent_r['intent']['slots']['x_valor'] else None
        except:
            x_valor = None
            
        
        try:
            #x_exponente = int(intent_r['intent']['slots']['x_exponente']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['id']) if 'values' in intent_r['intent']['slots']['x_exponente']['resolutions']['resolutionsPerAuthority'][0] else None
            x_exponente = int(slots['x_exponente'].resolutions.resolutions_per_authority[0].values[0].value.id)
        except:
            x_exponente = None
            
        try:
            #x_exponente_numero = int(intent_r['intent']['slots']['x_exponente_numero']['value']) if 'value' in intent_r['intent']['slots']['x_exponente_numero'] else None
            x_exponente_numero = int(slots['x_exponente_numero'].value)
        except:
            x_exponente_numero = None
        
        if x_exponente is None and x_exponente_numero is None:
            x_exponente = 1
        elif x_exponente is None and x_exponente_numero is not None:
            x_exponente = x_exponente_numero
            
        
    
            
        resultado = ".."
        
        texto_elevado = ""
        texto_valor = ""
        card_content = ""
        
        if x_exponente is None:
            texto_elevado = ""
        elif x_exponente == 2:
            texto_elevado = " al cuadrado"
        elif x_exponente == 3:
            texto_elevado = " al cubo" 
        elif x_exponente >= 4:
            texto_elevado = " elevado a la {} ".format(str(x_exponente)) 
        
        if variable != "" and x_valor == 1:
            texto_valor = ""
        else:
            texto_valor = str(x_valor if x_valor is not None else 1 )
            
        if variable != "" and x_valor is None:
            x_valor = 1
            
        if x_exponente is not None and x_valor is None:
            x_valor = 1
        
        if  variable == "":
            speech = "La derivada de una constante es 0" + ". ¿Qué más deseas realizar?"
            card_content = "La derivada de una constante es 0"
        else:
            texto_elevado_resultado = ""
            variable_resultado = variable;
            
            if x_exponente is None:
                texto_elevado_resultado = ""
            elif x_exponente-1 == 2:
                texto_elevado_resultado = " al cuadrado"
            elif x_exponente-1 == 3:
                texto_elevado_resultado = " al cubo" 
            elif x_exponente-1 >= 4:
                texto_elevado_resultado = " elevado a la {} ".format(str(x_exponente-1)) 
                
            if  variable != "" and x_exponente == 1:
                variable_resultado = ""
            resultado = str(x_valor * x_exponente) + " " + variable_resultado + texto_elevado_resultado
            
            
            if texto_valor == "1" and variable != "":
                texto_valor = ""
            speech = "La derivada de {} {} {} es : {} . ¿Qué más deseas realizar?".format(texto_valor,variable, texto_elevado , resultado)
            card_content = "La derivada de {} {} {} es : {}".format(texto_valor,variable, texto_elevado , resultado)
    
        session_attributes = {"texto_valor":texto_valor, "variable":variable, "texto_elevado":texto_elevado,"resultado":resultado}
            
        apl = apl_img_title_text(card_title, card_content)

        if viewport.get_viewport_profile(handler_input.request_envelope) == viewport.ViewportProfile.HUB_LANDSCAPE_LARGE or viewport.get_viewport_profile(handler_input.request_envelope) == viewport.ViewportProfile.HUB_LANDSCAPE_MEDIUM or viewport.get_viewport_profile(handler_input.request_envelope) == viewport.ViewportProfile.HUB_ROUND_SMALL or viewport.get_viewport_profile(handler_input.request_envelope) == viewport.ViewportProfile.TV_LANDSCAPE_XLARGE or viewport.get_viewport_profile(handler_input.request_envelope) == viewport.ViewportProfile.MOBILE_LANDSCAPE_SMALL:
            handler_input.response_builder.speak(speech).add_directive(
            RenderDocumentDirective(document=_load_apl_document(apl["json"]),datasources=apl["datasources"])
            ).set_should_end_session(False)
        else:
            handler_input.response_builder.speak(speech).set_card(SimpleCard(SKILL_NAME, re.sub('<[^<]+>', "",speech))).set_should_end_session(False)
            
        
        return handler_input.response_builder.response

class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ( is_intent_name("AMAZON.HelpIntent")(handler_input) or
                is_intent_name("topico_ayuda")(handler_input) )

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In HelpIntentHandler")

        handler_input.response_builder.speak(HELP_MESSAGE).ask(
            HELP_REPROMPT).set_card(SimpleCard(
                SKILL_NAME, re.sub('<[^<]+>', "",HELP_MESSAGE)))
        return handler_input.response_builder.response


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (is_intent_name("AMAZON.CancelIntent")(handler_input) or
                is_intent_name("AMAZON.StopIntent")(handler_input) or
                is_intent_name("salir")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In CancelOrStopIntentHandler")

        handler_input.response_builder.speak(STOP_MESSAGE).set_should_end_session(True)
        return handler_input.response_builder.response


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In SessionEndedRequestHandler")

        logger.info("Session ended reason: {}".format(
            handler_input.request_envelope.request.reason))
        return handler_input.response_builder.response


# Exception Handler
class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Catch all exception handler, log exception and
    respond with custom message.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.info("In CatchAllExceptionHandler")
        logger.error(exception, exc_info=True)

        handler_input.response_builder.speak(EXCEPTION_MESSAGE).ask(
            HELP_REPROMPT)

        return handler_input.response_builder.response


# Request and Response loggers
class RequestLogger(AbstractRequestInterceptor):
    """Log the alexa requests."""
    def process(self, handler_input):
        # type: (HandlerInput) -> None
        logger.debug("Alexa Request: {}".format(
            handler_input.request_envelope.request))


class ResponseLogger(AbstractResponseInterceptor):
    """Log the alexa responses."""
    def process(self, handler_input, response):
        # type: (HandlerInput, Response) -> None
        logger.debug("Alexa Response: {}".format(response))


# Register intent handlers
sb.add_request_handler(LaunchRequestHandler())

sb.add_request_handler(TopicoIntentHandler())
sb.add_request_handler(TopicoAleatorioIntentHandler())
sb.add_request_handler(DerivadaIntentHandler())
#sb.add_request_handler(SalirIntentHandler())


sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())

# Register exception handlers
sb.add_exception_handler(CatchAllExceptionHandler())

# TODO: Uncomment the following lines of code for request, response logs.
# sb.add_global_request_interceptor(RequestLogger())
# sb.add_global_response_interceptor(ResponseLogger())

# Handler name that is used on AWS lambda
lambda_handler = sb.lambda_handler()
