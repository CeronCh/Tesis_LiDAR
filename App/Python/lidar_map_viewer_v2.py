#%%
from tkinter import *
from tkinter import filedialog
import customtkinter
import serial
import serial.tools.list_ports as serial_ports
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import numpy as np
import time
from scipy import stats
from sklearn.metrics import mean_squared_error
from sklearn.linear_model import LinearRegression
import csv
from scipy import stats
import statsmodels.api as sm
import tkinter as tk

# -------------------------------------------Funciones para interfaz grafica-------------------------------------------
# Parámetros para el control deslizante que permite seleccionar el número de revoluciones para la captura de datos.
start_slider = 1
end_slider =  6
step_slider = 6
# Variables inicializadas en cero que se utilizan a nivel globlal
fig3 = None
LiDAR = None
real_radius = None
real_theta = None
data = []
extracted_hex_data = []
old_angle_rad = []
old_angle_deg = []
new_angle_rad = []
new_angle_deg = []
radio_dist = []
distx = []
disty = []
new_angles_rads = []
new_angle_degs = []
radio_dist_no_zeros = []
x_coords = []
y_coords = []

def open_port():
    global LiDAR
    expected_length = 60
    catch_button.configure(state="disabled")
    selected_port = port_menu.get()
    if selected_port:
        try:
            LiDAR = serial.Serial(selected_port, 230400, timeout = 10)
            port_selected_label.configure(text = f"Conectado {selected_port}")
            if LiDAR and LiDAR.is_open:
                num_data = 5
                for i in range(num_data):
                    try:
                        buffer = LiDAR.read_until(b"\n").strip()
                        if buffer.startswith(b'542C') and len(buffer) == expected_length:
                            pass
                        else:
                            pass
                    except serial.SerialTimeoutException:
                        pass
                    except Exception as e:
                        pass
                catch_button.configure(state = "normal")
                print(f"Conectado a {selected_port}")
                port_menu.configure(state = "disabled")
                open_button.configure(state = "disabled")
                return LiDAR
            else:
                print("El puerto no está abierto.")
        except serial.SerialException as e:
            print(f"No se pudo abrir {selected_port}: {str(e)}")
            port_selected_label.configure(text = f"No se conectó")
            catch_button.configure(state = "disabled")
    else:
        print("No se seleccionó ningún puerto.")
        port_selected_label.configure(text = "Seleccione puerto")
        catch_button.configure(state = "disabled")

def catch_samples():
    global LiDAR, data, extracted_hex_data, old_angle_rad, old_angle_deg, new_angle_rad, new_angle_deg, radio_dist, distx, disty, new_angles_rads, radio_dist_no_zeros, x_coords, y_coords, new_angle_degs
    expected_length = 60
    catch_button.configure(state = "disabled")
    revolution_slider.configure(state = "disabled")
    cw_rad.configure(state = "disabled")
    ccw_rad.configure(state = "disabled")
    save_data_button.configure(state = "disabled")
    save_data_hex_button.configure(state = "disabled")
    save_data_dec_button.configure(state = "disabled")
    save_processed_button.configure(state = "disabled")
    save_filtered_button.configure(state = "disabled")
    init_time = time.time()
    old_angle_rad, old_angle_deg, new_angle_rad, new_angle_deg, radio_dist, distx, disty = [], [], [], [], [], [], []
    LiDAR.reset_input_buffer()
    data = []
    if LiDAR and LiDAR.is_open:
        if int(revolution_slider.get()) == start_slider:
            num_data = expected_length
        elif int(revolution_slider.get()) == (end_slider/step_slider):
            num_data = expected_length*(end_slider/step_slider)
        elif int(revolution_slider.get()) == (end_slider/step_slider)*2:
            num_data = expected_length*(end_slider/step_slider)*2
        elif int(revolution_slider.get()) == (end_slider/step_slider)*3:
            num_data = expected_length*(end_slider/step_slider)*3
        elif int(revolution_slider.get()) == (end_slider/step_slider)*4:
            num_data = expected_length*(end_slider/step_slider)*4
        elif int(revolution_slider.get()) == (end_slider/step_slider)*5:
            num_data = expected_length*(end_slider/step_slider)*5
        elif int(revolution_slider.get()) == end_slider:
            num_data = expected_length*end_slider
        count = 0
        while count < num_data:
            try:
                buffer = LiDAR.read_until(b"\n").strip()
                if buffer.startswith(b'542C') and len(buffer) == expected_length:
                    data.append(buffer)
                    count += 1
                else:
                   pass
            except serial.SerialTimeoutException:
                print(f"Timeout en la muestra {count + 1}")
            except Exception as e:
                print(f"Error al leer el puerto: {str(e)}, muestra {count + 1}")
                break
        if count == num_data:
            headerless_data = strip_header(data)
            extracted_hex_data = split_data_hex(headerless_data)
            extracted_dec_data = convert_hex_dec(extracted_hex_data)
            old_angle_rad, old_angle_deg, new_angle_rad, new_angle_deg, radio_dist, distx, disty = process_dec_data(extracted_dec_data)
            new_angles_rads, radio_dist_no_zeros, x_coords, y_coords, new_angle_degs = filter_zero_distances(new_angle_rad, radio_dist, distx, disty, new_angle_deg)
            plots(new_angles_rads, radio_dist_no_zeros, x_coords, y_coords)
            
            #-----------------------------------SE PUEDE BORRAR
            #print("Datos procesados:")
            #for i, sample in enumerate(radio_dist, 1):
            #    print(f"Muestra procesada {i}: {sample}")
            #-----------------------------------SE PUEDE BORRAR
        final_time = time.time()
        total_time = final_time-init_time
        time_label2.configure(text = f"{total_time:.5f} s.")
        catch_button.configure(state = "normal")
        revolution_slider.configure(state = "normal")
        cw_rad.configure(state = "normal")
        ccw_rad.configure(state = "normal")
        save_data_button.configure(state = "normal")
        save_data_hex_button.configure(state = "normal")
        save_data_dec_button.configure(state = "normal")
        save_processed_button.configure(state = "normal")
        save_filtered_button.configure(state = "normal")
        return old_angle_rad, old_angle_deg, new_angle_rad, new_angle_deg, radio_dist, distx, disty
    else:
        print("El puerto no está abierto.")
        catch_button.configure(state = "normal")
        revolution_slider.configure(state = "normal")
        cw_rad.configure(state = "normal")
        ccw_rad.configure(state = "normal")
        save_data_button.configure(state = "disabled")
        save_data_hex_button.configure(state = "disabled")
        save_data_dec_button.configure(state = "disabled")
        save_processed_button.configure(state = "disabled")
        save_filtered_button.configure(state = "disabled")
        save_data_hex_button.configure(state = "disabled")
        return None, None, None, None, None, None, None

def strip_header(data_in):
    trim_data = []
    for item in data_in:
        if item.startswith(b'542C'):
            relevant_data = item[4:]
            trim_data.append(relevant_data)
    return trim_data
  
def split_data_hex(trim_data):
    hex_data = []
    for item in trim_data:
        hex_values = [item[i:i+2].decode('utf-8') for i in range(0, len(item), 2)]
        hex_data.append(hex_values)
    return hex_data

def convert_hex_dec(hex_data):
    dec_data = []
    for item in hex_data:
        dec_values = [int(value, 16) for value in item]
        dec_data.append(dec_values)
    return dec_data

