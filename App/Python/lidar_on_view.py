import time
import serial
import numpy as np
import matplotlib.pyplot as plt

# Variables globales y configuración de gráficos
selected_port = "COM3"  # Define el puerto aquí
baudrate = 230400
sampling_interval = 5  # Intervalo de tiempo en segundos entre cada captura

# Configuración inicial del gráfico
fig, (ax1, ax2) = plt.subplots(1, 2, subplot_kw={'polar': True}, figsize=(10, 5))
fig.patch.set_facecolor('#212121')
ax1.set_facecolor("#212121")
ax2.set_facecolor("#212121")
plt.ion()

# Variables de almacenamiento de datos
data = []
expected_length = 60

def open_port():
    try:
        LiDAR = serial.Serial(selected_port, baudrate, timeout=10)
        print(f"Conectado a {selected_port}")
        return LiDAR
    except serial.SerialException as e:
        print(f"No se pudo abrir el puerto {selected_port}: {str(e)}")
        return None

def catch_samples(LiDAR):
    data.clear()  # Limpiar datos previos
    count = 0
    while count < expected_length:
        try:
            buffer = LiDAR.read_until(b"\n").strip()
            if buffer.startswith(b'542C') and len(buffer) == expected_length:
                data.append(buffer)
                count += 1
        except serial.SerialTimeoutException:
            print(f"Timeout en la muestra {count + 1}")
        except Exception as e:
            print(f"Error al leer el puerto: {str(e)}, muestra {count + 1}")
            break

    if count == expected_length:
        headerless_data = strip_header(data)
        extracted_hex_data = split_data_hex(headerless_data)
        extracted_dec_data = convert_hex_dec(extracted_hex_data)
        return process_dec_data(extracted_dec_data)
    else:
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
    orientation = "CCW"
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

def update_plot(theta, r, x, y):
    ax1.clear()
    ax2.clear()
    ax1.set_facecolor("#212121")
    ax2.set_facecolor("#212121")
    ax1.plot(theta, r, ".", color="cyan", markersize=3)
    ax2.plot(x, y, ".", color="cyan", markersize=3)
    plt.draw()
    plt.pause(0.1)

def filter_zero_distances(new_angles_rads, distances, x_coords, y_coords, new_angle_degs):
    mask_zero = distances > 0
    return (new_angles_rads[mask_zero], distances[mask_zero], x_coords[mask_zero], y_coords[mask_zero], new_angle_degs[mask_zero])

# Ciclo principal
LiDAR = open_port()
if LiDAR:
    try:
        while True:
            old_angle_rad, old_angle_deg, new_angle_rad, new_angle_deg, radio_dist, distx, disty = catch_samples(LiDAR)
            new_angles_rads, radio_dist_no_zeros, x_coords, y_coords, new_angle_degs = filter_zero_distances(new_angle_rad, radio_dist, distx, disty, new_angle_deg)
            
            if new_angles_rads is not None:
                update_plot(new_angles_rads, radio_dist_no_zeros, x_coords, y_coords)
            time.sleep(sampling_interval)
    except KeyboardInterrupt:
        print("Detenido por el usuario.")
    finally:
        LiDAR.close()
        print("Puerto cerrado.")
else:
    print("No se pudo establecer conexión con el LiDAR.")
