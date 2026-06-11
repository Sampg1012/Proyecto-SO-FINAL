def FIFO(procesos, tamanio_marco):
    rastreador = [[-1] * tamanio_marco for _ in range(len(procesos))]
    puntero = 0
    fallo_pagina = 0

    for i, pagina in enumerate(procesos):
        if i >= 1:
            rastreador[i] = list(rastreador[i - 1])

        if pagina not in rastreador[i]:
            fallo_pagina += 1
            rastreador[i][puntero] = pagina
            puntero = (puntero + 1) % tamanio_marco

    return {
        "pasos": rastreador,
        "procesos": procesos,
        "fallos_pagina": fallo_pagina,
        "tasa_fallos": round(fallo_pagina / len(procesos) * 100, 1)
    }