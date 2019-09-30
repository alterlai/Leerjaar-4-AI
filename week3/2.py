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

for permutatie in list(itertools.permutations(stapel)):
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

    if found_solution:
        break