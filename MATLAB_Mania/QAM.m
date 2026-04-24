clc;
clear;
close all; % Added to close previous figures

M = 16;
x = (0:15);

% Binary Mapping
y1 = qammod(x, M, 'bin');

% Generate scatterplot (this automatically opens a figure)
scatterplot(y1);

% Add binary text labels (forced to black)
text(real(y1) + 0.1, imag(y1), dec2bin(x), 'Color', 'k');
title('16-QAM Binary Mapping', 'Color', 'k');

% Set axis limits
axis([-4 4 -4 4]);
xL = xlim; 
yL = ylim; % Added missing semicolon here

% Draw center axis lines (forced to black)
line([0 0], yL, 'Color', 'k');
line(xL, [0 0], 'Color', 'k');

% --- MAKE BACKGROUND WHITE AND AXES BLACK ---
set(gcf, 'Color', 'w'); 
set(gca, 'Color', 'w', 'XColor', 'k', 'YColor', 'k');

% Optional: Uncomment the line below if you want to auto-save it like the others!
% exportgraphics(gcf, '16QAM_Constellation.png', 'Resolution', 300);