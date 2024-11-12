#%%

import numpy as np
import matplotlib.pyplot as plt

# Datos de la tabla
radio_real = np.array([499, 449, 399, 349, 299, 249, 199, 149])
varianza_muestral = np.array([-0.7850,-0.4306, -0.6047, -0.9656, -0.9657, 0.1742, 0.9895, -0.0254])


# Graficar
plt.figure(figsize=(10, 6))
plt.scatter(radio_real, varianza_muestral, color='blue', label='Datos observados')

# Etiquetas y título
plt.xlabel("Radio real (mm)")
plt.ylabel("Sesgo ($\it{bias}$) promedial (mm)")
plt.title("Relación entre el radio real y el sesgo promedial")
plt.legend()
plt.grid(True)
plt.show()


#%%
# import pandas as pd
# import matplotlib.pyplot as plt
# import numpy as np

# # Parámetros de cambio
# outer_radius = 150
# arc = 130

# # Ruta del archivo
# path_csv = 'C:\\Users\\jrcer\\Universidad\\S10_2024\\TDG\\Tesis\\Pruebas\\Angulo45\\R130mm\\output_data_R130_P1.csv'
# df = pd.read_csv(path_csv, skiprows=1, header=None)

# # Columnas de interés del csv
# distances = df.iloc[:, 1]
# angles_deg = df.iloc[:, 4]

# # Listas para almacenar los valores encontrados en la cuarta columna
# last_dist_before_arc = []
# first_dist_arc = []
# last_dist_arc = []
# first_dist_after_arc = []


# # Banderas para seguimiento de estado
# last_i_dist_before_arc = None
# first_i_dist_arc = None
# last_i_dist_arc = None
# first_i_dist_after_arc = None
# serie_active = False


# # Itera sobre los valores para identificar los cambios
# for i, valor in enumerate(distances):
#     if valor == outer_radius:
#         if serie_active:
#             # Si se está en una serie de valores de arco, este es el primer valor después de pasar al arco
#             first_i_dist_after_arc = distances[i]
#             # Guardar los valores encontrados en la cuarta columna
#             last_dist_before_arc.append(last_i_dist_before_arc)
#             first_dist_arc.append(first_i_dist_arc)
#             last_dist_arc.append(last_i_dist_arc)
#             first_dist_after_arc.append(first_i_dist_after_arc)
#             # Reiniciar las variables de serie
#             serie_active = False
#             last_i_dist_before_arc = None
#             first_i_dist_arc = None
#             last_i_dist_arc = None
#             first_i_dist_after_arc = None
#         else:
#             # Actualiza el último valor en la cuarta columna antes de un cambio a valor_cambio
#             last_i_dist_before_arc = angles_deg[i]
    
#     elif valor == arc:
#         if not serie_active:
#             # Inicio de una nueva serie de valor_cambio
#             first_i_dist_arc = angles_deg[i]
#             serie_active = True
#         # Actualiza el último valor en la cuarta columna de la serie de valor_cambio
#         last_i_dist_arc = angles_deg[i]


# # Parámetros de figura
# letter_size = 7
# nominal_radius = 129
# real_last_angle_arc= 47
# last_angle_arc_min = min(first_dist_arc)
# last_angle_arc_max = max(first_dist_arc)

# fig1, axs1 = plt.subplots(figsize=(15, 6))
# axs1.plot(first_dist_arc, marker='.', linestyle='None', color='b', label='Medición angular')
# axs1.set_title(f"Gráfico de mediciones angulares para un arco de {nominal_radius} mm de radio finalizado a {real_last_angle_arc}°")
# axs1.set_xlabel("Índice de la medición")
# axs1.set_ylabel("Medición angular (°)")
# axs1.legend()
# axs1.grid(True)
# axs1.set_xlim([0, len(first_dist_arc)-1])
# axs1.text(0.82, 0.90, f"Valor mínimo: {last_angle_arc_min:.4f}", fontsize=letter_size, color='black', bbox=dict(facecolor='white', edgecolor='none'), linespacing=0.9, transform=axs1.transAxes)
# axs1.text(0.82, 0.85, f"Valor máximo: {last_angle_arc_max:.4f}", fontsize=letter_size, color='black', bbox=dict(facecolor='white', edgecolor='none'), linespacing=0.9, transform=axs1.transAxes)

# n_bins_sturges = int(np.ceil(np.log2(len(first_dist_arc)) + 1))
# fig2, axs2 = plt.subplots()
# axs2.hist(first_dist_arc, bins=n_bins_sturges, color='skyblue', edgecolor='black')
# axs2.set_title('Histograma de ángulo final medido para el arco')
# axs2.set_xlabel('Valores de ángulo final medido para el arco')
# axs2.set_ylabel('Frecuencia')
# plt.show()
# real_first_angle_arc= 42
# first_angle_arc_min = min(last_dist_arc)
# first_angle_arc_max = max(last_dist_arc)

# fig3, axs3 = plt.subplots(figsize=(15, 6))
# axs3.plot(last_dist_arc, marker='.', linestyle='None', color='b', label='Medición angular')
# axs3.set_title(f"Gráfico de mediciones angulares para un arco de {nominal_radius} mm de radio inicializado a {real_first_angle_arc}°")
# axs3.set_xlabel("Índice de la medición")
# axs3.set_ylabel("Medición angular (°)")
# axs3.legend()
# axs3.grid(True)
# axs3.set_xlim([0, len(last_dist_arc)-1])
# axs3.text(0.82, 0.90, f"Valor mínimo: {first_angle_arc_min:.4f}", fontsize=letter_size, color='black', bbox=dict(facecolor='white', edgecolor='none'), linespacing=0.9, transform=axs3.transAxes)
# axs3.text(0.82, 0.85, f"Valor máximo: {first_angle_arc_max:.4f}", fontsize=letter_size, color='black', bbox=dict(facecolor='white', edgecolor='none'), linespacing=0.9, transform=axs3.transAxes)

# n_bins_sturges = int(np.ceil(np.log2(len(first_dist_arc)) + 1))
# fig4, axs4 = plt.subplots()
# axs4.hist(last_dist_arc, bins=n_bins_sturges, color='skyblue', edgecolor='black')
# axs4.set_title('Histograma de ángulo inicial medido para el arco')
# axs4.set_xlabel('Valores de ángulo inicial medido para el arco')
# axs4.set_ylabel('Frecuencia')
# # Mostrar las gráficas
# plt.show()
# ##-------------------------------------R130----------------------------------------------------##
# #%%
# import pandas as pd
# import matplotlib.pyplot as plt
# import numpy as np
# import glob

# # Parámetros de cambio
# outer_radius = 150
# arc = 130

# # Ruta de la carpeta donde están los archivos CSV
# path_csv_folder = 'C:\\Users\\jrcer\\Universidad\\S10_2024\\TDG\\Tesis\\Pruebas\\Angulo45\\R130mm\\'

# # Obtener todos los archivos CSV en la carpeta
# csv_files = glob.glob(path_csv_folder + '*.csv')

# # Listas para almacenar los valores encontrados en la cuarta columna
# last_dist_before_arc = []
# first_dist_arc = []
# last_dist_arc = []
# first_dist_after_arc = []

# # Banderas para seguimiento de estado
# last_i_dist_before_arc = None
# first_i_dist_arc = None
# last_i_dist_arc = None
# first_i_dist_after_arc = None
# serie_active = False

# # Iterar sobre todos los archivos CSV
# for file in csv_files:
#     # Leer el archivo CSV
#     df = pd.read_csv(file, skiprows=1, header=None)
    
#     # Columnas de interés del csv
#     distances = df.iloc[:, 1]
#     angles_deg = df.iloc[:, 4]

