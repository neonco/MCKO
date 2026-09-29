import numpy as np

def gradient_descent(func, start_point, gamma, epsilon, steps):
    x = start_point
    start_lambda = 1e-9
    out = np.array([start_point])

    grad = (func(x + start_lambda) - func(x)) / start_lambda
    next_x = x - gamma * grad
    np.append(out, next_x)

    if steps == 0:
        while True:
            grad = (func(next_x) - func(x)) / (next_x - x)
            x, next_x = next_x, x - gamma * grad
            out = np.append(out, next_x)

            if np.linalg.norm(np.array(func(next_x) - func(x))) < epsilon:
                break

    else:
        for i in range(steps - 1):
            next_x, x = x - gamma * (func(next_x) - func(x)) / (next_x - x), next_x
            out = np.append(out, [next_x, func(next_x)])

    return out.reshape(-1, 1)