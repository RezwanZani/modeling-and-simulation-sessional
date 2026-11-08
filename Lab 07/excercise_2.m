clear;
clc;
close all;

N = 10000;          % Number of simulated flights
p_failure = 0.02;   % Probability of failure for each computer (2%)

rng(1);             % Set random seed for reproducibility

computerA_failures = 0;
computerB_failures = 0;
system_failures = 0;
system_operational = 0;


for flight = 1:N
    % Generate random numbers for Computer A and Computer B
    rA = rand();
    rB = rand();
    
    % Determine whether Computer A fails
    if rA < p_failure
        A_failed = true;
        computerA_failures = computerA_failures + 1;
    else
        A_failed = false;
    end
    
    % Determine whether Computer B fails
    if rB < p_failure
        B_failed = true;
        computerB_failures = computerB_failures + 1;
    else
        B_failed = false;
    end
    
    % Entire avionics system fails only if BOTH computers fail
    if A_failed && B_failed
        system_failures = system_failures + 1;
    else
        system_operational = system_operational + 1;
    end
end


simulated_failure_probability = system_failures / N;
simulated_failure_percentage = simulated_failure_probability * 100;

% P(System Failure) = P(A fails) * P(B fails)
theoretical_failure_probability = p_failure * p_failure;
theoretical_failure_percentage = theoretical_failure_probability * 100;

simulated_reliability = system_operational / N;
simulated_reliability_percentage = simulated_reliability * 100;


fprintf('Number of simulated flights = %d\n', N);
fprintf('Failure probability per computer = %.2f %%\n', p_failure * 100);
fprintf('Complete system failures = %d\n', system_failures);
fprintf('Simulated system failure probability = %.6f\n', simulated_failure_probability);
fprintf('Theoretical failure probability = %.6f\n', theoretical_failure_probability);
fprintf('Simulated system reliability = %.4f %%\n', simulated_reliability_percentage);

% Plot Results
figure;
categories = categorical({'System Operational', 'System Failed'});
values = [system_operational system_failures];
bar(categories, values);
ylabel('Number of Flights');
title('Avionics System Reliability - 10,000 Simulated Flights');
grid on;