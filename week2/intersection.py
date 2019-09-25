p1 = (2, 2)
q1 = (7, 7)
p2 = (3, 2)
q2 = (7, 6)

def ccw(A,B,C):
    return (C[1]-A[1]) * (B[0]-A[0]) > (B[1]-A[1]) * (C[0]-A[0])

# Return true if line segments AB and CD intersect
def intersect(A,B,C,D):
    return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)

print(intersect(p1, q1, p2, q2))


list = [1,2,3,4,5]
print(list[4:1:-1])