% Step 1: Define circuit parameters
Vcc = 5;      % Supply voltage in volts
R1 = 1e3;     % Resistor R1 in ohms
R2 = 10e3;    % Resistor R2 in ohms

% Step 2: Calculate threshold voltages
Vh = Vcc * (R2 / (R1 + R2));   % High threshold voltage (+4.545 V)
Vl = -Vcc * (R2 / (R1 + R2));  % Low threshold voltage (-4.545 V)

% Step 3: Set up voltage sweep and initialize output
Vin = linspace(-Vcc, Vcc, 1000);
Vout = zeros(size(Vin));

% Step 4: Simulate hysteresis behavior
for i = 2:length(Vin)
    if Vin(i) > Vh
        Vout(i) = Vcc;
    elseif Vin(i) < Vl
        Vout(i) = -Vcc;
    else
        Vout(i) = Vout(i-1);
    end
end

% Step 5: Plot Schmitt trigger input vs output
plot(Vin, Vout);
title('Schmitt Trigger Circuit');
xlabel('Input Voltage (V)');
ylabel('Output Voltage (V)');
grid on;
