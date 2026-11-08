% Matrix and Operator Operations

%% 1. Matrix Transposition & Concatenation
A = [1 2; 3 4];
B = [5 6; 7 8];

% Transpose a matrix
A_transposed = A'

% Combine matrices horizontally and vertically
combined_horizontal = [A, B]
combined_vertical = [A; B]

%% 2. Array Addition & Subtraction
% Operands must have the same size
sum_matrix = A + B
diff_matrix = A - B

%% 3. Array Multiplication vs. Matrix Multiplication
% Element-wise multiplication (operands must have the same shape)
array_mult = A .* B

% Matrix multiplication (inner dimensions must match)
matrix_mult = A * B

%% 4. Matrix Division (Solving Linear Systems)
% Element-wise division
array_div = A ./ B

% Left Division (\): Solves for X in A * X = B
X_left = A \ B

% Right Division (/): Solves for X in X * B = A
X_right = A / B

%% 5. Exponential Operations
% Element-wise power (raises each element individually)
array_power = A .^ 2

% Matrix power (A * A)
matrix_power = A ^ 2