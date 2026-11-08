% timer_example.m
% TOPIC: Using tic and toc to measure the elapsed time of an operation.

% Start the MATLAB stopwatch timer
tic

% Perform a computationally heavy sum calculation
sum(1:1e8);

% Stop the timer and print the elapsed execution time
toc
