% Red sine curve[cite: 1]
plot(x1,y1,'r')

% Keep the existing graph for additional plots[cite: 1]
hold on

% Black dotted cosine curve[cite: 1]
plot(x2,y2,'k:')

% Turn on grid lines[cite: 1]
grid on

% Add labels, titles, and legends[cite: 1]
title('A Sine Plot and a Cosine Plot')
xlabel('The argument of sine and cosine')
ylabel('The value of the sine or cosine')
legend('sine', 'cosine')

% Adjust view limits: [xmin xmax ymin ymax][cite: 1]
axis([-2 12 -1.5 1.5])