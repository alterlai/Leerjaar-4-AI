import itertools
import time

solution_found = False
start = time.clock()
for (L, M, N, E, J) in list(itertools.permutations([0,1,2,3,4])):
    # Marja mag niet op de began grond
    if M == 0:
        continue

    # NIels mag niet op de begane grond
    if N == 0:
        continue

    # Loes mag niet op de bovenste verdieping
    if L == 4:
        continue

    # Niels mag niet op de bovenste verdieping
    if N == 4:
        continue

    # Erik woont hoger dan marja
    if E - M < 0:
        continue

    # Joop en erik mogen niet onder of boven elkaar wonen.
    if abs(J-E) == 1:
        continue

    #Niels en marja mogen niet onder of boven elkaar wonen.
    if abs(N-M) == 1:
        continue

    # Als we hier komen voldoet de permutatie aan alle voorwaarden
    print("Solution:")
    print("L", L)
    print("M", M)
    print("N", N)
    print("E", E)
    print("J", J)
    break

end = time.clock()
print("Time:", end - start)



