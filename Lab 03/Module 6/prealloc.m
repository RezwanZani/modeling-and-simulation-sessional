% prealloc.m
% TOPIC: A fast implementation that reserves memory for the matrix before looping.

function A = prealloc
    % Define the target matrix dimension size
    N = 5000;
    
    % Preallocate the entire matrix with zeros to optimize memory allocation
    A = zeros(N, N);
    
    % Start the outer loop for rows
    for ii = 1:N
        % Start the inner loop for columns
        for jj = 1:N
            % Overwrite the pre-existing zeros with calculated values rapidly
            A(ii, jj) = ii * jj;
        end
    end
end