#     # Iterar sobre los valores para identificar los cambios
#     for i, valor in enumerate(distances):
#         if valor == outer_radius:
#             if serie_active:
#                 # Si se está en una serie de valores de arco, este es el primer valor después de pasar al arco
#                 first_i_dist_after_arc = angles_deg[i]
#                 # Guardar los valores encontrados en la cuarta columna
#                 last_dist_before_arc.append(last_i_dist_before_arc)
#                 first_dist_arc.append(first_i_dist_arc)
#                 last_dist_arc.append(last_i_dist_arc)
#                 first_dist_after_arc.append(first_i_dist_after_arc)
#                 # Reiniciar las variables de serie
#                 serie_active = False
#                 last_i_dist_before_arc = None
#                 first_i_dist_arc = None
#                 last_i_dist_arc = None
#                 first_i_dist_after_arc = None
#             else:
#                 # Actualiza el último valor en la cuarta columna antes de un cambio a valor_cambio
#                 last_i_dist_before_arc = angles_deg[i]
        
#         elif valor == arc:
#             if not serie_active:
#                 # Inicio de una nueva serie de valor_cambio
#                 first_i_dist_arc = angles_deg[i]
#                 serie_active = True
#             # Actualiza el último valor en la cuarta columna de la serie de valor_cambio
#             last_i_dist_arc = angles_deg[i]

# first_dist_arc = [value for value in first_dist_arc if value >= 47]
# last_dist_before_arc = [value for value in last_dist_before_arc if value >= 49]
# #%%
# # Parámetros de figura
# letter_size = 7
# nominal_radius = 129
# real_last_angle_arc= 47
# last_angle_arc_min = min(first_dist_arc)
# last_angle_arc_max = max(first_dist_arc)
# last_angle_arc_mean = np.mean(first_dist_arc)
# #last_angle_arc_var = np.var(first_dist_arc, ddof=1)
# last_angle_arc_bias = last_angle_arc_mean - real_last_angle_arc

# fig1, axs1 = plt.subplots(figsize=(15, 6))
# axs1.plot(first_dist_arc, marker='.', linestyle='None', color='b', label='Medición angular')
# axs1.set_title(f"Última medición angular en arco de {nominal_radius} mm de radio, finalizado a {real_last_angle_arc}°")
# axs1.set_xlabel("Índice de la medición")
# axs1.set_ylabel("Medición angular (°)")
# axs1.legend()
# axs1.grid(True)
# axs1.set_xlim([0, len(first_dist_arc)-1])
# axs1.text(0.82, 0.90, f"Valor mínimo: {last_angle_arc_min:.4f}", fontsize=letter_size, color='black', bbox=dict(facecolor='white', edgecolor='none'), linespacing=0.9, transform=axs1.transAxes)
# axs1.text(0.82, 0.87, f"Valor máximo: {last_angle_arc_max:.4f}", fontsize=letter_size, color='black', bbox=dict(facecolor='white', edgecolor='none'), linespacing=0.9, transform=axs1.transAxes)
# axs1.text(0.82, 0.84, f"Promedio: {last_angle_arc_mean:.4f}", fontsize=letter_size, color='black', bbox=dict(facecolor='white', edgecolor='none'), linespacing=0.9, transform=axs1.transAxes)
# axs1.text(0.82, 0.81, f"Bias: {last_angle_arc_bias:.4f}", fontsize=letter_size, color='black', bbox=dict(facecolor='white', edgecolor='none'), linespacing=0.9, transform=axs1.transAxes)
# #axs1.text(0.82, 0.78, f"Varianza muestral: {last_angle_arc_var:.4f}", fontsize=letter_size, color='black', bbox=dict(facecolor='white', edgecolor='none'), linespacing=0.9, transform=axs1.transAxes)


# fig2, axs2 = plt.subplots()
# n_bins_sturges_fig2 = int(np.ceil(np.log2(len(first_dist_arc)) + 1))
# axs2.hist(first_dist_arc, bins=10, color='skyblue', edgecolor='black')
# axs2.set_title(f'Distribución del ángulo final medido en el arco de {nominal_radius} mm de radio')
# axs2.set_xlabel('Valores de ángulo final medido')
# axs2.set_ylabel('Frecuencia')
# plt.show()

# real_first_angle_arc= 42
# first_angle_arc_min = min(last_dist_arc)
# first_angle_arc_max = max(last_dist_arc)
# first_angle_arc_mean = np.mean(last_dist_arc)
# #first_angle_arc_var = np.var(last_dist_arc, ddof=1)
# first_angle_arc_bias = first_angle_arc_mean - real_first_angle_arc


# fig3, axs3 = plt.subplots(figsize=(15, 6))
# axs3.plot(last_dist_arc, marker='.', linestyle='None', color='b', label='Medición angular')
# axs3.set_title(f"Primera medición angular en arco de {nominal_radius} mm de radio, iniciado a {real_first_angle_arc}°")
# axs3.set_xlabel("Índice de la medición")
# axs3.set_ylabel("Medición angular (°)")
# axs3.legend()
# axs3.grid(True)
# axs3.set_xlim([0, len(last_dist_arc)-1])
# axs3.text(0.82, 0.90, f"Valor mínimo: {first_angle_arc_min:.4f}", fontsize=letter_size, color='black', bbox=dict(facecolor='white', edgecolor='none'), linespacing=0.9, transform=axs3.transAxes)
# axs3.text(0.82, 0.87, f"Valor máximo: {first_angle_arc_max:.4f}", fontsize=letter_size, color='black', bbox=dict(facecolor='white', edgecolor='none'), linespacing=0.9, transform=axs3.transAxes)
# axs3.text(0.82, 0.84, f"Promedio: {first_angle_arc_mean:.4f}", fontsize=letter_size, color='black', bbox=dict(facecolor='white', edgecolor='none'), linespacing=0.9, transform=axs1.transAxes)
# axs3.text(0.82, 0.81, f"Bias: {first_angle_arc_bias:.4f}", fontsize=letter_size, color='black', bbox=dict(facecolor='white', edgecolor='none'), linespacing=0.9, transform=axs1.transAxes)
# #axs3.text(0.82, 0.78, f"Varianza muestral: {first_angle_arc_var:.4f}", fontsize=letter_size, color='black', bbox=dict(facecolor='white', edgecolor='none'), linespacing=0.9, transform=axs1.transAxes)

# fig4, axs4 = plt.subplots()
# n_bins_sturges_fig4 = int(np.ceil(np.log2(len(last_dist_arc)) + 1))
# axs4.hist(last_dist_arc, bins=10, color='skyblue', edgecolor='black')
# axs4.set_title(f'Distribución del ángulo inicial medido en el arco de {nominal_radius} mm de radio')
# axs4.set_xlabel('Valores de ángulo inicial medido')
# axs4.set_ylabel('Frecuencia')

# plt.show()

# real_first_angle_outer= 42
# first_angle_outer_min = min(first_dist_after_arc)
# first_angle_outer_max = max(first_dist_after_arc)
# first_angle_outer_mean = np.mean(first_dist_after_arc)
# #first_angle_outer_var = np.var(first_dist_after_arc, ddof=1)
# first_angle_outer_bias = first_angle_outer_mean - real_first_angle_outer


