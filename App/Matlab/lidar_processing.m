%% Comunicación Serial
% Se crea el objeto de puerto serial
LiDAR = serialport("COM3",230400);
LiDAR.Timeout = 10;
%% Lectura de datos
x = "00000000000000000000000000000000000000000000000000000000";
num_data = 70;
count = 0;
data = repmat(x, num_data, 1);
flush(LiDAR)
tic
try
    for i = 1:num_data
        buffer = readline(LiDAR);
        if isempty(buffer)
            
            count = count + 1;
        else
            data(i, :) = buffer;
            
        end 
    end
catch
    warning('Try Again.')
end
toc

%% Lectura de datos 3
num_data = 70;
data = cell(num_data, 1);  % Usa celdas para mayor flexibilidad

flush(LiDAR);  % Limpia el buffer antes de iniciar la lectura

tic
try
    for i = 1:num_data
        buffer = readline(LiDAR);
        if isempty(buffer)
            disp('Vacio')
        else
            data(i, :) = buffer;
            
        end 
    end
catch
    warning('Try Again.')
end
toc

%% Lectura de datos 2
num_data = 70;
data = cell(num_data, 1);  % Usa celdas para mayor flexibilidad

flush(LiDAR);  % Limpia el buffer antes de iniciar la lectura
tic
try
    for i = 1:num_data
        if LiDAR.NumBytesAvailable > 0  % Verifica si hay datos disponibles
            numBytes = LiDAR.NumBytesAvailable;  % Cantidad de bytes disponibles
            buffer = read(LiDAR, numBytes, "char");  % Lee los datos disponibles como caracteres
            if isempty(buffer)
                disp('Vacio');
            else
                data{i} = buffer;  % Almacena los datos leídos en la celda correspondiente
            end
        else
            disp('No hay datos disponibles');
        end
    end
catch 
end
toc

% Opcional: Mostrar los datos leídos
disp(data);
%% Procesamiento de datos 1
points = 12;
dist_angl = zeros(num_data*points, 2);
index = 1;
angles = repmat(3.14, 1, points);
for n = 1:num_data
    start_angle_l = hex2dec(extractBetween(data(n),1,2));
    start_angle_h = hex2dec(extractBetween(data(n),3,4));
    start_angle = bitor(bitshift(start_angle_h, 8), start_angle_l)/100;
    
    distances = zeros(points, 1);
    for m = 1:points
        idx = 4 + (m-1)*4;
        dist_l = hex2dec(extractBetween(data(n),idx+1,idx+2));
        dist_h = hex2dec(extractBetween(data(n),idx+3,idx+4));
        distances(m) = bitor(bitshift(dist_h, 8), dist_l);
    end
    
    end_angle_l = hex2dec(extractBetween(data(n),53,54));
    end_angle_h = hex2dec(extractBetween(data(n),55,56));
    end_angle = bitor(bitshift(end_angle_h, 8), end_angle_l)/100;
   
    step_angle = (end_angle - start_angle)/(points - 1);
    for l = 0:(points - 1)
        angles(l + 1) = start_angle + step_angle * l;
    end

    for b = 1:points
        dist_angl(index, 1) = deg2rad(angles(b));
        dist_angl(index, 2) = distances(b);
        index = index + 1;
    end
end
figure
polarplot(dist_angl(:,1),dist_angl(:,2),'.')
%% Procesamiento de datos 2
points = 12;
dist_angl = zeros(num_data*points, 2);
index = 1;
angles = repmat(3.14, 1, points);
for n = 1:num_data
    start_angle_l = hex2dec(extractBetween(data(n),1,2));
    start_angle_h = hex2dec(extractBetween(data(n),3,4));
    start_angle = bitor(bitshift(start_angle_h, 8), start_angle_l)/100;
    
    distances = zeros(points, 1);
    for m = 1:points
        idx = 4 + (m-1)*4;
        dist_l = hex2dec(extractBetween(data(n),idx+1,idx+2));
        dist_h = hex2dec(extractBetween(data(n),idx+3,idx+4));
        distances(m) = bitor(bitshift(dist_h, 8), dist_l);
    end
    
    end_angle_l = hex2dec(extractBetween(data(n),53,54));
    end_angle_h = hex2dec(extractBetween(data(n),55,56));
    end_angle = bitor(bitshift(end_angle_h, 8), end_angle_l)/100;
    
    if start_angle > end_angle
        step_angle = (360 - start_angle + end_angle)/(points - 1);
    else
        step_angle = (end_angle - start_angle)/(points - 1);
    end
    
    for l = 0:(points - 1)
        angles(l + 1) = start_angle + step_angle * l;
    end

    for b = 1:points
        dist_angl(index, 1) = deg2rad(angles(b));
        dist_angl(index, 2) = distances(b);
        index = index + 1;
    end
