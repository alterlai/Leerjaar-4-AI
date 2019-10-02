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
dfs_count = 0

def brute_force():
    count = 0  # telling van hoeveelheid iteraties voor hij de eerste oplossing vindt.
    solution_found_at_iteration = 0

    for permutatie in list(itertools.permutations(stapel)):
        count += 1
        found_solution = True       # Zet solution op true als tot hij wordt getriggerd door constraints.
        permutatie = {i:permutatie[i] for i in range(0,len(permutatie))}    # conversie naar dictionary

        if is_geldig_bord(permutatie):
            if solution_found_at_iteration == 0:
                solution_found_at_iteration = count
            solutions.append(permutatie)

    for solution in solutions:
        print_layout(solution)
    print("Oplossing gevonden bij iteratie: ", solution_found_at_iteration)


def dfs(stapel, bord_index=0, bord=None):
    global dfs_count
    dfs_count += 1
    # Maak een bord aan om kaarten op te leggen.
    if bord == None:
        bord = {i: '' for i in range(0,8)}

    if bord_index == len(bord):  # aangekomen bij de laatste kaart, en het bord is geldig. Oplossing gevonden!
        solutions.append(bord)
        return

    # Loop over alle kaarten die nog over zijn.
    for kaart in stapel:
        bord[bord_index] = kaart            # Plaats de kaart op het bord
        if is_geldig_bord(bord):
            nieuwe_stapel = stapel.copy()               # Maak een kopie van de stapel.
            nieuwe_stapel.remove(kaart)                # Verwijder de kaart uit de stapel
            dfs(nieuwe_stapel, bord_index+1, bord.copy())  # Als het een geldige bord state is, ga dieper.






def is_geldig_bord(bord):
    for current_index, kaart in bord.items():
        buren = list(bord[index] for index in grenzingen[current_index])  # Maak een lijst met kaarten die grenzen aan de huidige kaart.

        # elke Aas grenst aan een Heer
        if kaart == 'A' and 'H' not in buren and '' not in buren:
            return False

        # elke Heer grenst aan een Vrouw
        if kaart == 'H' and 'V' not in buren and '' not in buren:
            return False

        # Dezeflde kaarten mogen niet naast elkaar liggen
        if kaart != '' and kaart in buren:
            return False

        # elke Vrouw grenst aan een Boer
        if kaart == 'V' and 'B' not in buren and '' not in buren:
            return False

        # een (elke) aas grenst niet aan een vrouw.
        if kaart == 'A' and 'V' in buren and '' not in buren:
            return False


    return True

def print_layout(solution):
    print("[ ][ ][{}][ ]".format(solution[0]))
    print("[{}][{}][{}][ ]".format(solution[1], solution[2], solution[3]))
    print("[ ][{}][{}][{}]".format(solution[4], solution[5], solution[6]))
    print("[ ][ ][{}][]".format(solution[7]))
    print("-----------------------------")


brute_force()
for solution in solutions:
    print_layout(solution)

solutions = []
dfs(stapel)
for solution in solutions:
    print_layout(solution)
print("DFS count:", dfs_count)


