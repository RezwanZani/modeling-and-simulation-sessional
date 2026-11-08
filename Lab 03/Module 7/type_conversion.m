% type_conversion.m
% TOPIC: Converting values between different integer and character data types.

% Convert a standard number into an unsigned 16-bit integer
m = uint16(1234);

% Attempt to store a number larger than 255 in an 8-bit unsigned integer
k1 = uint8(500);

% Attempt to store 256 in a uint8, which limits to 255
k2 = uint8(256);

% Attempt to store a negative number in an unsigned integer, which limits to 0
k3 = uint8(-1);

% Check the data type of the variable k3
class(k3)

% Assign a numeric value to a variable
k4 = 2;
% Verify the default numeric data type is double
class(k4)

% Assign text to the variable
k5 = 'It makes sense';
% Verify the data type is now character array
class(k5)