def process_dec_data(dec_data):
    points = 12
    y_factor = 0.11923
    x_offset = 5.9
    y_offset = -18.975571
    last_shift_delta = 0
    shift = 0
    orientation = orientation_var.get()
    dist_angl = np.zeros((len(dec_data)*points, 5))
    angles = np.full(points, 3.14)
    index = 0
    for item in dec_data:
        start_angle_l = item[0]
        start_angle_h = item[1]
        start_angle = ((start_angle_h << 8)|start_angle_l)/100.00

        distances = np.zeros(points)
        for m in range(points):
            idx = 2+2*m
            dist_l = item[idx]
            dist_h = item[idx+1]
            distances[m] = (dist_h << 8)|dist_l
        
        end_angle_l = item[26]
        end_angle_h = item[27]
        end_angle = ((end_angle_h << 8)|end_angle_l)/100.00

        if start_angle > end_angle:
            step_angle = (360-start_angle+end_angle)/(points-1)
        else:
            step_angle = (end_angle-start_angle)/(points-1)
        
        angles = np.zeros(points)
        for l in range(points):
            angles[l] = start_angle + step_angle * l
        
        for b in range(points):
            if distances[b] > 0:
                x_val = distances[b] + x_offset
                y_val = distances[b]*y_factor+y_offset
                shift = np.degrees(np.arctan(y_val/x_val))
                if orientation == "CCW":
                    new_angle = (360 - angles[b])+shift
                else:
                    new_angle = angles[b]-shift
                last_shift_delta = shift
            else:
                if orientation == "CCW":
                    new_angle = (360-angles[b])+last_shift_delta
                else:
                    new_angle = angles[b]-last_shift_delta
            if new_angle>360:
                new_angle -= 360
            if new_angle<0:
                new_angle += 360
            dist_angl[index, 0] = np.radians(angles[b])
            dist_angl[index, 1] = angles[b]
            dist_angl[index, 2] = np.radians(new_angle)
            dist_angl[index, 3] = new_angle
            dist_angl[index, 4] = distances[b]
            index += 1

    indx = 0    
    dist_cc = np.zeros((len(dec_data) * points, 2))
    for p in range(len(dec_data)*points):
        dist_cc[indx, 0] = dist_angl[p, 4]*np.cos(dist_angl[p, 2])
        dist_cc[indx, 1] = dist_angl[p, 4]*np.sin(dist_angl[p, 2])
        indx += 1
    return dist_angl[:, 0], dist_angl[:, 1], dist_angl[:, 2], dist_angl[:, 3], dist_angl[:, 4], dist_cc[:, 0], dist_cc[:, 1]

def filter_zero_distances(new_angles_rads, distances, x_coords, y_coords, new_angle_degs):
    mask_zero = distances > 0
    return (new_angles_rads[mask_zero], distances[mask_zero], x_coords[mask_zero], y_coords[mask_zero], new_angle_degs[mask_zero])

def on_closing():
    axes1_canvas.get_tk_widget().destroy()
    fig1.clear()
    plt.close(fig1)
    axes2_canvas.get_tk_widget().destroy()
    fig2.clear()
    plt.close(fig2)
    plt.close('all')
    main_window.quit()
    main_window.destroy()

def plots(theta, r, x, y):
    ax1.clear()
    ax2.clear()
    ax1.set_facecolor("#212121") 
    ax2.set_facecolor("#212121")
    ax1.spines["polar"].set_edgecolor("white")
    ax2.spines["top"].set_edgecolor("white")
    ax2.spines["bottom"].set_edgecolor("white")
    ax2.spines["left"].set_edgecolor("white")
    ax2.spines["right"].set_edgecolor("white")

    ax1.tick_params(axis = "both", colors = "white")
    ax2.tick_params(axis = "both", colors = "white")
    ax1.plot(theta, r, ".", color = "cyan", markersize = 3) 
    ax2.plot(x, y, ".", color = "cyan", markersize = 3)
    axes1_canvas.draw()
    axes2_canvas.draw()
    r = []
    theta = []
    x = []
    y = []  

def sliding(value):
    n_samples_label.configure(text = f"Revoluciones: {int(revolution_slider.get())}")

def save_data_to_csv():
    global data
    try:
        save_data_csv = Tk()
        save_data_csv.withdraw()
        filename = filedialog.asksaveasfilename(defaultextension='.csv', filetypes=[('CSV files', '*.csv')], initialfile='output_data.csv')
        if filename:
            with open(filename, mode='w', newline='') as file:
                data_to_csv = csv.writer(file)
                for row in data:
                    data_to_csv.writerow([row])
            print(f"Datos guardados exitosamente en {filename}.")
        else:
            print("No se seleccionó ningún archivo.")
    except Exception as e:
        print(f"Error al guardar los datos en el archivo CSV: {str(e)}")
    pass

def save_hex_data():
    global extracted_hex_data
    try:
        save_hex_csv = Tk()
        save_hex_csv.withdraw()
        filename = filedialog.asksaveasfilename(defaultextension='.csv', filetypes=[('CSV files', '*.csv')], initialfile='output_data.csv')
        if filename:
            with open(filename, mode='w', newline='') as file:
                hex_to_csv = csv.writer(file)
                for row in extracted_hex_data:
                    hex_to_csv.writerow(row)
            print(f"Datos hexadecimales extraídos guardados en {filename}.")
        else:
            print("No se seleccionó ningún archivo.")
    except Exception as e:
        print(f"Error al guardar los datos hexadecimales: {str(e)}")
    pass

def save_dec_data():
    global extracted_dec_data
    try:
        save_dec_csv = Tk()
        save_dec_csv.withdraw()
        filename = filedialog.asksaveasfilename(defaultextension='.csv', filetypes=[('CSV files', '*.csv')], initialfile='output_data.csv')
        if filename:
            with open(filename, mode='w', newline='') as file:
                dec_to_csv = csv.writer(file)
                for row in extracted_dec_data:
                    dec_to_csv.writerow(row)
            print(f"Datos decimales extraídos guardados en {filename}.")
        else:
            print("No se seleccionó ningún archivo.")
    except Exception as e:
        print(f"Error al guardar los datos decimales: {str(e)}")
    pass

def save_processed_data():
    global old_angle_rad, old_angle_deg, new_angle_rad, new_angle_deg, radio_dist, distx, disty
    try:
        save_processed_csv = Tk()
        save_processed_csv.withdraw()
        filename = filedialog.asksaveasfilename(defaultextension='.csv', filetypes=[('CSV files', '*.csv')], initialfile='output_data.csv')
        if filename:
            with open(filename, mode='w', newline='') as file:
                processed_to_csv = csv.writer(file)
                processed_to_csv.writerow(['Old Angle (Rad)', 'Old Angle (Deg)', 'New Angle (Rad)', 'New Angle (Deg)', 'Radio', 'Distx', 'Disty'])
                for i in range(len(old_angle_rad)):
                    processed_to_csv.writerow([old_angle_rad[i], old_angle_deg[i], new_angle_rad[i], new_angle_deg[i], radio_dist[i], distx[i], disty[i]])
            print(f"Datos procesados guardados en {filename}.")
        else:
            print("No se seleccionó ningún archivo.")
    except Exception as e:
        print(f"Error al guardar los datos procesados: {str(e)}")

def save_filtered_data():
    global new_angles_rads, radio_dist_no_zeros, x_coords, y_coords, new_angle_degs
    try:
        save_filtered_csv = Tk()
        save_filtered_csv.withdraw()
        filename = filedialog.asksaveasfilename(defaultextension='.csv', filetypes=[('CSV files', '*.csv')], initialfile='output_data.csv')
        if filename:
            with open(filename, mode='w', newline='') as file:
                filtered_to_csv = csv.writer(file)
                filtered_to_csv.writerow(['New Angle (Rad)', 'Radio Filtered', 'X coords', 'Y coords', 'New Angle (Deg)'])
                for i in range(len(new_angles_rads)):
                    filtered_to_csv.writerow([new_angles_rads[i], radio_dist_no_zeros[i], x_coords[i], y_coords[i], new_angle_degs[i]])
            print(f"Datos filtrados guardados en {filename}.")
        else: 
            print("No se seleccionó ningún archivo.")
    except Exception as e:
        print(f"Error al guardar los datos filtrados: {str(e)}")

