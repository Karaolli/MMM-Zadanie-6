import numpy as np

def make_state_model(R, L, K_T, K_e, J, k): # Stworzenie macierzy modelu stanowego na podstawie parametrów układu
    A = np.array([[ -R/L, -K_e/L,    0],     # macierz stanu
                  [K_T/J,      0, -k/J],
                  [    0,      1,    0]])
    B = np.array([[1/L],                     # macierz sterowania/wejścia
                  [  0],
                  [  0]])
    C = np.array([[1, 0, 0],                 # macierz obserwacji/wyjścia
                  [0, 1, 0],
                  [0, 0, 1]])
    D = np.array([[0],                       # macierz sprzężenia bezpośredniego (w rzeczywistych układach równa 0)
                  [0],
                  [0]])
    return A, B, C, D
    #print(np.linalg.eigvals(A))

def rk4_step(x, u, dt, A, B, C, D): # Jeden krok symulacji za pomocą metody Rungego-Kutty 4-go rzędu
    def dxdt(x, u):
        return A @ x + B * u
    
    k1 = dxdt(x          , u)
    k2 = dxdt(x + k1*dt/2, u)
    k3 = dxdt(x + k2*dt/2, u)
    k4 = dxdt(x + k3*dt  , u)

    x += dt * (k1 + 2*k2 + 2*k3 + k4) / 6

    y = C @ x + D * u

    return x, y

def simulate(x0, u, dt, A, B, C, D): # Całkowita symulacja układu dla danego stanu początkowego oraz sygnału wejściowego
    x = x0
    y = np.zeros((len(u), C.shape[0]))
    for i in range(len(u)):
        x, y1 = rk4_step(x, u[i], dt, A, B, C, D)
        y[i] = y1.flatten()
    return y