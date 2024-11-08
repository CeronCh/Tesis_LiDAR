#%%
from tkinter import *
import customtkinter
import serial
import serial.tools.list_ports as serial_ports
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import numpy as np
import time
# -------------------------------------------Funciones para interfaz grafica-------------------------------------------
LiDAR = None
def open_port():
    global LiDAR
    catch_button.configure(state="disabled")
    selected_port = port_menu.get()
    if selected_port:
        try:
            LiDAR = serial.Serial(selected_port, 230400, timeout = 10)
            port_selected_label.configure(text = f"Conectado {selected_port}")
            if LiDAR and LiDAR.is_open:
                num_data = 5
                default_value = "00000000000000000000000000000000000000000000000000000000"
                data = [default_value] * num_data 
                for i in range(num_data):
                    try:
                        buffer = LiDAR.readline().decode("ascii").strip()
                        if not buffer:
                            pass
                        else:
                            data[i] = buffer
                    except serial.SerialTimeoutException:
                        pass
                    except Exception as e:
                        pass
                catch_button.configure(state = "normal")
                print(f"Conectado a {selected_port}")
                port_menu.configure(state = "disabled")
                open_button.configure(state = "disabled")
                return LiDAR
                #return serial.Serial(selected_port, 230400, timeout=10)
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
    global LiDAR
    init_time = time.time()
    catch_button.configure(state = "disabled")
    revolution_slider.configure(state = "disabled")
    cw_rad.configure(state = "disabled")
    ccw_rad.configure(state = "disabled")
    #data = None
    data = []
    dist0, dist1, dist2, dist3, dist4, distx, disty = [], [], [], [], [], [], []
    #------------------------------------------------------------QUITAR FUNCIONÓ PERO NO COMO SE ESPERABA
    #if LiDAR and LiDAR.is_open:
    #    LiDAR.close()
    #try:
    #    LiDAR.open()
    #except serial.SerialException as e:
    #    print(f"Error al reabrir el puerto: {str(e)}")
    #    catch_button.configure(state="normal")
    #    return data, None, None, None, None, None
    #------------------------------------------------------------QUITAR FUNCIONÓ PERO NO COMO SE ESPERABA
    LiDAR.reset_input_buffer()
    if LiDAR and LiDAR.is_open:
        if int(revolution_slider.get()) == 1:
            num_data = 60
        elif int(revolution_slider.get()) == 2:
            num_data = 120
        elif int(revolution_slider.get()) == 3:
            num_data = 180
        elif int(revolution_slider.get()) == 4:
            num_data = 240
        elif int(revolution_slider.get()) == 5:
            num_data = 300       
        #num_data = int(n_samples_entry.get())
        #default_value = "00000000000000000000000000000000000000000000000000000000"
        #data = [default_value] * num_data
        count = 0
        while count < num_data:
            try:
                buffer = LiDAR.readline().decode("ascii").strip()
                if not buffer:
                    pass
                    #print(f"Tiempo de espera agotado o buffer vacío en la muestra {i + 1}")
                    #2print(f"Tiempo de espera agotado o buffer vacío en la muestra {count + 1}")
                else:
                    data.append(buffer)
                    #data[i] = buffer
                    count += 1
            except serial.SerialTimeoutException:
                #print(f"Timeout en la muestra {i + 1}")
                print(f"Timeout en la muestra {count + 1}")
            except Exception as e:
                #print(f"Error al leer el puerto: {str(e)}, muestra {i + 1}")
                print(f"Error al leer el puerto: {str(e)}, muestra {count + 1}")
                break

        #for i in range(num_data):
        #    try:
        #        buffer = LiDAR.readline().decode("ascii").strip()
        #        if not buffer:
        #            print(f"Tiempo de espera agotado o buffer vacío en la muestra {i + 1}")
        #        else:
        #            data[i] = buffer
        #    except serial.SerialTimeoutException:
        #        print(f"Timeout en la muestra {i + 1}")
        #    except Exception as e:
        #        print(f"Error al leer el puerto: {str(e)}, muestra {i + 1}")
        if count == num_data:
            print("Datos capturados:")
            for i, sample in enumerate(data, 1):
                print(f"Muestra {i}: {sample}")
            dist0, dist1, dist2, dist3, dist4, distx, disty = process_data(data)
            plots(dist1, dist2, distx, disty)
        
        #n_samples_entry.delete(0,END)
        catch_button.configure(state = "normal")
        revolution_slider.configure(state = "normal")
        cw_rad.configure(state = "normal")
        ccw_rad.configure(state = "normal")
        final_time = time.time()
        total_time = final_time-init_time
        time_label2.configure(text = f"{total_time} s")
        return data, dist0, dist1, dist2, dist3, dist4, distx, disty
    else:
        print("El puerto no está abierto.")
        #n_samples_entry.delete(0,END)
        catch_button.configure(state = "normal")
        revolution_slider.configure(state = "normal")
        cw_rad.configure(state = "normal")
        ccw_rad.configure(state = "normal")
        return data, None, None, None, None, None, None, None
    
              
#def capture_samples():
#    LiDAR = open_port()
#    if LiDAR:
#        catch_samples(LiDAR)

def on_closing():
    axes1_canvas.get_tk_widget().destroy()
    fig1.clear()
    plt.close(fig1)
    axes2_canvas.get_tk_widget().destroy()
    fig2.clear()
    plt.close(fig2)
    main_window.quit()
    main_window.destroy()

