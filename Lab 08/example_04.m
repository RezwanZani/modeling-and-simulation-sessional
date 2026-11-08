% Step 1: Define transistor parameters
beta = 100;     % Current gain
R_C = 1e3;      % Collector resistor in ohms
V_CC = 10;      % Supply voltage in volts
I_B = 50e-6;    % Base current in amperes

% Step 2: Calculate currents and voltages
I_C = beta * I_B;          % Collector current
V_CE = V_CC - I_C * R_C;   % Collector-emitter voltage

% Step 3: Display result
disp(['Collector-Emitter Voltage: ', num2str(V_CE), ' V']);
