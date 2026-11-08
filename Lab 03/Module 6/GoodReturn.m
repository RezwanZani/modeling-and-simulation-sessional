% GoodReturn.m
% TOPIC: Using the return statement to exit all loops and the script simultaneously.

% Generate a random 5x8 matrix with integers up to 99
A = randi(99, 5, 8);

% Loop over each row of the matrix
for ii = 1:size(A, 1)
    % Loop over each column in the current row
    for jj = 1:size(A, 2)
        % Check if the current element is less than or equal to 90
        if A(ii, jj) <= 90
            % Replace that specific element with 0
            A(ii, jj) = 0;
        else
            % Terminate the entire function/script immediately
            return;
        end
    end
end
