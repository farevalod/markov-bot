markov-bot:  Procesamiento de lenguaje y generación automática de mensajes
utilizando expresiones regulares y cadenas de Markov.

CADENAS DE MARKOV
Sistema matematico que se transforma de un estado al otro,
con la propiedad de que el estado siguiente depende solo
de el estado actual, y no de los estados pasados.

Estados: palabras
Estado actual: Ultimas dos palabras

Se almacenan en una tabla valores [(p1, p2), px, py, pz...]
donde (p1, p2) son un par de palabras, y px, py, y pz son
posibles continuaciones leidas en algun tweet.
Los estados siguientes solo dependen de las dos ultimas
palabras, lo que puede llevar a resultados interesantes.

Nota:   Para buen funcionamiento del algoritmo de Markov, es necesario
        contar con una buena cantidad de texto de entrada. La calidad
        de los mensajes generados dependerá mucho de los usuarios que
        siga la cuenta utilizada. Debido a la gran cantidad de mensajes
        descargados, la actualización puede tomar hasta 30 segundos.

Francisco Arevalo