# fig5, axs5 = plt.subplots(figsize=(15, 6))
# axs5.plot(first_dist_after_arc, marker='.', linestyle='None', color='b', label='Medición angular')
# axs5.set_title(f"Última medición angular en círculo de {nominal_radius+20} mm de radio, finalizado a {real_first_angle_outer}°")
# axs5.set_xlabel("Índice de la medición")
# axs5.set_ylabel("Medición angular (°)")
# axs5.legend()
# axs5.grid(True)
# axs5.set_xlim([0, len(first_dist_after_arc)-1])
# axs5.text(0.82, 0.90, f"Valor mínimo: {first_angle_outer_min:.4f}", fontsize=letter_size, color='black', bbox=dict(facecolor='white', edgecolor='none'), linespacing=0.9, transform=axs5.transAxes)
# axs5.text(0.82, 0.87, f"Valor máximo: {first_angle_outer_max:.4f}", fontsize=letter_size, color='black', bbox=dict(facecolor='white', edgecolor='none'), linespacing=0.9, transform=axs5.transAxes)
# axs5.text(0.82, 0.84, f"Promedio: {first_angle_outer_mean:.4f}", fontsize=letter_size, color='black', bbox=dict(facecolor='white', edgecolor='none'), linespacing=0.9, transform=axs1.transAxes)
# axs5.text(0.82, 0.81, f"Bias: {first_angle_outer_bias:.4f}", fontsize=letter_size, color='black', bbox=dict(facecolor='white', edgecolor='none'), linespacing=0.9, transform=axs1.transAxes)
# #axs5.text(0.82, 0.78, f"Varianza muestral: {first_angle_outer_var:.4f}", fontsize=letter_size, color='black', bbox=dict(facecolor='white', edgecolor='none'), linespacing=0.9, transform=axs1.transAxes)


# fig6, axs6 = plt.subplots()
# n_bins_sturges_fig6 = int(np.ceil(np.log2(len(first_dist_after_arc)) + 1))
# axs6.hist(first_dist_after_arc, bins=10, color='skyblue', edgecolor='black')
# axs6.set_title(f'Distribución del ángulo final medido para el círculo de {nominal_radius+20} mm de radio')
# axs6.set_xlabel(f'Valores de ángulo final medido')
# axs6.set_ylabel('Frecuencia')

# plt.show()

# real_last_angle_outer= 47
# last_angle_outer_min = min(last_dist_before_arc)
# last_angle_outer_max  = max(last_dist_before_arc)
# last_angle_outer_mean = np.mean(last_dist_before_arc)
# #last_angle_outer_var = np.var(last_dist_before_arc, ddof=1)
# last_angle_outer_bias = last_angle_outer_mean - real_last_angle_outer


# fig7, axs7 = plt.subplots(figsize=(15, 6))
# axs7.plot(last_dist_before_arc, marker='.', linestyle='None', color='b', label='Medición angular')
# axs7.set_title(f"Primera medición angular en círculo de {nominal_radius+20} mm de radio, iniciado a {real_last_angle_outer}°")
# axs7.set_xlabel("Índice de la medición")
# axs7.set_ylabel("Medición angular (°)")
# axs7.legend()
# axs7.grid(True)
# axs7.set_xlim([0, len(last_dist_before_arc)-1])
# axs7.text(0.82, 0.90, f"Valor mínimo: {last_angle_outer_min:.4f}", fontsize=letter_size, color='black', bbox=dict(facecolor='white', edgecolor='none'), linespacing=0.9, transform=axs7.transAxes)
# axs7.text(0.82, 0.85, f"Valor máximo: {last_angle_outer_max:.4f}", fontsize=letter_size, color='black', bbox=dict(facecolor='white', edgecolor='none'), linespacing=0.9, transform=axs7.transAxes)
# axs7.text(0.82, 0.84, f"Promedio: {last_angle_outer_mean:.4f}", fontsize=letter_size, color='black', bbox=dict(facecolor='white', edgecolor='none'), linespacing=0.9, transform=axs1.transAxes)
# axs7.text(0.82, 0.81, f"Bias: {last_angle_outer_bias:.4f}", fontsize=letter_size, color='black', bbox=dict(facecolor='white', edgecolor='none'), linespacing=0.9, transform=axs1.transAxes)
# #axs7.text(0.82, 0.78, f"Varianza muestral: {last_angle_outer_var:.4f}", fontsize=letter_size, color='black', bbox=dict(facecolor='white', edgecolor='none'), linespacing=0.9, transform=axs1.transAxes)

# fig8, axs8 = plt.subplots()
# n_bins_sturges_fig8 = int(np.ceil(np.log2(len(last_dist_before_arc)) + 1))
# axs8.hist(last_dist_before_arc, bins=10, color='skyblue', edgecolor='black')
# axs8.set_title(f'Distribución del ángulo inicial medido para el círculo de {nominal_radius+20} mm de radio')
# axs8.set_xlabel(f'Valores de ángulo inicial medido')
# axs8.set_ylabel('Frecuencia')

# plt.show()
# # %%
# ##-------------------------------------R180----------------------------------------------------##
# #%%
# import pandas as pd
# import matplotlib.pyplot as plt
# import numpy as np
# import glob

# # Parámetros de cambio
# outer_radius = 200
# arc = 180
# tolerance = 2

# # Ruta de la carpeta donde están los archivos CSV
# path_csv_folder = 'C:\\Users\\jrcer\\Universidad\\S10_2024\\TDG\\Tesis\\Pruebas\\Angulo45\\R180mm\\'

# # Obtener todos los archivos CSV en la carpeta
# csv_files = glob.glob(path_csv_folder + '*.csv')

# # Listas para almacenar los valores encontrados en la cuarta columna
# last_dist_before_arc = []
# first_dist_arc = []
# last_dist_arc = []
# first_dist_after_arc = []

# # Banderas para seguimiento de estado
# last_i_dist_before_arc = None
# first_i_dist_arc = None
# last_i_dist_arc = None
# first_i_dist_after_arc = None
# serie_active = False

# # Iterar sobre todos los archivos CSV
# for file in csv_files:
#     # Leer el archivo CSV
#     df = pd.read_csv(file, skiprows=1, header=None)
    
#     # Columnas de interés del csv
#     distances = df.iloc[:, 1]
#     angles_deg = df.iloc[:, 4]

#     # Iterar sobre los valores para identificar los cambios
#     for i, valor in enumerate(distances):
#         if outer_radius - tolerance <= valor <= outer_radius + tolerance:
#             if serie_active:
#                 # Si se está en una serie de valores de arco, este es el primer valor después de pasar al arco
#                 first_i_dist_after_arc = angles_deg[i]
#                 # Guardar los valores encontrados en la cuarta columna
#                 last_dist_before_arc.append(last_i_dist_before_arc)
#                 first_dist_arc.append(first_i_dist_arc)
#                 last_dist_arc.append(last_i_dist_arc)
#                 first_dist_after_arc.append(first_i_dist_after_arc)
#                 # Reiniciar las variables de serie
#                 serie_active = False
#                 last_i_dist_before_arc = None
#                 first_i_dist_arc = None
#                 last_i_dist_arc = None
#                 first_i_dist_after_arc = None
#             else:
#                 # Actualiza el último valor en la cuarta columna antes de un cambio a valor_cambio
#                 last_i_dist_before_arc = angles_deg[i]
        
#         elif arc - tolerance <= valor <= arc + tolerance:
#             if not serie_active:
#                 # Inicio de una nueva serie de valor_cambio
#                 first_i_dist_arc = angles_deg[i]
#                 serie_active = True
#             # Actualiza el último valor en la cuarta columna de la serie de valor_cambio
#             last_i_dist_arc = angles_deg[i]
# #%%
# first_dist_arc = first_dist_arc[1200:]
# first_dist_arc = [value for value in first_dist_arc if value <= 47.6]
# last_dist_arc = last_dist_arc[1200:]
# last_dist_arc = [value for value in last_dist_arc if value >= 42.8]
# first_dist_after_arc = first_dist_after_arc[1200:]
# last_dist_before_arc = last_dist_before_arc[1200:]

