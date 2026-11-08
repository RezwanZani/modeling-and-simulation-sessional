% Clear command window and workspace
clc;
clear;

% --- Communication Data ---
distance = [0 50 100 150 200];      % Distance in km
signal = [-20 -35 -50 -65 -80];     % Signal strength in dBm

% --- Linear Model ---
% Fit a line to the distance vs. signal strength data
model = polyfit(distance, signal, 1);
k = model(1);  % Attenuation coefficient (slope)
S0 = model(2); % Initial signal strength (y-intercept)

fprintf("Signal Model:\n");
fprintf("S = %.3fd + %.2f\n", k, S0);

% --- Prediction for New Distances ---
newDistance = [250 300 400]; % Test distances
predictedSignal = k * newDistance + S0; % Calculate expected signal strength

disp("Distance:");
disp(newDistance);
disp("Signal Strength:");
disp(predictedSignal);

% --- Find Communication Limit ---
% Calculate the maximum distance before the signal drops to -100 dBm
limit = -100;
range = (limit - S0) / k;
fprintf("Maximum communication range = %.2f km\n", range);

% --- Plotting ---
plot(distance, signal, 'o'); % Plot actual test data
hold on;
plot(newDistance, predictedSignal, '*'); % Plot predicted data points
xlabel("Distance (km)");
ylabel("Signal Strength (dBm)");
title("Aircraft Communication Signal Attenuation");
grid on;