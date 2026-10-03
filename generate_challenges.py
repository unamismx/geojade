import json
from pathlib import Path

root=Path(__file__).parent

def q(text,answer,options,explanation,**extra):
    return dict(text=text,answer=answer,options=[answer]+options,explanation=explanation,**extra)

continents=['América','Europa','Asia','África','Oceanía']
world=[
('MEX','México','América'),('CAN','Canadá','América'),('BRA','Brasil','América'),('ARG','Argentina','América'),('CHL','Chile','América'),('COL','Colombia','América'),
('ESP','España','Europa'),('FRA','Francia','Europa'),('ITA','Italia','Europa'),('DEU','Alemania','Europa'),('GBR','Reino Unido','Europa'),('NOR','Noruega','Europa'),
('CHN','China','Asia'),('IND','India','Asia'),('JPN','Japón','Asia'),('KOR','Corea del Sur','Asia'),('THA','Tailandia','Asia'),('SAU','Arabia Saudita','Asia'),
('EGY','Egipto','África'),('MAR','Marruecos','África'),('DZA','Argelia','África'),('NGA','Nigeria','África'),('KEN','Kenia','África'),('ZAF','Sudáfrica','África'),
('AUS','Australia','Oceanía'),('NZL','Nueva Zelanda','Oceanía'),('IDN','Indonesia','Oceanía'),('PNG','Papúa Nueva Guinea','Oceanía'),('FJI','Fiyi','Oceanía')]
world_questions=[]
for i,(code,country,continent) in enumerate(world):
    wrong=[x for x in continents if x!=continent]
    world_questions.append(q('¿A qué continente pertenece el país marcado?',continent,wrong[:3],f'El país resaltado es {country} y pertenece a {continent}.',mapCode=code,continent=continent,country=country,mapType='continent'))

america=[('CAN','Canadá'),('USA','Estados Unidos'),('MEX','México'),('GTM','Guatemala'),('BLZ','Belice'),('HND','Honduras'),('NIC','Nicaragua'),('CRI','Costa Rica'),('PAN','Panamá'),('CUB','Cuba'),('COL','Colombia'),('VEN','Venezuela'),('ECU','Ecuador'),('PER','Perú'),('BRA','Brasil'),('BOL','Bolivia'),('PRY','Paraguay'),('CHL','Chile'),('ARG','Argentina'),('URY','Uruguay')]
america_questions=[]
for i,(code,country) in enumerate(america):
    others=[america[(i+j)%len(america)][1] for j in (4,9,14)]
    america_questions.append(q('¿Qué país de América está marcado?',country,others,f'El territorio resaltado corresponde a {country}.',mapCode=code,continent='América',country=country,mapType='america'))

mexico=[('SON','Sonora'),('BCN','Baja California'),('CHH','Chihuahua'),('COA','Coahuila'),('TAM','Tamaulipas'),('NLE','Nuevo León'),('ROO','Quintana Roo'),('CAM','Campeche'),('TAB','Tabasco'),('CHP','Chiapas'),('COL','Colima'),('NAY','Nayarit'),('BCS','Baja California Sur'),('SIN','Sinaloa'),('YUC','Yucatán'),('VER','Veracruz'),('JAL','Jalisco'),('MIC','Michoacán'),('GRO','Guerrero'),('OAX','Oaxaca'),('MEX','Estado de México'),('PUE','Puebla'),('MOR','Morelos'),('QUE','Querétaro'),('HID','Hidalgo'),('GUA','Guanajuato'),('SLP','San Luis Potosí'),('ZAC','Zacatecas'),('AGU','Aguascalientes'),('DUR','Durango'),('TLA','Tlaxcala'),('DIF','Ciudad de México')]
mexico_questions=[]
for i,(code,state) in enumerate(mexico):
    others=[mexico[(i+j)%len(mexico)][1] for j in (5,13,21)]
    mexico_questions.append(q('¿Qué entidad de México está marcada?',state,others,f'La entidad resaltada es {state}.',mexicoCode=code,mapType='mexico'))

ocean_data=[
('Pacífico',210,270),('Pacífico',80,300),('Pacífico',890,280),('Atlántico',410,270),('Atlántico',480,180),('Atlántico',390,360),
('Índico',680,330),('Índico',740,270),('Ártico',520,70),('Ártico',760,65),('Antártico',500,475),('Antártico',800,470)]
ocean_names=['Pacífico','Atlántico','Índico','Ártico','Antártico']
ocean_questions=[]
for ocean,x,y in ocean_data:
    wrong=[n for n in ocean_names if n!=ocean][:3]
    ocean_questions.append(q('¿Qué océano está señalado?',ocean,wrong,f'El punto está situado en el océano {ocean}.',mapPoint=[x,y],mapType='ocean'))

players=[
('Lionel Messi','messi.webp','Argentina · América'),('Kylian Mbappé','mbappe.webp','Francia · Europa'),('Jude Bellingham','bellingham.webp','Inglaterra · Europa'),('Erling Haaland','haaland.webp','Noruega · Europa'),('Vinícius Júnior','vinicius.webp','Brasil · América'),('Cristiano Ronaldo','ronaldo.webp','Portugal · Europa'),('Lamine Yamal','yamal.webp','España · Europa'),('Mohamed Salah','salah.webp','Egipto · África'),('Son Heung-min','son.webp','Corea del Sur · Asia'),('Raúl Jiménez','jimenez.webp','México · América')]
wc_questions=[]
for i,(player,image,answer) in enumerate(players):
    wrong=[players[(i+j)%len(players)][2] for j in (3,5,7)]
    wc_questions.append(q(f'¿Con qué selección jugó {player} en el Mundial 2026 y en qué continente está?',answer,wrong,f'{player} representó a {answer.replace(" · ",", país de ")}.',photo='players/'+image,player=player,mapType='player'))

