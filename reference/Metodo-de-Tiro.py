# Fecha: 22 de octubre de 2023
# Descripción: Calculo del control óptimo para el problema de saturación por contraste de magnetización para MRI en el caso de dos particulas y control mono-entrada.
#              El control se calculará mediante el método de tiro.

# Importamos las librerias necesarias
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import minimize
import matplotlib.pyplot as plt
from typing import Callable
from scipy.interpolate import interp1d


# Definimos las constantes del sistema
omega   = 202.946885422
T11     = 2 
T12     = 0.3
T21     = 2.5
T22     = 2.5
G1, g1  = 1/(T12*omega), 1/(T11*omega)  # Constantes de relajación de q1
G2, g2  = 1/(T22*omega), 1/(T21*omega)  # Constantes de relajación de q2
G,g     = (G1,G2), (g1,g2) # Constantes de relajación
T_min   = 26.17040   # Tiempo mínimo de saturación de q1

q0 = (0,1,0,1) # Condicion inicial

def arrayOesca(data:any)->None:
    """
    Esta función verifica si la entrada es un escalar o un arreglo de NumPy de escalares.

    :param data: Los datos de entrada que se van a verificar.
    """
    return np.isscalar(data) or (isinstance(data, np.ndarray) and np.isscalar(data).all()), "La entrada no es un escalar ni un arreglo de NumPy de escalares."

# Definimos la función que determina la dinámica del sistema (q' = f(q,u)) donde q = (q1,q2).
def f(q:np.array, u:float, G:tuple, g:tuple) -> np.array:
    """Dinámica dada por Bloch.

    Args:
        q (np.array): Vector de magnetización (q_1,q_2)
        u (float): Función de control
        G (tuple): Constantes de relajación
        g (tuple): Constantes de relajación

    Returns:
        np.array: Derivada de los vectores de magnetización

    Raises:
        AssertionError: Si q no es un np.ndarray.
        AssertionError: Si u no es un float.
        AssertionError: Si las dimensiones de q no es 2.
        AssertionError: Si G no es un tuple.
        AssertionError: Si g no es un tuple.
    """
    assert type(q) == np.ndarray, "q debe ser un np.ndarray."
    assert arrayOesca(u), "u debe ser un escalar o escalares en un ndarray."
    assert q.shape == (4,), "q debe ser un vector de dimensión 4."
    assert type(G) == tuple, "G debe ser un tuple."
    assert type(g) == tuple, "g debe ser un tuple."
    u1  = u
    #Coeficientes de relajación
    G_1, G_2 = G
    g_1, g_2 = g
    #Particulas
    q_1 = q[0:2]    #Primera particula
    q_2 = q[2:4]    #Segunda particula
    #Dinámicas
    f_1y = -G_1 * q_1[0] - u1 * q_1[1]
    f_1z = g_1 * (1-q_1[1]) + u1 * q_1[0]
    f_2y = -G_2 * q_2[0] - u1 * q_2[1]
    f_2z = g_2 * (1-q_2[1]) + u1 * q_2[0]
    return np.array([f_1y, f_1z, f_2y, f_2z])


U = []
#Solución del sistema acoplado a partir de una posisción inicial para el vector adjunto p
def sol_X(p0:np.array, G:tuple, g:tuple, t_f:float) -> np.array:
    """Trayectoria y vector adjunto asociado a la condición inicial p0 y coeficientes de relajación G,g para el tiempo final t_f.

    Args:
        p0 (np.array): Vector adjunto inicial
        G (tuple): Constantes de relajación
        g (tuple): Constantes de relajación
        t_f (float): Tiempo final

    Returns:
        np.array: Trajectoria y vector adjunto asociada al problema.

    Raises:
        AssertionError: Si p0 no es un np.ndarray.
        AssertionError: Si las dimensiones de p0 no es 4.
        AssertionError: Si G no es un tuple.
        AssertionError: Si g no es un tuple.
        AssertionError: Si t_f no es un escalar.
    """
    assert type(p0) == np.ndarray, "p0 debe ser un np.ndarray."
    assert p0.shape == (4,), "p0 debe ser un vector de dimensión 4."
    assert type(G) == tuple, "G debe ser un tuple."
    assert type(g) == tuple, "g debe ser un tuple."
    assert arrayOesca(t_f), "t_f debe ser un escalar o un array de escalares."
    #Coeficientes de relajación
    G_1, G_2 = G
    g_1, g_2 = g
    #Posición inicial
    x0 = np.array([q0[0],q0[1],q0[2],q0[3],p0[0],p0[1],p0[2],p0[3]])
    # Definimos la dinámica del sistema
    def dinamica(t,X):
        q,p = X[0:4],X[4:8]
        G_  = lambda q: np.array([-q[1],q[0],-q[3],q[2]])
        H_G = lambda q,p: p@G_(q)
        if abs(H_G(q,p)) > 10**-2:
            u1  = np.sign(H_G(q,p))
        else:
            d1 = g_1 - G_1
            d2 = g_2 - G_2
            GFF = np.array([g_1*(g_1-2*G_1)-d1**2*q[1], d1**2*q[0], g_2*(g_2-2*G_2)-d2**2*q[3], d2**2*q[2]])
            GFG = np.array([2*d1*q[0], g_1-2*d1*q[1], 2*d2*q[2], g_2-2*d2*q[3]])
            HGHFHF = p@GFF
            HGHFHG = p@GFG
            if abs(HGHFHG)  != 0:
                u1  = -HGHFHF/HGHFHG
            else:
                u1 = 0
        U.append(u1)
        q_dot = f(q,u1,G,g)
        p_dot = np.array([p[0]*G_1-p[1]*u1, p[0]*u1+p[1]*g_1, p[2]*G_2-p[3]*u1, p[2]*u1+p[3]*g_2])
        X_dot = np.array([q_dot,p_dot]).flatten()
        return X_dot
    sol = solve_ivp(dinamica, (0,t_f), x0, dense_output=True, t_eval=np.linspace(0, t_f, 1000))
    return interp1d(sol.t, sol.y, kind='linear')


