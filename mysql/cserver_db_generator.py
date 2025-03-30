import random as R
import csv
import math
import numbers
import re

rel_path_to_file = "CSE builds/Backend DB Exports/game_db_content.sql"

# 0. Helper methods
def inv_lerp(a,b,v):
    v = min(max(v,a),b)
    return (v-a) / (b-a)

# 1. Load data lists

# Sobre ciudadanos
nombres = {
    "humano":[],
    "corgo":["yerma","murmu","nadalor","pomero","flexor","torsor","talud","corroso","vigo","tocne","bino","wardware","meca"], # Únicos: "worbulo","turro"
    "feriseo":["forilisia","giripimbas","waifai","eska","fizz","parappa","sala","tritin","pana","rapo","nimba","pepo"], # Únicos: "pepuv","imp","epitaf"
    "exukente":["forku","kinfe","akeritov","kroxik","krikaracha","mosko","krass","krill","ter","kitle","lukanus","kito","krisopa","blattoke"] # Únicos: "kripo","vikal"
}
reader = csv.DictReader(open('datasets_cse/spanish-names-master/hombres.csv',encoding="utf-8"))
for row in reader: nombres["humano"].append(row['nombre'].split()[0].lower())
reader = csv.DictReader(open('datasets_cse/spanish-names-master/mujeres.csv',encoding="utf-8"))
for row in reader: nombres["humano"].append(row['nombre'].split()[0].lower())
apellidos = {
    "humano":[],
    "corgo":["torrifel","naineifai","kontro","rimpson","gavku","wacero","wormigon","brick","cimento","amperius","tronoco","mankis"],
    "feriseo":["ferelez","tipov","pililingi","giripimbez","charro","belulu","mandra","cecilia","surinam","xenopus"],
    "exukente":["kontrov","kenru","takep","lukkivy", "pouliya","hopper","mitta","chinchi","krepidopter","krabajo","vispa","pulgo","verakova"] # Únicos: "kosmi"(casta de la realeza)
}
reader = csv.DictReader(open('datasets_cse/spanish-names-master/apellidos-20.csv',encoding="utf-8"))
for row in reader: 
    apellidos["humano"].append(row['apellido'].lower())
    if len(apellidos["humano"]) >= 600: break
rangos_edad = { # Usar con distribución beta
    "humano":{"a":1.6,"b":2,"max":100},
    "corgo":{"a":1.6,"b":2,"max":140},
    "feriseo":{"a":2,"b":1.6,"max":50},
    "exukente":{"a":2,"b":2,"max":75}
}
rangos_altura = { # Usar con distribución normal
    "humano":{"m":1.7,"d":0.1,"fin_crecimiento":20},
    "corgo":{"m":2.2,"d":0.05,"fin_crecimiento":28},
    "feriseo":{"m":1.6,"d":0.4,"fin_crecimiento":12},
    "exukente":{"m":1.5,"d":0.1,"fin_crecimiento":16}
}
colores_pelo = {
    "humano":["negro","castaño","castaño oscuro","rubio","castaño claro","pelirrojo"],
    "corgo":["blanco","rubio"], # ¿Donde tienen el pelo?... Hehe
    "feriseo":[], #No tienen lmao
    "exukente":["dorado","azul"] # Jóven / Adulto
}

def gen_humano(dni):
    nombre = ""
    e = R.randint(1,200)
    if e == 1: nombre = R.choice(nombres["feriseo"])
    elif e == 2: nombre = R.choice(nombres["corgo"])
    else: nombre = R.choice(nombres["humano"])
    apellido = R.choice(apellidos["humano"])
    re = rangos_edad["humano"]
    edad = round( R.betavariate(re["a"],re["b"]) * re["max"] )
    color_pelo = R.choices(colores_pelo["humano"],weights=[150,100,100,80,100,10])[0]
    ra = rangos_altura["humano"]
    altura = round( R.gauss(ra["m"],ra["d"]) * inv_lerp(-3,ra["fin_crecimiento"],edad), 2)
    row = [dni, nombre, apellido, edad, color_pelo, altura, "humano"]
    return row

def gen_feriseo(dni):
    nombre = ""
    e = R.randint(1,200)
    if e == 1: nombre = R.choice(nombres["humano"])
    elif e == 2: nombre = R.choice(nombres["corgo"])
    else: nombre = R.choice(nombres["feriseo"])
    apellido = R.choice(apellidos["feriseo"])
    re = rangos_edad["feriseo"]
    edad = round( R.betavariate(re["a"],re["b"]) * re["max"] )
    color_pelo = ""
    ra = rangos_altura["feriseo"]
    altura = round( R.gauss(ra["m"],ra["d"]) * inv_lerp(-1,ra["fin_crecimiento"],edad), 2)
    row = [dni, nombre, apellido, edad, color_pelo, altura, "feriseo"]
    return row

def gen_corgo(dni):
    nombre = ""
    e = R.randint(1,200)
    if e == 1: nombre = R.choice(nombres["humano"])
    elif e == 2: nombre = R.choice(nombres["feriseo"])
    else: nombre = R.choice(nombres["corgo"])
    apellido = R.choice(apellidos["corgo"])
    re = rangos_edad["corgo"]
    edad = round( R.betavariate(re["a"],re["b"]) * re["max"] )
    color_pelo = R.choice(colores_pelo["corgo"])
    ra = rangos_altura["corgo"]
    altura = round( R.gauss(ra["m"],ra["d"]) * inv_lerp(-6,ra["fin_crecimiento"],edad), 2)
    row = [dni, nombre, apellido, edad, color_pelo, altura, "corgo"]
    return row

def gen_exukente(dni):
    nombre = R.choice(nombres["exukente"])
    apellido = R.choice(apellidos["exukente"])
    re = rangos_edad["exukente"]
    edad = round( R.betavariate(re["a"],re["b"]) * re["max"] )
    edad_bias = 0
    if edad > re["max"]/2: edad_bias = 1
    color_pelo = colores_pelo["exukente"][edad_bias]
    ra = rangos_altura["exukente"]
    altura = round( R.gauss(ra["m"],ra["d"]) * inv_lerp(-10,ra["fin_crecimiento"],edad), 2)
    row = [dni, nombre, apellido, edad, color_pelo, altura, "exukente"]
    return row

def gen_ciudadano(dni,h,c,f,e):
    p = R.randint(1,h+c+f+e)
    c = h+c; f = c+f
    if p <= h: return gen_humano(dni)
    elif p <= c: return gen_corgo(dni)
    elif p <= f: return gen_feriseo(dni)
    else: return gen_exukente(dni)

# Sobre vehículos
marcas_vehiculos = [
    "Gaston Marton", "Debugatti", "BWM", "Sigma Romero", "Citrïco", "Claudi", "Ferfari", "Fivd", "LLada", "Kai", "Hamburghini", "Mazdana",
    "Tayoto", "Nikkun", "Renaul", "Zeat", "Telas" ,"Supraru", "Opela", "Percebes-Benz", "Peyot"
]
colores_vehiculos = [
    "verde oscuro metálico", "morado tinto", "azul metálico", "azul eléctrico", "blanco perlado", "negro brillante", "verde oliva"
    "plateado cromado", "gris grafito", "rojo carmesí", "amarillo brillante", "verde esmeralda", "morado profundo", "naranja vibrante",
    "verde esperanza", "blanco roto", "blanco huevo", "rojo cereza", "rubí", "rojo prismático", "mandarina", "naranja coral",
    "verde cocodrilo", "negro medianoche", "humo", "lobo gris", "gris piedra", "marfil pálido", "blanco acústico", "blanco brillante",
]

# Sobre viviendas
calles = [ # "u" = casas Usadas (durante generación de viviendas)
    {"distrito":"humano","zonas":[
        {"direccion":"Avenida America","casas":100,"casas_por_edificio":6,"u":0},
        {"direccion":"Calle Albert Einstein","casas":40,"casas_por_edificio":4,"u":0},
        {"direccion":"Calle Marie Curie","casas":30,"casas_por_edificio":1,"u":0},
    ]},
    {"distrito":"feriseo","zonas":[
        {"direccion":"Avenida Reina Forilisia","casas":100,"casas_por_edificio":8,"u":0},
        {"direccion":"Calle Ojo de Chlungus","casas":16,"casas_por_edificio":1,"u":0},
        {"direccion":"Calle Giripimbas 3º","casas":50,"casas_por_edificio":4,"u":0},
    ]},
    {"distrito":"corgo","zonas":[
        {"direccion":"Avenida Warlow","casas":80,"casas_por_edificio":6,"u":0},
        {"direccion":"Calle Mok","casas":40,"casas_por_edificio":8,"u":0},
        {"direccion":"Calle Luw","casas":40,"casas_por_edificio":2,"u":0},
    ]},
    {"distrito":"exukente","zonas":[
        {"direccion":"Avenida Kosmi","casas":110,"casas_por_edificio":12,"u":0},
        {"direccion":"Calle Tripaloski","casas":20,"casas_por_edificio":8,"u":0},
        {"direccion":"Calle Korumiv","casas":20,"casas_por_edificio":4,"u":0},
    ]}
]

def crear_vivienda_segun_ciudadano(id,persona):
    titular = persona[0]
    especie = persona[6]
    edad = persona[3]
    if edad < 18: return [] # Los menores no poseen casas...
    # Elección de distrito
    e_idx = 0
    for i in range(len(calles)):
        if especie == calles[i]["distrito"]:
            e_idx = i
            break
    prob_distrito = [5,5,5,5]
    prob_distrito[e_idx] += 15 # Mayor probabilidad de vivir en su distrito
    distrito = R.choices([0,1,2,3],k=1,weights=prob_distrito)[0]
    # Elección de calle
    lista_zonas = calles[distrito]["zonas"]
    idx_zonas = []
    prob_zona = []
    for z in range(len(lista_zonas)):
        idx_zonas.append(z)
        prob_zona.append(lista_zonas[z]["casas"])
    calle_idx = R.choices(idx_zonas,k=1,weights=prob_zona)[0]
    datos_calle = lista_zonas[calle_idx]
    direccion = datos_calle["direccion"]
    # Elección de casa
    n_casas = datos_calle["casas"]
    n_cpe = datos_calle["casas_por_edificio"]
    casas_usadas = datos_calle["u"]
    esPiso = 0 if n_cpe == 1 else 1
    if casas_usadas >= n_casas: return []
    datos_calle["u"] += 1
    piso = 1+(casas_usadas % n_cpe)
    edificio = math.ceil(casas_usadas/n_cpe)
    
    direccion += " n" + str(edificio)
    if esPiso: direccion += " " + str(piso) + "º"

    return [id, direccion, titular, esPiso]

# Sobre rutas
localizaciones = [
    {"distrito":"humano","lista":[
        {"nombre":"Avenida America","pos":[20,10],"fama":100},
        {"nombre":"Calle Albert Einstein","pos":[20,5],"fama":60},
        {"nombre":"Calle Marie Curie","pos":[20,15],"fama":55},
        {"nombre":"Callejón L. Ernesto Miramontes","pos":[30,7],"fama":30},
        {"nombre":"Murica Guns","pos":[5,5],"fama":30},
        {"nombre":"Mega Milky","pos":[10,15],"fama":90},
    ]},
    {"distrito":"feriseo","lista":[
        {"nombre":"Avenida Reina Forilisia","pos":[60,10],"fama":100},
        {"nombre":"Calle Ojo de Chlungus","pos":[60,5],"fama":50},
        {"nombre":"Calle Giripimbas 3º","pos":[60,15],"fama":60},
        {"nombre":"Callejón Zaruli","pos":[70,12],"fama":30},
        {"nombre":"Paul's Pizzeria","pos":[60,17],"fama":90},
        {"nombre":"Feri Teatro","pos":[55,8],"fama":60},
        {"nombre":"Wet Groove","pos":[72,6],"fama":40},
    ]},
    {"distrito":"corgo","lista":[
        {"nombre":"Avenida Warlow","pos":[100,10],"fama":100},
        {"nombre":"Calle Mok","pos":[100,5],"fama":55},
        {"nombre":"Calle Luw","pos":[100,15],"fama":55},
        {"nombre":"Callejón Gavku","pos":[95,7],"fama":30},
        {"nombre":"Rincón del Turro","pos":[110,6],"fama":30},
        {"nombre":"Corgomatic","pos":[92,17],"fama":30},
    ]},
    {"distrito":"exukente","lista":[
        {"nombre":"Avenida Kosmi","pos":[14,10],"fama":100},
        {"nombre":"Calle Tripaloski","pos":[140,5],"fama":40},
        {"nombre":"Calle Korumiv","pos":[140,15],"fama":40},
        {"nombre":"Callejón Kroxik Takep 31th","pos":[125,18],"fama":25},
    ]},
]

def distrito_aleatorio(nombre_especie):
    idx_especie = 0
    if nombre_especie == "feriseo": idx_especie = 1
    elif nombre_especie == "corgo": idx_especie = 2
    elif nombre_especie == "exukente": idx_especie = 3
    distrito = idx_especie
    r = R.random()
    for mov_op in range(2,6):
        p = 1/(mov_op)
        if r < p:
            if distrito == 0: distrito += 1
            elif distrito == 3: distrito -= 1
            else: distrito += R.choice([1,-1])
    return distrito
def localizacion_aleatoria(distrito_idx):
    zonas_distrito = localizaciones[distrito_idx]["lista"]
    w = []
    for z in zonas_distrito:
        w.append(z["fama"])
    return R.choices(zonas_distrito,k=1,weights=w)[0]

def calcular_distancia_viaje(pos_origen,pos_destino):
    v_dif = [pos_destino[0] - pos_origen[0], pos_destino[1] - pos_origen[1]]
    return round( math.sqrt((v_dif[0]*v_dif[0])+(v_dif[1]*v_dif[1])) ,2)
    

