# Ejercicio 3: Dominio con recursos numéricos

Una vez visto el manejo de los fluents en PDDL2.1, y sus posibles modificaciones (assign, increase, decrease), realiza las siguientes tareas:

1) Define una variable numérica que represente el consumo de un recurso, tal que el consumo del recurso sea inversamente proporcional al consumo de tiempo; es decir, a menos tiempo, más consumo del recurso.

Definimos la variable fuel de la grua. Cuanto más rápido vaya la grua, más combustible y menos tiempo.
Por el contrario, si la grua va lenta, gastará menos combustible pero más tiempo.


2) Define dos versiones del dominio:
    a. Una versión donde el recurso no sea renovable, es decir, no se puede recargar
    b. Una versión donde el recurso es renovable

3) Ejecuta dos instancias de cada nuevo dominio con LPG. Recuerda que la función a
optimizar ahora será: (:metric minimize (<recurso-definido>))

4) Ejecuta las mismas instancias de cada dominio pero minimizando el tiempo:
(:metric minimize (total-time))

5) Compara los resultados obtenidos.