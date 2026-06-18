# Code Smells en `statement()`

## 1. Long Function
`statement` hace demasiadas cosas a la vez: calcula montos, calcula créditos de volumen, formatea moneda y construye el string de salida. Debería dividirse en funciones más pequeñas (calcular monto por función, calcular créditos por función, generar el statement por función).

## 2. Función anidada con responsabilidad propia
`format_as_dollars` está definida dentro de `statement`, pero es una utilidad de formato genérica que no depende del estado de la función externa. Debería ser una función de nivel superior (o un módulo de utilidades), reutilizable y testeable de forma aislada.

## 3. Condicionales basados en tipo (Switch en tipo / type-checking)
El bloque `if play['type'] == "tragedy" / elif == "comedy" / else raise` es un code smell clásico (*type code*). Cada vez que se agregue un nuevo tipo de obra hay que tocar esta función. Es un candidato perfecto para **polimorfismo** (una clase o estrategia por tipo de obra) o un diccionario de funciones de cálculo.

## 4. Lógica duplicada / repetida (type-check repetido)
El tipo de obra se vuelve a comparar más abajo (`if "comedy" == play["type"]`) para calcular los créditos de volumen. Es la misma condición evaluada dos veces en dos lugares distintos, lo que viola DRY y hace fácil que ambas ramas queden inconsistentes si se modifica una sin la otra.

## 5. Magic Numbers
Hay múltiples números "mágicos" sin explicación de su significado: `40000`, `30000`, `30`, `1000`, `20`, `10000`, `500`, `300`, `5`. No queda claro qué representan (¿son centavos? ¿reglas de negocio?) ni por qué tienen esos valores. Deberían ser constantes con nombre (`BASE_TRAGEDY_AMOUNT`, `AUDIENCE_THRESHOLD`, etc.) o, mejor, vivir dentro de la lógica específica de cada tipo de obra.

## 6. Mutación incremental de variables acumuladoras (side effects en bucle)
`total_amount`, `volume_credits` y `result` se van mutando dentro del bucle `for`. Esto mezcla cálculo de datos con construcción de texto, dificultando testear cada cálculo por separado.

## 7. Mezcla de niveles de abstracción
Dentro del mismo `for` se mezcla: cálculo de negocio (montos, créditos), formateo de presentación (`format_as_dollars`, armado del string) y construcción del reporte final. Esto dificulta reutilizar la lógica de cálculo en otro contexto (por ejemplo, generar un reporte en HTML).

## 8. Falta de estructura de datos intermedia
No existe un objeto/diccionario que represente "el desempeño calculado" (obra, monto, créditos, audiencia). Toda la información viaja como variables sueltas, lo que complica extender el cálculo o reusarlo (Refactoring de Fowler lo resuelve introduciendo algo como `PerformanceCalculator`).

## 9. Nombres poco descriptivos
`perf`, `this_amount` son nombres genéricos. Por ejemplo, `this_amount` podría ser `performance_amount`, y `perf` podría ser `performance`.

## 10. Manejo de errores con `raise` en medio del flujo de cálculo
El `raise ValueError` está bien en sí, pero combinado con todo lo demás, agrava el problema de "Long Function": el control de errores, el cálculo y el formateo están todos entrelazados.

## 11. Construcción de strings con concatenación (`result +=`)
Construir el reporte con concatenaciones sucesivas de string mezcla la responsabilidad de "calcular datos" con "renderizar texto". Sería más flexible separar el cálculo de datos del renderizado (por ejemplo, devolver una lista de líneas o un objeto con los datos y generar el texto en una función separada).

## 12. Comentarios que indican que el código no se explica solo
Comentarios como `# add volume credits` o `# print line for this order` son señales de que el código podría (y debería) ser más expresivo por sí mismo, por ejemplo extrayendo esas líneas a funciones con nombres claros (`add_volume_credits_for(perf)`).

## 13. Lineas sin contenido al final del codigo
El estilizado de python requiere que la ultima linea de codigo no sea una linea vacía.