# Sobre correos
plantillas_correo_relleno = [ # {n} = nombre, {d} = direccion casa
    {"emisor":"noreply@steel.com","asunto":"¡1 JUEGO QUE QUIERES ESTÁ DE OFERTA!","contenido":"¡Un juego de tu lista de deseados está de oferta! \\n¡Promoción especial! La promoción finaliza mañana.\\n Ciertos precios y descuentos pueden sufrir cambios. Encontrarás más información en la página de la tienda de Steel."},
    {"emisor":"no-reply@ferifiestas.com","asunto":"Entrada Confirmada","contenido":"Entrada Confirmada. ¡Hola {n}! Aquí tienes tu entrada para Feri Teatro.\\n Puedes descargarla en tu dispositivo desde el siguiente botón y presentarla en la entrada del recinto."},
    {"emisor":"no-reply@ferifiestas.com","asunto":"Entrada Confirmada","contenido":"Entrada Confirmada. ¡Hola {n}! Aquí tienes tu entrada para Wet Groove.\\n Puedes descargarla en tu dispositivo desde el siguiente botón y presentarla en la entrada del recinto."},
    {"emisor":"confirmacionpedido@paulspizzeria.com","asunto":"Gracias por comprar en Paul's Pizzeria","contenido":"Hola, {n}, acabamos de recibir tu pedido ¡Nos ponemos manos a la obra! Llevaremos tu pedido a tu casa. \\nForma de pago: Con targeta. \\n\\nRespuesta automática, por favor no responda a este mensaje."},
    {"emisor":"loteria100por100realnofake@l0teria.com","asunto":"GANASTE LA LOTERÍA","contenido":"¡Enhorabuena <nombre>, tu número de lotería ha sido premiado con 100.000.000! Inicia sesión con tu cuenta universal desde el siguiente botón para reclamar ingresar el dinero."},
    {"emisor":"noreply@eelbanco.com","asunto":"Promoción Familiar","contenido":"Accede a tu cuenta bancaria para conocer las ventajas de incluir las cuentas de tus familiares con este nuev plan de ahorro. \\nRecuerda que por tu seguridad nunca te pediremos la contraseña y no debe acceder al banco desde ningún link  por correo"},
    {"emisor":"noreply@ee1banco.com","asunto":"TU CUENTA ESTÁ EN PELIGRO","contenido":"Se ha detectado un error en tu cuenta y debe iniciar sesión para arreglar el problema. \\nSi no se realizan acciones en las próximas 48 horas, su cuenta bancaria quedará suspendida. \\nInicie sesión al banco desde el siguiente link."},
    {"emisor":"verylegal@notpiramid.com","asunto":"Teletrabajo","contenido":"¡Trabaje desde casa! Le ofertamos teletrabajo únicamente de 8 a 12 ¡Gane 3000 al mes! Ponte en contacto con @DariusVex en Woofer para más información ¡Las crypto monedas son el futuro!"},
] # Ejemplo uso: "... {n}...".format(n="nombre")

def direccion_correo_aleatorio(c): # c = ciudadano
    destinatario = ""
    posibles_fragmentos = [c[1]]
    cachos_apellido = c[2].split()
    for cacho in cachos_apellido:
        if len(cacho) >= 4:
            posibles_fragmentos.append(cacho)
    aux = R.sample( posibles_fragmentos,k=R.randint(1,len(posibles_fragmentos)) )
    if R.random() < 0.35: aux.append(c[3])

    cool = R.random()
    if c[3] < 24:
        if cool < 0.05: destinatario += "xXx"
        elif cool < 0.20: destinatario += "X"
    sep_barra = R.random() < 0.5
    for i in range(len(aux)):
        if i > 0 and R.random() < 0.30: 
            if sep_barra: destinatario += "_"
            else: destinatario += "."
        destinatario += str(aux[i])
    if c[3] < 24:
        if cool < 0.05: destinatario += "xXx"
        elif cool < 0.20: destinatario += "X"

    destinatario += "@eelmail.com"
    return destinatario

# Sobre PingBúsquedas
ciudadano_ip = {}

def generar_ip_publica():
    while True:
        byte1 = R.randint(1,191)
        if byte1 == 10: continue # privadas
        if byte1 == 127: continue # localhost
        byte2 = R.randint(0,255)
        if byte1 == 172 and (byte2 >= 16 and byte2 <= 31): continue
        byte3 = R.randint(0,255)
        byte4 = R.randint(0,255)
        if byte1 < 127: # Red clase A
            if byte2 == 0 and byte3 == 0 and byte4 == 0: continue # dirección de red
            if byte2 == 255 and byte3 == 255 and byte4 == 255: continue # broadcast
        elif byte1 < 192: # Red clase B
            if byte3 == 0 and byte4 == 0: continue # dirección de red
            if byte3 == 255 and byte4 == 255: continue # broadcast
        final_ip = ".".join([str(byte1),str(byte2),str(byte3),str(byte4)])
        return final_ip

def asignar_ips_a_ciudadanos():
    # IPs públicas a ciudadanos según su hogar (por cada vivienda)
    prev_v = -1
    ip = ""
    for i in range(len(alojadoEn)):
        par = alojadoEn[i]
        v = par[0]
        if v != prev_v: ip = generar_ip_publica()
        c = par[1]
        if ciudadano_ip.get(c) == None: ciudadano_ip[c] = []
        ciudadano_ip[c].append(ip)
        prev_v = v
    # IPs públicas por cada localización de forma aleatoria
    for l in localizaciones:
        n = len(l["lista"])
        for i in range(n):
            ip = generar_ip_publica()
            for j in range(60):
                c_dni = R.choice(ciudadanos)[0]
                if ciudadano_ip.get(c_dni) == None: ciudadano_ip[c_dni] = []
                if ip in ciudadano_ip[c_dni]: continue
                ciudadano_ip[c_dni].append(ip)

plantillas_busquedas = [ # {a} = sustantivo, {b} = otro sustantivo distinta a {a}, {c} = verbo infinitivo, # {d} = verbo gerundio
    "Cómo entrenar para {a}",
    "Cómo hacer {a}",
    "Quién inventó el {a}",
    "{a}",
    "Canción del {a}",
    "Canción de {c}",
    "Música para {c}",
    "Cuándo es el día del {a}",
    "Cuántos días faltan para {a}",
    "Cómo hacer {a} en {b}",
    "Cómo hacer {a} con {b}",
    "Cuántas {a} hay en {b}",
    "Cómo {c} rápido",
    "Cómo {c} en {a}",
    "Cómo {c} {a}",
    "Cómo {c} a {a}",
    "Cómo {c} con {a}",
    "Qué es {a}",
    "Se me olvidó cómo {c}",
]
peso_busquedas = [10,30,15,10,12,12,18,10,10,20,20,20,15,40,40,30,30,20,20]
verbos = [
    "abrazar","atraer","abrir","acampar","beber","aburrir","aceptar","conmover","conocer","atribuir","amar","correr","concluir",
    "amasar","coser","conducir","asimilar","creer","convertir","disasociar","defender","cumplir","caminar","demoler","debatir",
    "cantar","decidir","embellecer","decir","declarar","describir","difundir","dibujar","diluir","empezar","favorecer","discutir",
    "escuchar","elegir","esperar","hacer","escribir","estacionar","leer","esparcir","iluminar","morir","informar","mover","oír",
    "lavar","nacer","partir","mezclar","oscurecer","permitir","negar","poner","posar","recibir","querer","reír","restar","repartir",
    "secar","resistir","señalar","sentir","simular","sonreír","soñar","suprimir","subrayar","toser","venir","terminar","volver","vestir",
    "matar","tener","comprar","buscar"]
sustantivos = [
    "sal", "estrella", "puente", "leona", "submarinista", "puerta", "caballo", "Júpiter", "tela", "miedo", "pierna",
    "jugo", "cielo", "banco", "gato", "doctor", "hielo", "inteligencia", "bondad", "dolor", "azúcar", "araña", "vaso",
    "arena", "sardina", "carnicero", "fuego", "arquitecto", "agua", "hermano", "hinchazón", "médico", "análisis", "rueda",
    "mesa", "zapatero", "sueño", "casa", "ejército", "libro", "vestido", "abogado", "embarcación", "cine", "pimienta",
    "paraguas", "boca", "pertenencias", "bandera", "reloj", "sufrimiento", "México", "mano", "guantes", "perro", "Vía Láctea",
    "bicicleta", "aguacate", "cebra", "hambre", "equipo", "río", "resfriado", "Luna", "flauta", "rebaño", "humano",
    "satisfacción", "harina", "orgullo", "sobrino", "picor", "ventana", "enfermería", "expedición", "valor", "planta",
    "ganas", "pez", "cristal", "río", "estudiante", "sed", "sofá", "voluntad", "sacacorchos", "atención", "cuadro", "leche", 
    "calor", "vino", "mar", "cantante", "música", "almendra", "manzana", "pepinillo", "patata", "cocreta", "almondiga",
    "corgo", "exukente", "feriseo", "tarta", "empanada"
]

def busqueda_aleatoria():
    busqueda = R.choices(plantillas_busquedas,k=1,weights=peso_busquedas)[0]
    s = R.sample(sustantivos,k=2)
    r = R.random()
    if r < 0.01: s[R.randint(0,1)] = R.choice(nombres["humano"])
    if r < 0.0125: s[R.randint(0,1)] = R.choice(nombres["feriseo"])
    if r < 0.015: s[R.randint(0,1)] = R.choice(nombres["corgo"])
    if r < 0.0175: s[R.randint(0,1)] = R.choice(nombres["exukente"])
    v = R.choice(verbos)
    return busqueda.format(a=s[0],b=s[1],c=v)

# Sobre Transbordos
entidades_transbordos = [
    "Nidolé", "Ares", "PUPSICO", "Mbidia", "Zisco", "Mike", "Amazin", "Sangsung",
    "Corgus INC", "ANTS", "ToadSoap", "Morioh", "FizzFuss", "HowHungryHorse"
]
entidades_transbordos = entidades_transbordos + marcas_vehiculos

# Sobre AsistenteVoz
asistente_prompts = [ # {a} = Llamada al asistente (inicio prompt), {o} = orden, {p} = pregunta, {m} = modales ("por favor")
    "{a}, {o}{m}",
    "{a} {p}",
    "{a} {p} y {p2}",
]
asistente_inicios = [ "Asistente", "Señorita Asistente", "Cacharro","Oye asistente"]
asistente_modales = [ ", gracias", ", por favor", ", corazón"]
asistente_ordenes = [
    "pon música wena", "pon música jazz", "ponme música del cantante este que me gusta mucho", "música humana", 
    "pon música indígena ferisea", "reproduce mi lista de reproducción favorita", "play despacito", "música romántica",
    "música relajante para estudiar", "música relajante para dormir", "enciende la radio", "recuérdame mañana la cita",
    "incluye en la lista de recetas el último plato"
]
asistente_preguntas = [ # {n} = det + sustantivo plural (los humanos), {s} = sustantivo normal, {p} = nombre persona
    "¿Qué música escuchan {n}?", "¿Cómo de fuerte son {n}?", "¿Por qué se extinguieron {n}?",
    "¿Cuáles son los ingredientes para hacer una {s}?", "¿Cómo se hacen {s}?", "¿Cómo puedo gustarle a {n}?",
    "¿Cómo puedo gustarle a {p}?", "¿Qué huecos tengo hoy en mi agenda?", "añade a la lista de la compra {s}",
    "¿Qué fue antes el huevo o la gallina?", "¿Qué fue antes el huevo o el glup?", "¿Cómo se alimentan {n}?",
    "¿Qué {s} me recomiendas hoy?", "¿Cómo está el {s}?", "¿Cómo está el exterior espacial?", "¿Cuánto cuesta un {s}?"
]
sustantivos_plural = [
    "los humanos", "los feriseos", "los corgos", "los exukentes", "los hombres", "las mujeres", "los vehículos", "los glup",
    "los animales"
]

def gen_log_asistente():
    r = R.random()
    log = ""
    inicio = R.choices(asistente_inicios,k=1,weights=[60,15,5,20])[0]
    if r < 0.2:
        log = inicio+", "+busqueda_aleatoria()
    elif r < 0.5:
        orden = R.choice(asistente_ordenes)
        modales = ""
        if R.random() < 0.2: modales = R.choice(asistente_modales)
        log = asistente_prompts[0].format(a=inicio,o=orden,m=modales)
    elif r < 0.6:
        preguntas = R.sample(asistente_preguntas,k=2)
        for i in range(len(preguntas)):
            e = R.choice(["humano","feriseo","corgo","exukente"])
            preguntas[i] = preguntas[i].format(n=R.choice(sustantivos_plural),p=R.choice(nombres[e]),s=R.choice(sustantivos))
        log = asistente_prompts[2].format(a=inicio, p=preguntas[0], p2=preguntas[1])
    else:
        pregunta = R.choice(asistente_preguntas)
        e = R.choice(["humano","feriseo","corgo","exukente"])
        pregunta = pregunta.format(n=R.choice(sustantivos_plural),p=R.choice(nombres[e]),s=R.choice(sustantivos))
        log = asistente_prompts[1].format(a=inicio,p=pregunta)
    return log

