import numpy as np

def calculate_distance(lm1,lm2):
        # Эта функция должна дать расстояние между лендмарками, на основе растояний расчитать интенсивность динамики
        # temp solution
        return np.linalg.norm(np.array([lm1.x, lm1.y, lm1.z]) - np.array([lm2.x, lm2.y, lm2.z]))


# Note velocity calculator
def velocity_calculator(val):
    return int(val / 4)


rows, cols = 4, 4
dy, dx = h / rows, w / cols

