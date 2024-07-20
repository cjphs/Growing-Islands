V = [0, 2, 6, 10, 18, 20]
C = [1, 4, 8, 15, 21]

def f(v_0, v_1, v_2, v_3):
    top = (v_3 - v_0)
    bottom = v_2 - v_1
    print(f"{top} / {bottom}")

    return (top/bottom)/2

omega = 999999
for i in range(1, len(V)-2):
    w = f(V[i-1], V[i], V[i+1], V[i+2])
    print(w)
    omega = min(omega, w)

print(omega)

for i in range(0, len(V)-1):
    v = V[i]
    v_next = V[i+1]

    c = C[i]

    if i > 0:
        c_prev = C[i-1]
    else:
        c_prev = -999999

    if i < len(C)-1:
        c_next = C[i+1]
    else:
        c_next = 9999999

    l1 = c - omega * (c - v)
    l2 = c + omega * (v_next - c)

    a = (c - l1 <= l1 - c_prev)
    b = (l2 - c <= c_next - l2)

    print()
    print(f"{c_prev} |{v}|...{l1}  {c}  {l2}...|{v_next}| {c_next}")
    print(f"{c-l1} {l1-c_prev} {a}")
    print(f"{l2 - c} {c_next - l2} {b}")

    print()
    print()