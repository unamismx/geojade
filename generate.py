import json
from pathlib import Path
root=Path(__file__).parent
questions=[]
def add(cat,text,answer,others,explanation):
    questions.append(dict(id=f'q{len(questions)+1}',category=cat,text=text,answer=answer,options=[answer]+others,explanation=explanation))
caps=[('Aguascalientes','Aguascalientes'),('Baja California','Mexicali'),('Baja California Sur','La Paz'),('Campeche','San Francisco de Campeche'),('Chiapas','Tuxtla Gutiérrez'),('Chihuahua','Chihuahua'),('Coahuila','Saltillo'),('Colima','Colima'),('Durango','Victoria de Durango'),('Guanajuato','Guanajuato'),('Guerrero','Chilpancingo'),('Hidalgo','Pachuca'),('Jalisco','Guadalajara'),('Estado de México','Toluca'),('Michoacán','Morelia'),('Morelos','Cuernavaca'),('Nayarit','Tepic'),('Nuevo León','Monterrey'),('Oaxaca','Oaxaca de Juárez'),('Puebla','Puebla de Zaragoza'),('Querétaro','Santiago de Querétaro'),('Quintana Roo','Chetumal'),('San Luis Potosí','San Luis Potosí'),('Sinaloa','Culiacán'),('Sonora','Hermosillo'),('Tabasco','Villahermosa'),('Tamaulipas','Ciudad Victoria'),('Tlaxcala','Tlaxcala de Xicohténcatl'),('Veracruz','Xalapa'),('Yucatán','Mérida'),('Zacatecas','Zacatecas')]
for i,(state,capital) in enumerate(caps):
    add('capitales',f'¿Cuál es la capital de {state}?',capital,[caps[(i+j)%len(caps)][1] for j in (3,8,15)],f'{capital} es la capital de {state}.')
    add('capitales',f'{capital} es la capital de…',state,[caps[(i+j)%len(caps)][0] for j in (4,9,17)],f'{capital} es la capital de {state}.')
add('capitales','¿Cuál es la capital de México?','Ciudad de México',['Guadalajara','Monterrey','Mérida'],'Ciudad de México es la capital del país y una entidad federativa; no es un estado.')
add('capitales','¿Cuál es la capital de Quintana Roo, aunque Cancún sea más famosa?','Chetumal',['Cancún','Tulum','Playa del Carmen'],'La ciudad más famosa o más grande no siempre es la capital: en Quintana Roo es Chetumal.')
continents={
'América del Norte':['México','Canadá','Estados Unidos'],
'América del Sur':['Brasil','Argentina','Chile','Perú','Colombia','Ecuador','Bolivia','Uruguay','Paraguay','Venezuela'],
'Europa':['España','Portugal','Italia','Alemania','Noruega','Suecia','Finlandia','Polonia','Grecia','Irlanda','Islandia','Suiza','Austria','Bélgica','Países Bajos'],
'Asia':['Japón','China','India','Vietnam','Tailandia','Corea del Sur','Nepal','Mongolia','Pakistán','Bangladés','Arabia Saudita','Camboya','Laos','Singapur','Sri Lanka'],
'África':['Kenia','Nigeria','Sudáfrica','Marruecos','Argelia','Túnez','Etiopía','Ghana','Senegal','Tanzania','Madagascar','Uganda','Zambia'],
'Oceanía':['Australia','Nueva Zelanda','Fiyi','Samoa']}
for region,countries in continents.items():
    for country in countries:
        other=[x for x in continents if x!=region][:3]
        add('mundo',f'¿En qué continente o región continental se encuentra {country}?',region,other,f'{country} se encuentra en {region}.')