def edge_filter(x_coord, y_coord, edge, real_value, interval, border_exclusion):
    if edge == "Horizontal":
        nominal_val = 200
        edge_mask = (np.abs(y_coord-real_value) <= interval) & (np.abs(x_coord)<(nominal_val-border_exclusion))
    elif edge == "Vertical":
        nominal_val = 200
        edge_mask = (np.abs(x_coord-real_value) <= interval) & (np.abs(y_coord)<(nominal_val-border_exclusion))
    print(f"Puntos filtrados para {edge}: {np.sum(edge_mask)}")
    return x_coord[edge_mask], y_coord[edge_mask]

def fit_regression(x, y, edge):
    regression_linear = LinearRegression()
    predicted_line = None
    if edge == "Horizontal":
        regression_linear.fit(x.reshape(-1, 1), y)
        predicted_line = regression_linear.predict(x.reshape(-1, 1))
    elif edge == "Vertical":
        regression_linear.fit(y.reshape(-1, 1), x)
        predicted_line = regression_linear.predict(y.reshape(-1, 1))
    else:
        raise ValueError(f"Valor de 'edge' inesperado: {edge}. Use 'Horizontal' o 'Vertical'.")
    
    return regression_linear, predicted_line

def edges_analysis():
    global x_coords, y_coords, fig3
    plt.close('fig1')
    plt.close('fig2')
    plt.close('all')
    letter_size = 7
    expected_value_sup = 200
    interval_sup = 5
    border_exclusion_sup = 8
    x_sup, y_sup = edge_filter(x_coords, y_coords, "Horizontal", expected_value_sup, interval_sup, border_exclusion_sup)
    regression_linear_sup, predicted_line_sup = fit_regression(x_sup, y_sup, "Horizontal")
    
    coef_sup = regression_linear_sup.coef_[0]
    intercept_sup = regression_linear_sup.intercept_
    rmse_sup = np.sqrt(mean_squared_error(y_sup, predicted_line_sup))
    x_with_intercept_sup = sm.add_constant(x_sup)
    model_sup = sm.OLS(y_sup, x_with_intercept_sup)
    results_sup = model_sup.fit()
    confidence_intervals_sup = results_sup.conf_int(alpha=0.05)
    differences_sup = y_sup - expected_value_sup
    mean_difference_sup = np.mean(differences_sup)
    max_value_sup = np.max(y_sup)
    min_value_sup = np.min(y_sup)
    range_value_sup = max_value_sup - min_value_sup

    fig3, ax3 = plt.subplots(figsize=(8, 4), num='fig3')
    ax3.scatter(x_sup, y_sup, color = "blue", s = 3, label='Arista superior')
    ax3.plot(x_sup, predicted_line_sup, color='red', label='Regresión superior')
    
    ax3.text(90, 198, f"Ecuación: y = {coef_sup:.4f}x + {intercept_sup:.4f}", fontsize=letter_size, color='black')
    ax3.text(90, 197, f"RMSE: {rmse_sup:.4f}", fontsize=letter_size, color='black')
    ax3.text(90, 196, f"IC Pendiente: ({confidence_intervals_sup[1][0]:.4f}, {confidence_intervals_sup[1][1]:.4f})", fontsize=letter_size, color='black')
    ax3.text(90, 195, f"IC Intercepto: ({confidence_intervals_sup[0][0]:.4f}, {confidence_intervals_sup[0][1]:.4f})", fontsize=letter_size, color='black')
    ax3.text(90, 194, f"Diferencia promedio: {mean_difference_sup:.4f}", fontsize=letter_size, color='black')
    ax3.text(90, 193, f"Punto máximo: {max_value_sup:.4f}", fontsize=letter_size, color='black')
    ax3.text(90, 192, f"Punto mínimo: {min_value_sup:.4f}", fontsize=letter_size, color='black')
    ax3.text(90, 191, f"Rango: {range_value_sup:.4f}", fontsize=letter_size, color='black')


    ax3.set_xlim([-210, 210])
    ax3.set_ylim([190, 210])
    
    ax3.legend()
    ax3.set_title('Análisis de arista horizontal superior')
    

    expected_value_inf = -200
    interval_inf = 5
    border_exclusion_inf = 8
    x_inf, y_inf = edge_filter(x_coords, y_coords, "Horizontal", expected_value_inf, interval_inf, border_exclusion_inf)
    regression_linear_inf, predicted_line_inf = fit_regression(x_inf, y_inf, "Horizontal")
    
    coef_inf = regression_linear_inf.coef_[0]
    intercept_inf = regression_linear_inf.intercept_
    rmse_inf = np.sqrt(mean_squared_error(y_inf, predicted_line_inf))
    x_with_intercept_inf = sm.add_constant(x_inf)
    model_inf = sm.OLS(y_inf, x_with_intercept_inf)
    results_inf = model_inf.fit()
    confidence_intervals_inf = results_inf.conf_int(alpha=0.05)
    differences_inf = y_inf - expected_value_inf
    mean_difference_inf = np.mean(differences_inf)
    max_value_inf = np.max(y_inf)
    min_value_inf = np.min(y_inf)
    range_value_inf = max_value_inf - min_value_inf

    fig4, ax4 = plt.subplots(figsize=(8, 4), num='fig4')
    ax4.scatter(x_inf, y_inf, color = "blue", s = 3, label='Arista inferior')
    ax4.plot(x_inf, predicted_line_inf, color='red', label='Regresión inferior')
    
    ax4.text(88, -198, f"Ecuación: y = {coef_inf:.4f}x + {intercept_inf:.4f}", fontsize=letter_size, color='black')
    ax4.text(88, -197, f"RMSE: {rmse_inf:.4f}", fontsize=letter_size, color='black')
    ax4.text(88, -196, f"IC Pendiente: ({confidence_intervals_inf[1][0]:.4f}, {confidence_intervals_inf[1][1]:.4f})", fontsize=letter_size, color='black')
    ax4.text(88, -195, f"IC Intercepto: ({confidence_intervals_inf[0][0]:.4f}, {confidence_intervals_inf[0][1]:.4f})", fontsize=letter_size, color='black')
    ax4.text(88, -194, f"Diferencia promedio: {mean_difference_inf:.4f}", fontsize=letter_size, color='black')
    ax4.text(88, -193, f"Punto máximo: {max_value_inf:.4f}", fontsize=letter_size, color='black')
    ax4.text(88, -192, f"Punto mínimo: {min_value_inf:.4f}", fontsize=letter_size, color='black')
    ax4.text(88, -191, f"Rango: {range_value_inf:.4f}", fontsize=letter_size, color='black')


    ax4.set_xlim([-210, 210])
    ax4.set_ylim([-190, -210])
    
    ax4.legend()
    ax4.set_title('Análisis de arista horizontal inferior')
    
    expected_value_right = 200
    interval_right = 5
    border_exclusion_right = 8
    x_right, y_right = edge_filter(x_coords, y_coords, "Vertical", expected_value_right, interval_right, border_exclusion_right)
    regression_linear_right, predicted_line_right = fit_regression(x_right, y_right, "Vertical")
    
    coef_right = regression_linear_right.coef_[0]
    intercept_right = regression_linear_right.intercept_
    rmse_right = np.sqrt(mean_squared_error(x_right, predicted_line_right))
    #std_dev_right = np.std(y_right - predicted_line_right)
    x_with_intercept_right = sm.add_constant(y_right)  # Agregar una constante para el intercepto
    model_right = sm.OLS(x_right, x_with_intercept_right)
    results_right = model_right.fit()
    confidence_intervals_right = results_right.conf_int(alpha=0.05)
    differences_right = x_right - expected_value_right
    mean_difference_right = np.mean(differences_right)
    max_value_right = np.max(x_right)
    min_value_right = np.min(x_right)
    range_value_right = max_value_right - min_value_right

    fig5, ax5 = plt.subplots(figsize=(5, 8), num='fig5')
    ax5.scatter(x_right, y_right, color = "blue", s = 3, label='Arista derecha')
    ax5.plot(predicted_line_right, y_right, color='red', label='Regresión derecha')
    
    ax5.text(191, 160, f"Ecuación: y = {coef_right:.4f}x + {intercept_right:.4f}", fontsize=letter_size, color='black')
    ax5.text(191, 150, f"RMSE: {rmse_right:.4f}", fontsize=letter_size, color='black')
    #ax5.text(190, -197, f"Desviación Estándar: {std_dev_sup:.4f}", fontsize=letter_size, color='black')
    ax5.text(191, 140, f"IC Pendiente: ({confidence_intervals_right[1][0]:.4f}, {confidence_intervals_right[1][1]:.4f})", fontsize=letter_size, color='black')
    ax5.text(191, 130, f"IC Intercepto: ({confidence_intervals_right[0][0]:.4f}, {confidence_intervals_right[0][1]:.4f})", fontsize=letter_size, color='black')
    ax5.text(191, 120, f"Diferencia promedio: {mean_difference_right:.4f}", fontsize=letter_size, color='black')
    ax5.text(191, 110, f"Punto máximo: {max_value_right:.4f}", fontsize=letter_size, color='black')
    ax5.text(191, 100, f"Punto mínimo: {min_value_right:.4f}", fontsize=letter_size, color='black')
    ax5.text(191, 90, f"Rango: {range_value_right:.4f}", fontsize=letter_size, color='black')


    ax5.set_xlim([190, 210])
    ax5.set_ylim([-210, 210])
    
    ax5.legend()
    ax5.set_title('Análisis de arista vertical derecha')
    
    expected_value_left = -200
    interval_left = 5
    border_exclusion_left = 8
    x_left, y_left = edge_filter(x_coords, y_coords, "Vertical", expected_value_left, interval_left, border_exclusion_left)
    regression_linear_left, predicted_line_left = fit_regression(x_left, y_left, "Vertical")
    
    coef_left = regression_linear_left.coef_[0]
    intercept_left = regression_linear_left.intercept_
    rmse_left = np.sqrt(mean_squared_error(x_left, predicted_line_left))
    #std_dev_left = np.std(y_left - predicted_line_left)
    x_with_intercept_left = sm.add_constant(y_left)  # Agregar una constante para el intercepto
    model_left = sm.OLS(x_left, x_with_intercept_left)
    results_left = model_left.fit()
    confidence_intervals_left = results_left.conf_int(alpha=0.05)
    differences_left = x_left - expected_value_left
    mean_difference_left = np.mean(differences_left)
    max_value_left = np.max(x_left)
    min_value_left = np.min(x_left)
    range_value_left = max_value_left - min_value_left

    fig6, ax6 = plt.subplots(figsize=(5, 8), num='fig6')
    ax6.scatter(x_left, y_left, color = "blue", s = 3, label='Arista izquierda')
    ax6.plot(predicted_line_left, y_left, color='red', label='Regresión izquierda')
    
    ax6.text(-191, 160, f"Ecuación: y = {coef_left:.4f}x + {intercept_left:.4f}", fontsize=letter_size, color='black')
    ax6.text(-191, 150, f"RMSE: {rmse_left:.4f}", fontsize=letter_size, color='black')
    #ax6.text(-191, -197, f"Desviación Estándar: {std_dev_sup:.4f}", fontsize=letter_size, color='black')
    ax6.text(-191, 140, f"IC Pendiente: ({confidence_intervals_left[1][0]:.4f}, {confidence_intervals_left[1][1]:.4f})", fontsize=letter_size, color='black')
    ax6.text(-191, 130, f"IC Intercepto: ({confidence_intervals_left[0][0]:.4f}, {confidence_intervals_left[0][1]:.4f})", fontsize=letter_size, color='black')
    ax6.text(-191, 120, f"Diferencia promedio: {mean_difference_left:.4f}", fontsize=letter_size, color='black')
    ax6.text(-191, 110, f"Punto máximo: {max_value_left:.4f}", fontsize=letter_size, color='black')
    ax6.text(-191, 100, f"Punto mínimo: {min_value_left:.4f}", fontsize=letter_size, color='black')
    ax6.text(-191, 90, f"Rango: {range_value_left:.4f}", fontsize=letter_size, color='black')


    ax6.set_xlim([-190, -210])
    ax6.set_ylim([-210, 210])
    
    ax6.legend()
    ax6.set_title('Análisis de arista vertical izquierda')
    
    fig7, ax7 = plt.subplots(figsize=(8, 8), num='fig7')
    ax7.scatter(x_sup, y_sup, color = "blue", s = 3)
    ax7.plot(x_sup, predicted_line_sup, color='red')
    ax7.scatter(x_inf, y_inf, color = "blue", s = 3)
    ax7.plot(x_inf, predicted_line_inf, color='red')
    ax7.scatter(x_right, y_right, color = "blue", s = 3)
    ax7.plot(predicted_line_right, y_right, color='red')
    ax7.scatter(x_left, y_left, color = "blue", s = 3, label='Puntos capturados')
    ax7.plot(predicted_line_left, y_left, color='red', label='Regresión realizada')
    ax7.set_xlim([-210, 210])
    ax7.set_ylim([-210, 210])
    
    ax7.legend()
    ax7.set_title('Análisis de reconstrucción')
    
    plt.show()
    #plt.axhline(200, color='black', linestyle='--')
    #plt.axhline(-200, color='black', linestyle='--')
    
    # x_inf, y_inf = edge_filter(x_coords, y_coords, "Horizontal", -200, 5, 8)
    # regression_linear_inf, predicted_line_inf = fit_regression(x_inf, y_inf, "Horizontal")
    
    # plt.scatter(x_inf, y_inf, color='red', label='Arista inferior')
    # plt.plot(x_inf, predicted_line_inf, color='red', label='Regresión inferior')
    

    # x_right, y_right = edge_filter(x_coords, y_coords, "Vertical", 200, 5, 8)
    # regression_linear_right, predicted_line_right = fit_regression(x_right, y_right, "Vertical")
    
    # x_left, y_left = edge_filter(x_coords, y_coords, "Vertical", -200, 5, 8)
    # regression_linear_left, predicted_line_left = fit_regression(x_left, y_left, "Vertical")

    # plt.figure(figsize=(8, 4))
    # plt.scatter(x_right, y_right, color='green', label='Arista derecha')
    # plt.plot(x_right, predicted_line_right, color='green', label='Regresión derecha')
    
    # plt.scatter(x_left, y_left, color='purple', label='Arista izquierda')
    # plt.plot(x_left, predicted_line_left, color='purple', label='Regresión izquierda')
    
    # plt.xlim([-210, 210])
    # plt.ylim([-210, 210])
    # plt.axhline(200, color='black', linestyle='--')
    # plt.axhline(-200, color='black', linestyle='--')
    
    # plt.legend()
    # plt.title('Análisis de Aristas Verticales')
    # plt.show()