# #%%
# # Parámetros de figura
# letter_size = 7
# nominal_radius = 179
# real_last_angle_arc= 47
# last_angle_arc_min = min(first_dist_arc)
# last_angle_arc_max = max(first_dist_arc)
# last_angle_arc_mean = np.mean(first_dist_arc)
# #last_angle_arc_var = np.var(first_dist_arc, ddof=1)
# last_angle_arc_bias = last_angle_arc_mean - real_last_angle_arc

# fig1, axs1 = plt.subplots(figsize=(15, 6))
# axs1.plot(first_dist_arc, marker='.', linestyle='None', color='b', label='Medición angular')
# axs1.set_title(f"Última medición angular en arco de {nominal_radius} mm de radio, finalizado a {real_last_angle_arc}°")
# axs1.set_xlabel("Índice de la medición")
# axs1.set_ylabel("Medición angular (°)")
# axs1.legend()
# axs1.grid(True)
# axs1.set_xlim([0, len(first_dist_arc)-1])
# axs1.text(0.82, 0.90, f"Valor mínimo: {last_angle_arc_min:.4f}", fontsize=letter_size, color='black', bbox=dict(facecolor='white', edgecolor='none'), linespacing=0.9, transform=axs1.transAxes)
# axs1.text(0.82, 0.87, f"Valor máximo: {last_angle_arc_max:.4f}", fontsize=letter_size, color='black', bbox=dict(facecolor='white', edgecolor='none'), linespacing=0.9, transform=axs1.transAxes)
# axs1.text(0.82, 0.84, f"Promedio: {last_angle_arc_mean:.4f}", fontsize=letter_size, color='black', bbox=dict(facecolor='white', edgecolor='none'), linespacing=0.9, transform=axs1.transAxes)
# axs1.text(0.82, 0.81, f"Bias: {last_angle_arc_bias:.4f}", fontsize=letter_size, color='black', bbox=dict(facecolor='white', edgecolor='none'), linespacing=0.9, transform=axs1.transAxes)
# #axs1.text(0.82, 0.78, f"Varianza muestral: {last_angle_arc_var:.4f}", fontsize=letter_size, color='black', bbox=dict(facecolor='white', edgecolor='none'), linespacing=0.9, transform=axs1.transAxes)


# fig2, axs2 = plt.subplots()
# n_bins_sturges_fig2 = int(np.ceil(np.log2(len(first_dist_arc)) + 1))
# axs2.hist(first_dist_arc, bins=8, color='skyblue', edgecolor='black')
# axs2.set_title(f'Distribución del ángulo final medido en el arco de {nominal_radius} mm de radio')
# axs2.set_xlabel('Valores de ángulo final medido')
# axs2.set_ylabel('Frecuencia')
# plt.show()

# real_first_angle_arc= 42
# first_angle_arc_min = min(last_dist_arc)
# first_angle_arc_max = max(last_dist_arc)
# first_angle_arc_mean = np.mean(last_dist_arc)
# #first_angle_arc_var = np.var(last_dist_arc, ddof=1)
# first_angle_arc_bias = first_angle_arc_mean - real_first_angle_arc


# fig3, axs3 = plt.subplots(figsize=(15, 6))
# axs3.plot(last_dist_arc, marker='.', linestyle='None', color='b', label='Medición angular')
# axs3.set_title(f"Primera medición angular en arco de {nominal_radius} mm de radio, iniciado a {real_first_angle_arc}°")
# axs3.set_xlabel("Índice de la medición")
# axs3.set_ylabel("Medición angular (°)")
# axs3.legend()
# axs3.grid(True)
# axs3.set_xlim([0, len(last_dist_arc)-1])
# axs3.text(0.82, 0.90, f"Valor mínimo: {first_angle_arc_min:.4f}", fontsize=letter_size, color='black', bbox=dict(facecolor='white', edgecolor='none'), linespacing=0.9, transform=axs3.transAxes)
# axs3.text(0.82, 0.87, f"Valor máximo: {first_angle_arc_max:.4f}", fontsize=letter_size, color='black', bbox=dict(facecolor='white', edgecolor='none'), linespacing=0.9, transform=axs3.transAxes)
# axs3.text(0.82, 0.84, f"Promedio: {first_angle_arc_mean:.4f}", fontsize=letter_size, color='black', bbox=dict(facecolor='white', edgecolor='none'), linespacing=0.9, transform=axs1.transAxes)
# axs3.text(0.82, 0.81, f"Bias: {first_angle_arc_bias:.4f}", fontsize=letter_size, color='black', bbox=dict(facecolor='white', edgecolor='none'), linespacing=0.9, transform=axs1.transAxes)
# #axs3.text(0.82, 0.78, f"Varianza muestral: {first_angle_arc_var:.4f}", fontsize=letter_size, color='black', bbox=dict(facecolor='white', edgecolor='none'), linespacing=0.9, transform=axs1.transAxes)

# fig4, axs4 = plt.subplots()
# n_bins_sturges_fig4 = int(np.ceil(np.log2(len(last_dist_arc)) + 1))
# axs4.hist(last_dist_arc, bins=9, color='skyblue', edgecolor='black')
# axs4.set_title(f'Distribución del ángulo inicial medido en el arco de {nominal_radius} mm de radio')
# axs4.set_xlabel('Valores de ángulo inicial medido')
# axs4.set_ylabel('Frecuencia')

# plt.show()

# real_first_angle_outer= 42
# first_angle_outer_min = min(first_dist_after_arc)
# first_angle_outer_max = max(first_dist_after_arc)
# first_angle_outer_mean = np.mean(first_dist_after_arc)
# #first_angle_outer_var = np.var(first_dist_after_arc, ddof=1)
# first_angle_outer_bias = first_angle_outer_mean - real_first_angle_outer


# fig5, axs5 = plt.subplots(figsize=(15, 6))
# axs5.plot(first_dist_after_arc, marker='.', linestyle='None', color='b', label='Medición angular')
# axs5.set_title(f"Última medición angular en círculo de {nominal_radius+20} mm de radio, finalizado a {real_first_angle_outer}°")
# axs5.set_xlabel("Índice de la medición")
# axs5.set_ylabel("Medición angular (°)")
# axs5.legend()
# axs5.grid(True)
# axs5.set_xlim([0, len(first_dist_after_arc)-1])
# axs5.text(0.82, 0.90, f"Valor mínimo: {first_angle_outer_min:.4f}", fontsize=letter_size, color='black', bbox=dict(facecolor='white', edgecolor='none'), linespacing=0.9, transform=axs5.transAxes)
# axs5.text(0.82, 0.87, f"Valor máximo: {first_angle_outer_max:.4f}", fontsize=letter_size, color='black', bbox=dict(facecolor='white', edgecolor='none'), linespacing=0.9, transform=axs5.transAxes)
# axs5.text(0.82, 0.84, f"Promedio: {first_angle_outer_mean:.4f}", fontsize=letter_size, color='black', bbox=dict(facecolor='white', edgecolor='none'), linespacing=0.9, transform=axs1.transAxes)
# axs5.text(0.82, 0.81, f"Bias: {first_angle_outer_bias:.4f}", fontsize=letter_size, color='black', bbox=dict(facecolor='white', edgecolor='none'), linespacing=0.9, transform=axs1.transAxes)
# #axs5.text(0.82, 0.78, f"Varianza muestral: {first_angle_outer_var:.4f}", fontsize=letter_size, color='black', bbox=dict(facecolor='white', edgecolor='none'), linespacing=0.9, transform=axs1.transAxes)


