import matplotlib.pyplot as plt

# Valores en el eje x
x_labels = [149,349,499]

# Datos de mínimos, máximos y promedios
minimos = [221.0423,221.6696,221.7479]
maximos = [221.6051,222.2405,222.5588]
promedios = [221.3194,221.9399,222.1962]

# Crear la figura y el eje
plt.figure(figsize=(10, 6))

# Graficar cada punto con sus mínimos, máximos y promedios
for i, x in enumerate(x_labels):
    # Línea vertical entre el mínimo y el máximo pasando por el promedio
    plt.vlines(x, minimos[i], maximos[i], color='black', linestyle='--')

    # Línea horizontal en el valor mínimo para la "T" invertida
    plt.hlines(minimos[i], x - 5, x + 5, color='red', label='Mínimo' if i == 0 else "")

    # Línea horizontal en el valor máximo para la "T" hacia arriba
    plt.hlines(maximos[i], x - 5, x + 5, color='green', label='Máximo' if i == 0 else "")

    # Graficar el promedio como un punto
    plt.plot(x, promedios[i], 'o', color='blue', label='Promedio' if i == 0 else "")

#plt.axhline(y=42, color='grey', linestyle='-', linewidth=1.5, label='Medición angular teórica (42°)')

# Etiquetas y leyenda
plt.xlabel("Distancia radial (mm)")
plt.ylabel("Medición angular (°)")
plt.title("Dispersión de la primera medición angular en círculo externo después de finalizar el arco (222°)")
plt.xticks(x_labels)
plt.legend(loc='lower right')
plt.grid(True, linestyle="--", alpha=0.7)

# Mostrar el gráfico
plt.show()