def radius_analysis():
    global radio_dist_no_zeros, real_radius

    letter_size = 10
    radius_mean = np.mean(radio_dist_no_zeros)
    radius_var = np.var(radio_dist_no_zeros, ddof=1)
    sta_des_s = np.std(radio_dist_no_zeros, ddof=1)
    dif_mean_radius = radius_mean - real_radius

    def on_closing_new_window(radius_windows_stats):
        plt.close(fig8)
        radius_windows_stats.destroy()
    def on_closing_new_window2(radius_windows):
        plt.close(fig9)
        radius_windows.destroy()
    radius_windows_stats = tk.Toplevel(main_window)
    radius_windows_stats.title("Gráfico de mediciones radiales con estadísticas")
    radius_windows_stats.protocol("WM_DELETE_WINDOW", lambda: on_closing_new_window(radius_windows_stats))


    fig8, ax8 = plt.subplots(figsize=(18, 8), num = "fig8")
    ax8.clear()
    
    ax8.plot(radio_dist_no_zeros, marker='.', linestyle='None', color='b', label='Medición radial')
    ax8.set_title(f"Gráfico de mediciones radiales para un radio real de {real_radius:.2f} mm")
    ax8.set_xlabel("Índice de la medición")
    ax8.set_ylabel("Distancia radial (mm)")
    ax8.legend()
    ax8.grid(True)
    ax8.set_xlim([0, len(radio_dist_no_zeros)-1])
    ax8.set_ylim([real_radius-10, real_radius+10])
    yticks = range(int(real_radius - 10)-1, int(real_radius + 10)+1, 2)
    ax8.set_yticks(yticks)
    ax8.text(0.85, 0.90, f"Promedio: {radius_mean:.4f}", fontsize=letter_size, color='black', bbox=dict(facecolor='white', edgecolor='none'), linespacing=0.9, transform=ax8.transAxes)
    ax8.text(0.85, 0.85, f"Varianza muestral: {radius_var:.4f}", fontsize=letter_size, color='black', bbox=dict(facecolor='white', edgecolor='none'), linespacing=0.9, transform=ax8.transAxes)
    ax8.text(0.85, 0.80, f"Desviación muestral: {sta_des_s:.4f}", fontsize=letter_size, color='black', bbox=dict(facecolor='white', edgecolor='none'), linespacing=0.9, transform=ax8.transAxes)
    ax8.text(0.85, 0.75, f"Bias: {dif_mean_radius:.4f}", fontsize=letter_size, color='black', bbox=dict(facecolor='white', edgecolor='none'), linespacing=0.9,transform=ax8.transAxes)

    axes8_canvas = FigureCanvasTkAgg(fig8, master=radius_windows_stats)
    axes8_canvas.draw()
    axes8_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    toolbar8 = NavigationToolbar2Tk(axes8_canvas, radius_windows_stats)
    toolbar8.update()
    toolbar8.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    radius_windows = tk.Toplevel(main_window)
    radius_windows.title("Gráfico de mediciones radiales")
    #radius_windows.geometry("800x600")

    radius_windows.protocol("WM_DELETE_WINDOW", lambda: on_closing_new_window2(radius_windows))
    
    fig9, ax9 = plt.subplots(figsize=(10, 6), num = "fig9")
    ax9.clear()
    ax9.plot(radio_dist_no_zeros, marker='.', linestyle='None', color='b', label='Medición radial')
    ax9.set_title(f"Gráfico de mediciones radiales para un radio real de {real_radius:.2f} mm")
    ax9.set_xlabel("Índice de la medición")
    ax9.set_ylabel("Distancia radial (mm)")
    ax9.legend()
    ax9.grid(True)
    ax9.set_xlim([0, len(radio_dist_no_zeros)-1])
    ax9.set_ylim([real_radius-10, real_radius+10])

    axes9_canvas = FigureCanvasTkAgg(fig9, master=radius_windows)
    axes9_canvas.draw()
    axes9_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    toolbar9 = NavigationToolbar2Tk(axes9_canvas, radius_windows)
    toolbar9.update()
    toolbar9.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    