# fig6, axs6 = plt.subplots()
# n_bins_sturges_fig6 = int(np.ceil(np.log2(len(first_dist_after_arc)) + 1))
# axs6.hist(first_dist_after_arc, bins=9, color='skyblue', edgecolor='black')
# axs6.set_title(f'Distribución del ángulo final medido para el círculo de {nominal_radius+20} mm de radio')
# axs6.set_xlabel(f'Valores de ángulo final medido')
# axs6.set_ylabel('Frecuencia')

# plt.show()

# real_last_angle_outer= 47
# last_angle_outer_min = min(last_dist_before_arc)
# last_angle_outer_max  = max(last_dist_before_arc)
# last_angle_outer_mean = np.mean(last_dist_before_arc)
# #last_angle_outer_var = np.var(last_dist_before_arc, ddof=1)
# last_angle_outer_bias = last_angle_outer_mean - real_last_angle_outer


# fig7, axs7 = plt.subplots(figsize=(15, 6))
# axs7.plot(last_dist_before_arc, marker='.', linestyle='None', color='b', label='Medición angular')
# axs7.set_title(f"Primera medición angular en círculo de {nominal_radius+20} mm de radio, iniciado a {real_last_angle_outer}°")
# axs7.set_xlabel("Índice de la medición")
# axs7.set_ylabel("Medición angular (°)")
# axs7.legend()
# axs7.grid(True)
# axs7.set_xlim([0, len(last_dist_before_arc)-1])
# axs7.text(0.82, 0.90, f"Valor mínimo: {last_angle_outer_min:.4f}", fontsize=letter_size, color='black', bbox=dict(facecolor='white', edgecolor='none'), linespacing=0.9, transform=axs7.transAxes)
# axs7.text(0.82, 0.85, f"Valor máximo: {last_angle_outer_max:.4f}", fontsize=letter_size, color='black', bbox=dict(facecolor='white', edgecolor='none'), linespacing=0.9, transform=axs7.transAxes)
# axs7.text(0.82, 0.84, f"Promedio: {last_angle_outer_mean:.4f}", fontsize=letter_size, color='black', bbox=dict(facecolor='white', edgecolor='none'), linespacing=0.9, transform=axs1.transAxes)
# axs7.text(0.82, 0.81, f"Bias: {last_angle_outer_bias:.4f}", fontsize=letter_size, color='black', bbox=dict(facecolor='white', edgecolor='none'), linespacing=0.9, transform=axs1.transAxes)
# #axs7.text(0.82, 0.78, f"Varianza muestral: {last_angle_outer_var:.4f}", fontsize=letter_size, color='black', bbox=dict(facecolor='white', edgecolor='none'), linespacing=0.9, transform=axs1.transAxes)

# fig8, axs8 = plt.subplots()
# n_bins_sturges_fig8 = int(np.ceil(np.log2(len(last_dist_before_arc)) + 1))
# axs8.hist(last_dist_before_arc, bins=8, color='skyblue', edgecolor='black')
# axs8.set_title(f'Distribución del ángulo inicial medido para el círculo de {nominal_radius+20} mm de radio')
# axs8.set_xlabel(f'Valores de ángulo inicial medido')
# axs8.set_ylabel('Frecuencia')

# plt.show()

# ##-------------------------------------R230----------------------------------------------------##
# #%%
# import pandas as pd
# import matplotlib.pyplot as plt
# import numpy as np
# import glob

# # Parámetros de cambio
# outer_radius = 250
# arc = 230
# tolerance = 2

# # Ruta de la carpeta donde están los archivos CSV
# path_csv_folder = 'C:\\Users\\jrcer\\Universidad\\S10_2024\\TDG\\Tesis\\Pruebas\\Angulo45\\R230mm\\'

# # Obtener todos los archivos CSV en la carpeta
# csv_files = glob.glob(path_csv_folder + '*.csv')

# # Listas para almacenar los valores encontrados en la cuarta columna
# last_dist_before_arc = []
# first_dist_arc = []
# last_dist_arc = []
# first_dist_after_arc = []

# # Banderas para seguimiento de estado
# last_i_dist_before_arc = None
# first_i_dist_arc = None
# last_i_dist_arc = None
# first_i_dist_after_arc = None
# serie_active = False

# # Iterar sobre todos los archivos CSV
# for file in csv_files:
#     # Leer el archivo CSV
#     df = pd.read_csv(file, skiprows=1, header=None)
    
#     # Columnas de interés del csv
#     distances = df.iloc[:, 1]
#     angles_deg = df.iloc[:, 4]

#     # Iterar sobre los valores para identificar los cambios
#     for i, valor in enumerate(distances):
#         if outer_radius - tolerance <= valor <= outer_radius + tolerance:
#             if serie_active:
#                 # Si se está en una serie de valores de arco, este es el primer valor después de pasar al arco
#                 first_i_dist_after_arc = angles_deg[i]
#                 # Guardar los valores encontrados en la cuarta columna
#                 last_dist_before_arc.append(last_i_dist_before_arc)
#                 first_dist_arc.append(first_i_dist_arc)
#                 last_dist_arc.append(last_i_dist_arc)
#                 first_dist_after_arc.append(first_i_dist_after_arc)
#                 # Reiniciar las variables de serie
#                 serie_active = False
#                 last_i_dist_before_arc = None
#                 first_i_dist_arc = None
#                 last_i_dist_arc = None
#                 first_i_dist_after_arc = None
#             else:
#                 # Actualiza el último valor en la cuarta columna antes de un cambio a valor_cambio
#                 last_i_dist_before_arc = angles_deg[i]
        
#         elif arc - tolerance <= valor <= arc + tolerance:
#             if not serie_active:
#                 # Inicio de una nueva serie de valor_cambio
#                 first_i_dist_arc = angles_deg[i]
#                 serie_active = True
#             # Actualiza el último valor en la cuarta columna de la serie de valor_cambio
#             last_i_dist_arc = angles_deg[i]
# #%%
# first_dist_arc = first_dist_arc[1000:]
# first_dist_arc = [value for value in first_dist_arc if value >= 46]
# last_dist_arc = last_dist_arc[1000:]
# first_dist_after_arc = first_dist_after_arc[1000:]
# last_dist_before_arc = last_dist_before_arc[1000:]
# last_dist_before_arc = [value for value in last_dist_before_arc if value <= 46]


# #%%
# # Parámetros de figura
# letter_size = 7
# nominal_radius = 229
# real_last_angle_arc= 47
# last_angle_arc_min = min(first_dist_arc)
# last_angle_arc_max = max(first_dist_arc)
# last_angle_arc_mean = np.mean(first_dist_arc)
# #last_angle_arc_var = np.var(first_dist_arc, ddof=1)
# last_angle_arc_bias = last_angle_arc_mean - real_last_angle_arc

# fig1, axs1 = plt.subplots(figsize=(15, 6))
# axs1.plot(first_dist_arc, marker='.', linestyle='None', color='b', label='Medición angular')
# axs1.set_title(f"Última medición angular en arco de {nominal_radius} mm de radio, finalizado a {real_last_angle_arc}°")
# axs1.set_xlabel("Índice de la medición")
# axs1.set_ylabel("Medición angular (°)")
# axs1.legend()
# axs1.grid(True)
# axs1.set_xlim([0, len(first_dist_arc)-1])
# axs1.text(0.82, 0.90, f"Valor mínimo: {last_angle_arc_min:.4f}", fontsize=letter_size, color='black', bbox=dict(facecolor='white', edgecolor='none'), linespacing=0.9, transform=axs1.transAxes)
# axs1.text(0.82, 0.87, f"Valor máximo: {last_angle_arc_max:.4f}", fontsize=letter_size, color='black', bbox=dict(facecolor='white', edgecolor='none'), linespacing=0.9, transform=axs1.transAxes)
# axs1.text(0.82, 0.84, f"Promedio: {last_angle_arc_mean:.4f}", fontsize=letter_size, color='black', bbox=dict(facecolor='white', edgecolor='none'), linespacing=0.9, transform=axs1.transAxes)
# axs1.text(0.82, 0.81, f"Bias: {last_angle_arc_bias:.4f}", fontsize=letter_size, color='black', bbox=dict(facecolor='white', edgecolor='none'), linespacing=0.9, transform=axs1.transAxes)
# #axs1.text(0.82, 0.78, f"Varianza muestral: {last_angle_arc_var:.4f}", fontsize=letter_size, color='black', bbox=dict(facecolor='white', edgecolor='none'), linespacing=0.9, transform=axs1.transAxes)


