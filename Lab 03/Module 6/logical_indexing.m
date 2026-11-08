% logical_indexing.m
% TOPIC: Creating true/false masks to filter data and modify arrays directly.

% Define the original numerical vector
v = [56 34 -2 7 29 53 30 -3 5 45];

% Create a logical mask identifying non-negative values
keepers = v >= 0;

% Extract only the non-negative values into a new vector using the mask
w = v(keepers);

% Select negative values directly and add 100 to them in a single step
v(v < 0) = v(v < 0) + 100;

% Define a new 2x3 matrix
A = [1 2 3; 4 5 6];

% Extract all elements greater than 2 into a column vector
B = A(A > 2);

% Convert the entire matrix into a single column-major vector
A_column_major = A(:);
