% norealloc.m
% TOPIC: A slow implementation where the matrix changes size on every loop iteration.

function norealloc
    % Define the target matrix dimension size
    N = 5000;
    
    % Start the outer loop for rows
    for ii = 1:N
        % Start the inner loop for columns
        for jj = 1:N
            % Dynamically grow the array which drastically slows down execution
            A(ii, jj) = ii * jj;
        end
    end
end