# fig2, axs2 = plt.subplots()
# n_bins_sturges_fig2 = int(np.ceil(np.log2(len(first_dist_arc)) + 1))
# axs2.hist(first_dist_arc, bins=8, color='skyblue', edgecolor='black')
# axs2.set_title(f'Distribución del ángulo final medido en el arco de {nominal_radius} mm de radio')
# axs2.set_xlabel('Valores de ángulo final medido')
# axs2.set_ylabel('Frecuencia')
# plt.show()

# real_first_angle_arc= 42
# first_angle_arc_min = min(last_dist_arc)
# first_angle_arc_max = max(last_dist_arc)
# first_angle_arc_mean = np.mean(last_dist_arc)
# #first_angle_arc_var = np.var(last_dist_arc, ddof=1)
# first_angle_arc_bias = first_angle_arc_mean - real_first_angle_arc


# fig3, axs3 = plt.subplots(figsize=(15, 6))
# axs3.plot(last_dist_arc, marker='.', linestyle='None', color='b', label='Medición angular')
# axs3.set_title(f"Primera medición angular en arco de {nominal_radius} mm de radio, iniciado a {real_first_angle_arc}°")
# axs3.set_xlabel("Índice de la medición")
# axs3.set_ylabel("Medición angular (°)")
# axs3.legend()
# axs3.grid(True)
# axs3.set_xlim([0, len(last_dist_arc)-1])
# axs3.text(0.82, 0.90, f"Valor mínimo: {first_angle_arc_min:.4f}", fontsize=letter_size, color='black', bbox=dict(facecolor='white', edgecolor='none'), linespacing=0.9, transform=axs3.transAxes)
# axs3.text(0.82, 0.87, f"Valor máximo: {first_angle_arc_max:.4f}", fontsize=letter_size, color='black', bbox=dict(facecolor='white', edgecolor='none'), linespacing=0.9, transform=axs3.transAxes)
# axs3.text(0.82, 0.84, f"Promedio: {first_angle_arc_mean:.4f}", fontsize=letter_size, color='black', bbox=dict(facecolor='white', edgecolor='none'), linespacing=0.9, transform=axs1.transAxes)
# axs3.text(0.82, 0.81, f"Bias: {first_angle_arc_bias:.4f}", fontsize=letter_size, color='black', bbox=dict(facecolor='white', edgecolor='none'), linespacing=0.9, transform=axs1.transAxes)
# #axs3.text(0.82, 0.78, f"Varianza muestral: {first_angle_arc_var:.4f}", fontsize=letter_size, color='black', bbox=dict(facecolor='white', edgecolor='none'), linespacing=0.9, transform=axs1.transAxes)

# fig4, axs4 = plt.subplots()
# n_bins_sturges_fig4 = int(np.ceil(np.log2(len(last_dist_arc)) + 1))
# axs4.hist(last_dist_arc, bins=9, color='skyblue', edgecolor='black')
# axs4.set_title(f'Distribución del ángulo inicial medido en el arco de {nominal_radius} mm de radio')
# axs4.set_xlabel('Valores de ángulo inicial medido')
# axs4.set_ylabel('Frecuencia')

# plt.show()

# real_first_angle_outer= 42
# first_angle_outer_min = min(first_dist_after_arc)
# first_angle_outer_max = max(first_dist_after_arc)
# first_angle_outer_mean = np.mean(first_dist_after_arc)
# #first_angle_outer_var = np.var(first_dist_after_arc, ddof=1)
# first_angle_outer_bias = first_angle_outer_mean - real_first_angle_outer


# fig5, axs5 = plt.subplots(figsize=(15, 6))
# axs5.plot(first_dist_after_arc, marker='.', linestyle='None', color='b', label='Medición angular')
# axs5.set_title(f"Última medición angular en círculo de {nominal_radius+20} mm de radio, finalizado a {real_first_angle_outer}°")
# axs5.set_xlabel("Índice de la medición")
# axs5.set_ylabel("Medición angular (°)")
# axs5.legend()
# axs5.grid(True)
# axs5.set_xlim([0, len(first_dist_after_arc)-1])
# axs5.text(0.82, 0.90, f"Valor mínimo: {first_angle_outer_min:.4f}", fontsize=letter_size, color='black', bbox=dict(facecolor='white', edgecolor='none'), linespacing=0.9, transform=axs5.transAxes)
# axs5.text(0.82, 0.87, f"Valor máximo: {first_angle_outer_max:.4f}", fontsize=letter_size, color='black', bbox=dict(facecolor='white', edgecolor='none'), linespacing=0.9, transform=axs5.transAxes)
# axs5.text(0.82, 0.84, f"Promedio: {first_angle_outer_mean:.4f}", fontsize=letter_size, color='black', bbox=dict(facecolor='white', edgecolor='none'), linespacing=0.9, transform=axs1.transAxes)
# axs5.text(0.82, 0.81, f"Bias: {first_angle_outer_bias:.4f}", fontsize=letter_size, color='black', bbox=dict(facecolor='white', edgecolor='none'), linespacing=0.9, transform=axs1.transAxes)
# #axs5.text(0.82, 0.78, f"Varianza muestral: {first_angle_outer_var:.4f}", fontsize=letter_size, color='black', bbox=dict(facecolor='white', edgecolor='none'), linespacing=0.9, transform=axs1.transAxes)


# fig6, axs6 = plt.subplots()
# n_bins_sturges_fig6 = int(np.ceil(np.log2(len(first_dist_after_arc)) + 1))
# axs6.hist(first_dist_after_arc, bins=9, color='skyblue', edgecolor='black')
# axs6.set_title(f'Distribución del ángulo final medido para el círculo de {nominal_radius+20} mm de radio')
# axs6.set_xlabel(f'Valores de ángulo final medido')
# axs6.set_ylabel('Frecuencia')

# plt.show()

# real_last_angle_outer= 47
# last_angle_outer_min = min(last_dist_before_arc)
# last_angle_outer_max  = max(last_dist_before_arc)
# last_angle_outer_mean = np.mean(last_dist_before_arc)
# #last_angle_outer_var = np.var(last_dist_before_arc, ddof=1)
# last_angle_outer_bias = last_angle_outer_mean - real_last_angle_outer