# Sobre Megamilky Productos
lista_productos = [
#    {"n":"","t":"aceite","p":0.0},
    {"n":"Aceite de Oliva Virgen Extra","t":"aceite","p":41.95},
    {"n":"Aceite de Girasol","t":"aceite","p":13.70},
    {"n":"Aceite de Furilim","t":"aceite","p":33.40},
    {"n":"Aceite de Wowoc","t":"aceite","p":29.95},
    {"n":"Vinagre de Manzana","t":"aceite","p":4.90},
#    {"n":"","t":"especia","p":0.0},
    {"n":"Orégano","t":"especia","p":1.90},
    {"n":"Pimienta Negra","t":"especia","p":2.65},
    {"n":"Vorelino","t":"especia","p":4.15},
#    {"n":"","t":"salsa","p":0.0},
    {"n":"Ketchup","t":"salsa","p":2.15},
    {"n":"Salsa Barbacoa","t":"salsa","p":2.45},
    {"n":"Peri Yelipoc","t":"salsa","p":2.95},
#    {"n":"","t":"bebida","p":0.0},
    {"n":"Agua Mineral","t":"bebida","p":2.50},
    {"n":"Cola Pupsi","t":"bebida","p":9.90},
    {"n":"Agua Ferisea","t":"bebida","p":0.95},
#    {"n":"","t":"aperitivo","p":0.0},
    {"n":"Nuez Natural","t":"aperitivo","p":3.15},
    {"n":"Almendra Natural","t":"aperitivo","p":3.60},
    {"n":"Cacahuete frito","t":"aperitivo","p":2.80},
    {"n":"Veviriv deshidratado","t":"aperitivo","p":3.50},
#    {"n":"","t":"frutas y verduras","p":0.0},
    {"n":"Manzana","t":"frutas y verduras","p":1.5},
    {"n":"Naranja","t":"frutas y verduras","p":1.3},
    {"n":"Patata","t":"frutas y verduras","p":1.5},
    {"n":"Lechuga","t":"frutas y verduras","p":2.9},
    {"n":"Limón","t":"frutas y verduras","p":1.3},
    {"n":"Pepino","t":"frutas y verduras","p":1.0},
    {"n":"Melón","t":"frutas y verduras","p":6.2},
    {"n":"Zidra","t":"frutas y verduras","p":2.1},
    {"n":"Ango","t":"frutas y verduras","p":1.9},
    {"n":"Safre","t":"frutas y verduras","p":1.7},
    {"n":"Pinia","t":"frutas y verduras","p":2.9},
#    {"n":"","t":"comida origen animal","p":0.0},
    {"n":"Huevos de Glup","t":"comida origen animal","p":3.0},
    {"n":"Sardina","t":"comida origen animal","p":4.25},
    {"n":"Pavo","t":"comida origen animal","p":10.75},
    {"n":"Grillo","t":"comida origen animal","p":1.5},
    {"n":"Creciyo","t":"comida origen animal","p":1.9},
    {"n":"Glup","t":"comida origen animal","p":7.95},
    {"n":"Carne de Pavo Impreso en Laboratorio","t":"comida origen animal","p":6.75},
#    {"n":"","t":"conservas","p":0.0},
    {"n":"Lata de Atún","t":"conservas","p":8.75},
    {"n":"Lata de Sardina","t":"conservas","p":3.95},
    {"n":"Bote de Guisantes","t":"conservas","p":2.2},
    {"n":"Lata de Teril","t":"conservas","p":1.95},
#    {"n":"","t":"cuidado personal y salud","p":0.0},
    {"n":"Champú","t":"cuidado personal y salud","p":5.85},
    {"n":"Acondicionador","t":"cuidado personal y salud","p":7.1},
    {"n":"Crema Hidratante para Feriseos","t":"cuidado personal y salud","p":8.45},
    {"n":"Sustancia Protectora para Exoesqueletos","t":"cuidado personal y salud","p":10.0},
#    {"n":"","t":"maquillaje","p":0.0},
    {"n":"Maquillaje Base","t":"maquillaje","p":8.30},
    {"n":"Pincel Iluminador","t":"maquillaje","p":5.50},
    {"n":"Pack Cremas Feriseas","t":"maquillaje","p":12.0},
    {"n":"Tinta Bioluminiscente Corporal para Exukentes","t":"maquillaje","p":9.95},
#    {"n":"","t":"para mascotas","p":0.0},
    {"n":"Pienso para Glup","t":"para mascotas","p":14.85},
    {"n":"Paté para Gato Premium Deluxe Baño en Oro Luxury (& Nnuckles)","t":"para mascotas","p":48.95},
    {"n":"Teril vivos para Trilinguinos","t":"para mascotas","p":3.50},
#    {"n":"","t":"comida preparada","p":0.0},
    {"n":"Pizza Congelada","t":"comida preparada","p":4.0},
    {"n":"Tortilla (sin cebolla) Congelada","t":"comida preparada","p":3.0},
    {"n":"Teriles Planchados","t":"comida preparada","p":4.5},
    {"n":"Empanadilla Sorpresa","t":"comida preparada","p":3.5},
    {"n":"Pollo Teriyaki","t":"comida preparada","p":6.0},
#    {"n":"","t":"moda","p":0.0},
    {"n":"Camiseta de Paul el Oso Polar","t":"moda","p":17.0},
    {"n":"Gorra de Gloria la Gallina","t":"moda","p":5.0},
    {"n":"Vestido Corto","t":"moda","p":16.0},
    {"n":"Botas Electromagnéticas","t":"moda","p":25.0},
    {"n":"Traje Espacial Humano (aire no incluido)","t":"moda","p":150.01},
    {"n":"Vel Feriseo","t":"moda","p":14.0},
    {"n":"Pantalón Cargo Corgo","t":"moda","p":9.0},
    {"n":"Uniforme Modular Anti-radiación (todas las especies)","t":"moda","p":52.0},
#    {"n":"","t":"hogar","p":0.0},
    {"n":"Colchón","t":"hogar","p":200.0},
    {"n":"Pack Hábitat Feriseo","t":"hogar","p":380.0},
    {"n":"Manta","t":"hogar","p":21.0},
    {"n":"Roca Natural para Corgo","t":"hogar","p":111.0},
    {"n":"Fregona","t":"hogar","p":6.50},
    {"n":"Escoba","t":"hogar","p":5.50},
    {"n":"Legía","t":"hogar","p":9.95},
    {"n":"Antimicrobiano, alguicida y desodorante 3 en 1 para piscinas","t":"hogar","p":7.98},
    {"n":"Alguicida Clasic","t":"hogar","p":7.15}, # 73
    {"n":"Alguicida Premium 99% puro","t":"hogar","p":10.95},
#    {"n":"","t":"electrodomésticos","p":0.0},
    {"n":"Lavadora","t":"electrodomésticos","p":400.0},
    {"n":"Microondas","t":"electrodomésticos","p":80.0},
    {"n":"Frigorífico","t":"electrodomésticos","p":250.0},
    {"n":"Lavavajillas","t":"electrodomésticos","p":400.0},
    {"n":"Placa de Inducción","t":"electrodomésticos","p":180.0},
    {"n":"Robot de Cocina (Adepto a cultura culinaria espacial)","t":"electrodomésticos","p":200.0},
    {"n":"Robot Aspiradora Polimorfo","t":"electrodomésticos","p":600.0},
#    {"n":"","t":"informática","p":0.0},
    {"n":"Pantalla LED","t":"informática","p":400.0},
    {"n":"Pantalla Holográfica","t":"informática","p":500.0},
    {"n":"Unidad de Computación Móvil (UCM)","t":"informática","p":1000.0},
    {"n":"Torre de Computación Gerwum","t":"informática","p":1200.0},
    {"n":"Funfriend (AI PDA)","t":"informática","p":300.0},
    {"n":"Asistente de Voz","t":"informática","p":30.0}, # 87
    {"n":"Biocomputadora","t":"informática","p":2000.0},
#    {"n":"","t":"juguetes","p":0.0},
    {"n":"Pack Legu (1000 piezas)","t":"juguetes","p":24.0},
    {"n":"Blem","t":"juguetes","p":12.0},
    {"n":"Monopolindre","t":"juguetes","p":20.0},
    {"n":"Dos (Juego de Cartas)","t":"juguetes","p":4.0},
    {"n":"Mini Multi Instrumento Musical (Se transforma en más de 100 instrumentos!)","t":"juguetes","p":80.0},
#    {"n":"","t":"papeleria y arte","p":0.0},
    {"n":"Libro 50 Luces de Gray","t":"papeleria y arte","p":50.0},
    {"n":"Libro Hurry Potery!","t":"papeleria y arte","p":16.0},
    {"n":"Pack Pinturas Dooburu","t":"papeleria y arte","p":10.5},
    {"n":"Tinta Dooburu","t":"papeleria y arte","p":8.95},
    {"n":"Latas Pintura en Spray Dooburu","t":"papeleria y arte","p":4.50}, # 98
    {"n":"Cuaderno Reescribible (8 TB)","t":"papeleria y arte","p":20.0},
    {"n":"Pegatinas Yellow Kitty","t":"papeleria y arte","p":3.20},
]

# Sobre MuricaGuns ArmasRegistradas 
lista_armas = [
    ["Bate de Baseball","ItWasInSelfDefenseISwear"],
    ["Navaja de Acero","Arma Blanca"],
    ["Zapinator (Irreal)","Arma Láser"],
    ["Bee Gun","Arma Artrópoda"],
    ["Luna","Arma Láser"],
    ["MembraneBuffer","Arma Acústica"],
    ["Lanza Ferisea","Arma Blanca"],
    ["Puño de Aleación","Equipamiento"],
    ["Gafas de proteccion","Equipamiento"],
    ["Peto Anti-estático","Equipamiento"],
    ["Disco Ball","Arma Láser"],
    ["Estoque","Arma Blanca"],
    ["Boomerang Teledirigido","Arma Inútil"],
    ["Pistola Látigo","Arma de contención"],
]

# Sobre Corgomatic
posibles_cambios_vehiculos = [ # Ordenado según la probabilidad de aparación
    "revisión general",
    "cambio de aceite",
    "cambio del líquido de freno",
    "cambio de neumáticos frontales",
    "cambio de neumáticos traseros",
    "actualización de Sistema Operativo",
    "capa de pintura color {c}",
    "reparación de lunas traseras",
    "reparación de lunas frontales",
    "reparación de lunas laterales",
    "cambio de llantas",
    "revisión de reactores",
    "cambio de crioslina para reactores",
    "revisión del Space-Hopper",
    "puesta a punto para viaje espacial (certificación EEL)",
    "cambio de carrocería",
    "pintura de diseño (artista feriseo)",
]

def mod_vehiculo_aleatoria():
    n = len(posibles_cambios_vehiculos)
    idx = math.ceil(R.betavariate(0.7,2)*(n-1))
    mod = posibles_cambios_vehiculos[idx]
    if "{c}" in mod:
        mod = mod.format(c=R.choice(colores_vehiculos))
    return mod

def gen_cambios_vehiculo(n):
    cambios = mod_vehiculo_aleatoria()
    for i in range(1,n):
        cambios += ", "+mod_vehiculo_aleatoria()
    return cambios

# Sobre Pauls Pizzeria
pp_catalogo = {
    "servicios y equipo":[
        {"PacoFiestas Co":[
            "Carrito de Globos",
            "Dispensadora de Bolas de Chicle",
            "Dispensador de Limonada Payasín Limoncín",
            "Luces de Discoteca forma Pizza",
            "Luces de Neón para Escenario",
            "Cortinas de Escenario",
        ]},
        {"Metal as Duck":[
            "Puertas de alta seguridad",
            "Sistema de Aire Acondicionado",
            "Señal de Tráfico novedosa",
        ]},
        {"Sansitarios":[
            "Estación de Médica",
        ]},
        {"Electrolatinos":[
            "Equipo de Altavoces Deluxe",
        ]},
    ],
    "atracción":[
        {"DangurStrangur":[
            "Máquina recreativa Antonieta y su Motocicleta",
            "Máquina recreativa Jacinto y los Fantasmas en el Laberinto",
            "Escaleras y Serpientes (Versión Realista)",
        ]},
        {"Divertiños":[
            "Cadete Caramelo",
            "Piscina de Bolas",
            "Torre de Bolas",
            "Castillo de Bolas",
            "Lago de Patitos",
        ]},
        {"Robles Nobles":[
            "Escenario",
        ]},
    ],
    "animatrónico":[
        {"Corgomatic":[
            "Hernesto el Hamster", 
            "Lucas el Lobo", 
            "Gloria la Gallina",
            "Paul el oso Polar",
            "Connor el Connejo",
        ]},
        {"Anima-Pixas SL":[
            "Crazy Frog", # Easter egg xD
            "Alex el León", # Easter egg xD
            "El oso Yoga", # Easter egg xD
            "Cerdito Valiente", # Easter egg xD
        ]},
        {"Cutrónicos SA":[
            "Bob el Cubo",
            "Señor Abracitos",
        ]},
    ],
    "consumible":[
        {"PacoFiestas Co":[
            "Vasos y Platos de Papel",
            "Vasos y Platos de Colores",
            "SET DE FIESTAAAAAAS",
            "Set de Fiestas de NEON Deluxe",
        ]}
    ],
}

# Generales
def fecha_aleatoria():
    year = R.randint(2223,2224)
    month = 1
    day = 1
    if year == 2223:
        month = R.randint(4,12)
        day = R.randint(1,30)
    else:
        month = R.randint(1,4); day = 1
        if month == 2: day = R.randint(1,28)
        else: day = R.randint(1,30)
    return "-".join([str(year),str(month),str(day)])

def fecha_por_indice(i):
    i += 90 # Empieza el mes 4 del 2223
    y = 2223
    if i >= 360: y = 2224
    m = (math.floor(i/30) % 12) +1
    d = (i % 30) +1
    if m == 2: d = min(d,28)
    return "-".join([str(y),str(m),str(d)])

