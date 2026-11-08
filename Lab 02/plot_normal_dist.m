% Generate one million normally distributed random numbers
r = randn(1,1000000);

% Plot histogram with 100 bins to visualize the bell curve
hist(r,100)