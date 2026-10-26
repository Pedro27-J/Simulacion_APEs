; APE 4 - VISUALIZACION DE PYTHON EN NETLOGO
; NetLogo NO calcula contagios: importa resultados_python.csv.
; Compatible con el CSV producido por python/view.py (CsvExporter).
; Los agentes son una representacion de los conteos agregados del CSV.

extensions [csv]

globals [
  datos-sir
  indice-actual
  cargado?
  tiempo-actual
  susceptibles-actuales
  infectados-actuales
  recuperados-actuales
  pico-infectados
  tiempo-pico
]

turtles-own [ estado-sir ]

; Lee el archivo ubicado junto al modelo .nlogo.
to cargar-python
  clear-all
  set cargado? false

  if not file-exists? "resultados_python.csv" [
    user-message "No se encontro resultados_python.csv. Copialo en la misma carpeta del modelo de NetLogo."
    stop
  ]

  let contenido csv:from-file "resultados_python.csv"
  if empty? contenido [
    user-message "El archivo CSV esta vacio."
    stop
  ]
  if (first contenido) != ["tiempo" "susceptibles" "infectados" "recuperados"] [
    user-message "Encabezado invalido. Se requiere: tiempo,susceptibles,infectados,recuperados"
    stop
  ]

  set datos-sir but-first contenido
  if empty? datos-sir [
    user-message "El CSV no contiene resultados."
    stop
  ]

  let primera first datos-sir
  if length primera != 4 [ error "La primera fila tiene un numero incorrecto de columnas." ]
  let poblacion sum (but-first primera)
  if poblacion <= 0 [ error "La poblacion debe ser positiva." ]

  ; Comprueba que todos los registros sean consecutivos y mantengan el total.
  let previo-t -1
  let previo-s poblacion
  let previo-r 0
  foreach datos-sir [ fila ->
    if length fila != 4 [ error "Cada registro debe tener cuatro columnas." ]
    let t item 0 fila
    let s item 1 fila
    let i item 2 fila
    let r item 3 fila
    if not (is-number? t and is-number? s and is-number? i and is-number? r) [
      error "El CSV contiene un valor no numerico."
    ]
    if t != (previo-t + 1) [ error "Los tiempos deben ir desde 0, de uno en uno." ]
    if (s < 0 or i < 0 or r < 0 or (s + i + r) != poblacion) [
      error "Los conteos S, I, R deben ser no negativos y sumar la misma poblacion."
    ]
    if (s > previo-s or r < previo-r) [
      error "Los susceptibles no pueden aumentar ni los recuperados disminuir."
    ]
    set previo-t t
    set previo-s s
    set previo-r r
  ]

  set pico-infectados max (map [ fila -> item 2 fila ] datos-sir)
  let fila-del-pico first (filter [ fila -> (item 2 fila) = pico-infectados ] datos-sir)
  set tiempo-pico item 0 fila-del-pico
  random-seed 42  ; solamente la representacion, NO el modelo Python

  create-turtles poblacion [
    set shape "person"
    set size 0.85
    set heading 0
    setxy ((who mod 10) - 4.5) (4.5 - floor (who / 10))
    set estado-sir "S"
    set color green
  ]

  set cargado? true
  set indice-actual 0
  aplicar-fila
  graficar-todo
  reset-ticks
end

; Muestra todo el historial (0..100) inmediatamente al cargar.
to graficar-todo
  foreach datos-sir [ fila ->
    let t item 0 fila
    let s item 1 fila
    let i item 2 fila
    let r item 3 fila

    set-current-plot "EVOLUCION SIR (PYTHON)"
    set-current-plot-pen "S"
    plotxy t s
    set-current-plot-pen "I"
    plotxy t i
    set-current-plot-pen "R"
    plotxy t r

    set-current-plot "SUSCEPTIBLES"
    plotxy t s
    set-current-plot "INFECTADOS"
    plotxy t i
    set-current-plot "RECUPERADOS"
    plotxy t r
  ]
end

; Reproduce un paso temporal del CSV en la poblacion mostrada.
to avanzar
  if not cargado? [
    user-message "Primero presiona CARGAR PYTHON."
    stop
  ]
  if indice-actual >= ((length datos-sir) - 1) [ stop ]
  set indice-actual indice-actual + 1
  aplicar-fila
  tick
  wait (0.4 / velocidad)
end

; El boton REPRODUCIR es Forever. La parada sucede aqui para
; detener realmente el boton al terminar el ultimo registro.
to reproducir
  if not cargado? [
    user-message "Primero presiona CARGAR PYTHON."
    stop
  ]
  if indice-actual >= ((length datos-sir) - 1) [ stop ]
  avanzar
end

; Reconstruye el estado inicial usando los datos ya cargados.
to reiniciar
  if not cargado? [
    user-message "Primero presiona CARGAR PYTHON."
    stop
  ]
  set indice-actual 0
  ask turtles [
    set estado-sir "S"
    set color green
  ]
  aplicar-fila
  reset-ticks
end

