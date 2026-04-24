clc;
clear all;
close all;

samples = 2000;
nos = 4; % number of users

% Frequencies in Hz
mfreq = [30 40 50 60]; % Modulating signal frequencies
cfreq = [300 600 900 1200]; % Carrier frequencies
freqdev = 50; % Frequency deviation

% Global Sampling Frequency (Fs) 
Fs = 10000; 

% Generate proper time vector based on Fs
t = (0:samples-1) / Fs; 

% Preallocate arrays for speed and stability
m = zeros(nos, samples);
y = zeros(nos, samples);
z = zeros(nos, samples);

% Generate modulating signals
for i = 1:nos
    m(i,:) = sin(2*pi*mfreq(i)*t) + 2*sin(pi*4*t);
end

% Generate the modulated signals
for i = 1:nos
    y(i,:) = fmmod(m(i,:), cfreq(i), Fs, freqdev);
end

% Pass the combined modulated signals through the AWGN channel
ch_op = awgn(sum(y, 1), 0, 'measured'); 

% Demodulate the received channel signal at the base station
for i = 1:nos
    z(i,:) = fmdemod(ch_op, cfreq(i), Fs, freqdev);
end

% --- PLOTTING & SAVING ---
C = {'k', 'b', 'r', 'g'}; 

% Plot & Save the combined channel signal
figure('Name', 'Channel Output', 'Color', 'w');
plot(t, ch_op, 'Color', [.5 .6 .7]); 
xlabel('Time (s)');
ylabel('Amplitude');
title('Combined FDMA Signal passing through Channel');
set(gca, 'Color', 'w', 'XColor', 'k', 'YColor', 'k');

% --> SAVING COMMAND 1 <--
exportgraphics(gcf, 'FDMA_Combined_Channel.png', 'Resolution', 300);


% Loop to plot & Save individual user data
for i = 1:nos
    figure('Name', ['User ', num2str(i), ' Processing'], 'Color', 'w');
    
    % 1. Original Modulating Signal
    subplot(3,1,1);
    plot(t, m(i,:), 'Color', C{i});
    xlabel('Time (s)');
    ylabel('Amplitude');
    title(['User ', num2str(i), ': Original Modulating Signal']);
    
    % 2. Modulated Carrier Signal
    subplot(3,1,2);
    plot(t, y(i,:), 'Color', C{i});
    xlabel('Time (s)');
    ylabel('Amplitude');
    title(['User ', num2str(i), ': Modulated Signal (Carrier = ', num2str(cfreq(i)), ' Hz)']);
    
    % 3. Demodulated Signal
    subplot(3,1,3);
    plot(t, z(i,:), 'Color', C{i});
    xlabel('Time (s)');
    ylabel('Amplitude');
    title(['User ', num2str(i), ': Demodulated Signal']);
    
    % Apply white background styling
    set(findall(gcf, 'Type', 'axes'), 'Color', 'w', 'XColor', 'k', 'YColor', 'k');
    
    % --> SAVING COMMAND 2 <--
    filename = ['FDMA_User_', num2str(i), '_Processing.png'];
    exportgraphics(gcf, filename, 'Resolution', 300);
end