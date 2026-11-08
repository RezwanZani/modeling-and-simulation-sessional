% Step 1: Define parameters and voltage range
Is = 1e-12; % Saturation current in amperes
Vt = 0.025; % Thermal voltage in volts
V = linspace(-0.7, 0.7, 1000); % Applied voltage sweep

% Step 2: Calculate diode current using Shockley equation
I = Is * (exp(V / Vt) - 1);

% Step 3: Plot I-V characteristics
plot(V, I);
xlabel('Voltage (V)');
ylabel('Current (I)');
title('I-V Characteristics of a Diode');
grid on;