abu=[
q('Abu pregunta: ¿Qué país dio su nombre a la línea del ecuador?','Ecuador',['Brasil','Kenia','Indonesia'],'La República del Ecuador tomó su nombre de la línea ecuatorial.'),
q('¿Cuál es la isla más grande del mundo si Australia se considera continente?','Groenlandia',['Madagascar','Nueva Guinea','Borneo'],'Groenlandia es la isla más grande; Australia se clasifica como continente.'),
q('¿Qué país africano también tiene territorio en Asia?','Egipto',['Kenia','Nigeria','Marruecos'],'La península del Sinaí, parte de Egipto, se encuentra en Asia.'),
q('¿Cuál de estas ciudades es la capital de Australia?','Canberra',['Sídney','Melbourne','Perth'],'Canberra es la capital; Sídney y Melbourne son más grandes.'),
q('¿Qué país está completamente rodeado por Sudáfrica?','Lesoto',['Esuatini','Botsuana','Namibia'],'Lesoto es un enclave: todo su límite terrestre es con Sudáfrica.'),
q('¿Cuál de estos continentes no tiene países soberanos?','Antártida',['Oceanía','África','América'],'La Antártida está regida por tratados y no contiene países soberanos.'),
q('Si sales de la costa oriental de Yucatán en línea recta hacia el este, ¿qué encuentras primero?','El mar Caribe',['El océano Pacífico','Guatemala','Campeche'],'Al este de la península está el mar Caribe.'),
q('¿Qué estado mexicano tiene costa tanto en el Pacífico como en el golfo de México?','Ninguno',['Oaxaca','Veracruz','Chiapas'],'Ninguna entidad mexicana toca simultáneamente esas dos costas.'),
q('¿Qué país sudamericano no tiene salida al mar?','Paraguay',['Chile','Ecuador','Uruguay'],'Paraguay y Bolivia carecen de costa; entre estas opciones, es Paraguay.'),
q('¿Qué país une América del Norte con América del Sur?','Panamá',['Cuba','Ecuador','Belice'],'El istmo de Panamá forma el puente terrestre entre ambas regiones.'),
q('¿Cuál es el océano más grande del planeta?','Pacífico',['Atlántico','Índico','Ártico'],'El Pacífico ocupa más superficie que cualquier otro océano.'),
q('¿Cuál está más cerca del polo sur?','Argentina',['Canadá','España','Japón'],'El extremo austral de Argentina se acerca mucho más a la Antártida.'),
q('¿La línea del ecuador atraviesa México?','No',['Sí, por Chiapas','Sí, por Yucatán','Sí, por Oaxaca'],'México se encuentra completamente al norte del ecuador.'),
q('¿Cuál es la capital de Quintana Roo?','Chetumal',['Cancún','Tulum','Playa del Carmen'],'Cancún es la ciudad más famosa, pero la capital es Chetumal.'),
q('¿Cuál de estas ciudades NO es una de las tres capitales de Sudáfrica?','Johannesburgo',['Pretoria','Ciudad del Cabo','Bloemfontein'],'Sudáfrica reparte funciones de capital entre Pretoria, Ciudad del Cabo y Bloemfontein.'),
q('¿Qué país está a la vez en Europa y Asia?','Turquía',['Portugal','Japón','Australia'],'Turquía ocupa territorio a ambos lados del Bósforo.'),
q('¿Cuál es el país más grande del mundo por superficie?','Rusia',['Canadá','China','Estados Unidos'],'Rusia es el país con mayor superficie terrestre.'),
q('¿Qué isla del Caribe está más cerca de la península de Yucatán?','Cuba',['Puerto Rico','Jamaica','Barbados'],'El canal de Yucatán separa la península de Cuba.'),
q('Si en Mérida son las 8:00 y viajas hacia el este, ¿el amanecer ocurre antes o después?','Antes',['Después','A la misma hora exacta','Sólo cambia en invierno'],'Hacia el este, el Sol aparece antes en el horizonte.'),
q('¿Cuál de estos nombres corresponde a un país y también a su capital?','Panamá',['Brasil','Canadá','Australia'],'La capital de Panamá se llama Ciudad de Panamá.')]
for item in abu:item['abu']=True;item['mapType']='abu'

challenges={
'world':{'title':'Países y continentes','subtitle':'Países marcados en mapas ampliados','icon':'🌍','length':8,'questions':world_questions},
'america':{'title':'Países de América','subtitle':'Reconoce el país resaltado','icon':'🧭','length':8,'questions':america_questions},
'mexico':{'title':'Estados de México','subtitle':'Mapa con división política','icon':'🇲🇽','length':8,'questions':mexico_questions},
'oceans':{'title':'Océanos','subtitle':'Ubica los grandes océanos','icon':'🌊','length':8,'questions':ocean_questions},
'worldcup':{'title':'Mundial 2026','subtitle':'Estrellas, selecciones y continentes','icon':'⚽','length':8,'questions':wc_questions},
'abu':{'title':'Abu Pregunta','subtitle':'Preguntas difíciles y medio tramposas','icon':'🎓','length':10,'questions':abu}}
(root/'challenges.js').write_text('window.CHALLENGES='+json.dumps(challenges,ensure_ascii=False,indent=2)+';\n')