; Actualiza el total de agentes respetando cada conteo del archivo CSV.
; El CSV solo contiene conteos, no identidades individuales.
; Por ello, se seleccionan agentes ilustrativos para representar cambios.
to aplicar-fila
  let fila item indice-actual datos-sir
  set tiempo-actual item 0 fila
  set susceptibles-actuales item 1 fila
  set infectados-actuales item 2 fila
  set recuperados-actuales item 3 fila

  let recuperaciones (recuperados-actuales - (count turtles with [ estado-sir = "R" ]))
  if recuperaciones > 0 [
    ask (n-of recuperaciones (turtles with [ estado-sir = "I" ])) [
      set estado-sir "R"
      set color blue
    ]
  ]

  let contagios ((count turtles with [ estado-sir = "S" ]) - susceptibles-actuales)
  if contagios > 0 [
    ask (n-of contagios (turtles with [ estado-sir = "S" ])) [
      set estado-sir "I"
      set color red
    ]
  ]

  if (count turtles with [ estado-sir = "S" ]) != susceptibles-actuales [
    error "No coincide el conteo de susceptibles con el CSV."
  ]
  if (count turtles with [ estado-sir = "I" ]) != infectados-actuales [
    error "No coincide el conteo de infectados con el CSV."
  ]
  if (count turtles with [ estado-sir = "R" ]) != recuperados-actuales [
    error "No coincide el conteo de recuperados con el CSV."
  ]
end

@#$#@#$#@
GRAPHICS-WINDOW
20
133
472
581
-1
-1
29.0
1
10
1
1
1
0
1
1
1
-6
6
-6
6
1
1
1
ticks
30.0

BUTTON
20
25
158
62
CARGAR PYTHON
cargar-python
NIL
1
T
OBSERVER
NIL
NIL
NIL
NIL
1

BUTTON
168
25
270
62
PASO
avanzar
NIL
1
T
OBSERVER
NIL
NIL
NIL
NIL
1

BUTTON
280
25
398
62
REPRODUCIR
reproducir
T
1
T
OBSERVER
NIL
NIL
NIL
NIL
0

BUTTON
407
25
527
62
REINICIAR
reiniciar
NIL
1
T
OBSERVER
NIL
NIL
NIL
NIL
1

SLIDER
20
74
307
107
velocidad
velocidad
1
10
4.0
1
1
NIL
HORIZONTAL

MONITOR
20
601
104
648
Tiempo
tiempo-actual
0
1
12

MONITOR
109
601
222
648
S (verde)
susceptibles-actuales
0
1
12

MONITOR
228
601
336
648
I (rojo)
infectados-actuales
0
1
12

MONITOR
341
601
461
648
R (azul)
recuperados-actuales
0
1
12

MONITOR
20
659
228
705
Pico infectados
pico-infectados
0
1
12

MONITOR
235
659
461
705
Tiempo del pico
tiempo-pico
0
1
12

PLOT
496
133
803
377
EVOLUCION SIR (PYTHON)
Tiempo
Personas
0.0
100.0
0.0
100.0
false
true
"" ""
PENS
"S" 1.0 0 -10899396 true "" ""
"I" 1.0 0 -2674135 true "" ""
"R" 1.0 0 -13345367 true "" ""

PLOT
815
133
1121
377
SUSCEPTIBLES
Tiempo
Personas
0.0
100.0
0.0
100.0
false
true
"" ""
PENS
"S" 1.0 0 -10899396 true "" ""

PLOT
496
390
803
633
INFECTADOS
Tiempo
Personas
0.0
100.0
0.0
100.0
false
true
"" ""
PENS
"I" 1.0 0 -2674135 true "" ""

PLOT
815
390
1121
633
RECUPERADOS
Tiempo
Personas
0.0
100.0
0.0
100.0
false
true
"" ""
PENS
"R" 1.0 0 -13345367 true "" ""

@#$#@#$#@
# APE 4: Integracion Python -> NetLogo

## Proposito
Visualizar el modelo SIR ya calculado por el programa Python + SimPy (semana 4).

NetLogo solamente lee `resultados_python.csv`. NO calcula nuevas infecciones ni recuperaciones.

## Uso
1. Poner `modelo_sir_netlogo.nlogo` y `resultados_python.csv` juntos.
2. Pulsar **CARGAR PYTHON** para importar las 101 filas, dibujar las cuatro graficas y mostrar t=0.
3. Pulsar **PASO** para mostrar el siguiente instante, o **REPRODUCIR** para animar los 100 pasos. Pulsar otra vez REPRODUCIR para detener.
4. Usar **REINICIAR** para volver al tiempo 0 con los mismos datos. Ajustar **velocidad** si se desea.

## Estados
- Verde = Susceptible
- Rojo = Infectado
- Azul = Recuperado

Cada persona grafica representa un individuo del total. El CSV no guarda IDs de personas;
la asignacion de colores a personas individuales es meramente ilustrativa, pero los
conteos S, I y R coinciden exactamente en cada paso con el CSV.

## Datos
Columnas: `tiempo,susceptibles,infectados,recuperados`.
Parametros de Python: N=100, infectados iniciales=5, beta=0.30, gamma=0.10,
100 pasos y semilla 42. Si se modifican en Python, regenerar y volver a cargar el CSV.

@#$#@#$#@
default
true
0
Polygon -7500403 true true 150 5 40 250 150 205 260 250

circle
false
0
Circle -7500403 true true 0 0 300

person
false
0
Circle -7500403 true true 110 5 80
Polygon -7500403 true true 105 90 120 195 90 285 105 300 135 300 150 225 165 300 195 300 210 285 180 195 195 90
Rectangle -7500403 true true 127 79 172 94
Polygon -7500403 true true 195 90 240 150 225 180 165 105
Polygon -7500403 true true 105 90 60 150 75 180 135 105

@#$#@#$#@
NetLogo 6.3.0
@#$#@#$#@

@#$#@#$#@

@#$#@#$#@

@#$#@#$#@

@#$#@#$#@
default
0.0
-0.2 0 0.0 1.0
0.0 1 1.0 0.0
0.2 0 0.0 1.0
link direction
true
0
Line -7500403 true 150 150 90 180
Line -7500403 true 150 150 210 180
@#$#@#$#@
1
@#$#@#$#@
