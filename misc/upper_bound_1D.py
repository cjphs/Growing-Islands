V = [0, 2, 6, 10, 20, 22]

P = [0.25, 2.05, 6.1, 19.9, 21]

# p_0 = P_{i-1}, p_1 = P_i, p_2 = P_{i+1}
# v_0 = V_{i}, v_1 = V_{i+1}
def compute_omega_step(p_0, p_1, p_2, v_0, v_1):
    c = (v_0 + v_1)/2
    
    omega_1 = (2*c - (p_0 + p_1))/(v_1 - v_0)
    omega_2 = (p_1 + p_2 - 2*c)/(v_1 - v_0)

    print(f"omega_1 = {omega_1}, omega_2 = {omega_2}")

    return min(omega_1, omega_2)


def compute_omega(V, P):
    omega = 999999
    for i in range(1, len(V)-2):
        w = compute_omega_step(P[i-1], P[i], P[i+1], V[i], V[i+1])
        omega = min(omega, w)
    
    return omega


omega = compute_omega(V, P)

if omega < 0:
    print("cringe ({omega} < 0, no solution)")
else:
    print(f"omega = {omega}")


for i in range(0, len(V)-1):
    v = V[i]
    v_next = V[i+1]

    c = (v + v_next)/2

    p = P[i]

    if i > 0:
        p_prev = P[i-1]
    else:
        p_prev = -999999

    if i < len(P)-1:
        p_next = P[i+1]
    else:
        p_next = 9999999

    l1 = c - omega * (c - v)
    l2 = c + omega * (v_next - c)

    a = (p - l1 <= l1 - p_prev)
    b = (l2 - p <= p_next - l2)

    print()
    print(f"{p_prev} |{v}|...{l1}  {p}  {l2}...|{v_next}| {p_next}")
    print(f"{p-l1} {l1-p_prev} {a}")
    print(f"{l2 - p} {p_next - l2} {b}")