# América del Norte y del Sur se presentan como regiones de América.
pairs=[('Yucatán','Campeche'),('Yucatán','Quintana Roo'),('Campeche','Tabasco'),('Campeche','Quintana Roo'),('Chiapas','Tabasco'),('Chiapas','Oaxaca'),('Oaxaca','Guerrero'),('Oaxaca','Puebla'),('Guerrero','Morelos'),('Guerrero','Michoacán'),('Jalisco','Colima'),('Jalisco','Nayarit'),('Jalisco','Guanajuato'),('Sonora','Chihuahua'),('Sonora','Sinaloa'),('Chihuahua','Durango'),('Chihuahua','Coahuila'),('Coahuila','Nuevo León'),('Nuevo León','Tamaulipas'),('Durango','Sinaloa')]
neighbors={s:set() for s,c in caps}
for a,b in pairs: neighbors[a].add(b);neighbors[b].add(a)
# Distractores deliberadamente lejanos para evitar otras fronteras válidas.
south=['Yucatán','Quintana Roo','Campeche','Chiapas','Tabasco']
north=['Baja California','Baja California Sur','Sonora','Chihuahua','Coahuila','Nuevo León','Tamaulipas']
for a,b in pairs:
    for state,answer in [(a,b),(b,a)]:
        pool=north if state in south or state in ['Oaxaca','Guerrero','Morelos','Michoacán'] else south
        wrong=[x for x in pool if x!=answer and x!=state and x not in neighbors[state]][:3]
        add('vecinos',f'¿Cuál de estos estados comparte frontera terrestre con {state}?',answer,wrong,f'{state} y {answer} son vecinos: comparten una frontera terrestre.')