def hora_aleatoria():
    horas = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]
    hora = str(R.choices(horas,k=1,weights=[2,1,0,0,0,1,3,8,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,6])[0])
    hora += ":" + str(R.randint(0,59)) + ":" + str(R.randint(0,59)) # minutos y segundos
    return hora

def scramble_ids(table,exclude=[]):
    n = len(table)
    R.shuffle(table)
    
    if len(exclude) == 0:
        for i in range(n):
            table[i][0] = i # Las IDs (claves primarias) están siempre en la primera columna de la tabla.
    else:
        id = 0
        for i in range(n):
            if table[i][0] in exclude: continue
            table[i][0] = id # Las IDs (claves primarias) están siempre en la primera columna de la tabla.
            id += 1
            while id in exclude: id += 1


# 2. Table data generation
write_header = True
def guardar_tabla(path,data,header,rows_per_file=3000):
    stored = 0
    n = len(data)
    file_num = 0
    while stored < n:
        with open(path+str(file_num)+".csv", mode='w',encoding='utf-8') as file:
            if write_header: file.write(header+'\n')
            ini = stored
            max_n = min(n,ini+rows_per_file)
            for i in range(ini,max_n):
                file.write(';'.join(map(str,data[i])) + '\n')
            stored = max_n
        file_num += 1
    print("Finished writing table",path,"in",str(file_num),"files")

def generar_como_sql(table_name,header,array):
    content = "INSERT INTO `"+table_name+"` ("
    content+= ('`'+header[0]+"`")
    for i in range(1,len(header)):
        content+= (',`'+header[i]+"`")
    content += ") VALUES\n"

    if len(array) == 0: print(array)
    for i in range(len(array)):
        content += "("
        row = array[i]
        for c in row:
            if isinstance(c,numbers.Number): content += str(c)
            elif isinstance(c,list): print(c)
            else: content += '"'+c+'"'
            content += ","
        content = re.sub(',$',')',content)
        content += ",\n"
    content = re.sub(',\n$',';\n\n',content)
    guardar_sql(rel_path_to_file,content)
    print("Guardando contenido de la tabla "+table_name+" en formato SQL. ("+str(len(array))+" rows)")
    return content

def guardar_sql(path,content,m='a'):
    with open(path, mode=m,encoding='utf-8') as file:
        file.write(content)


# Dif 1
ciudadanos = []
def guardar_ciudadanos():
    path = "CSE builds/Backend DB Exports/tabla_ciudadanos"
    header = "dni;nombre;apellidos;edad;colorPelo;altura;especie"
    guardar_tabla(path,ciudadanos,header)
def generar_ciudadanos():
    for i in range(800):
        ciudadanos.append(gen_ciudadano(i,30,25,30,20))

vehiculos = []
def guardar_vehiculos():
    path = "CSE builds/Backend DB Exports/tabla_vehiculos"
    header = "matricula;idTitular;marca;color"
    guardar_tabla(path,vehiculos,header)
def generar_vehiculos():
    letter = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    n = len(ciudadanos)
    v = 0
    for i in range(n):
        if R.randint(1,2) != 1: continue
        titular = i
        if ciudadanos[titular][3] < 18: continue # Los menores no pueden tener coche
        mat = f"{v:04d}"+''.join(map(str,R.choices(letter,k=3)))
        marca = R.choice(marcas_vehiculos)
        if ciudadanos[titular][6] == 'Exukente' and R.randrange(0,5) == 0: marca = "LLada"
        color = R.choice(colores_vehiculos)
        
        row = [mat,titular,marca,color]
        vehiculos.append(row)
        v += 1
        if v > 9999: v = 0

viviendas = []
def guardar_viviendas():
    path = "CSE builds/Backend DB Exports/tabla_viviendas"
    header = "id;direccion;titular;esPiso"
    guardar_tabla(path,viviendas,header)
def generar_viviendas():
    id = 0
    for persona in ciudadanos:
        row = crear_vivienda_segun_ciudadano(id,persona)
        if row == []: continue
        viviendas.append(row)
        id += 1

alojadoEn = []
def guardar_alojadoEn():
    path = "CSE builds/Backend DB Exports/tabla_alojadoEn"
    header = "vivienda;ciudadano"
    guardar_tabla(path,alojadoEn,header)
def generar_alojadoEn():
    gente_asignada = [False]*len(ciudadanos)
    # 1º Los titulares de las casas
    for v in viviendas:
        ciudadano = v[2]
        vivienda = v[0]
        row = [vivienda,ciudadano]
        gente_asignada[ciudadano] = True
        alojadoEn.append(row)
        # Cálcular cúantos hijos puede tener el titular
        espacio_hijos = 1
        p = R.random()
        for i in range(2,5):
            if p < 1/i: 
                espacio_hijos += 1
        apellido = ciudadanos[ciudadano][2]
        # Buscar jóvenes con mismo apellido que el titular
        for c in ciudadanos:
            if espacio_hijos <= 0: break
            id = c[0]
            if gente_asignada[id]: continue
            edad = c[3]
            if edad > 24: continue
            otro_apellido = c[2]
            if otro_apellido == apellido:
                gente_asignada[id] = True
                alojadoEn.append([vivienda,id])
                espacio_hijos -= 1

rutas = []
def guardar_rutas():
    path = "CSE builds/Backend DB Exports/tabla_rutas"
    header = "matricula;zonaOrigen;zonaDestino;distanciaViaje;fecha"
    guardar_tabla(path,rutas,header,12000)
def generar_rutas():
    for v in vehiculos:
        matricula = v[0]
        titular = v[1]
        if titular >= len(ciudadanos): continue
        especie = ciudadanos[titular]
        viajes = R.randint(10,50)
        for t in range(viajes):
            distrito_origen = distrito_aleatorio(especie)
            distrito_destino = distrito_aleatorio(especie)
            zona_origen = localizacion_aleatoria(distrito_origen)
            zona_destino = localizacion_aleatoria(distrito_destino)
            while zona_destino == zona_origen: # Don't make dumb travels form-to the same location
                zona_destino = localizacion_aleatoria(distrito_destino)

            origen = zona_origen["nombre"]; p_o = zona_origen["pos"]
            destino = zona_destino["nombre"]; p_d = zona_destino["pos"]
            distancia = calcular_distancia_viaje(p_o,p_d)
            fecha = fecha_aleatoria()
            row = [matricula, origen, destino, distancia, fecha]
            rutas.append(row)
            # Viaje de vuelta a su distrito
            if localizaciones[distrito_origen]["distrito"] == especie and R.random() < 0.5:
                row = [matricula, destino, origen, distancia, fecha]
                rutas.append(row)

correos = []
persona_correo = {}
def guardar_correos():
    path = "CSE builds/Backend DB Exports/tabla_correos"
    header = "id;fecha;emisor;destinatario;asunto;contenido"
    guardar_tabla(path,correos,header)
def generar_correos():
    # Se generan direcciones de correo para todos los ciudadanos
    for c in ciudadanos: persona_correo[c[0]] = direccion_correo_aleatorio(c)
    id = 0
    # Los correo basura (anuncios y timos)
    for p in plantillas_correo_relleno:
        n_objetivos = R.randint(250,350)
        elegidos = R.sample(ciudadanos,k=n_objetivos)
        for c in elegidos:
            if c[3] < R.randint(12,18): continue
            emisor = p["emisor"]
            asunto = p["asunto"]
            contenido = p["contenido"].format(n=c[1])
            destinatario = persona_correo[c[0]]
            # Repeat up to 6 times with different dates
            t = 1
            r = R.randint(1,6)/6
            while r <= 1/t:
                fecha = fecha_aleatoria()
                row = [id,fecha,emisor,destinatario,asunto,contenido]
                correos.append(row)
                id += 1
                t += 1
    # Los correos entre personas reales
    asuntos = [["Fotos vacaciones","Holaaaa {p}, quería preguntarte si no te importa compartir conmigo las fotos de nuestras últimas vacaciones"],
               ["Ayudita","Hola mama, he gomitado, por favor ven a recogerme."],
               ["Regalito","Te he compartido a través de la memoria en la nube ese juego que conseguí de forma completamente legal hehe"],
               ["Papeles arreglados","Hola {p}, ya he solucionado el problema que tenías con los papeles, ya sólo tienes que ir tu a firmar una cosa más y listo. Te paso adjunto los documentos y todo lo necesario."],
    ]
    for c in ciudadanos:
        other_c = R.choice(ciudadanos)
        emisor = persona_correo[c[0]]
        destinatario = persona_correo[other_c[0]]
        fecha = fecha_aleatoria()
        a = R.choice(asuntos)
        asunto = a[0]
        contenido = a[1].format(p=other_c[1])
        row = [id,fecha,emisor,destinatario,asunto,contenido]
        correos.append(row)
        id += 1

pingBusquedas = []
def guardar_pingBusquedas():
    path = "CSE builds/Backend DB Exports/tabla_pingBusquedas"
    header = "correo;busqueda;fecha;ip"
    guardar_tabla(path,pingBusquedas,header,5000)
def generar_pingBusquedas():
    n = 4000
    personas = R.choices(ciudadanos,k=n)
    asignar_ips_a_ciudadanos()
    for i in range(n):
        c = personas[i]
        dni = c[0]
        dir_correo = persona_correo[dni]
        ip_list = ciudadano_ip.get(dni)
        if ip_list == None: continue
        ip = R.choice(ip_list) # Una ip aleatoria en la que frecuenta el ciudadano seleccionado
        fecha = fecha_aleatoria()
        busqueda = busqueda_aleatoria()
        row = [dir_correo,busqueda,fecha,ip]
        pingBusquedas.append(row)

transbordos = []
def guardar_transbordos():
    path = "CSE builds/Backend DB Exports/tabla_transbordos"
    header = "id;numPuerto;fechaLlegada;entidadSolicitante"
    guardar_tabla(path,transbordos,header)
def generar_transbordos():
    id = 0
    for entidad in entidades_transbordos:
        for i in range(R.randrange(24,36)):
            numPuerto = R.randint(1,32)
            llegada = fecha_aleatoria()
            row = [id,numPuerto,llegada,entidad]
            transbordos.append(row)
            id+=1

# Dif 2
asistente_voz = []
def guardar_asistente_voz():
    path = "CSE builds/Backend DB Exports/tabla_asistente_voz"
    header = "id;dniPpropietario;fecha;log"
    guardar_tabla(path,asistente_voz,header,8000) # Se pueden poner más filas por archivo pero es dificil bajar de los 2 archivos...
def generar_asistente_voz():
    poseen_asistente = R.sample(ciudadanos,k=min(len(ciudadanos),R.randint(200,300)))
    id = 0
    for i in range(365):
        fecha = fecha_por_indice(i)
        n = R.randrange(16,50)
        for j in range(n):
            hora = hora_aleatoria()
            datetime = fecha+" "+hora
            c = R.choice(poseen_asistente)
            dni = c[0]
            log = gen_log_asistente()
            row = [id,dni,datetime,log]
            asistente_voz.append(row)
            id += 1

megamilky_productos = []
def guardar_megamilky_productos():
    path = "CSE builds/Backend DB Exports/tabla_megamilky_productos"
    header = "id;nombre;precio;tipo;stock"
    guardar_tabla(path,megamilky_productos,header)
def generar_megamilky_productos():
    for i in range(len(lista_productos)):
        prod = lista_productos[i]
        row = [i,prod["n"],prod["p"],prod["t"],R.randrange(10,100)]
        megamilky_productos.append(row)

megamilky_ventas = []
def guardar_megamilky_ventas():
    path = "CSE builds/Backend DB Exports/tabla_megamilky_ventas"
    header = "id;idCliente;fecha;idProducto;cantidad"
    guardar_tabla(path,megamilky_ventas,header,14000)
def generar_megamilky_ventas():
    n_fechas = 378
    id = 0
    for i in range(n_fechas):
        fecha = fecha_por_indice(i)
        clientes = R.sample(ciudadanos,k=R.randint(25,40))
        for c in clientes:
            dni = c[0]
            productos = R.sample(megamilky_productos,k=R.randint(1,3))
            for p in productos:
                id_prod = p[0]
                cantidad = math.ceil(R.betavariate(1.3,4) * 5)
                if "lguicida" in p[1]:
                    if c[6] != "feriseo":
                        if R.random() > 0.1: continue
                    else: cantidad += 2
                if cantidad == 0: cantidad = 1
                row = [id,dni,fecha,id_prod,cantidad]
                megamilky_ventas.append(row)
                id += 1

muricaGuns_armasRegistradas = []
def guardar_muricaGuns_armasRegistradas():
    path = "CSE builds/Backend DB Exports/tabla_muricaGuns_armasRegistradas"
    header = "numSerie;dni;producto;tipo"
    guardar_tabla(path,muricaGuns_armasRegistradas,header,26000)
def generar_muricaGuns_armasRegistradas():
    for a in lista_armas:
        prod = a[0]
        tipo = a[1]
        n = R.randrange(5,20)
        for i in range(n):
            numSerie = R.randrange(0,4294967295) # 4 byte int only pls
            # Busca 3 candidatos y escoge el más viejo
            candidatos = R.sample(ciudadanos,k=3)
            comprador = candidatos[0]
            for p in range(1,len(candidatos)):
                c = candidatos[p]
                if c[3] > comprador[3]:
                    comprador = c
            dni = comprador[0]
            row = [numSerie,dni,prod,tipo]
            muricaGuns_armasRegistradas.append(row)
            
corgomatic = []
def guardar_corgomatic():
    path = "CSE builds/Backend DB Exports/tabla_corgomatic"
    header = "matricula;fecha;cambios"
    guardar_tabla(path,corgomatic,header,26000)
