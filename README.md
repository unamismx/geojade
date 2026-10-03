# GeoJade

Aplicación estática en español para explorar geografía desde Safari en iPad, sin cuentas ni servicios de IA.

## Funciones

- Menú de seis retos independientes de 8 a 10 preguntas: mundo, América, México, océanos, Mundial 2026 y Abu Pregunta.
- Mapas ampliados por continente y mapa político de México con sus 32 entidades.
- Reto Mundial 2026 con diez futbolistas y fotografías acreditadas de Wikimedia Commons.
- Abu Pregunta reúne preguntas deliberadamente más difíciles y una ilustración creada a partir de la fotografía proporcionada por el usuario.
- Preguntas y opciones aleatorias; ubicación, vecinos, capitales, mundo y razonamiento.
- Retroalimentación inmediata, revisión de errores y resultado por categoría.
- Pausa, recuperación de sesión e historial de hasta 20 resultados en el mismo navegador, mediante localStorage.
- Sin anuncios, analítica, peticiones externas ni registro. Necesita internet para cargar los archivos; no ofrece un modo sin conexión.
- No adapta automáticamente la dificultad. Las etapas siguen una secuencia fija; las preguntas dentro de cada etapa se seleccionan al azar.
- América del Norte y América del Sur se presentan como regiones de América. Ciudad de México se distingue de los 31 estados.
- Para la etapa visual se usa la convención escolar de cinco continentes habitados: América, Europa, Asia, África y Oceanía. Los mapas se derivan de Natural Earth, cuyos datos vectoriales son de dominio público.

## Publicar en GitHub Pages

En el repositorio: Settings → Pages → Build and deployment → Source: Deploy from a branch → Branch: main → Folder: / (root) → Save.

Cuando termine el despliegue, abre https://unamismx.github.io/geojade/ en Safari. Usa Compartir → Añadir a pantalla de inicio.

El avance queda en ese navegador y dispositivo. Borrar sus datos o usar navegación privada puede impedir su conservación. No se sincroniza entre dispositivos.

## Desarrollo

No requiere instalación ni compilación. `python3 -m http.server 8000` sirve el proyecto localmente. `python3 generate.py` regenera `questions.js`; `python3 make_map.py` regenera `map-data.js` y descarga el GeoJSON público de Natural Earth si no está presente.