def process_data(data_in):
    points = 12
    if int(revolution_slider.get()) == 1:
        num_data = 60
    elif int(revolution_slider.get()) == 2:
        num_data = 120
    elif int(revolution_slider.get()) == 3:
        num_data = 180
    elif int(revolution_slider.get()) == 4:
        num_data = 240
    elif int(revolution_slider.get()) == 5:
        num_data = 300  
    #num_data = int(n_samples_entry.get())
    orientation = orientation_var.get()
    dist_angl = np.zeros((num_data * points, 5))
    angles = np.full(points, 3.14)
    index = 0
    y_factor = 0.11923
    x_offset = 5.9
    y_offset = -18.975571
    last_shift_delta = 0
    shift = 0
    for i, sample in enumerate(data_in):
        if len(sample) < 28:  # Asegúrate de que el tamaño es el esperado
            print(f"Error: Tamaño inesperado de muestra en la entrada {i + 1}")
            continue
        processed_bytes = [sample[j:j+2] for j in range(0, len(sample), 2)]
        start_angle_l = int(processed_bytes[0],16)
        start_angle_h = int(processed_bytes[1],16)
        start_angle = ((start_angle_h << 8)|start_angle_l)/100.00

        distances = np.zeros(points)
        for m in range(points):
            idx=2+2*m
            dist_l = int(processed_bytes[idx], 16)  # Extrae y convierte los caracteres idx+1 e idx+2
            dist_h = int(processed_bytes[idx+1], 16)  # Extrae y convierte los caracteres idx+3 e idx+4
            distances[m] = (dist_h << 8) | dist_l
        
        end_angle_l = int(processed_bytes[26],16)
        end_angle_h = int(processed_bytes[27],16)
        end_angle = ((end_angle_h << 8)|end_angle_l)/100.00

        if start_angle > end_angle:
            step_angle = (360-start_angle+end_angle)/(points-1)
        else:
            step_angle = (end_angle-start_angle)/(points-1)
        
        for l in range(points):
            angles[l] = start_angle + step_angle * l
        
        for b in range(points):
            if distances[b] > 0:
                x_val = distances[b] + x_offset
                y_val = distances[b]*y_factor+y_offset
                shift = np.degrees(np.arctan(y_val/x_val))
                if orientation == "CW":
                    new_angle = (360 - angles[b])+shift
                else:
                    new_angle = angles[b]-shift
                last_shift_delta = shift
            else:
                if orientation == "CW":
                    new_angle = (360-angles[b])+last_shift_delta
                else:
                    new_angle = angles[b]-last_shift_delta
            if new_angle>360:
                new_angle -= 360
            if new_angle<0:
                new_angle += 360
            dist_angl[index, 0] = np.radians(angles[b])
            dist_angl[index, 1] = distances[b]
            dist_angl[index, 2] = np.radians(new_angle)
            dist_angl[index, 3] = angles[b]
            dist_angl[index, 4] = new_angle
            index += 1
    indx = 0    
    dist_cc = np.zeros((num_data * points, 2))
    for p in range(num_data*points):
        dist_cc[indx, 0] = dist_angl[p, 1]*np.cos(dist_angl[p, 2])
        dist_cc[indx, 1] = dist_angl[p, 1]*np.sin(dist_angl[p, 2])
        indx += 1
    return dist_angl[:, 0], dist_angl[:, 1], dist_angl[:, 2], dist_angl[:, 3], dist_angl[:, 4], dist_cc[:, 0], dist_cc[:, 1]

def plots(r, theta, x, y):
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
main_window.geometry("1000x700")
main_window.title("LiDAR Viewer")
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

revolution_slider = customtkinter.CTkSlider(samples_frame, from_ = 1, to = 5, number_of_steps = 4, command = sliding)
revolution_slider.configure(fg_color = color_hover_widget, progress_color = color_widget, width = 120, height = 20)
revolution_slider.grid(row = 2, column = 4, padx = 5, pady = 5)
revolution_slider.set(1)

n_samples_label = customtkinter.CTkLabel(samples_frame, text = f"Revoluciones: {int(revolution_slider.get())}")
n_samples_label.configure(font = ("Helvetica", 12), text_color = main_letter)
n_samples_label.grid(row = 2, column = 3, padx = 5, pady = 5)

#n_samples_entry = customtkinter.CTkEntry(samples_frame, placeholder_text="No. de muestra (60-200)")
#n_samples_entry.configure(font=("Helvetica", 12), text_color=main_letter)
#n_samples_entry.grid(row=2, column=4, padx=5, pady = 5)

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

orientation_var =  customtkinter.StringVar(value = "CW")
cw_rad = customtkinter.CTkRadioButton(orientation_frame, text = "CW", value = "CW", variable = orientation_var)
cw_rad.configure(hover_color = color_hover_widget, border_width_unchecked = 3, border_width_checked = 6, radiobutton_width = 15, radiobutton_height = 15)
cw_rad.grid(row = 2, column = 6, sticky = "W", padx = (10,5), pady = 5)

ccw_rad = customtkinter.CTkRadioButton(orientation_frame, text = "CCW", value = "CCW", variable = orientation_var)
ccw_rad.configure(hover_color = color_hover_widget, border_width_unchecked = 3, border_width_checked = 6, radiobutton_width = 15, radiobutton_height = 15)
ccw_rad.grid(row = 2, column = 6, sticky = "W", padx = (65,5), pady = 5)

# ---------------------------------------Definicion de sección de toma de muestras----------------------------------------
time_frame = customtkinter.CTkFrame(main_window, width = 140, height = 68)
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
axes_tabview.grid(row = 3, column = 0, columnspan = 7, padx = 5, pady = 5)
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
main_window.mainloop()
# %%