def generar_corgomatic():
    n = R.randrange(1000,1500)
    for i in range(n):
        mat = R.choice(vehiculos)[0]
        fecha = fecha_aleatoria()
        n_cambios = 1
        p = R.random()
        if p < 0.25: n_cambios += 1
        if p < 0.05: n_cambios += 1
        if p < 0.005: n_cambios += 1
        cambios = gen_cambios_vehiculo(n_cambios)
        row = [mat,fecha,cambios]
        corgomatic.append(row)

# Dif 4
rinconDelTurro_Reservas = []
def guardar_rinconDelTurro_Reservas():
    path = "CSE builds/Backend DB Exports/tabla_rinconDelTurro_Reservas"
    header = "id;comensales;fecha"
    guardar_tabla(path,rinconDelTurro_Reservas,header,10000)
def generar_rinconDelTurro_Reservas():
    for i in range(0,350):
        fin_semana = i%7 <= 1
        mesas = R.randrange(4,10)
        if fin_semana: mesas *= 2
        for c in range(mesas):
            comensales = R.choices([1,2,3,4,5,6],k=1,weights=[10,30,23,30,25,30])[0]
            datetime = fecha_por_indice(i)+" "+str(R.randint(11,23))+":"+str(R.randint(0,59))+":00"
            rinconDelTurro_Reservas.append([0,comensales,datetime])

rinconDelTurro_Mesas = []
def guardar_rinconDelTurro_Mesas():
    path = "CSE builds/Backend DB Exports/tabla_rinconDelTurro_mesas"
    header = "idReserva;dniCliente"
    guardar_tabla(path,rinconDelTurro_Mesas,header,26000)
def generar_rinconDelTurro_Mesas():
    n = len(rinconDelTurro_Reservas)
    for r in range(n):
        reserva = rinconDelTurro_Reservas[r][0]
        comensales = rinconDelTurro_Reservas[r][1]
        clientes = R.sample(ciudadanos,k=comensales) 
        # Podría currarmelo para meter familias pero es mucho trabajo
        # para algo que prácticamente nadie se va a dar cuenta.
        for c in range(comensales):
            dni = clientes[c][0]
            rinconDelTurro_Mesas.append([reserva,dni])

transbordos_Empleados = []
def guardar_transbordos_Empleados():
    path = "CSE builds/Backend DB Exports/tabla_transbordos_empleados"
    header = "idTransbordo;dniEmpleado"
    guardar_tabla(path,transbordos_Empleados,header,10000)
def generar_transbordos_Empleados():
    # Obteniendo empleados
    trabajadores_fijos = []
    while len(trabajadores_fijos) <= 15:
        candidatos = R.sample(ciudadanos,k=30)
        for c in candidatos:
            if c[3] >= 16: # Puede trabajar legalmente
                trabajadores_fijos.append(c[0])
    # Asignando empleados
    for i in range(len(transbordos)):
        n_involucrados = R.randint(1,3)
        asignados = R.sample(trabajadores_fijos,k=n_involucrados)
        id_transbordo = transbordos[i][0]
        for dni in asignados:
            transbordos_Empleados.append([id_transbordo,dni])

paulsPizzeria_Inventario = []
def guardar_paulsPizzeria_Inventario():
    path = "CSE builds/Backend DB Exports/tabla_paulsPizzeria_inventario"
    header = "id;objeto;tipo;proveedor;cantidad"
    guardar_tabla(path,paulsPizzeria_Inventario,header,10000)
def generar_paulsPizzeria_Inventario():
    for tipo in pp_catalogo:
        unico = tipo == "animatrónico"
        proveedores = pp_catalogo[tipo]
        for i in range(len(proveedores)):
            for proveedor in proveedores[i]:
                listado = proveedores[i][proveedor]
                for objeto in listado:
                    cantidad = 1
                    if not unico: cantidad = R.randint(2,5)
                    paulsPizzeria_Inventario.append([0,objeto,tipo,proveedor,cantidad])

grabacionRestaurante = []
def guardar_grabacionRestaurante():
    path = "CSE builds/Backend DB Exports/tabla_grabacionRestaurante"
    header = "transcripcion;hora"
    guardar_tabla(path,grabacionRestaurante,header)
def generar_grabacionRestaurante():
    # Nada aleatorio, se meten los datos directamente y ya esta.
    global grabacionRestaurante
    grabacionRestaurante = [
        ["Oye ¿Y tú que vas a pedir?","2224-04-27 14:21:06"], # 2 humanas, reserva para las 14
        ["No se... ojalá indicasen en el menú si el tipo de comida es vegetal o animal.","2224-04-27 14:21:12"],
        ["Ah es verdad, eras vegana. No sé mucho del idioma Corgo, y mi implante traductor tampoco está sacando mucho en claro. Siempre le podemos preguntar al camarero supongo.","2224-04-27 14:21:20"],
        ["¿Vienen a la mesa como en nuestra cultura?","2224-04-27 14:21:29"],
        ["¿Supongo? Osea, aunque sea un negocio familiar, creo que a lo largo de estos años se han ido mezclando las culturas entre especies.","2224-04-27 14:21:32"],
        ["Ah ¡Qué fascinante!","2224-04-27 14:21:41"],
        ["Sí, la verdad es que la vida en el EEL es muy diferente a la vida en la tierra. Es un poco como la diferencia entre vivir en pueblo y en ciudad, solo que más espacial.","2224-04-27 14:21:45"],
        ["Espero que me guste entonces... Al final vine aquí sobretodo por trabajo. ¡Ah mira! Ese debe ser el camarero","2224-04-27 14:21:55"],
        ["Soy camarera, señorita. Pero no pasa nada, ya estamos acostumbradas a que los humanos no sepan distinguir el género de los Corgos.","2224-04-27 14:22:02"],
        ["¡Uy disculpe! ¡No era mi intención!","2224-04-27 14:22:05"],
        ["No pasa nada. ¿Qué van a pedir?","2224-04-27 14:22:11"],
        ["Pues...","2224-04-27 14:22:15"],
        ["[ininteligible]","2224-04-27 14:22:16"], # 2 Corgos (da igual el género), reserva para las 15 (uno se llama Nadalor)
        ["Ah, me alegra que tu familia tenga actualmente una mejor calidad de vida en Lorwon.","2224-04-27 14:58:53"],
        ["Nadalor, me agrada tu comentario. He de añadir que todo ha sido gracias a esta empresa que hemos formado.","2224-04-27 14:59:00"],
        ["Desde luego, fue un gran plan aprovechar la ola emergente de empleo en el EEL.","2224-04-27 14:59:08"],
        ["Ya conoces el dicho, (una expresión Corgo difícil de traducir que relaciona el ciclo de vida de un animal autóctono con la economía)","2224-04-27 14:59:14"],
        ["(Se ríe en Corgo), siempre es así.","2224-04-27 14:59:19"],
        ["¿Me pueden decir nombre y hora de la reserva, caballeros?","2224-04-27 14:59:23"],
        ["Por supuesto, a nombre de Nadalor, la reserva la hicimos para las 15:00","2224-04-27 14:59:26"],
        ["[ininteligible]","2224-04-27 14:59:28"],
        ["¿Por qué hemos elegido este sitio?","2224-04-27 22:04:26"], # 2 humanos y un exukente, reserva para las 22
        ["Sencillamente porque tienen el mejor Kaluc al Wowoc. Es... una receta de familia según me han contado.","2224-04-27 22:04:29"],
        ["Ah interesante ¿Y nada más? Te recuerdo que me debes algo, y una cena no va a ser suficiente para pagarlo.","2224-04-27 22:04:34"],
        ["Nooo claro que no, relaja esas pinzas. Todo a su debido tiempo, primero disfruta de la cena, luego pediremos el postre. Eso sí será suficiente para cerrar el trato.","2224-04-27 22:04:42"],
        ["No me gustan tus juegos, humano. Ni me gusta que le digas pinzas a mis mandíbulas. Además, valoro mi tiempo, no me hagas perdelo por un poco de teatrillo.","2224-04-27 22:04:51"],
        ["Confía. Más tarde pídele al camarero un poco de Limón y Sal. Irá al almacén, donde pone sólo personal corgo. Tu pedirá que lo sigas.","2224-04-27 22:04:59"],
        ["¿Limón y Sal? ¿Especias humanas en un restaurante familiar Corgo?","2224-04-27 22:05:04"],
        ["Es lo que tiene la universalización... Se mezclan culturas, se intercambian unas cosas con otras...","2224-04-27 22:05:09"],
        ["Muy bien, muy bien. ¿Y vosotros qué?","2224-04-27 22:05:16"],
        ["A nosotros por degracia no nos dejan entrar. Sólo Corgos y Exukentes...","2224-04-27 22:05:19"],
        ["[ininteligible]","2224-04-27 22:05:23"],
        ["¿Este es el restaurante de tu familia?","2224-04-27 23:09:15"], # Meca y Pepuv xD (no tienen reserva)
        ["¡Correcto Pepuv! Mis padres montaron el negocio en nuestro planeta natal, pero decidieron ir a lo grande y trasladarse aquí al EEL.","2224-04-27 23:09:18"],
        ["Wow, la verdad es que es sorprendente... Pensar que ahora vuestro negocio es conocido en toda la galaxia... debes de estar orgullosa.","2224-04-27 23:09:26"],
        ["¡Tú lo has dicho!","2224-04-27 23:09:31"],
        ["¿Oye y no tenemos que pedir mesa o algo?","2224-04-27 23:09:35"],
        ["¡No hace falta que hagamos reserva, soy su hija!","2224-04-27 23:09:38"],
        ["Ah ya veo...","2224-04-27 23:09:41"],
        ["Vaya, todo lo del menú suena muy rico. Ya que este sitio es de tus padres... ¿Qué me recomiendas? Seguro que sabes cuáles son los mejores platos","2224-04-27 23:09:45"],
        ["Ja ja ja. Verás, este plato del menú no se lo pide muchos clientes, pero de pequeña siempre fue mi comida favorita cuando todavía vivía en mi planeta.","2224-04-27 23:09:53"],
        ["Ah... muy bien... ¡Qué intriga! De pequeña ¿eh?","2224-04-27 23:10:01"],
        ["Oye Meca... lo cierto es que nunca ha salido con una mujer que mida 2 veces mi tamaño, ni 3... ni 4... Osea, quiero decir...","2224-04-27 23:10:08"],
        ["Ah, no te preocupes por eso Pepuv, no me importa que seas bajito. Pienso que eres adorable y muy listo, y eso es lo que me importa.","2224-04-27 23:10:16"],
        ["Listo ¿eh?... jejeh","2224-04-27 23:10:21"],
        ["Ja ja ja, también me hacen gracia tus expresiones.","2224-04-27 23:10:25"],
        ["¡Eh Meca! ¡Qué hace ese Feriseo ahí!","2224-04-27 23:11:07"],
        ["¡Estoy saliendo con él papá!","2224-04-27 23:11:12"],
        ["¡¿Qué?!","2224-04-27 23:11:15"],
        ["¡¡¡CARIÑO ESTAS NO SON HORAS DE GRITAR!!!","2224-04-27 23:11:18"],
        ["(Suspiro) Esos eran mi padre y mi madre... A mi padre no le hace mucha gracia que tenga parejas que no sean Corgos.","2224-04-27 23:11:23"],
        ["Ah... qué bien, para nada dan miedo...","2224-04-27 23:11:29"],
        ["Buenas noches Meca, buenas noches señor... ?","2224-04-27 23:11:34"],
        ["Eh...","2224-04-27 23:11:37"],
        ["Pepuv, se llama Pepuv.","2224-04-27 23:11:38"],
        ["Tranquilo Pepuv no le hagas caso a mi marido, íbamos a cerrar pronto, pero parece ser una noche especial para mi hija.","2224-04-27 23:11:41"],
        ["Ah... espero no ser una molestia...","2224-04-27 23:11:48"],
        ["Para nada. Además, si te sirve de consuelo yo cocinaré. Puedes estar tranquilo, mi marido no pondrá veneno ni nada parecido en tu plato. Ja ja ja ja","2224-04-27 23:11:52"],
        ["[ininteligible]","2224-04-27 23:12:04"],
    ]


# SPECIFIC CASE RELATED ROWS REMAINING
# TODO:
# Están hechos hasta p2d5 (quitando el caso secundario de dificultad 3 que es inexistente ahora mismo)

# 3. Complete generation in one go
R.seed(27272727) # Se fija la semilla para no tener que importar todas las tablas si se hace algun cambio en una tabla sólamente
# Dif 1 tables:
# CIUDADANOS
generar_ciudadanos()
ciudadanos_fijos = []
# p1d1
ciudadanos.append([0,"Menganito","Menganez",24,"pelirrojo",1.96,"humano"])
# p2d1
ciudadanos.append([0,"lukanus","krakaro",39,"azul",1.51,"exukente"])
ciudadanos.append([0,"verik","krakaro",21,"azul",1.55,"exukente"])
p2d1_sol = [0,"luvkrav","krakaro",23,"azul",1.49,"exukente"]
ciudadanos.append(p2d1_sol)
# pEd1
pEd1_hacker = gen_exukente(0)
pEd1_hacker[1] = "arkimov"; pEd1_hacker[2] = "verakova"
ciudadanos.append(pEd1_hacker)
pEd1_victima = gen_humano(0)
pEd1_victima[1] = "juanito"; pEd1_victima[2] = "javanero"
ciudadanos.append(pEd1_victima)
# p1d2
p1d2_sol = [0,"miguel","yakson",36,"castaño",1.79,"humano"]
ciudadanos.append(p1d2_sol)
# p2d2
p2d2_sol = [0,"nadalor","wombo",54,"blanco",2.11,"corgo"]
ciudadanos.append(p2d2_sol) # Poli corgo corrupta
ciudadanos.append([0,"karalina","chinchi",20,"dorado",1.41,"exukente"]) # Novia del solicitante del caso
#pEd2
pEd2_sol = [0,"vokef","blattoke",29,"azul",1.54,"exukente"]
ciudadanos.append(pEd2_sol)
decoy = []
for i in range(len(ciudadanos)):
    if ciudadanos[i][6] == "feriseo":
        decoy = ciudadanos[i]