def validate_radius():
    global real_radius
    radius_input = radius_entry.get()
    if not radius_input:
        print("Entrada inválida, ingrese un valor.")
        statics_circular_button.configure(state="disabled")
        return
    try:
        real_radius = float(radius_input)
    except ValueError:
        print("Entrada inválida, ingrese un número válido.")
        statics_circular_button.configure(state="disabled")
        return

    if real_radius < 9 or real_radius > 8000:
        print("Valor fuera de rango, ingrese un número entre 9 y 8000.")
        statics_circular_button.configure(state="disabled")
    else:
        statics_circular_button.configure(state="normal")
    
def validate_theta():
    global real_theta
    theta_input = theta_entry.get()
    if not theta_input:
        print("Entrada inválida, ingrese un valor.")
        statics_theta_button.configure(state="disabled")
        return
    try:
        real_theta = float(theta_input)
    except ValueError:
        print("Entrada inválida, ingrese un número válido.")
        statics_theta_button.configure(state="disabled")
        return

    if real_theta < 0 or real_theta > 360:
        print("Valor fuera de rango, ingrese un número entre 0 y 360.")
        statics_theta_button.configure(state="disabled")
    else:
        statics_theta_button.configure(state="normal")


def theta_analysis():
    global new_angle_degs, real_theta
    lower_limit_theta = real_theta-2.5
    upper_limit_theta = real_theta+2.5
    mask_angles = (new_angle_degs >= lower_limit_theta) & (new_angle_degs <= upper_limit_theta)
    filtered_angles = new_angle_degs[mask_angles]
    
    letter_size = 10
    theta_mean = np.mean(filtered_angles)
    theta_var = np.var(filtered_angles, ddof=1)
    theta_sta_des_s = np.std(filtered_angles, ddof=1)
    dif_mean_theta = theta_mean - real_theta

    def on_closing_new_window_theta(theta_windows_stats):
        plt.close(fig10)
        theta_windows_stats.destroy()
    def on_closing_new_window2_theta(theta_windows):
        plt.close(fig11)
        theta_windows.destroy()
    theta_windows_stats = tk.Toplevel(main_window)
    theta_windows_stats.title("Gráfico de mediciones angulares con estadísticas")
    #radius_windows_stats.geometry("800x600")
    theta_windows_stats.protocol("WM_DELETE_WINDOW", lambda: on_closing_new_window_theta(theta_windows_stats))


    fig10, ax10 = plt.subplots(figsize=(10, 6), num = "fig10")
    ax10.clear()
    
    ax10.plot(filtered_angles, marker='.', linestyle='None', color='b', label='Medición angular')
    ax10.set_title(f"Gráfico de mediciones angulares para un ángulo real de {real_theta:.2f}°")
    ax10.set_xlabel("Índice de la medición")
    ax10.set_ylabel("Meidicón angular (°)")
    ax10.legend()
    ax10.grid(True)
    ax10.set_xlim([0, len(filtered_angles)-1])
    ax10.set_ylim([real_theta-5, real_theta+5])
    ax10.text(0.85, 0.90, f"Promedio: {theta_mean:.4f}", fontsize=letter_size, color='black', bbox=dict(facecolor='white', edgecolor='none'), linespacing=0.9, transform=ax10.transAxes)
    ax10.text(0.85, 0.85, f"Varianza muestral: {theta_var:.4f}", fontsize=letter_size, color='black', bbox=dict(facecolor='white', edgecolor='none'), linespacing=0.9, transform=ax10.transAxes)
    ax10.text(0.85, 0.80, f"Desviación muestral: {theta_sta_des_s:.4f}", fontsize=letter_size, color='black', bbox=dict(facecolor='white', edgecolor='none'), linespacing=0.9, transform=ax10.transAxes)
    ax10.text(0.85, 0.75, f"Bias: {dif_mean_theta:.4f}", fontsize=letter_size, color='black', bbox=dict(facecolor='white', edgecolor='none'), linespacing=0.9,transform=ax10.transAxes)
