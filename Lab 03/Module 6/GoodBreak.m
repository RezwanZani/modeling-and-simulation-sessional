% GoodBreak.m
% TOPIC: Using a logical flag to successfully break out of all nested loops.

% Generate a random 5x8 matrix with integers up to 99
A = randi(99, 5, 8);

% Initialize a logical flag for loop control to false
found = false;

% Loop over each row of the matrix
for ii = 1:size(A, 1)
    % Loop over each column in the current row
    for jj = 1:size(A, 2)
        % Check if the current element is less than or equal to 90
        if A(ii, jj) <= 90
            % Replace that specific element with 0
            A(ii, jj) = 0;
        else
            % Set the control flag to true and break the inner loop
            found = true;
            break;
        end
    end
    
    % Check the control flag to break the outer loop as well
    if found
        % Break out of the outer loop
        break;
    end
end
