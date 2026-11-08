% Radar Detection Range Prediction (Nonlinear Regression)
% Exponential Decay Model: S(D) = alpha * exp(-beta * D)

clc; clear; close all;

% 1. Experimental Radar Data
dist_km    = 10:10:100; % Target distance (km)
signal_dbm = [92, 78, 65, 54, 46, 38, 33, 28, 24, 20]; % Signal strength (dBm)

% 2. Initial Data Visualization
figure('Name', 'Radar Data', 'Color', 'w');
scatter(dist_km, signal_dbm, 80, 'k', 'filled'); grid on;
xlabel('Target Distance (km)'); ylabel('Received Signal Strength (dBm)');
title('Empirical Radar Signal Attenuation');

% 3. Model Definition & Nonlinear Fitting
% b(1) represents alpha, b(2) represents beta
decay_model = @(b, x) b(1) .* exp(-b(2) .* x);
initial_guess = [100, 0.05]; % Reasonable starting points

% Least squares curve fitting
options = optimset('Display', 'off');
params = lsqcurvefit(decay_model, initial_guess, dist_km, signal_dbm, [], [], options);

alpha_est = params(1);
beta_est  = params(2);

fprintf('--- Nonlinear Model Optimization ---\n');
fprintf('Alpha (\x03B1) = %.4f\n', alpha_est);
fprintf('Beta (\x03B2)  = %.6f\n', beta_est);

% 4. Evaluate Model Accuracy
pred_signal = decay_model(params, dist_km);
residuals = signal_dbm - pred_signal;
rmse = sqrt(mean(residuals.^2));

% Calculate R-squared for nonlinear fit
ss_tot = sum((signal_dbm - mean(signal_dbm)).^2);
ss_res = sum(residuals.^2);
r_squared = 1 - (ss_res / ss_tot);

fprintf('\n--- Performance Metrics ---\n');
fprintf('RMSE      = %.4f dBm\n', rmse);
fprintf('R-Squared = %.4f\n', r_squared);
fprintf('\nFinal Equation: S(D) = %.4f * exp(-%.6f * D)\n', alpha_est, beta_est);

% 5. Plot Fitted Decay Curve vs Actual Data
d_smooth = linspace(min(dist_km), max(dist_km), 200);
s_smooth = decay_model(params, d_smooth);

figure('Name', 'Fitted Model', 'Color', 'w');
scatter(dist_km, signal_dbm, 80, 'b', 'filled'); hold on;
plot(d_smooth, s_smooth, 'r-', 'LineWidth', 2); grid on;
xlabel('Target Distance D (km)'); ylabel('Signal Strength S (dBm)');
title('Nonlinear Regression: Radar Detection Range');
legend('Measured Data', 'Fitted Exponential Curve');

% 6. Model Extrapolation (Prediction)
test_dist = 120; % Predicting beyond our measured data
pred_val = decay_model(params, test_dist);
fprintf('\n--- Extrapolation ---\n');
fprintf('Predicted signal at %.1f km = %.4f dBm\n', test_dist, pred_val);
