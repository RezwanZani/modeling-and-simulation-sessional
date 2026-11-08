% Step 1: Define parameters
R = 50;        % Resistance in ohms
L = 100e-3;    % Inductance in henrys
C = 10e-6;     % Capacitance in farads
f = 60;        % Frequency in Hz

% Step 2: Compute angular frequency and complex impedance
omega = 2 * pi * f;
Z = R + 1i * (omega * L - 1 / (omega * C));

% Step 3: Display total impedance magnitude
disp(['Impedance: ', num2str(abs(Z)), ' Ohms']);
