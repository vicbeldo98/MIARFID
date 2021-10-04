import matplotlib.pyplot as plt
plt.plot([418, 836, 1254, 1672, 2090], [330000, 294512, 308610, 313638, 308004], marker=".")
# plt.plot([2, 50, 100, 1000, 10000], [0.25, 18.20, 35, 174.41, 2304.28], marker=".", label="heuristics")
plt.axis([400, 2100, 290000, 320000])
# plt.legend()
plt.ylabel('Distancia')
plt.xlabel('Máxima longitud de la solución')
plt.title('Impacto del máximo tamaño de la solución en la distancia')
plt.show()