# fig7, axs7 = plt.subplots(figsize=(15, 6))
# axs7.plot(last_dist_before_arc, marker='.', linestyle='None', color='b', label='Medición angular')
# axs7.set_title(f"Primera medición angular en círculo de {nominal_radius+20} mm de radio, iniciado a {real_last_angle_outer}°")
# axs7.set_xlabel("Índice de la medición")
# axs7.set_ylabel("Medición angular (°)")
# axs7.legend()
# axs7.grid(True)
# axs7.set_xlim([0, len(last_dist_before_arc)-1])
# axs7.text(0.82, 0.90, f"Valor mínimo: {last_angle_outer_min:.4f}", fontsize=letter_size, color='black', bbox=dict(facecolor='white', edgecolor='none'), linespacing=0.9, transform=axs7.transAxes)
# axs7.text(0.82, 0.85, f"Valor máximo: {last_angle_outer_max:.4f}", fontsize=letter_size, color='black', bbox=dict(facecolor='white', edgecolor='none'), linespacing=0.9, transform=axs7.transAxes)
# axs7.text(0.82, 0.84, f"Promedio: {last_angle_outer_mean:.4f}", fontsize=letter_size, color='black', bbox=dict(facecolor='white', edgecolor='none'), linespacing=0.9, transform=axs1.transAxes)
# axs7.text(0.82, 0.81, f"Bias: {last_angle_outer_bias:.4f}", fontsize=letter_size, color='black', bbox=dict(facecolor='white', edgecolor='none'), linespacing=0.9, transform=axs1.transAxes)
# #axs7.text(0.82, 0.78, f"Varianza muestral: {last_angle_outer_var:.4f}", fontsize=letter_size, color='black', bbox=dict(facecolor='white', edgecolor='none'), linespacing=0.9, transform=axs1.transAxes)

# fig8, axs8 = plt.subplots()
# n_bins_sturges_fig8 = int(np.ceil(np.log2(len(last_dist_before_arc)) + 1))
# axs8.hist(last_dist_before_arc, bins=8, color='skyblue', edgecolor='black')
# axs8.set_title(f'Distribución del ángulo inicial medido para el círculo de {nominal_radius+20} mm de radio')
# axs8.set_xlabel(f'Valores de ángulo inicial medido')
# axs8.set_ylabel('Frecuencia')

# plt.show()