#len(radio_dist_no_zeros)-401
    axes10_canvas = FigureCanvasTkAgg(fig10, master=theta_windows_stats)
    axes10_canvas.draw()
    axes10_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    toolbar10 = NavigationToolbar2Tk(axes10_canvas, theta_windows_stats)
    toolbar10.update()
    toolbar10.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    theta_windows = tk.Toplevel(main_window)
    theta_windows.title("Gráfico de mediciones angulares")
    #radius_windows.geometry("800x600")

    theta_windows.protocol("WM_DELETE_WINDOW", lambda: on_closing_new_window2_theta(theta_windows))
    
    fig11, ax11 = plt.subplots(figsize=(10, 6), num = "fig11")
    ax11.clear()
    ax11.plot(filtered_angles, marker='.', linestyle='None', color='b', label='Medición angular')
    ax11.set_title(f"Gráfico de mediciones angulares para un ángulo real de {real_theta:.2f}°")
    ax11.set_xlabel("Índice de la medición")
    ax11.set_ylabel("Medición angular (°)")
    ax11.legend()
    ax11.grid(True)
    ax11.set_xlim([0, len(filtered_angles)-1])
    ax11.set_ylim([real_theta-10, real_theta+10])

    axes11_canvas = FigureCanvasTkAgg(fig11, master=theta_windows)
    axes11_canvas.draw()
    axes11_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    toolbar11 = NavigationToolbar2Tk(axes11_canvas, theta_windows)
    toolbar11.update()
    toolbar11.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# -------------------------------------------Definicion de colores principales------------------------------------------
border_frame = "#6B6B6B"
border_widget = "#000000"
color_widget = "#1B2DA1"
color_hover_widget = "#3D84DB"
main_letter = "#FFFFFF"
# -------------------------------------------Definicion de pantalla principal-------------------------------------------
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")
main_window = customtkinter.CTk()
main_window.geometry("1015x700")
main_window.title("LiDAR MapViewer")
main_window.protocol("WM_DELETE_WINDOW", on_closing)
# ---------------------------------------Definicion de sección de conexión a COM----------------------------------------
conection_frame = customtkinter.CTkFrame(main_window)
conection_frame.configure(border_width = 1, border_color = border_frame)
conection_frame.grid(row = 0, column = 0, columnspan = 3, rowspan= 3, padx = 5, pady = 5)

conection_label = customtkinter.CTkLabel(conection_frame, text = "Conexión")
conection_label.configure(font = ("Helvetica", 12), text_color = main_letter)
conection_label.grid(row = 0, column = 0, sticky = "W", padx = 5, pady = 1)

port_selected_label = customtkinter.CTkLabel(conection_frame, text = "")
port_selected_label.configure(font = ("Helvetica", 12), text_color = main_letter)
port_selected_label.grid(row = 0, column = 1, columnspan = 2, padx = 5, pady = 1, sticky = "E")

line_canvas_frame1 = customtkinter.CTkCanvas(conection_frame, height = 1, bg = "#6B6B6B", highlightthickness = 0)
line_canvas_frame1.grid(row = 1, column = 0, columnspan = 3, sticky = "EW")
line_canvas_frame1.create_line(0, 0, 500, 0, fill = "#6B6B6B", width = 1)

com_label = customtkinter.CTkLabel(conection_frame, text = "Puerto COM:")
com_label.configure(font = ("Helvetica", 12), text_color = main_letter)
com_label.grid(row = 2, column = 0, padx = 5, pady = 5)

ports = [port.device for port in serial_ports.comports()]
port_menu = customtkinter.CTkComboBox(conection_frame,state = "readonly", values = ports)
port_menu.configure(height = 27, width = 150, font = ("Helvetica", 12), dropdown_font = ("Helvetica", 12), text_color = main_letter, corner_radius = 7, border_width = 1, border_color = border_widget, button_color = color_widget, dropdown_hover_color = color_hover_widget)
port_menu.grid(row = 2, column = 1, pady = 5)

open_button = customtkinter.CTkButton(conection_frame, text = "Abrir Puerto", command = open_port)
open_button.configure(height = 27, width = 100, font = ("Helvetica", 12), text_color = main_letter, fg_color = color_widget, hover_color = color_hover_widget, corner_radius = 7, border_width = 1, border_color = border_widget)
open_button.grid(row = 2, column = 2, padx = 5, pady = 5)

# ---------------------------------------Definicion de sección de toma de muestras----------------------------------------
samples_frame = customtkinter.CTkFrame(main_window)
samples_frame.configure(border_width = 1, border_color = border_frame)
samples_frame.grid(row = 0, column = 3, columnspan = 3, rowspan = 3, padx = 5, pady = 5)

samples_label = customtkinter.CTkLabel(samples_frame, text = "Revoluciones capturadas")
samples_label.configure(font = ("Helvetica", 12), text_color = main_letter)
samples_label.grid(row = 0, column = 3, columnspan = 2, sticky = "W", padx = 5, pady = 1)

line_canvas_frame2 = customtkinter.CTkCanvas(samples_frame, height = 1, bg = "#6B6B6B", highlightthickness = 0)
line_canvas_frame2.grid(row = 1, column = 3, columnspan = 3, sticky = "EW")
line_canvas_frame2.create_line(0, 0, 500, 0, fill = "#6B6B6B", width = 1)

revolution_slider = customtkinter.CTkSlider(samples_frame, from_ = start_slider, to = end_slider, number_of_steps = step_slider, command = sliding)#180, 179 ESTABA EN 4
revolution_slider.configure(fg_color = color_hover_widget, progress_color = color_widget, width = 120, height = 20)
revolution_slider.grid(row = 2, column = 4, padx = 5, pady = 5)
revolution_slider.set(1)

n_samples_label = customtkinter.CTkLabel(samples_frame, text = f"Revoluciones: {int(revolution_slider.get())}")
n_samples_label.configure(font = ("Helvetica", 12), text_color = main_letter)
n_samples_label.grid(row = 2, column = 3, padx = 3, pady = 5)

catch_button = customtkinter.CTkButton(samples_frame, text = "Captura", command = catch_samples)
catch_button.configure(height = 27, width = 100, font = ("Helvetica", 12), text_color = main_letter, fg_color = color_widget, hover_color = color_hover_widget, corner_radius = 7, border_width = 1, border_color = border_widget, state = "disabled")
catch_button.grid(row = 2, column = 5, padx = 5, pady = 5)
# ---------------------------------------------Definicion de sección de giro----------------------------------------------
orientation_frame = customtkinter.CTkFrame(main_window, width = 140, height = 68)
orientation_frame.configure(border_width = 1, border_color = border_frame)
orientation_frame.grid(row = 0, column = 6, rowspan = 3, padx = 5, pady = 5)
orientation_frame.grid_propagate(False) 
orientation_frame.grid_columnconfigure(6, weight = 1)

line_canvas_frame3 = customtkinter.CTkCanvas(orientation_frame, height = 1, bg = "#6B6B6B", highlightthickness = 0)
line_canvas_frame3.grid(row = 1, column = 6, sticky = "EW")
line_canvas_frame3.create_line(0, 0, 140, 0, fill = "#6B6B6B", width = 1)