# s1d2
s1d2_exu = [0,"kev","pouliya",26,"azul",1.49,"exukente"]
ciudadanos.append(s1d2_exu)
# s2d2
s2d2_humano1 = gen_humano(0)
s2d2_humano2 = gen_humano(0)
s2d2_humano3 = gen_humano(0)
ciudadanos.append(s2d2_humano1)
ciudadanos.append(s2d2_humano2)
ciudadanos.append(s2d2_humano3)
# s3d2
ciudadanos_fijos.append(618)
s3d2_feri = gen_feriseo(618)
s3d2_exu = gen_exukente(0)
ciudadanos.append(s3d2_feri)
ciudadanos.append(s3d2_exu)
# p1d3
p1d3_fam1 = [0,"jalfonsés","varetta",54,"castaño",1.81,"humano"]
p1d3_fam2 = [0,"remora","varetta",52,"castaño",1.59,"humano"]
p1d3_fam3 = [0,"pepe","varetta",28,"castaño",1.80,"humano"]
ciudadanos.append(p1d3_fam1)
ciudadanos.append(p1d3_fam2)
ciudadanos.append(p1d3_fam3)
vanessavaretta = [0,"vanessa","varetta",23,"castaño",1.62,"humano"]
p1d3_sol = [0,"hernesto","galeano",26,"rubio",1.85,"humano"]
ciudadanos.append(vanessavaretta)
ciudadanos.append(p1d3_sol)
# p2d4
p2d4_h1 = gen_humano(0)
p2d4_h2 = gen_humano(0)
ciudadanos.append(p2d4_h1)
ciudadanos.append(p2d4_h2)
# pEd4
pEd4_decoy_14_h1 = gen_humano(0); pEd4_decoy_14_h1[3] = 26
pEd4_decoy_14_h2 = gen_humano(0); pEd4_decoy_14_h2[3] = 27
ciudadanos.append(pEd4_decoy_14_h1)
ciudadanos.append(pEd4_decoy_14_h2)
pEd4_decoy_15_c1 = gen_corgo(0); pEd4_decoy_15_c1[3] = 39; pEd4_decoy_15_c1[1] = "nadalor"
pEd4_decoy_15_c2 = gen_corgo(0); pEd4_decoy_15_c2[3] = 41
ciudadanos.append(pEd4_decoy_15_c1)
ciudadanos.append(pEd4_decoy_15_c2)
pEd4_h1 = gen_humano(0); pEd4_h1[3] = 47
pEd4_h2 = gen_humano(0); pEd4_h2[3] = 34
pEd4_ex = gen_exukente(0); pEd4_ex[3] = 28
ciudadanos.append(pEd4_h1)
ciudadanos.append(pEd4_h2)
ciudadanos.append(pEd4_ex)
# p2d5
p2d5_ex = gen_exukente(0)
# pEd5
pEd5_vikal = [0,"vikal","kontrov",51,"azul",1.6,"exukente"]
pEd5_hac = [0,"Tomás","Timado",68,"negro",1.74,"humano"]
# easter eggs
ciudadanos.append([0,"akizetesche","qou jokzi",999,"???",1.8,"obesk"]) # Akizet (Corru Observer)
scramble_ids(ciudadanos,ciudadanos_fijos)

# VEHICULOS
generar_vehiculos()
# p2d1
vehiculos.append(["0415KRI",p2d1_sol[0],"Llada","negro"])
# pEd2
vehiculos.append(["0251VAK",pEd2_sol[0],"BWM","carmesí"])
# s1d2
s1d2_vehiculo = ["0312XIO",s1d2_exu[0],"Llada","morado tinto"]
vehiculos.append(s1d2_vehiculo)
# p1d4
p1d4_vehiculo1 = ["0274CJH",R.choice(ciudadanos)[0],"Renaul","negro brillante"]
p1d4_vehiculo2 = ["0682ACY",R.choice(ciudadanos)[0],"Llada","lobo gris"]
p1d4_vehiculo3 = ["0285PRN",R.choice(ciudadanos)[0],"Supraru","negro medianoche"]
p1d4_vehiculo4 = ["0102MVM",R.choice(ciudadanos)[0],"Citrïco","blanco roto"]
p1d4_vehiculo5 = ["0427QEG",R.choice(ciudadanos)[0],"Llada","gris grafito"]
vehiculos.append(p1d4_vehiculo1)
vehiculos.append(p1d4_vehiculo2)
vehiculos.append(p1d4_vehiculo3)
vehiculos.append(p1d4_vehiculo4)
vehiculos.append(p1d4_vehiculo5)
# "0274CJH","0682ACY","0285PRN","0102MVM","0427QEG"
# p2d5
p2d5_vehiculo = ["0842SBW",p2d5_ex[0],"Llada","verde cocodrilo"]
vehiculos.append(p2d5_vehiculo)
# pEd5
pEd5_vikal_v = ["0411UCK",pEd5_vikal[0],"Renaul","negro medianoche"]
pEd5_hac_v = ["0129ZWB",pEd5_hac[0],"Hamburghini","amarillo brillante"]
# Easter Eggs
vehiculos.append(["LMQ 95",9595,"McQueen","rojo"])
R.shuffle(vehiculos)

# VIVIENDAS
generar_viviendas()
# s3d2
s3d2_vivienda = [0, "Calle Tripaloski n2 9º",s3d2_exu[0], 1]
viviendas.append(s3d2_vivienda)
viviendas.append([0, "Calle Korumiv n1 9º",138, 1]) # Decoy
viviendas.append([0, "Calle Korumiv n2 9º",319, 1]) # Decoy
# p1d3
p1d3_vivienda = [] 
while p1d3_vivienda == []: p1d3_vivienda = crear_vivienda_segun_ciudadano(len(viviendas),p1d3_sol)
viviendas.append(p1d3_vivienda)
# p2d5
p2d5_vivienda = [0, "Callejón Kroxik Takep 31th n8 5º", p2d5_ex[0], 1]
scramble_ids(viviendas)

# ALOJADOEN
generar_alojadoEn()
# s3d2
alojadoEn.append([s3d2_vivienda[0],s3d2_exu[0]])
# p1d3
alojadoEn.append([p1d3_vivienda[0],p1d3_sol[0]])
alojadoEn.append([p1d3_vivienda[0],vanessavaretta[0]])
# p2d5
alojadoEn.append([p2d5_vivienda[0],p2d5_ex[0]])
R.shuffle(alojadoEn)

# RUTAS
generar_rutas()
# s2d1 (Asegurar que haya al menos 1)
rutas.append([R.choice(vehiculos)[0],"Plaza Ojo de Chlungus","Mega Milky",50.99,"2224-03-11"])
# p2d3
wetgroove = localizaciones[1]["lista"][6]; avcosmi = localizaciones[3]["lista"][0]; korumiv = localizaciones[3]["lista"][2]; cgavku = localizaciones[2]["lista"][4]
rutas.append([R.choice(vehiculos)[0],wetgroove["nombre"],avcosmi["nombre"],calcular_distancia_viaje(wetgroove["pos"],avcosmi["pos"]),"2224-04-21"])
rutas.append([R.choice(vehiculos)[0],wetgroove["nombre"],avcosmi["nombre"],calcular_distancia_viaje(wetgroove["pos"],avcosmi["pos"]),"2224-04-21"])
rutas.append([R.choice(vehiculos)[0],wetgroove["nombre"],avcosmi["nombre"],calcular_distancia_viaje(wetgroove["pos"],avcosmi["pos"]),"2224-04-21"])
rutas.append([R.choice(vehiculos)[0],wetgroove["nombre"],korumiv["nombre"],calcular_distancia_viaje(wetgroove["pos"],korumiv["pos"]),"2224-04-21"])
rutas.append([R.choice(vehiculos)[0],wetgroove["nombre"],korumiv["nombre"],calcular_distancia_viaje(wetgroove["pos"],korumiv["pos"]),"2224-04-21"])
rutas.append([R.choice(vehiculos)[0],wetgroove["nombre"],cgavku["nombre"],calcular_distancia_viaje(wetgroove["pos"],cgavku["pos"]),"2224-04-21"])
# p1d5
rturro = localizaciones[2]["lista"][4]
rutas.append([R.choice(vehiculos)[0],avcosmi["nombre"],rturro["nombre"],calcular_distancia_viaje(avcosmi["pos"],rturro["pos"]),"2224-01-30"])
rutas.append([R.choice(vehiculos)[0],avcosmi["nombre"],rturro["nombre"],calcular_distancia_viaje(avcosmi["pos"],rturro["pos"]),"2224-01-21"])
rutas.append([R.choice(vehiculos)[0],avcosmi["nombre"],rturro["nombre"],calcular_distancia_viaje(avcosmi["pos"],rturro["pos"]),"2224-02-13"])
rutas.append([R.choice(vehiculos)[0],avcosmi["nombre"],rturro["nombre"],calcular_distancia_viaje(avcosmi["pos"],rturro["pos"]),"2224-02-06"])
rutas.append([R.choice(vehiculos)[0],avcosmi["nombre"],rturro["nombre"],calcular_distancia_viaje(avcosmi["pos"],rturro["pos"]),"2224-04-15"])
miramontes = localizaciones[0]["lista"][3]
rutas.append([R.choice(vehiculos)[0],rturro["nombre"],korumiv["nombre"],calcular_distancia_viaje(rturro["pos"],korumiv["pos"]),"2224-01-30"])
rutas.append([R.choice(vehiculos)[0],rturro["nombre"],cgavku["nombre"],calcular_distancia_viaje(rturro["pos"],cgavku["pos"]),"2224-01-21"])
rutas.append([R.choice(vehiculos)[0],rturro["nombre"],miramontes["nombre"],calcular_distancia_viaje(rturro["pos"],localizaciones[2]["lista"][0]["pos"]),"2224-02-13"])
rutas.append([R.choice(vehiculos)[0],rturro["nombre"],miramontes["nombre"],calcular_distancia_viaje(rturro["pos"],localizaciones[2]["lista"][0]["pos"]),"2224-02-06"])
rutas.append([R.choice(vehiculos)[0],rturro["nombre"],miramontes["nombre"],calcular_distancia_viaje(rturro["pos"],localizaciones[1]["lista"][0]["pos"]),"2224-04-15"])
# p2d5
ccorgomatic = localizaciones[2]["lista"][5]; l1 = localizacion_aleatoria(0); l2 = localizacion_aleatoria(0); l3 = localizacion_aleatoria(1)
localizacion_aleatoria(0)
rutas.append([p2d5_vehiculo[0],ccorgomatic["nombre"],l1["nombre"],calcular_distancia_viaje(ccorgomatic["pos"],l1["pos"]),"2224-04-28"])
rutas.append([R.choice(vehiculos)[0],ccorgomatic["nombre"],l2["nombre"],calcular_distancia_viaje(ccorgomatic["pos"],l2["pos"]),"2224-04-28"]) # decoy
rutas.append([R.choice(vehiculos)[0],ccorgomatic["nombre"],l3["nombre"],calcular_distancia_viaje(ccorgomatic["pos"],l3["pos"]),"2224-04-28"]) # decoy
# pEd5
ckt31 = localizaciones[3]["lista"][3]; avam = localizaciones[0]["lista"][0];
rutas.append([pEd5_vikal_v[0],ckt31["nombre"],cgavku["nombre"],calcular_distancia_viaje(ckt31["pos"],cgavku["pos"]),"2224-04-29"])
rutas.append([pEd5_hac_v[0],avam["nombre"],ckt31["nombre"],calcular_distancia_viaje(avam["pos"],ckt31["pos"]),"2224-04-29"])
rutas.append([pEd5_hac_v[0],ckt31["nombre"],cgavku["nombre"],calcular_distancia_viaje(ckt31["pos"],cgavku["pos"]),"2224-04-29"])
rutas.append([pEd5_hac_v[0],cgavku["nombre"],avcosmi["nombre"],calcular_distancia_viaje(cgavku["pos"],avcosmi["pos"]),"2224-04-29"])
R.shuffle(rutas)

