% Reset the random number generator to seed 0[cite: 1]
rng(0)
% Generate a 1x3 vector of random numbers[cite: 1]
rand(1,3)

% Reset again to seed 1[cite: 1]
rng(1)
rand(1,3)

% Randomize the generator using the current time so it doesn't repeat[cite: 1]
rng('shuffle');
[rand, randn, randi(10)]