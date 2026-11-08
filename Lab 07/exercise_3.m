clear;
clc;
close all;

x_true = 0;      % True East-West position in meters
y_true = 0;      % True North-South position in meters
mu = 0;          % Mean GPS error in meters
sigma = 8;       % Standard deviation of GPS error in meters
N = 2000;        % Number of simulated GPS readings

rng(1);          % Set random number seed for reproducibility

% Generate random GPS errors
Ex = mu + sigma * randn(N, 1);
Ey = mu + sigma * randn(N, 1);

% Calculate indicated GPS positions
x_GPS = x_true + Ex;
y_GPS = y_true + Ey;

% Calculate total horizontal position error
D = sqrt(Ex.^2 + Ey.^2);

% Calculate basic statistics
mean_position_error = mean(D);
maximum_position_error = max(D);

% Determine readings within 10 meters
within_10m = D <= 10;
number_within_10m = sum(within_10m);
percentage_within_10m = (number_within_10m / N) * 100;

% Determine readings within 20 meters
within_20m = D <= 20;
number_within_20m = sum(within_20m);
percentage_within_20m = (number_within_20m / N) * 100;

fprintf('Number of GPS readings = %d\n', N);
fprintf('True aircraft position = (%.1f, %.1f) m\n', x_true, y_true);
fprintf('GPS error standard deviation = %.2f m\n', sigma);
fprintf('Mean horizontal position error = %.2f m\n', mean_position_error);
fprintf('Maximum horizontal error = %.2f m\n', maximum_position_error);
fprintf('Readings within 10 m = %d\n', number_within_10m);
fprintf('Percentage within 10 m = %.2f %%\n', percentage_within_10m);
fprintf('Readings within 20 m = %d\n', number_within_20m);
fprintf('Percentage within 20 m = %.2f %%\n', percentage_within_20m);

figure;
scatter(x_GPS, y_GPS, 15, 'filled');
hold on;

% Mark the actual aircraft position
plot(x_true, y_true, 'kp', 'MarkerSize', 14, 'MarkerFaceColor', 'k');

% Draw 10-meter accuracy circle
theta = linspace(0, 2*pi, 360);
x_circle10 = x_true + 10 * cos(theta);
y_circle10 = y_true + 10 * sin(theta);
plot(x_circle10, y_circle10, '--', 'LineWidth', 1.5);

% Draw 20-meter accuracy circle
x_circle20 = x_true + 20 * cos(theta);
y_circle20 = y_true + 20 * sin(theta);
plot(x_circle20, y_circle20, '--', 'LineWidth', 1.5);

% Graph formatting
xlabel('East-West Position Error (m)');
ylabel('North-South Position Error (m)');
title('Simulated GPS Position Errors');
legend('Simulated GPS Readings', 'True Aircraft Position', '10 m Boundary', '20 m Boundary', 'Location', 'best');
axis equal;
grid on;
hold off;