# CORREOS
generar_correos()
# pEd1
correo1_hacker = "director@pickiecast.com"
correo2_hacker = direccion_correo_aleatorio(pEd1_hacker)
correo_victima = "juanitojavanero@picklecast.com"
def datos_para_pEd1():
    fecha_min = 210
    fecha_max = 410
    # 0º Generar correos empresa
    direcciones = []
    direcciones.append(correo_victima)
    direcciones.append("director@picklecast.com")
    n_dir = 30
    n1 = R.sample(nombres["humano"],k=n_dir)
    n2 = R.sample(apellidos["humano"],k=n_dir)
    for i in range(0,n_dir): direcciones.append(n1[i]+n2[i]+"@picklecast.com")
    n_dir += 2

    # 1º Meter correo random entre empreados de la empresa
    automatizados = [ # Grupo reducido de trabajadores, cualquier fecha
        ["Tiene una nueva reunión","Se le ha incluido una nueva reunión para el {d}, por favor confirme su asistencia."],
        ["Han compartido un archivo nuevo","{t} ha compartido el siguiente documento"]
    ]
    for i in range(0,40):
        c = R.choice(automatizados)
        f_i = R.randint(fecha_min,fecha_max)
        f = fecha_por_indice(f_i)
        d = R.sample(direcciones,k=2)
        correos.append([0,f,"cloudy@eeldrive.com",d[0],c[0],c[1].format(d=fecha_por_indice(f_i+R.randint(2,7)),t=d[1])])
    # deadlines
    for i in range(8):
        f_idx = R.randint(fecha_min,fecha_max)
        f = fecha_por_indice(f_idx)
        deadline = fecha_por_indice(f_idx+14)
        e_idx = R.randint(2,n_dir)
        emisor = direcciones[e_idx]
        r = e_idx - 1
        r2 = 2+(e_idx+3)%(n_dir-2)
        for j in range(2,n_dir):
            if j == e_idx: continue
            correos.append([0,f,emisor,direcciones[j],"Planificación","Saludos, os escribo para decir que tenemos estas 2 últimas semanas para terminar el proyecto, es decir, hasta el {f}.".format(f=deadline)])
        fate = R.choice([-1,0,1])
        if fate == 0:
            correos.append([0,f,direcciones[r],emisor,"Planificación","Saludos, va a estar un poco justo ¿Podrías pedir más tiempo?"])
            correos.append([0,f,emisor,direcciones[r],"Planificación","Lo siento, he hecho todo lo que podía, ya he intentado negociar la fecha con ellos pero dicen que la fecha es crítica para el equipo de marketing."])
            correos.append([0,f,direcciones[r2],emisor,"Planificación","Se hará lo que pueda... en fin, otro proyecto sin pulir y a penas estable..."])
            correos.append([0,f,emisor,direcciones[r2],"Planificación","Lo comprendo, [virtual_hug.jpg]"])
            correos.append([0,f,direcciones[r2],emisor,"Planificación","¡Noooooo! ¡La imagen tiene transparencia falsa!"])
        elif fate == 1:
            correos.append([0,f,direcciones[r],emisor,"Planificación","Buenas, el proyecto avanza adecuadamente, estará listo para esa fecha sin problemas."])
            correos.append([0,f,emisor,direcciones[r],"Planificación","¡Me alegra escuchar eso!"])
        elif fate == -1:
            correos.append([0,f,direcciones[r],emisor,"Planificación","Buenos días, ni de coña estará listo para esa fecha [sad_cat_on_tree.png]"])
            correos.append([0,f,direcciones[r2],emisor,"Planificación","Buenas, propongo que les sugieras que se metan la deadline por donde les quepa"])
            correos.append([0,f,emisor,direcciones[r2],"Planificación","Por favor, no responda así a los correos, que se almacenan y luego los jefes pueden ver lo que has dicho."])
            correos.append([0,f,direcciones[r2],emisor,"Planificación","Me da igual tío, ya no aguanto más..."])
    # seguimiento
    debates_internos = [
        "Saludos, ¿Cómo va el progreso de {p}?",
        "Buenas, va de lujo",
        "Buenas, todo está avanzando concorde a la fecha establecida",
        "Buenas, nuestro equipo va un poco justo de tiempo, pero todo debería de ir bien",
        "Buenas, el nuevo algoritmo no está funcionando como debería, necesitamos más tiempo de pruebas",
    ]; proyectos=["la nueva API","el servidor","la nueva página","las características experimentales"]
    for i in range(40):
        f = fecha_por_indice(R.randint(fecha_min,fecha_max))
        d = R.sample(direcciones,k=2)
        p = R.choice(proyectos)
        correos.append([0,f,d[0],d[1],"Seguimiento",debates_internos[0].format(p=p)])
        idx = R.randint(1,4)
        correos.append([0,f,d[1],d[0],"Seguimiento",debates_internos[idx]])
    # intercambios
    inter = R.sample(direcciones,k=2)
    correos.append([0,fecha_por_indice(R.randint(fecha_min,fecha_max)),inter[0],inter[1],"Consulta","Tío ¿Cómo funcionaba esto? ¿No hay documentación?"])
    correos.append([0,fecha_por_indice(R.randint(fecha_min,fecha_max)),inter[1],inter[0],"Consulta","Hola, yo soy la documentación."])
    inter = R.sample(direcciones,k=2)
    correos.append([0,fecha_por_indice(R.randint(fecha_min,fecha_max)),inter[0],inter[1],"Consulta","Buenos días, revisa tu código, no funciona."])
    inter = R.sample(direcciones,k=2)
    correos.append([0,fecha_por_indice(R.randint(fecha_min,fecha_max)),inter[0],inter[1],"Coordinación","Saludos compañero, yo ya he terminado mi parte, ya puedes continuar."])
    inter = R.sample(direcciones,k=2)
    correos.append([0,fecha_por_indice(R.randint(fecha_min,fecha_max)),inter[0],inter[1],"Coordinación","Hola, no toques esa parte del código, la estoy editando yo y paso de pelarme con el repositorio."])

    celebraciones = [ # Como broadcast, fechas específicas
        ["¡Feliz Juagüelin grupo!","¡Feliz Juagüelin! ¿Cómo se dice? ¡Feliz Jua-jauwilin grupo soy {t}!"],
        ["Feliz año nuevo","Buenas, me gustaría comunicarles a todos que pasen un feliz año nuevo terrestre."],
    ]
    dir_celebs = R.sample(direcciones,k=round(n_dir/2))
    dc_emisor = dir_celebs[round(n_dir/2)-1]
    for i in range(len(dir_celebs)-1):
        correos.append([0,"2223-10-31",dc_emisor,dir_celebs[i],celebraciones[0][0],celebraciones[0][1].format(t=dc_emisor)])
        correos.append([0,"2224-01-01",dc_emisor,dir_celebs[i],celebraciones[1][0],celebraciones[1][1]])

    otros = [ # Como broadcast, cualquier fecha
        ["Charla sobre igualdad interespecie","Saludos, hoy en día es cuanto más importa saber convivir con diferentes especies. Es importante saber sobre la cultura de los demás, conocer cómo viven y sus necesidades. Por eso la junta BPI ha preparado una charla [link] para conocernos mejor. ¡Trabajemos en un próspero futuro juntos!"],
        ["Charla sobre el uso de nuevas tecnologías","Buenos días, siempre hay cosas que aprender de nuestros compañeros extraterrestres, y las técnicas de comunicación que se han desarrollado en el EEL gracias a la colaboración han superado límites que ni sabíamos que habían. Aprende a como usar estas tecnologías en esta charla [link]"],
        ["Charla sobre el feminismo (terrestre)","Aparentemente el resto de especies no tienen este tipo de problemas... Por favor no seamos el hazme reir del EEL y demostremos que nosotros también somos una civilización avanzada. [link]"],
        ["Charla sobre técnicas justas en el trabajo físico","Hola buenas, esta charla no tiene mucho sentido en esta empresa, pero el gobierno exige que todos los trabajadores puedan recibir la charla. Dejo el link por aquí para la persona interesada. [link]"],
        ["Congreso interestelar de trabajadores","ASISTE AL CONGRESO DONDE LAS EMPRESAS DE TODA LA VÍA LÁCTEA SE REUNEN PARA HABLAR SOBRE LO BIEN QUE FUNCIONAN Y LA GRAN CANTIDAD DE DINERO QUE GANAN A COSTA DE UNA INTERMINABLE LISTA DE TÉCNICAS ABUSIVAS PARA LOS TRABAJADORES Y CONSUMIDORES. [link]"],
        ["Congreso EEL del sector del entretenimiento","El próximo congreso del sector del entretenimiento se acerca. En este congreso tanto empresas como creadores de contenido hablarán sobre sus experiencias, consejos y el estado actual del mercado."],
        ["Congreso EEL tecnológico",""],
        ["Mensaje del sindicato del sector digital",""],
        ["Mensaje del sindicato de empresa","Bua, el CEO la ha vuelto a liar, adivinad a quienes les tocan sufrir las consecuencias."],
    ]
    otros_emisor = ["sindicatoseel@gov.com","sindicatoseel@gov.com","sindicatoseel@gov.com","sindicatoseel@gov.com","congresistas@gov.com","congresistas@gov.com","congresistas@gov.com","sindicatoseel@gov.com","sindicatoseel@gov.com"]
    otros_fechas = []
    for i in range(len(otros)): otros_fechas.append(fecha_por_indice(R.randint(fecha_min,fecha_max)))
    for d in direcciones:
        for i in range(len(otros)):
            correos.append([0,otros_fechas[i],otros_emisor[i],d,otros[i][0],otros[i][1]])

    # 2º Meter el correo malicioso
    correos.append([0,"2224-04-17",correo1_hacker,correo_victima,"Error con tus credenciales","Saludos Juanito, ha habido un error en el sistema y hemos perdido tus datos. Soporte ha comentado que si vuelves a iniciar sesión aquí debería de solucionarse: [link]"])
datos_para_pEd1()
def datos_para_pEd5():
    correos.append([0,"2224-03-26","vikalkontrov@antmsg.exu","cribking@anonmail.com","Negocios","Buenos días, como respuesta a su último mensaje, no sé de que me habla. Nuestra organización no tiene un almacén secreto. Aún así, espero que nuestro trato siga en pie, estoy dispuesto a darle el porcentaje acordado de las ganancias en las que esté involucrado."])
    correos.append([0,"2224-04-19","vikalkontrov@antmsg.exu","cribking@anonmail.com","Recordatorio","Buenos días, quería informarle que el siguiente intercambio de vienes se hará el 19 de abril, a la hora acordada. Debe comunicarme los detalles del vehículo que va a usar para que no hayan... confusiones durante la transferencia."])
    correos.append([0,"2224-04-19","cribking@anonmail.com","vikalkontrov@antmsg.exu","Recordatorio (respuesta)","Buenas. Mi coche es y siempre será un Hamburghini de color amarillo."])
    correos.append([0,"2224-04-19","vikalkontrov@antmsg.exu","cribking@anonmail.com","Recordatorio (respuesta) (respuesta)","Será suficiente, terrestre."])
    correos.append([0,"2223-11-16","vikalkontrov@antmsg.exu","cribking@anonmail.com","Feri Teatro - Miembro platino","¡Saludos! Le hablamos desde el Feri Teatro por ser nuestro cliente número 1. Y para agradecérselo, le hemos dado un aparcamiento privado en el garaje del establecimiento para que siempre encuentre sitio para aparcar su vehículo. ¡Además le será gratis! No tiene por qué enviar ningún formulario, simplemente muestre su tarjeta de Feri-socio en dicho aparcamiento y no se le aplicará ningún pago. Muchas gracias por todo, disfrutamos el que usted disfrute de nuestro teatro."])
datos_para_pEd5()
scramble_ids(correos)

# PINBUSQUEDAS
generar_pingBusquedas()
# pEd1
ip_hacker = "148.48.91.102"
pingBusquedas.append([correo1_hacker,"PickleCast.com","2224-04-17",ip_hacker])
pingBusquedas.append([correo1_hacker,busqueda_aleatoria(),"2224-04-17",ip_hacker])
for i in range(13): pingBusquedas.append([correo2_hacker,busqueda_aleatoria(),fecha_aleatoria(),ip_hacker])
R.shuffle(pingBusquedas)

# TRANSBORDOS
generar_transbordos()
# s1d1
transbordos.append([0,R.randint(1,32),"2224-04-18","Nidolé"])
# pEd3
for i in range(5):
    transbordos.append([0,R.randint(4,8),fecha_aleatoria(),"ANTS"])
    transbordos.append([0,R.randint(4,8),fecha_aleatoria(),"Nidolé"])
# p2d4
p2d4_t1 = [0,8,"2224-04-19",R.choice(entidades_transbordos)]
p2d4_t2 = [0,8,"2224-04-20",R.choice(entidades_transbordos)]
p2d4_t3 = [0,8,"2224-04-23",R.choice(entidades_transbordos)]
p2d4_t4 = [0,8,"2224-04-24",R.choice(entidades_transbordos)]
transbordos.append(p2d4_t1)
transbordos.append(p2d4_t2)
transbordos.append(p2d4_t3)
transbordos.append(p2d4_t4)
scramble_ids(transbordos)


