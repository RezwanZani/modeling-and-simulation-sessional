% Reduce vertical spacing in the command window
format compact 

% Generate 10 million random numbers (press Ctrl+C to stop)
rand(10000000, 1) 

% Generate a single random number
rand 

% Basic variable assignment and arithmetic
a = 1;
b = 2;
c = 3;
sum = a + b + c;

% Clear specific variables from the workspace
clear a
clear b

% Wipe out all variables
clear all 

% Clear the command window
clc 

% Save and load workspace variables
save
clear
load