orientation_label = customtkinter.CTkLabel(orientation_frame, text = "Giro")
orientation_label.configure(font = ("Helvetica", 12), text_color = main_letter)
orientation_label.grid(row = 0, column = 6, sticky = "W", padx = 5, pady = 1)

orientation_var =  customtkinter.StringVar(value = "CCW")
cw_rad = customtkinter.CTkRadioButton(orientation_frame, text = "CW", value = "CW", variable = orientation_var)
cw_rad.configure(hover_color = color_hover_widget, border_width_unchecked = 3, border_width_checked = 6, radiobutton_width = 15, radiobutton_height = 15)
cw_rad.grid(row = 2, column = 6, sticky = "W", padx = (10,5), pady = 5)

ccw_rad = customtkinter.CTkRadioButton(orientation_frame, text = "CCW", value = "CCW", variable = orientation_var)
ccw_rad.configure(hover_color = color_hover_widget, border_width_unchecked = 3, border_width_checked = 6, radiobutton_width = 15, radiobutton_height = 15)
ccw_rad.grid(row = 2, column = 6, sticky = "W", padx = (65,5), pady = 5)

# ---------------------------------------Definicion de sección de tiempo de muestras----------------------------------------
time_frame = customtkinter.CTkFrame(main_window, width = 160, height = 68)
time_frame.configure(border_width = 1, border_color = border_frame)
time_frame.grid(row = 0, column = 9, rowspan = 3, padx = 5, pady = 5) 
time_frame.grid_propagate(False) 
time_frame.grid_columnconfigure(9, weight = 1)

time_label = customtkinter.CTkLabel(time_frame, text = "Tiempo de captura")
time_label.configure(font = ("Helvetica", 12), text_color = main_letter)
time_label.grid(row = 0, column = 9, sticky = "W", padx = 5, pady = 1)

line_canvas_frame3 = customtkinter.CTkCanvas(time_frame, height = 1, bg = "#6B6B6B", highlightthickness = 0)
line_canvas_frame3.grid(row = 1, column = 9, sticky = "EW")
line_canvas_frame3.create_line(0, 0, 10, 0, fill = "#6B6B6B", width = 1)

time_label2 = customtkinter.CTkLabel(time_frame, text = "")
time_label2.configure(font = ("Helvetica", 12), text_color = main_letter)
time_label2.grid(row = 2, column = 9, sticky = "W",padx = 5, pady = 1)

# ---------------------------------------Definicion de sección para graficar ejes----------------------------------------
axes_tabview = customtkinter.CTkTabview(main_window, width = 835, height = 600)
axes_tabview.configure(border_width = 1, border_color = border_frame)
axes_tabview.grid(row = 3, column = 0, columnspan = 7, rowspan = 20, padx = 5, pady = 5)
axes_tabview.grid_propagate(False) 
tab1 = axes_tabview.add("Coordenadas Polares")
tab2 = axes_tabview.add("Coordenadas Cartesianas")
tab1.grid_rowconfigure(0, weight = 1)
tab1.grid_columnconfigure(0, weight = 1)
tab2.grid_rowconfigure(0, weight = 1)
tab2.grid_columnconfigure(0, weight = 1)


fig1, ax1 = plt.subplots(subplot_kw = {"projection": "polar"})
fig1.patch.set_facecolor("#212121")
ax1.set_facecolor("#212121") 
ax1.spines["polar"].set_edgecolor("white")
ax1.tick_params(axis = "both", colors = "white")

axes1_canvas = FigureCanvasTkAgg(fig1, master = tab1)
axes1_widget = axes1_canvas.get_tk_widget()
axes1_widget.config(width = 690, height = 690)
axes1_widget.grid(row = 5, column = 0)

toolbar_frame = customtkinter.CTkFrame(tab1)
toolbar_frame.grid(row = 4, column = 0, sticky = "EW")
toolbar = NavigationToolbar2Tk(axes1_canvas, toolbar_frame)
toolbar.update()

fig2, ax2 = plt.subplots()
fig2.patch.set_facecolor("#212121")
ax2.set_facecolor("#212121") 
ax2.spines["top"].set_edgecolor("white")
ax2.spines["bottom"].set_edgecolor("white")
ax2.spines["left"].set_edgecolor("white")
ax2.spines["right"].set_edgecolor("white")
ax2.tick_params(axis = "both", colors = "white")

axes2_canvas = FigureCanvasTkAgg(fig2, master = tab2)
axes2_widget = axes2_canvas.get_tk_widget()
axes2_widget.config(width = 705, height = 685)
axes2_widget.grid(row = 5, column = 0)

toolbar2_frame = customtkinter.CTkFrame(tab2)
toolbar2_frame.grid(row = 4, column = 0, sticky = "EW")
toolbar2 = NavigationToolbar2Tk(axes2_canvas, toolbar2_frame)
toolbar2.update()

# ---------------------------------------Definicion de sección para guardar muestras----------------------------------------
save_frame = customtkinter.CTkFrame(main_window, width = 160, height =350)
save_frame.configure(border_width = 1, border_color = border_frame)
save_frame.grid(row = 3, column = 9, rowspan = 15, padx = 5, pady = 5) 
save_frame.grid_propagate(False) 
save_frame.grid_columnconfigure(9, weight = 1)

save_label = customtkinter.CTkLabel(save_frame, text = "Guardar mediciones")
save_label.configure(font = ("Helvetica", 12), text_color = main_letter)
save_label.grid(row = 3, column = 9, sticky = "W", padx = 5, pady = 1)

line_canvas_frame4 = customtkinter.CTkCanvas(save_frame, height = 1, bg = "#6B6B6B", highlightthickness = 0)
line_canvas_frame4.grid(row = 4, column = 9, sticky = "EW")
line_canvas_frame4.create_line(0, 0, 10, 0, fill = "#6B6B6B", width = 1)

save_raw_label = customtkinter.CTkLabel(save_frame, text = "Datos sin procesar:")
save_raw_label.configure(font = ("Helvetica", 12), text_color = main_letter)
save_raw_label.grid(row = 5, column = 9, sticky = "W", padx = 5, pady = 1)

save_data_button = customtkinter.CTkButton(save_frame, text = "Guardar", command = save_data_to_csv)
save_data_button.configure(height = 27, width = 100, font = ("Helvetica", 12), text_color = main_letter, fg_color = color_widget, hover_color = color_hover_widget, corner_radius = 7, border_width = 1, border_color = border_widget, state = "disabled")
save_data_button.grid(row = 6, column = 9, padx = 5, pady = (0, 5))

line_canvas_frame5 = customtkinter.CTkCanvas(save_frame, height = 1, bg = "#6B6B6B", highlightthickness = 0)
line_canvas_frame5.grid(row = 7, column = 9, sticky = "EW")
line_canvas_frame5.create_line(0, 0, 10, 0, fill = "#6B6B6B", width = 1)

save_hex_label = customtkinter.CTkLabel(save_frame, text = "Datos en hexadecimal:")
save_hex_label.configure(font = ("Helvetica", 12), text_color = main_letter)
save_hex_label.grid(row = 8, column = 9, sticky = "W", padx = 5, pady = 1)

save_data_hex_button = customtkinter.CTkButton(save_frame, text = "Guardar", command = save_hex_data)
save_data_hex_button.configure(height = 27, width = 100, font = ("Helvetica", 12), text_color = main_letter, fg_color = color_widget, hover_color = color_hover_widget, corner_radius = 7, border_width = 1, border_color = border_widget, state = "disabled")
save_data_hex_button.grid(row = 9, column = 9, padx = 5, pady = (0, 5))