# # %%
##-------------------------------------R280----------------------------------------------------##
'''
#%%
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import glob

# Parámetros de cambio
outer_radius = 300
arc = 280
tolerance = 2

# Ruta de la carpeta donde están los archivos CSV
path_csv_folder = 'C:\\Users\\jrcer\\Universidad\\S10_2024\\TDG\\Tesis\\Pruebas\\Angulo45\\R280mm\\'

# Obtener todos los archivos CSV en la carpeta
csv_files = glob.glob(path_csv_folder + '*.csv')

# Listas para almacenar los valores encontrados en la cuarta columna
last_dist_before_arc = []
first_dist_arc = []
last_dist_arc = []
first_dist_after_arc = []

# Banderas para seguimiento de estado
last_i_dist_before_arc = None
first_i_dist_arc = None
last_i_dist_arc = None
first_i_dist_after_arc = None
serie_active = False

# Iterar sobre todos los archivos CSV
for file in csv_files:
    # Leer el archivo CSV
    df = pd.read_csv(file, skiprows=1, header=None)
    
    # Columnas de interés del csv
    distances = df.iloc[:, 1]
    angles_deg = df.iloc[:, 4]

    # Iterar sobre los valores para identificar los cambios
    for i, valor in enumerate(distances):
        if outer_radius - tolerance <= valor <= outer_radius + tolerance:
            if serie_active:
                # Si se está en una serie de valores de arco, este es el primer valor después de pasar al arco
                first_i_dist_after_arc = angles_deg[i]
                # Guardar los valores encontrados en la cuarta columna
                last_dist_before_arc.append(last_i_dist_before_arc)
                first_dist_arc.append(first_i_dist_arc)
                last_dist_arc.append(last_i_dist_arc)
                first_dist_after_arc.append(first_i_dist_after_arc)
                # Reiniciar las variables de serie
                serie_active = False
                last_i_dist_before_arc = None
                first_i_dist_arc = None
                last_i_dist_arc = None
                first_i_dist_after_arc = None
            else:
                # Actualiza el último valor en la cuarta columna antes de un cambio a valor_cambio
                last_i_dist_before_arc = angles_deg[i]
        
        elif arc - tolerance <= valor <= arc + tolerance:
            if not serie_active:
                # Inicio de una nueva serie de valor_cambio
                first_i_dist_arc = angles_deg[i]
                serie_active = True
            # Actualiza el último valor en la cuarta columna de la serie de valor_cambio
            last_i_dist_arc = angles_deg[i]
#%%
# first_dist_arc = first_dist_arc[1000:]
first_dist_arc = [value for value in first_dist_arc if value <= 48]
# last_dist_arc = last_dist_arc[1000:]
# first_dist_after_arc = first_dist_after_arc[1000:]
# last_dist_before_arc = last_dist_before_arc[1000:]
last_dist_before_arc = [value for value in last_dist_before_arc if value >= 46]

#%%
# Parámetros de figura
letter_size = 7
nominal_radius = 279
real_last_angle_arc= 47

last_angle_arc_min = min(first_dist_arc)
last_angle_arc_max = max(first_dist_arc)
last_angle_arc_mean = np.mean(first_dist_arc)
#last_angle_arc_var = np.var(first_dist_arc, ddof=1)
last_angle_arc_bias = last_angle_arc_mean - real_last_angle_arc
print(f"{last_angle_arc_min:.4f}")
print(f"{last_angle_arc_max:.4f}")
print(f"{last_angle_arc_mean:.4f}")
print(f"{last_angle_arc_bias:.4f}")

delta_first_dist_arc = [value - real_last_angle_arc for value in first_dist_arc]
delta_last_angle_arc_min = min(delta_first_dist_arc)
delta_last_angle_arc_max = max(delta_first_dist_arc)
delta_last_angle_arc_mean = np.mean(delta_first_dist_arc)
fig1, axs1 = plt.subplots(figsize=(15, 6))
axs1.plot(delta_first_dist_arc, marker='.', linestyle='None', color='b', label='Medición angular')
axs1.set_title(f"Deltas de la ultima medición angular en arco de {nominal_radius} mm de radio, finalizado a {real_last_angle_arc}°")
axs1.set_xlabel("Índice de la medición")
axs1.set_ylabel("Delta angular (°)")
axs1.legend()
axs1.grid(True)
axs1.set_xlim([0, len(delta_first_dist_arc)-1])
axs1.text(0.82, 0.90, f"Valor mínimo: {delta_last_angle_arc_min:.4f}", fontsize=letter_size, color='black', bbox=dict(facecolor='white', edgecolor='none'), linespacing=0.9, transform=axs1.transAxes)
axs1.text(0.82, 0.87, f"Valor máximo: {delta_last_angle_arc_max:.4f}", fontsize=letter_size, color='black', bbox=dict(facecolor='white', edgecolor='none'), linespacing=0.9, transform=axs1.transAxes)
axs1.text(0.82, 0.84, f"Promedio: {delta_last_angle_arc_mean:.4f}", fontsize=letter_size, color='black', bbox=dict(facecolor='white', edgecolor='none'), linespacing=0.9, transform=axs1.transAxes)


fig2, axs2 = plt.subplots()
n_bins_sturges_fig2 = int(np.ceil(np.log2(len(first_dist_arc)) + 1))
axs2.hist(delta_last_angle_arc_min, bins=8, color='skyblue', edgecolor='black')
axs2.set_title(f'Distribución de los deltas del ángulo final medido en el arco de {nominal_radius} mm de radio')
axs2.set_xlabel('Deltas de ángulo final medido')
axs2.set_ylabel('Frecuencia')
plt.show()

real_first_angle_arc= 42

first_angle_arc_min = min(last_dist_arc)
first_angle_arc_max = max(last_dist_arc)
first_angle_arc_mean = np.mean(last_dist_arc)
#first_angle_arc_var = np.var(last_dist_arc, ddof=1)
first_angle_arc_bias = first_angle_arc_mean - real_first_angle_arc
print(f"{first_angle_arc_min:.4f}")
print(f"{first_angle_arc_max:.4f}")
print(f"{first_angle_arc_mean:.4f}")
print(f"{first_angle_arc_bias:.4f}")

delta_last_dist_arc = [value - real_first_angle_arc for value in last_dist_arc]
delta_first_angle_arc_min = min(delta_last_dist_arc)
delta_first_angle_arc_max = max(delta_last_dist_arc)
delta_first_angle_arc_mean = np.mean(delta_last_dist_arc)

fig3, axs3 = plt.subplots(figsize=(15, 6))
axs3.plot(delta_last_dist_arc, marker='.', linestyle='None', color='b', label='Medición angular')
axs3.set_title(f"Deltas de la primera medición angular en arco de {nominal_radius} mm de radio, iniciado a {real_first_angle_arc}°")
axs3.set_xlabel("Índice de la medición")
axs3.set_ylabel("Delta angular (°)")
axs3.legend()
axs3.grid(True)
axs3.set_xlim([0, len(delta_last_dist_arc)-1])
axs3.text(0.82, 0.90, f"Valor mínimo: {delta_first_angle_arc_min:.4f}", fontsize=letter_size, color='black', bbox=dict(facecolor='white', edgecolor='none'), linespacing=0.9, transform=axs3.transAxes)
axs3.text(0.82, 0.87, f"Valor máximo: {delta_first_angle_arc_max:.4f}", fontsize=letter_size, color='black', bbox=dict(facecolor='white', edgecolor='none'), linespacing=0.9, transform=axs3.transAxes)
axs3.text(0.82, 0.84, f"Promedio: {delta_first_angle_arc_mean:.4f}", fontsize=letter_size, color='black', bbox=dict(facecolor='white', edgecolor='none'), linespacing=0.9, transform=axs1.transAxes)

fig4, axs4 = plt.subplots()
n_bins_sturges_fig4 = int(np.ceil(np.log2(len(last_dist_arc)) + 1))
axs4.hist(delta_last_dist_arc, bins=9, color='skyblue', edgecolor='black')
axs4.set_title(f'Distribución de los deltas del ángulo inicial medido en el arco de {nominal_radius} mm de radio')
axs4.set_xlabel('Deltas de ángulo inicial medido')
axs4.set_ylabel('Frecuencia')

plt.show()

real_first_angle_outer= 42

first_angle_outer_min = min(first_dist_after_arc)
first_angle_outer_max = max(first_dist_after_arc)
first_angle_outer_mean = np.mean(first_dist_after_arc)
#first_angle_outer_var = np.var(first_dist_after_arc, ddof=1)
first_angle_outer_bias = first_angle_outer_mean - real_first_angle_outer
print(f"{first_angle_outer_min:.4f}")
print(f"{first_angle_outer_max:.4f}")
print(f"{first_angle_outer_mean:.4f}")
print(f"{first_angle_outer_bias:.4f}")


delta_first_dist_after_arc = [value - real_first_angle_outer for value in first_dist_after_arc]
delta_first_angle_outer_min = min(delta_first_dist_after_arc)
delta_first_angle_outer_max = max(delta_first_dist_after_arc)
delta_first_angle_outer_mean = np.mean(delta_first_dist_after_arc)

fig5, axs5 = plt.subplots(figsize=(15, 6))
axs5.plot(delta_first_dist_after_arc, marker='.', linestyle='None', color='b', label='Medición angular')
axs5.set_title(f"Última medición angular en círculo de {nominal_radius+20} mm de radio, finalizado a {real_first_angle_outer}°")
axs5.set_xlabel("Índice de la medición")
axs5.set_ylabel("Medición angular (°)")
axs5.legend()
axs5.grid(True)
axs5.set_xlim([0, len(delta_first_dist_after_arc)-1])
axs5.text(0.82, 0.90, f"Valor mínimo: {delta_first_angle_outer_min:.4f}", fontsize=letter_size, color='black', bbox=dict(facecolor='white', edgecolor='none'), linespacing=0.9, transform=axs5.transAxes)
axs5.text(0.82, 0.87, f"Valor máximo: {delta_first_angle_outer_max:.4f}", fontsize=letter_size, color='black', bbox=dict(facecolor='white', edgecolor='none'), linespacing=0.9, transform=axs5.transAxes)
axs5.text(0.82, 0.84, f"Promedio: {delta_first_angle_outer_mean:.4f}", fontsize=letter_size, color='black', bbox=dict(facecolor='white', edgecolor='none'), linespacing=0.9, transform=axs1.transAxes)


fig6, axs6 = plt.subplots()
n_bins_sturges_fig6 = int(np.ceil(np.log2(len(first_dist_after_arc)) + 1))
axs6.hist(first_dist_after_arc, bins=9, color='skyblue', edgecolor='black')
axs6.set_title(f'Distribución de los deltas del ángulo final medido para el círculo de {nominal_radius+20} mm de radio')
axs6.set_xlabel(f'Deltas del ángulo final medido')
axs6.set_ylabel('Frecuencia')

plt.show()

real_last_angle_outer= 47

last_angle_outer_min = min(last_dist_before_arc)
last_angle_outer_max  = max(last_dist_before_arc)
last_angle_outer_mean = np.mean(last_dist_before_arc)
#last_angle_outer_var = np.var(last_dist_before_arc, ddof=1)
last_angle_outer_bias = last_angle_outer_mean - real_last_angle_outer
print(f"{last_angle_outer_min:.4f}")
print(f"{last_angle_outer_max:.4f}")
print(f"{last_angle_outer_mean:.4f}")
print(f"{last_angle_outer_bias:.4f}")


delta_last_dist_before_arc = [value - real_last_angle_outer for value in last_dist_before_arc]
delta_last_angle_outer_min = min(delta_last_dist_before_arc)
delta_last_angle_outer_max  = max(delta_last_dist_before_arc)
delta_last_angle_outer_mean = np.mean(delta_last_dist_before_arc)


fig7, axs7 = plt.subplots(figsize=(15, 6))
axs7.plot(delta_last_dist_before_arc, marker='.', linestyle='None', color='b', label='Medición angular')
axs7.set_title(f"Deltas de la primera medición angular en círculo de {nominal_radius+20} mm de radio, iniciado a {real_last_angle_outer}°")
axs7.set_xlabel("Índice de la medición")
axs7.set_ylabel("Delta angular (°)")
axs7.legend()
axs7.grid(True)
axs7.set_xlim([0, len(delta_last_dist_before_arc)-1])
axs7.text(0.82, 0.90, f"Valor mínimo: {delta_last_angle_outer_min:.4f}", fontsize=letter_size, color='black', bbox=dict(facecolor='white', edgecolor='none'), linespacing=0.9, transform=axs7.transAxes)
axs7.text(0.82, 0.87, f"Valor máximo: {delta_last_angle_outer_max:.4f}", fontsize=letter_size, color='black', bbox=dict(facecolor='white', edgecolor='none'), linespacing=0.9, transform=axs7.transAxes)
axs7.text(0.82, 0.84, f"Promedio: {delta_last_angle_outer_mean:.4f}", fontsize=letter_size, color='black', bbox=dict(facecolor='white', edgecolor='none'), linespacing=0.9, transform=axs1.transAxes)

fig8, axs8 = plt.subplots()
n_bins_sturges_fig8 = int(np.ceil(np.log2(len(last_dist_before_arc)) + 1))
axs8.hist(delta_last_dist_before_arc, bins=8, color='skyblue', edgecolor='black')
axs8.set_title(f'Distribución de los deltas del ángulo inicial medido para el círculo de {nominal_radius+20} mm de radio')
axs8.set_xlabel(f'Deltas del ángulo inicial medido')
axs8.set_ylabel('Frecuencia')

plt.show()
'''