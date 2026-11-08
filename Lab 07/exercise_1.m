clear; clc; close all;

H_true = 10000; % true altitude
mu = 0;         % mean sensor error
sigma = 25;     % Standard Deviation of sensors error
N = 1000;       % Number of alt meas.

rng(1);
sensor_error = mu + sigma * randn(N, 1); % Generate 1000 Normally distributed rand numbers and calculate the error

H_measured = H_true + sensor_error;

mean_altitude = mean(H_measured);
minimum_altitude = min(H_measured);
maximum_altitude = max(H_measured);
std_altitude = std(H_measured);

large_error = abs(sensor_error) > 50;
number_large_errors = sum(large_error);
percentage_large_errors = (number_large_errors / N) * 100;

% Print the parameters
fprintf('True altitude = %.2f ft\n', H_true);
fprintf('Number of measurements = %d\n', N);

% Print the results for errors > 50 ft
fprintf('Readings with error > 50 ft = %d\n', number_large_errors);
fprintf('Percentage with error > 50 ft = %.2f %%\n', percentage_large_errors);

figure;
histogram(H_measured, 30);
xlabel('Measured Altitude (ft)');
ylabel('Frequency');
title('Distribution of Aircraft Altimeter Measurements');
grid on;

% Show the true altitude using a vertical line
hold on;
xline(H_true, '--', 'True Altitude = 10,000 ft', 'LineWidth', 2);
hold off;