V = [0, 2, 6, 10, 20, 22]

P = [1, 4, 8, 19, 21]


# p_0 = P_{i-1}, p_1 = P_i, p_2 = P_{i+1}
# v_0 = V_{i}, v_1 = V_{i+1}
def compute_omega_step(p_0, p_1, p_2, v_0, v_1):
    c = (v_0 + v_1) / 2

    omega_1 = (2 * c - (p_0 + p_1)) / (v_1 - v_0)
    omega_2 = (p_1 + p_2 - 2 * c) / (v_1 - v_0)

    return min(omega_1, omega_2)


def compute_omega(V, P):
    omega = 999999
    for i in range(1, len(V) - 2):
        w = compute_omega_step(P[i - 1], P[i], P[i + 1], V[i], V[i + 1])
        omega = min(omega, w)

    return omega


def check_satisfied(V, P, omega):
    for i in range(0, len(V) - 1):
        v = V[i]
        v_next = V[i + 1]

        c = (v + v_next) / 2

        p = P[i]

        if i > 0:
            p_prev = P[i - 1]
        else:
            p_prev = -999999

        if i < len(P) - 1:
            p_next = P[i + 1]
        else:
            p_next = 9999999

        l1 = c - omega * (c - v)
        l2 = c + omega * (v_next - c)

        a = p - l1 <= l1 - p_prev
        b = l2 - p <= p_next - l2

        if not (a and b):
            return False
    return True


def compute_nudge_directions(V, P, omega, phi=1):
    N = [0 for _ in range(len(P))]

    for i in range(1, len(P) - 2):
        v = V[i]
        v_next = V[i + 1]

        p = P[i]
        p_prev = P[i - 1]
        p_next = P[i + 1]

        l1 = v
        l2 = v_next

        a = p - l1 <= l1 - p_prev
        b = l2 - p <= p_next - l2

        if not a:
            N[i] += (l1 - p) * phi
            N[i - 1] += (p_prev - l1) * phi
        if not b:
            N[i] += (l2 - p) * phi
            N[i + 1] += (p_next - l1) * phi

    nudged = [min(max(p + n, v), v_next) for p, n in zip(P, N)]

    return nudged


omega = compute_omega(V, P)

P2 = compute_nudge_directions(V, P, 1, 0.6)

print(P)
print(P2, compute_omega(V, P2))

phi = 0.05

for i in range(20):
    P2 = compute_nudge_directions(V, P2, omega, phi)
    o = compute_omega(V, P2)
    print(P2)
    print(o, phi)
    phi += 0.05

if omega < 0:
    print("cringe ({omega} < 0, no solution)")
else:
    print(f"omega = {omega}")

print(f"Is satisfied: {check_satisfied(V, P, omega)}")
print(f"Is satisfied: {check_satisfied(V, P, 1)}")
