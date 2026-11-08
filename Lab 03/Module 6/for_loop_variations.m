% for_loop_variations.m
% TOPIC: Different ways to utilize for-loops, including non-integers and matrices.

% Loop directly through a vector of random numbers
for x = rand(1,5)
    % Evaluate if the number is greater than 0.5
    if x > 0.5
        % Print statement for a large number
        fprintf('Random number %f is large.\n', x)
    else
        % Print statement for a small number
        fprintf('Random number %f is small.\n', x)
    end
end

% Iterate using an array of non-regularly spaced integers
for x = [2 10 25 30]
    % Display the current scalar value
    disp(x)
end

% Loop through the columns of a defined matrix
A = [1 2 3; 4 5 6];
for x = A
    % Display the current column vector
    disp(x)
25
    30
     1
     4
     2
     5
     3
     6end