# Definimos la función (or minimizar) que nos da el error entre el valor calculado y el valor esperado en las condiciones de transversalidad de Pontryagin
def error(p0:np.array, G:tuple, g:tuple, t_f:float) -> float:
    """Error entre el valor calculado y el valor esperado en las condiciones de transversalidad.

    Args:
        p0 (np.array): Vector adjunto inicial
        G (tuple): Constantes de relajación
        g (tuple): Constantes de relajación
        t_f (float): Tiempo final

    Returns:
        float: Error entre el valor calculado y el valor esperado en las condiciones de transversalidad.

    Raises:
        AssertionError: Si p0 no es un np.ndarray.
        AssertionError: Si las dimensiones de p0 no es 4.
        AssertionError: Si G no es un tuple.
        AssertionError: Si g no es un tuple.
        AssertionError: Si t_f no es un escalar.
    """
    assert type(p0) == np.ndarray, "p0 debe ser un np.ndarray."
    assert p0.shape == (4,), "p0 debe ser un vector de dimensión 4."
    assert type(G) == tuple, "G debe ser un tuple."
    assert type(g) == tuple, "g debe ser un tuple."
    assert arrayOesca(t_f), "t_f debe ser un escalar o un array de escalares."
    # Calculamos la trayectoria y el vector adjunto asociado a la condición inicial p0
    sol = sol_X(p0,G,g,t_f) # Trayectoria calculada
    q1  = sol(t_f)[0:2]     # Posición final de la primera partícula
    q2  = sol(t_f)[2:4]     # Posición final de la segunda particula
    p2  = sol(t_f)[6:8]     # Posición final del segundo vector adjunto
    p_0 = -1/2              # Constante de Pontryagin
    # Calculamos el error
    error = np.linalg.norm(q1) + np.linalg.norm(p2-(-2*p_0*q2))
    return error

# Encontramos la condición inicial del vector adjunto (p0) que minimiza el error
def p0(G:tuple, g:tuple, t_f:float) -> np.array:
    """Condición inicial del vector adjunto (p0) que minimiza el error.

    Args:
        G (tuple): Constantes de relajación
        g (tuple): Constantes de relajación
        t_f (float): Tiempo final

    Returns:
        np.array: Condición inicial del vector adjunto (p0) que minimiza el error.

    Raises:
        AssertionError: Si G no es un tuple.
        AssertionError: Si g no es un tuple.
        AssertionError: Si t_f no es un escalar.
    """
    assert type(G) == tuple, "G debe ser un tuple."
    assert type(g) == tuple, "g debe ser un tuple."
    assert arrayOesca(t_f), "t_f debe ser un escalar o un array de escalares."
    # Definimos la condición inicial del vector adjunto
    p0 = np.array([-0.0728204,0.0620243,0.306497,-0.582856])
    # Encontramos la condición inicial del vector adjunto que minimiza el error
    sol = minimize(error, p0, args=(G,g,t_f), method='Nelder-Mead', tol=1e-6)
    return sol.x

# Trayectoria óptima de las partículas q1 y q2
def sol_optimo(G:tuple, g:tuple, t_f:float) -> np.array:
    """Trayectoria óptima de las partículas q1 y q2.

    Args:
        G (tuple): Constantes de relajación
        g (tuple): Constantes de relajación
        t_f (float): Tiempo final

    Returns:
        np.array: Trayectoria óptima de las partículas q1 y q2.

    Raises:
        AssertionError: Si G no es un tuple.
        AssertionError: Si g no es un tuple.
        AssertionError: Si t_f no es un escalar.
    """
    assert type(G) == tuple, "G debe ser un tuple."
    assert type(g) == tuple, "g debe ser un tuple."
    assert arrayOesca(t_f), "t_f debe ser un escalar o un array de escalares."
    # Calculamos la condición inicial del vector adjunto que minimiza el error
    p_0 = p0(G,g,t_f)
    # Calculamos la trayectoria óptima de las partículas q1 y q2
    sol = sol_X(p_0,G,g,t_f)
    q1  = lambda t: sol(t)[0:2]
    q2  = lambda t: sol(t)[2:4]
    return q1,q2

# Graficamos las trayectorias de q1 y q2 en el intervalo [0,t_f] dentro de la bola de Bloch para G, g, t_f=1.1*T_min. El eje horizontal correspondiendo al eje y y el eje vertical al eje z.
t_f = 1.3*T_min
q1,q2 = sol_optimo(G,g,t_f)
t = np.linspace(0,t_f,1000)
q1 = q1(t)
q2 = q2(t)
plt.plot(q1[0],q1[1],label='q1')
plt.plot(q2[0],q2[1],label='q2')
plt.axis('equal')
plt.xlim([-1.05, 1.05])
plt.ylim([-1.05, 1.05])
plt.legend()
plt.xlabel('y')
plt.ylabel('z')
plt.title('Trayectorias de q1 y q2')
plt.show()