basic=[
('¿Dónde se encuentra Yucatán dentro de México?','En el sureste',['En el noroeste','En el centro','En el noreste'],'Yucatán está en el sureste del país.'),
('¿Cuál de estos estados está en el noroeste de México?','Sonora',['Yucatán','Chiapas','Tabasco'],'Sonora está en el noroeste y limita con Estados Unidos.'),
('¿Cuál de estos estados está en el sur de México?','Chiapas',['Chihuahua','Coahuila','Sonora'],'Chiapas está en el sur, junto a Guatemala.'),
('¿Cuál de estos estados está en la península de Yucatán?','Quintana Roo',['Puebla','Durango','Colima'],'La parte mexicana de la península comprende Yucatán, Campeche y Quintana Roo.'),
('¿Cuál de estos estados NO tiene frontera con Estados Unidos?','Durango',['Sonora','Chihuahua','Coahuila'],'Durango no llega a la frontera con Estados Unidos.'),
('¿Cuál de estos estados tiene frontera con Estados Unidos?','Nuevo León',['Jalisco','Puebla','Yucatán'],'Nuevo León tiene una pequeña frontera con Texas.'),
('¿Qué país está al norte de México?','Estados Unidos',['Guatemala','Belice','Brasil'],'Estados Unidos comparte toda la frontera norte de México.'),
('¿Qué país comparte frontera con Quintana Roo?','Belice',['Costa Rica','Canadá','Cuba'],'Belice se encuentra al sur de Quintana Roo.'),
('¿Qué país comparte frontera con Chiapas?','Guatemala',['Panamá','Estados Unidos','Honduras'],'Chiapas limita con Guatemala.'),
('¿Qué mar está junto a Cancún?','Mar Caribe',['Mar Mediterráneo','Mar Rojo','Mar Báltico'],'Cancún tiene costa en el mar Caribe.'),
('¿Qué océano está junto a Acapulco?','Pacífico',['Atlántico','Índico','Ártico'],'Acapulco, Guerrero, está en la costa del Pacífico.'),
('¿Qué océano está junto a Puerto Vallarta?','Pacífico',['Índico','Ártico','Atlántico'],'Puerto Vallarta, Jalisco, tiene costa en el Pacífico.'),
('¿Qué estado tiene costa en el golfo de México?','Veracruz',['Guanajuato','Querétaro','Chihuahua'],'Veracruz tiene una extensa costa en el golfo de México.'),
('¿Qué estado tiene costa en el Pacífico?','Guerrero',['Yucatán','Nuevo León','Hidalgo'],'Guerrero tiene costa en el Pacífico.'),
('¿En qué estado está Cancún?','Quintana Roo',['Yucatán','Campeche','Tabasco'],'Cancún está en Quintana Roo.'),
('¿En qué estado está Guadalajara?','Jalisco',['Nuevo León','Puebla','Oaxaca'],'Guadalajara es una ciudad de Jalisco y su capital.'),
('¿En qué estado está Tijuana?','Baja California',['Baja California Sur','Sonora','Sinaloa'],'Tijuana está en Baja California, cerca de Estados Unidos.'),
('¿Qué estado está en la península de Baja California?','Baja California Sur',['Sonora','Jalisco','Nayarit'],'La península está dividida entre Baja California y Baja California Sur.'),
('¿Cuál de estos estados tiene costa?','Sinaloa',['Zacatecas','Aguascalientes','Guanajuato'],'Sinaloa tiene costa en el Pacífico y en el golfo de California.'),
('¿Cuál de estos estados NO tiene costa?','Querétaro',['Veracruz','Guerrero','Yucatán'],'Querétaro está en el interior del país.')]
for t,a,o,e in basic:add('mexico',t,a,o,e)
reason=[
('Sales de Mérida hacia Cancún. ¿A qué estado entras?','Quintana Roo',['Campeche','Tabasco','Oaxaca'],'Mérida está en Yucatán y Cancún en Quintana Roo.'),
('Vas de Yucatán a Tabasco por la ruta costera. ¿Qué estado atraviesas?','Campeche',['Chiapas','Veracruz','Sonora'],'La ruta costera pasa de Yucatán a Campeche y después a Tabasco.'),
('Mi capital es Chetumal y tengo costa caribeña. ¿Qué estado soy?','Quintana Roo',['Yucatán','Campeche','Veracruz'],'Ambas pistas corresponden a Quintana Roo.'),
('Mi capital es Hermosillo y limito con Estados Unidos. ¿Qué estado soy?','Sonora',['Sinaloa','Nayarit','Durango'],'Hermosillo es la capital de Sonora, un estado fronterizo.'),
('Mi capital es Tuxtla Gutiérrez y limito con Guatemala. ¿Qué estado soy?','Chiapas',['Oaxaca','Puebla','Guerrero'],'Tuxtla Gutiérrez está en Chiapas, junto a Guatemala.'),
('¿Qué estado de la península está al este de Yucatán?','Quintana Roo',['Campeche','Tabasco','Chiapas'],'Quintana Roo ocupa el lado oriental de la península.'),
('Si el norte está arriba en un mapa, ¿dónde está el este?','A la derecha',['A la izquierda','Abajo','Arriba'],'En un mapa orientado con el norte arriba, el este queda a la derecha.'),
('Si el norte está arriba en un mapa, ¿dónde está el oeste?','A la izquierda',['A la derecha','Arriba','Abajo'],'El oeste queda a la izquierda cuando el norte está arriba.'),
('Caminas al norte y después regresas por el mismo camino. ¿Hacia dónde vuelves?','Al sur',['Al este','Al oeste','Al norte'],'El sur es la dirección opuesta al norte.'),
('Viajas hacia el este y das media vuelta. ¿Hacia dónde vas ahora?','Al oeste',['Al norte','Al sur','Al este'],'El oeste es la dirección opuesta al este.'),
('México y Japón miran hacia un mismo gran océano. ¿Cuál?','Pacífico',['Índico','Ártico','Atlántico'],'El Pacífico está entre las costas occidentales de América y las orientales de Asia.'),
('Viajas de Brasil a Argentina. ¿Cambias de región continental?','No, ambos están en América del Sur',['Sí, llegas a Europa','Sí, llegas a Asia','Sí, llegas a África'],'Brasil y Argentina pertenecen a América del Sur.'),
('Viajas de España a Japón. ¿A qué continente llegas?','Asia',['África','Europa','Oceanía'],'España está en Europa y Japón en Asia.'),
('Buscas un país de Oceanía. ¿Qué viaje sirve?','Ir a Nueva Zelanda',['Ir a Italia','Ir a Kenia','Ir a Perú'],'Nueva Zelanda está en Oceanía.'),
('En un mapa con el norte arriba, avanzas hacia abajo. ¿Qué dirección sigues?','Sur',['Norte','Este','Oeste'],'Abajo corresponde al sur en ese mapa.'),
('¿Qué ruta une tres estados vecinos de la península?','Yucatán → Campeche → Quintana Roo',['Yucatán → Sonora → Quintana Roo','Campeche → Chihuahua → Yucatán','Quintana Roo → Jalisco → Campeche'],'Yucatán limita con Campeche, y Campeche con Quintana Roo.')]
for t,a,o,e in reason:add('reto',t,a,o,e)
assert len(questions)==200,len(questions)
for q in questions:assert len(set(q['options']))==4 and q['answer'] in q['options'],q
(root/'questions.js').write_text('window.QUESTIONS = '+json.dumps(questions,ensure_ascii=False,indent=2)+';\n')
