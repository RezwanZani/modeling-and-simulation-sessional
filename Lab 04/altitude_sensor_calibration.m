% Clear command window and workspace
clc;
clear;

% --- Calibration Data ---
Altitude = [0 1000 2000 3000 4000]; % Altitude in meters
Voltage = [0.5 1.8 3.1 4.4 5.7];    % Corresponding sensor voltage in Volts

% --- Linear Fitting ---
% Use polyfit to find the coefficients of a 1st-degree polynomial (linear line)
model = polyfit(Altitude, Voltage, 1);
m = model(1); % Slope (sensitivity coefficient)
c = model(2); % Y-intercept (initial voltage offset)

fprintf("Calibration Equation:\n");
fprintf("V = %.4fH + %.2f\n", m, c);

% --- Predict Voltage for New Altitudes ---
newAltitude = [2500 3500 5000]; % Altitudes to test
predictedVoltage = m * newAltitude + c; % Apply the linear equation

disp("Altitude:");
disp(newAltitude);
disp("Voltage:");
disp(predictedVoltage);

% --- Plotting the Data and Predictions ---
plot(Altitude, Voltage, 'o'); % Plot original data points as circles
hold on;                      % Keep the current plot to add more data
plot(newAltitude, predictedVoltage, '*'); % Plot predicted data points as asterisks
xlabel("Altitude (m)");
ylabel("Sensor Voltage (V)");
title("Altitude Sensor Calibration Model");
grid on;