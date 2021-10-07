import matplotlib.pyplot as plt
plt.plot([1, 10, 50, 100], [203714, 203714, 203714, 203714], marker=".", label="cota inferior")
plt.plot([1, 10, 50, 100], [303198, 298286, 290215, 290215], marker=".", label="heuristica")
plt.axis([0, 100, 200000, 303400])
plt.legend()
plt.ylabel('Distancia')
plt.xlabel('Iteraciones')
plt.title('Impacto delas iteraciones en la distancia')
plt.show()
