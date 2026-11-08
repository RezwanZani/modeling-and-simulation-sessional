% Step 1: Define filter parameters
Fs = 1000;     % Sampling frequency in Hz
Fpass1 = 100;  % First passband cutoff frequency in Hz
Fpass2 = 200;  % Second passband cutoff frequency in Hz
N = 50;        % Filter order

% Step 2: Design FIR bandpass filter
bpFilt = designfilt('bandpassfir', 'FilterOrder', N, ...
    'CutoffFrequency1', Fpass1, 'CutoffFrequency2', Fpass2, ...
    'SampleRate', Fs);

% Step 3: Visualize filter frequency response
fvtool(bpFilt);
title('Bandpass Filter Design');