line_canvas_frame6 = customtkinter.CTkCanvas(save_frame, height = 1, bg = "#6B6B6B", highlightthickness = 0)
line_canvas_frame6.grid(row = 10, column = 9, sticky = "EW")
line_canvas_frame6.create_line(0, 0, 10, 0, fill = "#6B6B6B", width = 1)

save_dec_label = customtkinter.CTkLabel(save_frame, text = "Datos en decimal:")
save_dec_label.configure(font = ("Helvetica", 12), text_color = main_letter)
save_dec_label.grid(row = 11, column = 9, sticky = "W", padx = 5, pady = 1)

save_data_dec_button = customtkinter.CTkButton(save_frame, text = "Guardar", command = save_dec_data)
save_data_dec_button.configure(height = 27, width = 100, font = ("Helvetica", 12), text_color = main_letter, fg_color = color_widget, hover_color = color_hover_widget, corner_radius = 7, border_width = 1, border_color = border_widget, state = "disabled")
save_data_dec_button.grid(row = 12, column = 9, padx = 5, pady = (0, 5))

line_canvas_frame7 = customtkinter.CTkCanvas(save_frame, height = 1, bg = "#6B6B6B", highlightthickness = 0)
line_canvas_frame7.grid(row = 13, column = 9, sticky = "EW")
line_canvas_frame7.create_line(0, 0, 10, 0, fill = "#6B6B6B", width = 1)

save_processed_label = customtkinter.CTkLabel(save_frame, text = "Datos procesados:")
save_processed_label.configure(font = ("Helvetica", 12), text_color = main_letter)
save_processed_label.grid(row = 14, column = 9, sticky = "W", padx = 5, pady = 1)

save_processed_button = customtkinter.CTkButton(save_frame, text = "Guardar", command = save_processed_data)
save_processed_button.configure(height = 27, width = 100, font = ("Helvetica", 12), text_color = main_letter, fg_color = color_widget, hover_color = color_hover_widget, corner_radius = 7, border_width = 1, border_color = border_widget, state = "disabled")
save_processed_button.grid(row = 15, column = 9, padx = 5, pady = (0, 5))

line_canvas_frame8 = customtkinter.CTkCanvas(save_frame, height = 1, bg = "#6B6B6B", highlightthickness = 0)
line_canvas_frame8.grid(row = 16, column = 9, sticky = "EW")
line_canvas_frame8.create_line(0, 0, 10, 0, fill = "#6B6B6B", width = 1)

save_filtered_label = customtkinter.CTkLabel(save_frame, text = "Datos filtrados:")
save_filtered_label.configure(font = ("Helvetica", 12), text_color = main_letter)
save_filtered_label.grid(row = 17, column = 9, sticky = "W", padx = 5, pady = 1)

save_filtered_button = customtkinter.CTkButton(save_frame, text = "Guardar", command = save_filtered_data)
save_filtered_button.configure(height = 27, width = 100, font = ("Helvetica", 12), text_color = main_letter, fg_color = color_widget, hover_color = color_hover_widget, corner_radius = 7, border_width = 1, border_color = border_widget, state = "disabled")
save_filtered_button.grid(row = 18, column = 9, padx = 5)

# ---------------------------------------Definicion de sección para estadísticas----------------------------------------
statics_frame = customtkinter.CTkFrame(main_window, width = 160, height = 240)
statics_frame.configure(border_width = 1, border_color = border_frame)
statics_frame.grid(row = 19, column = 9, rowspan = 11, padx = 5, pady = 5) 
statics_frame.grid_propagate(False) 
statics_frame.grid_columnconfigure(9, weight = 1)

statistics_label = customtkinter.CTkLabel(statics_frame, text = "Estadísticas geométricas")
statistics_label.configure(font = ("Helvetica", 12), text_color = main_letter)
statistics_label.grid(row = 20, column = 9, sticky = "W", padx = 5, pady = 1)

line_canvas_frame9 = customtkinter.CTkCanvas(statics_frame, height = 1, bg = "#6B6B6B", highlightthickness = 0)
line_canvas_frame9.grid(row = 21, column = 9, sticky = "EW")
line_canvas_frame9.create_line(0, 0, 10, 0, fill = "#6B6B6B", width = 1)

circular_radius_label = customtkinter.CTkLabel(statics_frame, text = "Radio circular (mm):")
circular_radius_label.configure(font = ("Helvetica", 12), text_color = main_letter)
circular_radius_label.grid(row = 22, column = 9, sticky = "W", padx = 5, pady = 1)

radius_entry = customtkinter.CTkEntry(statics_frame)
radius_entry.configure(font = ("Helvetica", 12), text_color = main_letter, width = 40, height = 20)
radius_entry.grid(row = 22, column = 9, sticky = "E", padx = 5, pady = (1,0))
radius_entry.bind("<KeyRelease>", lambda event: validate_radius())   

statics_circular_button = customtkinter.CTkButton(statics_frame, text = "Obtener", command = radius_analysis)
statics_circular_button.configure(height = 27, width = 100, font = ("Helvetica", 12), text_color = main_letter, fg_color = color_widget, hover_color = color_hover_widget, corner_radius = 7, border_width = 1, border_color = border_widget, state = "disabled")
statics_circular_button.grid(row = 23, column = 9, padx = 5)

circular_theta_label = customtkinter.CTkLabel(statics_frame, text = "Ángulo (°):")
circular_theta_label.configure(font = ("Helvetica", 12), text_color = main_letter)
circular_theta_label.grid(row = 25, column = 9, sticky = "W", padx = 5, pady = (1,0))

theta_entry = customtkinter.CTkEntry(statics_frame)
theta_entry.configure(font = ("Helvetica", 12), text_color = main_letter, width = 90, height = 20)
theta_entry.grid(row = 25, column = 9, sticky = "E", padx = 5, pady = (1,0))
theta_entry.bind("<KeyRelease>", lambda event: validate_theta())   

statics_theta_button = customtkinter.CTkButton(statics_frame, text = "Obtener", command = theta_analysis)
statics_theta_button.configure(height = 27, width = 100, font = ("Helvetica", 12), text_color = main_letter, fg_color = color_widget, hover_color = color_hover_widget, corner_radius = 7, border_width = 1, border_color = border_widget, state = "disabled")
statics_theta_button.grid(row = 26, column = 9, padx = 5, pady = (0,5))

line_canvas_frame11 = customtkinter.CTkCanvas(statics_frame, height = 1, bg = "#6B6B6B", highlightthickness = 0)
line_canvas_frame11.grid(row = 27, column = 9, sticky = "EW")
line_canvas_frame11.create_line(0, 0, 10, 0, fill = "#6B6B6B", width = 1)

quadrilaterals_label = customtkinter.CTkLabel(statics_frame, text = "Aristas cuadriláteros")
quadrilaterals_label.configure(font = ("Helvetica", 12), text_color = main_letter)
quadrilaterals_label.grid(row = 28, column = 9, sticky = "W", padx = 5, pady = 1)

statics_quadrilaterals_button = customtkinter.CTkButton(statics_frame, text = "Obtener", command = edges_analysis)
statics_quadrilaterals_button.configure(height = 27, width = 100, font = ("Helvetica", 12), text_color = main_letter, fg_color = color_widget, hover_color = color_hover_widget, corner_radius = 7, border_width = 1, border_color = border_widget, state = "disabled")
statics_quadrilaterals_button.grid(row = 29, column = 9, padx = 5, pady = (0,5))


main_window.mainloop()
#%%