# Dif 2 tables:
generar_asistente_voz()
# p1d2
asistente_voz.append([0,p1d2_sol[0],"2224-04-17 01:27:31","¿Mañana entonces tendrás preparada la bomba? Perfe..."])
# s3d2
def contenido_grabacion_s3d2():
    asistente_voz.append([0,s3d2_feri[0],"2224-04-14 20:13:47","Vamos, asistente, sé que grabas las interacciones y conversaciones, no me defraudes."])
    asistente_voz.append([0,s3d2_feri[0],"2224-04-14 20:14:01","Asistente, ponte en modo escucha activa."])
    asistente_voz.append([0,s3d2_feri[0],"2224-04-14 20:14:08","Me lo guardaré dentro de la ropa o algo..."])
    asistente_voz.append([0,s3d2_feri[0],"2224-04-14 20:53:27","Ah, vosotros debéis de ser los que me llamaron para ese proyecto... Ya os he dicho que no estoy interesado"])
    asistente_voz.append([0,s3d2_feri[0],"2224-04-14 20:53:36","Parece ser que con la amenaza no bastó ¿eh? No te preocupes, que venir vas a venir con nosotros."])
    asistente_voz.append([0,s3d2_feri[0],"2224-04-14 20:53:49","No tengo opción ¿verdad?"])
    asistente_voz.append([0,s3d2_feri[0],"2224-04-14 20:53:52","¿Qué te hace pensar eso? ¿La pistola láser que se hunde en tu nuca? ¿O que te hayamos arrinconado detrás del supermercado?"])
    asistente_voz.append([0,s3d2_feri[0],"2224-04-14 20:53:59","¡Entra en el coche!"])
    asistente_voz.append([0,s3d2_feri[0],"2224-04-14 20:55:22","¿No creéis que es un poco excesivo que me tapéis la cabeza y todo?"])
    asistente_voz.append([0,s3d2_feri[0],"2224-04-14 20:55:27","No"])
    asistente_voz.append([0,s3d2_feri[0],"2224-04-14 20:55:39","He de decir que no es la primera vez que me han puesto una bolsa en la cabeza, pero esa vez iba a una fiesta especial..."])
    asistente_voz.append([0,s3d2_feri[0],"2224-04-14 20:55:43","No me jodas. Ahora no es puto momento para hablar de tus fantasías sexuales tío."])
    asistente_voz.append([0,s3d2_feri[0],"2224-04-14 20:55:57","Ooooh no me refería a eso, verás, una vez mi mujer contrató mi actor feriseo favorito para que me secuestrase por mi cumpleaños, cómo la quiero... esos detalles son los que hacen que la llama de una relación nunca se apague."])
    asistente_voz.append([0,s3d2_feri[0],"2224-04-14 20:56:21","Si no le habéis hecho ninguna sorpresa o regalo a vuestras parejas últimamente, os aconsejo que lo hagáis, no hay nada mejor que ver la felicidad en el rostro de tu pareja después de darle un regalo"])
    asistente_voz.append([0,s3d2_feri[0],"2224-04-14 20:56:41","Ahora que lo dices dentro de poco es el cumpleaños de mi... No, joder no me líes. Cállate ya."])
    asistente_voz.append([0,s3d2_feri[0],"2224-04-14 20:57:34","Ya hemos llegado jefe."])
    asistente_voz.append([0,s3d2_feri[0],"2224-04-14 20:57:40","Muy bien, ahora tranquilito, como armes jaleo no dudaré en disparar"])
    asistente_voz.append([0,s3d2_feri[0],"2224-04-14 21:01:23","¡Ay! ¿Oye no crees que es un poco innecesario atarme a una silla? Oh, ya puedo ver..."])
    asistente_voz.append([0,s3d2_feri[0],"2224-04-14 21:02:08","Bueno, dado que denegaste nuestra oferta anterior, esta es la nueva oferta. Vas a diseñar un desencriptador para los dispositivos de comunicación VE-48, o te quedarás aquí hasta que mueras de hambre."])
    asistente_voz.append([0,s3d2_feri[0],"2224-04-14 21:02:18","¿Los que usan la policia?"])
    asistente_voz.append([0,s3d2_feri[0],"2224-04-14 21:02:22","Y los políticos, jeje"])
    asistente_voz.append([0,s3d2_feri[0],"2224-04-14 21:02:24","Cierra el pico"])
    asistente_voz.append([0,s3d2_feri[0],"2224-04-14 21:02:27","Perdón jefe..."])
    asistente_voz.append([0,s3d2_feri[0],"2224-04-14 21:02:36","No creo que pueda hacer nada..."])
    asistente_voz.append([0,s3d2_feri[0],"2224-04-14 21:02:38","Shhh... Seguro que puedes, eres un ingeniero de renombre, sabemos de qué eres capaz."])
    asistente_voz.append([0,s3d2_feri[0],"2224-04-14 21:02:45","¿Y si prefiero morir de hambre?"])
    asistente_voz.append([0,s3d2_feri[0],"2224-04-14 21:02:49","¿Darías tu vida por mantener los secretos de la empresa en la que trabajas? Qué estúpido... Muy bien, cambio de planes. Vamos a por tu mujer."])
    asistente_voz.append([0,s3d2_feri[0],"2224-04-14 21:02:54","NO ESPERA... ¿Seguro que no podemos llegar a un acuerdo? Uno en el que no esté involucrada mi familia..."])
    asistente_voz.append([0,s3d2_feri[0],"2224-04-14 21:02:38","Ya te lo he dicho, o empiezas a trabajar o adios a tu mujer."])
    asistente_voz.append([0,s3d2_feri[0],"2224-04-14 21:02:41","Eh... por cierto, hablando de mi mujer, creo que debería llamarla, le dije que iba a comprar y si no vuelvo se preocupará... dejadme llamarla para que le diga que he hecho planes con unos amigos."])
    asistente_voz.append([0,s3d2_feri[0],"2224-04-14 21:03:19","Está bien, pero como se te ocurra decir algo sospechoso, dispararé."])
    asistente_voz.append([0,s3d2_feri[0],"2224-04-14 21:03:38","¡Hola amor! Llamaba para decir que me he encontrado unos amigos corgos de camino al supermercado, me han contado un plan chulísimo y me han convencido, por eso voy a estar unos días fuera ¡Te quiero amooor! ¡Adioos!"])
    asistente_voz.append([0,s3d2_feri[0],"2224-04-14 21:05:48","Oye, ahora que lo pienso, ¿No ha sido un poco tonto llevarme con la cabeza tapada, si luego me ponéis al lado de una ventana?"])
    asistente_voz.append([0,s3d2_feri[0],"2224-04-14 21:05:52","De hecho puedo ver la cabeza de la estatua del rey exukente, por lo que puedo deducir que cláramente estamos en la calle korumiv. Es más, por la altura diría que estamos en un noveno."])
    asistente_voz.append([0,s3d2_feri[0],"2224-04-14 21:05:55","Te crees muy listo por ser un ingeniero pero tu cabeza sólo sabe montar cacharritos, te has equivocado de calle, y eso que sólo hay dos calles en todo el distrito exukente ¡JAJAJA!"])
    asistente_voz.append([0,s3d2_feri[0],"2224-04-14 21:06:01","Hmmm, supongo que tienes razón… Calle Tripaloki entonces ¿no?"])
    asistente_voz.append([0,s3d2_feri[0],"2224-04-14 21:06:13","¡Cállate ya pesado! ¡Como sigas te agujereo la frente!"])
    asistente_voz.append([0,s3d2_feri[0],"2224-04-14 21:06:21","¿De verdad me dispararías? Si estoy aquí es porque os hago falta..."])
    asistente_voz.append([0,s3d2_feri[0],"2224-04-14 21:06:24","QUÉ TE CALLES HE DICHO, JODER ¿Y QUÉ COÑO HACES PONIENDO OJITOS TIERNOS?, TÍO, PONTE TÚ CON ESTE, prefiero ponerme a vigilar todo el día antes que escuchar una palabra más de este keveerik."])
    asistente_voz.append([0,s3d2_feri[0],"2224-04-14 21:06:31","Joo... sólo quería sacar conversación, sois unos aburridos..."])
    asistente_voz.append([0,s3d2_feri[0],"2224-04-14 21:06:36","Estas en un puto secuestro, NO TIENES QUE DIVERTIRTE. Ay, Feriseo tenía que ser..."])
    asistente_voz.append([0,s3d2_feri[0],"2224-04-14 21:06:42","¡Eh! Eso es racista..."])
    asistente_voz.append([0,s3d2_feri[0],"2224-04-14 21:06:45","Ya está, te lo has buscado, trae las  herramientas de tortura."])
    asistente_voz.append([0,s3d2_feri[0],"2224-04-14 21:06:49","O-ooh..."])
contenido_grabacion_s3d2()
# easter eggs
asistente_voz.append([0,9999,"2000-05-01 22:48:15","KRONK, PULL THE LEVER!"])
asistente_voz.append([0,9999,"2000-05-01 22:48:18","WRONG LEVEEEEEEEER!"])
scramble_ids(asistente_voz)

generar_megamilky_productos()
generar_megamilky_ventas()
# pEd2
id_alguicida = 73
megamilky_ventas.append([0,decoy[0],"2224-03-23",id_alguicida,10])
megamilky_ventas.append([0,pEd2_sol[0],"2224-04-10",id_alguicida,8])
# s2d2
id_spray_lata = 98
megamilky_ventas.append([0,s2d2_humano3[0],"2224-04-10",id_spray_lata,2])
megamilky_ventas.append([0,s2d2_humano1[0],"2224-04-16",id_spray_lata,5])
megamilky_ventas.append([0,s2d2_humano2[0],"2224-04-15",id_spray_lata,5])
megamilky_ventas.append([0,s2d2_humano3[0],"2224-04-15",id_spray_lata,4])
# s3d2
id_asistente_voz = 87
megamilky_ventas.append([0,s3d2_feri[0],"2224-04-14",id_asistente_voz,1])

scramble_ids(megamilky_ventas)

generar_muricaGuns_armasRegistradas()
# p2d2
muricaGuns_armasRegistradas.append([984528335,p2d2_sol[0],lista_armas[4][0],lista_armas[4][1]])
R.shuffle(muricaGuns_armasRegistradas)

generar_corgomatic()
# s1d2
corgomatic.append([s1d2_vehiculo[0],"2224-04-16","cambio de neumáticos traseros, reparación de lunas traseras, capa de pintura color morado tinto"])
# p1d4
corgomatic.append(["0274CJH","2224-04-13","cambio de llantas, cambio de carrocería"])
corgomatic.append(["0682ACY","2224-04-19","cambio de llantas, cambio de carrocería"])
corgomatic.append(["0285PRN","2224-04-14","cambio de llantas, cambio de carrocería, actualización de Sistema Operativo"])
corgomatic.append(["0102MVM","2224-04-17","cambio de llantas, cambio de carrocería"])
corgomatic.append(["0427QEG","2224-04-16","cambio de llantas, cambio de carrocería, cambio de aceite"])
# p2d5
corgomatic.append([p2d5_vehiculo[0],"224-04-28",mod_vehiculo_aleatoria()])

# Dif 4 tables:
generar_rinconDelTurro_Reservas()
# pEd4
reserva1_27 = [0,2,"2224-04-27 14:00"]
reserva2_27 = [0,2,"2224-04-27 15:00"]
reserva3_27 = [0,3,"2224-04-27 22:00"]
rinconDelTurro_Reservas.append(reserva1_27)
rinconDelTurro_Reservas.append(reserva2_27)
rinconDelTurro_Reservas.append(reserva3_27)
scramble_ids(rinconDelTurro_Reservas)

generar_rinconDelTurro_Mesas()
# pEd4
rinconDelTurro_Mesas.append([reserva1_27[0],pEd4_decoy_14_h1[0]])
rinconDelTurro_Mesas.append([reserva1_27[0],pEd4_decoy_14_h2[0]])
rinconDelTurro_Mesas.append([reserva2_27[0],pEd4_decoy_15_c1[0]])
rinconDelTurro_Mesas.append([reserva2_27[0],pEd4_decoy_15_c2[0]])
rinconDelTurro_Mesas.append([reserva3_27[0],pEd4_h1[0]])
rinconDelTurro_Mesas.append([reserva3_27[0],pEd4_h2[0]])
rinconDelTurro_Mesas.append([reserva3_27[0],pEd4_ex[0]])

generar_transbordos_Empleados()
# p2d4
transbordos_Empleados.append([p2d4_t1[0],p2d4_h1[0]]); transbordos_Empleados.append([p2d4_t1[0],p2d4_h2[0]])
transbordos_Empleados.append([p2d4_t2[0],p2d4_h1[0]]); transbordos_Empleados.append([p2d4_t2[0],p2d4_h2[0]])
transbordos_Empleados.append([p2d4_t3[0],p2d4_h1[0]])
transbordos_Empleados.append([p2d4_t4[0],p2d4_h1[0]]); transbordos_Empleados.append([p2d4_t4[0],p2d4_h2[0]])

generar_grabacionRestaurante()


generar_paulsPizzeria_Inventario()
scramble_ids(paulsPizzeria_Inventario)


# 6. Save all tables
guardar_sql(rel_path_to_file,"USE `db_game`;\n\n",'w')
generar_como_sql("ciudadanos",["dni","nombre","apellidos","edad","colorPelo","altura","especie"],ciudadanos)
generar_como_sql("viviendas",["id","direccion","titular","esPiso"],viviendas)
generar_como_sql("vehiculos",["matricula","idTitular","marca","color"],vehiculos)
generar_como_sql("alojadoEn",["vivienda","ciudadano"],alojadoEn)
generar_como_sql("rutas",["matricula","zonaOrigen","zonaDestino","distanciaViaje","fecha"],rutas)
generar_como_sql("correos",["id","fecha","emisor","destinatario","asunto","contenido"],correos)
generar_como_sql("pingBusquedas",["correo","busqueda","fecha","ip"],pingBusquedas)
generar_como_sql("transbordos",["id","numPuerto","fechaLlegada","entidadSolicitante"],transbordos)

generar_como_sql("asistenteVoz",["id","dniPropietario","fecha","log"],asistente_voz)
generar_como_sql("megaMilky_productos",["id","nombre","precio","tipo","stock"],megamilky_productos)
generar_como_sql("megaMilky_ventas",["id","dniCliente","fecha","idProducto","cantidad"],megamilky_ventas)
generar_como_sql("muricaGuns_armasRegistradas",["numSerie","dni","tipo","marca"],muricaGuns_armasRegistradas)
generar_como_sql("corgomatic",["matricula","fecha","cambios"],corgomatic)

generar_como_sql("rinconDelTurro_reservas",["id","comensales","fecha"],rinconDelTurro_Reservas)
generar_como_sql("rinconDelTurro_mesas",["idReserva","dniCliente"],rinconDelTurro_Mesas)
generar_como_sql("transbordos_empleados",["idTransbordo","dniEmpleado"],transbordos_Empleados)
generar_como_sql("grabacionRestaurante",["transcripcion","hora"],grabacionRestaurante)
generar_como_sql("paulsPizzeria_inventario",["id","objeto","tipo","proveedor","existencias"],paulsPizzeria_Inventario)