end
figure
polarplot(dist_angl(:,1),dist_angl(:,2),'.')
%%
buffer = [];
data = [];
%%
indx = 1;
dist_cc = zeros(num_data*points, 2);
for p = 1:num_data*points
        dist_cc(indx,1) = dist_angl(p,2)*cos(dist_angl(p,1));
        dist_cc(indx,2) = dist_angl(p,2)*sin(dist_angl(p,1));
        indx =indx + 1;
end
plot(dist_cc(:,1),dist_cc(:,2),'.')

%%
%% Procesamiento de datos 3
points = 12;
dist_angl = zeros(num_data*points, 5);
index = 1;
angles = repmat(3.14, 1, points);
y_factor = 0.11923;
x_offset = 5.9;
y_offset = -18.975571;
right_hand = 1;
last_shift_delta = 0;
shift = 0;

for n = 1:num_data
    start_angle_l = hex2dec(extractBetween(data(n),1,2));
    start_angle_h = hex2dec(extractBetween(data(n),3,4));
    start_angle = bitor(bitshift(start_angle_h, 8), start_angle_l)/100;
    
    distances = zeros(points, 1);
    for m = 1:points
        idx = 4 + (m-1)*4;
        dist_l = hex2dec(extractBetween(data(n),idx+1,idx+2));
        dist_h = hex2dec(extractBetween(data(n),idx+3,idx+4));
        distances(m) = bitor(bitshift(dist_h, 8), dist_l);
    end
    
    end_angle_l = hex2dec(extractBetween(data(n),53,54));
    end_angle_h = hex2dec(extractBetween(data(n),55,56));
    end_angle = bitor(bitshift(end_angle_h, 8), end_angle_l)/100;
    
    if start_angle > end_angle
        step_angle = (360 - start_angle + end_angle)/(points - 1);
    else
        step_angle = (end_angle - start_angle)/(points - 1);
    end
    
    for l = 0:(points - 1)
        angles(l + 1) = start_angle + step_angle * l;
    end
    

    for b = 1:points
        if distances(b) > 0
            x_val = distances(b) + x_offset;
            y_val = distances(b) * y_factor + y_offset;
            shift = rad2deg(atan(y_val/x_val));
            if right_hand
                new_angle = (360 - angles(b)) + shift;
            else
                new_angle = angles(b) - shift;
            end
            last_shift_delta = shift;
        else
            if right_hand
                new_angle = (360 - angles(b)) + last_shift_delta;
            else
                new_angle = angles(b) - last_shift_delta;
            end
        end

        if new_angle > 360
            new_angle = new_angle - 360;
        end
        if new_angle < 0
            new_angle = new_angle + 360;
        end
        dist_angl(index, 2) = distances(b);
        dist_angl(index, 1) = deg2rad(angles(b));
        dist_angl(index, 3) = deg2rad(new_angle);
        dist_angl(index, 4) = angles(b);
        dist_angl(index, 5) = new_angle;
        index = index + 1;
    end
end
figure
polarplot(dist_angl(:,1),dist_angl(:,2),'.')
thetaticks(0:15:360)
figure
polarplot(dist_angl(:,3),dist_angl(:,2),'.')
thetaticks(0:15:360)
%%
indx = 1;
dist_cc = zeros(num_data*points, 2);
for p = 1:num_data*points
        dist_cc(indx,1) = dist_angl(p,2)*cos(dist_angl(p,3));
        dist_cc(indx,2) = dist_angl(p,2)*sin(dist_angl(p,3));
        indx =indx + 1;
end
figure
plot(dist_cc(:,1),dist_cc(:,2),'.')

%% 8/3/2024 - Pruebas IRL
%% Ejemplo 7: con handler y "limitrate", actualización cada K muestras
%  Se recomienda esta opción para los mini-proyectos, si la anterior limita mucho la
%  frecuencia de muestreo.

N = 1000;  % Aumentar el número de datos arriba, para apreciar mejor el efecto.
t = linspace(0,2*pi,N)';    % no es necesario trasponer, es para tener vectores columna
y = cos(10*t);
K = 10;    % Restricción: K debe ser factor de N. Se puede ajustar el código abajo para
           % eliminar esta restricción. 
        
figure(7); clf;
h7 = plot(t,zeros(N,1));
xlim([0,t(end)]);
buffer = zeros(K,1);
k = 1;

tic;
for n = 1:N
    buffer(k) = y(n);
    
    if(k == K)
        h7.YData((n-K+1):n) = buffer;   % Asume que K es factor de N. De lo contrario,
                                        % hay que hacer ajustes adicionales.
        drawnow limitrate
        k = 1;
    else
        k = k + 1;    
    end
end

tiempo7 = toc
