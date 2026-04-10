# la gramatica 
gramatica = [
    ('S', ['A', 'B', 'uno']),
    ('A', ['dos', 'B']),
    ('A', ['e']),
    ('B', ['C', 'D']),
    ('B', ['tres']),
    ('B', ['e']),
    ('C', ['cuatro', 'A', 'B']),
    ('C', ['cinco']),
    ('D', ['seis']),
    ('D', ['e']),
]

# los no terminales de la gramatica
no_terminales = ['S', 'A', 'B', 'C', 'D']

# CALCULAR FIRST
def calcular_first():
    # inicializo todos los FIRST vacios
    first = {}
    for nt in no_terminales:
        first[nt] = set()

    # repito hasta que no haya cambios
    hubo_cambio = True
    while hubo_cambio:
        hubo_cambio = False

        for izq, der in gramatica:
            tam_antes = len(first[izq])

            # si la produccion es epsilon la agrego directo
            if der == ['e']:
                first[izq].add('e')

            else:
                # recorro simbolo por simbolo el lado derecho
                for simbolo in der:
                    # si es terminal lo agrego y paro
                    if simbolo not in no_terminales:
                        first[izq].add(simbolo)
                        break
                    else:
                        # si es no terminal agrego su first sin epsilon
                        for x in first[simbolo]:
                            if x != 'e':
                                first[izq].add(x)

                        # si ese no terminal no puede ser epsilon, paro
                        if 'e' not in first[simbolo]:
                            break
                else:
                    # si todos los simbolos pueden ser epsilon
                    # entonces la cabeza tambien puede
                    first[izq].add('e')

            # si el conjunto cambio marco que hubo cambio
            if len(first[izq]) != tam_antes:
                hubo_cambio = True

    return first

#CALCULAR FOLLOW
def calcular_follow(first):
    # inicializo todos los FOLLOW vacios
    follow = {}
    for nt in no_terminales:
        follow[nt] = set()

    # el simbolo inicial siempre tiene $ en su follow
    follow['S'].add('$')

    # repito hasta que no haya cambios
    hubo_cambio = True
    while hubo_cambio:
        hubo_cambio = False

        for izq, der in gramatica:
            for i in range(len(der)):
                simbolo = der[i]

                # solo me interesan los no terminales
                if simbolo not in no_terminales:
                    continue

                tam_antes = len(follow[simbolo])

                # miro lo que viene despues del simbolo actual
                resto = der[i+1:]

                if len(resto) == 0:
                    # si no hay nada despues, agrego el follow de la cabeza
                    for x in follow[izq]:
                        follow[simbolo].add(x)

                else:
                    # calculo el first del resto
                    first_resto = set()
                    todos_epsilon = True

                    for s in resto:
                        if s not in no_terminales:
                            first_resto.add(s)
                            todos_epsilon = False
                            break
                        else:
                            for x in first[s]:
                                if x != 'e':
                                    first_resto.add(x)
                            if 'e' not in first[s]:
                                todos_epsilon = False
                                break

                    # agrego el first del resto al follow del simbolo
                    for x in first_resto:
                        follow[simbolo].add(x)

                    # si todo el resto puede ser epsilon
                    # agrego el follow de la cabeza
                    if todos_epsilon:
                        for x in follow[izq]:
                            follow[simbolo].add(x)

                if len(follow[simbolo]) != tam_antes:
                    hubo_cambio = True

    return follow


# CALCULAR PREDICCION
def calcular_prediccion(first, follow):
    prediccion = []

    for izq, der in gramatica:
        pred = set()

        # calculo el first del lado derecho
        first_der = set()
        todos_epsilon = True

        if der == ['e']:
            first_der.add('e')
        else:
            for s in der:
                if s not in no_terminales:
                    first_der.add(s)
                    todos_epsilon = False
                    break
                else:
                    for x in first[s]:
                        if x != 'e':
                            first_der.add(x)
                    if 'e' not in first[s]:
                        todos_epsilon = False
                        break

        # agrego el first sin epsilon
        for x in first_der:
            if x != 'e':
                pred.add(x)

        # si puede derivar epsilon agrego el follow
        if todos_epsilon or 'e' in first_der:
            for x in follow[izq]:
                pred.add(x)

        prediccion.append((izq, der, pred))

    return prediccion

first      = calcular_first()
follow     = calcular_follow(first)
prediccion = calcular_prediccion(first, follow)

print("===========================================")
print("GRAMATICA")
print("===========================================")
for izq, der in gramatica:
    print(izq, "->", ' '.join(der))

print()
print("===========================================")
print("CONJUNTOS FIRST")
print("===========================================")
for nt in no_terminales:
    print("FIRST(" + nt + ") =", first[nt])

print()
print("===========================================")
print("CONJUNTOS FOLLOW")
print("===========================================")
for nt in no_terminales:
    print("FOLLOW(" + nt + ") =", follow[nt])

print()
print("===========================================")
print("CONJUNTOS DE PREDICCION")
print("===========================================")
for izq, der, pred in prediccion:
    print("PRED(" + izq + " -> " + ' '.join(der) + ") =", pred)

print()
print("===========================================")
print("VERIFICACION LL(1)")
print("===========================================")
es_ll1 = True
for nt in no_terminales:
    vistos = {}
    for izq, der, pred in prediccion:
        if izq != nt:
            continue
        for token in pred:
            if token in vistos:
                print("CONFLICTO en", nt, ": el token", token, "aparece en dos reglas")
                print("  ->", nt, "->", ' '.join(vistos[token]))
                print("  ->", nt, "->", ' '.join(der))
                es_ll1 = False
            else:
                vistos[token] = der

if es_ll1:
    print("La gramatica SI es LL(1)")
else:
    print("La gramatica NO es LL(1)")
