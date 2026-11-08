% check_classes.m
% TOPIC: Checking the default data types of variables and expressions in MATLAB.

% Create a standard numeric variable
x = 35;
% Check the data type of the variable x
class(x)

% Check the data type of the number zero
class(0)

% Check the data type of an imaginary number calculation
class(sqrt(-1))

% Create a 3x4 matrix of random numbers
a = rand(3,4);

% Create a vector from 1 to 8
y = 1:8;

% Display memory and data type information for all variables
whos

% Check the data type of the default answer variable
class(ans)
