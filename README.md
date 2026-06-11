# Proyecto-SO-FINAL
Trabajar en el proyecto de Sistemas Operativos 
Fecha de avance --> 11/06
Fecha de entrega --> 17/06

Esta es una explicacion del simulador(simulador_reemplazo.py):

Simulador de Algoritmos de Reemplazo de Páginas
Este proyecto implementa un simulador visual de algoritmos de reemplazo de páginas en memoria, desarrollado en Python utilizando la librería tkinter para la interfaz gráfica.

¿Qué problema resuelve?
En los sistemas operativos, cuando la memoria RAM está llena y un proceso necesita una nueva página, el sistema debe decidir cuál página sacar para hacer espacio. Los algoritmos de reemplazo de páginas definen esa lógica. Este simulador permite visualizar y comparar cómo se comporta cada algoritmo ante una misma secuencia de referencias.

Algoritmos implementados
FIFO (First In, First Out)
Reemplaza la página que lleva más tiempo en memoria. Es el más simple: funciona como una cola, la primera en entrar es la primera en salir. No considera si una página se usa frecuentemente o no.
LRU (Least Recently Used)
Reemplaza la página que no ha sido usada hace más tiempo. Lleva un registro del orden de uso reciente, por lo que toma decisiones más inteligentes que FIFO. Es uno de los más usados en la práctica.
OPT — Óptimo
Reemplaza la página que tardará más tiempo en volver a ser usada en el futuro. Produce la menor cantidad de fallos de página posible, pero es teórico: en la realidad no se puede predecir el futuro. Sirve como referencia para comparar los demás algoritmos.
Clock (Segunda Oportunidad)
Variante eficiente de LRU. Usa un puntero circular y un bit de referencia por página. Si una página fue usada recientemente, se le da una "segunda oportunidad" antes de ser reemplazada. Es práctico y con buen rendimiento.

Funcionamiento del simulador
El usuario ingresa una cadena de referencias de páginas (secuencia de números que representan las páginas que solicita un proceso), define el número de marcos de página disponibles en memoria, y selecciona el algoritmo a simular.
El simulador genera una tabla donde cada columna representa un acceso a una página. Se puede ver en tiempo real el estado de los marcos en cada paso, diferenciando visualmente con colores:

🟢 Verde — la página ya estaba en memoria (hit)
🔴 Rojo — la página no estaba y hubo fallo (fault)

Al final de cada tabla se muestra el total de fallos, hits y la tasa de fallos.
También cuenta con un botón "Comparar todos" que ejecuta los cuatro algoritmos simultáneamente con la misma entrada y señala cuál tuvo el mejor rendimiento.

Tecnologías usadas

Python 3 — lenguaje principal
tkinter — interfaz gráfica nativa de Python, sin dependencias externas
Integrantes:
-kevin hernandez 6902420020
-jose herrera 6902420001
-samuel porto 6902420035
-juan miguel ramirez ortiz 6902420038
