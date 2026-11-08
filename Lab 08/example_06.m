% Step 1: Define circuit components and input
Rin = 10e3;   % Input resistor in ohms
Rf = 100e3;   % Feedback resistor in ohms
Vin = 1;      % Input voltage in volts

% Step 2: Calculate voltage gain and output voltage
Av = -Rf / Rin;     % Voltage gain (-10)
Vout = Av * Vin;    % Output voltage

% Step 3: Display result
disp(['Output Voltage: ', num2str(Vout), ' V']);
