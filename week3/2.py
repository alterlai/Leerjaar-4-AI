import itertools

# A) 8 kaarten: A, A, H, H, V, V, B, B
# 8 variabelen met een domein van 8. Bij elke beurt mag je 1 minder kiezen dus 8! = 40320 Permutaties.

stapel =  ['A', 'A', 'H', 'H', 'V', 'V', 'B', 'B']
grenzingen = {
    0 : [3],
    1 : [2],
    2 : [1, 4, 4],
    3 : [0, 2, 5],
    4 : [2, 5],
    5 : [3, 6, 7, 4],
    6 : [5],
    7 : [5]
}
solutions = []

def brute_force():
    count = 0  # telling van hoeveelheid iteraties voor hij de eerste oplossing vindt.
    solution_found_at_iteration = 0

    for permutatie in list(itertools.permutations(stapel)):
        count += 1
        found_solution = True       # Zet solution op true als tot hij wordt getriggerd door constraints.
        permutatie = {i:permutatie[i] for i in range(0,len(permutatie))}    # conversie naar dictionary

        for current_index, kaart in permutatie.items():
            buren = list(permutatie[index] for index in grenzingen[current_index])  # Maak een lijst met kaarten die grenzen aan de huidige kaart.

            # elke Aas grenst aan een Heer
            if kaart == 'A' and 'H' not in buren:
                found_solution = False

            # elke Heer grenst aan een Vrouw
            if kaart == 'H' and 'V' not in buren:
                found_solution = False

            # elke Vrouwgrenst aan een Boer
            if kaart == 'V' and 'B' not in buren:
                found_solution = False

            # een (elke) aas grenst niet aan een vrouw.
            if kaart == 'A' and 'V' in buren:
                found_solution = False

            # Dezeflde kaarten mogen niet naast elkaar liggen
            if kaart in  buren:
                found_solution = False

        if found_solution:
            if solution_found_at_iteration == 0:
                solution_found_at_iteration = count
            solutions.append(permutatie)

    for solution in solutions:
        print_layout(solution)
    print("Oplossing gevonden bij iteratie: ", solution_found_at_iteration)

def print_layout(solution):
    print("[ ][ ][{}][ ]".format(solution[0]))
    print("[{}][{}][{}][ ]".format(solution[1], solution[2], solution[3]))
    print("[ ][{}][{}][{}]".format(solution[4], solution[5], solution[6]))
    print("[ ][ ][{}][]".format(solution[7]))
    print("-----------------------------")

brute_force()



