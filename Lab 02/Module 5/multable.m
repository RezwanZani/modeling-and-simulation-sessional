function [table, summa] = multable(n, m)
    if nargin < 1
        error('must have at least one input argument');
    end
    
    if nargin < 2
        m = n;
    elseif ~isscalar(m) || m < 1 || m ~= fix(m)
        error('m needs to be a positive integer');
    end
    
    if ~isscalar(n) || n < 1 || n ~= fix(n)
        error('n needs to be a positive integer');
    end
    
    table = (1:n)' * (1:m);
    
    if nargout == 2
        summa = sum(table(:));
    end
end
