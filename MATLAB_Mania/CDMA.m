clc;
clear;
close all;

% --- 1. INITIALIZATION ---
LD = 5;  % Length of Data
LG = 10; % Length of Gold Code

% Generate random binary Data and Gold Code
Data = randi([0 1], 1, LD);
Goldcode = randi([0 1], 1, LG);

% --- 2. SPREADING (TRANSMITTER) ---
% Preallocate spread array for speed
spread = zeros(1, LD * LG); 
k = 1;

for i = 1:LD
    for j = 1:LG
        % XOR spreading logic
        spread(1,k) = xor(Data(1,i), Goldcode(1,j));
        k = k + 1;
    end
end

% --- 3. PLOTTING TRANSMITTER ---
figure('Name', 'CDMA Transmitter', 'Color', 'w');

% Create pulses so time axes align perfectly on graphs
Data_pulse = repelem(Data, LG);
Gold_pulse = repmat(Goldcode, 1, LD);

subplot(3,1,1);
stem(Data_pulse, 'filled');
ylabel('Amplitude'); title('Original Data Sequence');
ylim([-0.5 1.5]);

subplot(3,1,2);
stem(Gold_pulse, 'filled');
ylabel('Amplitude'); title('Gold Code (Repeated)');
ylim([-0.5 1.5]);

subplot(3,1,3);
stem(spread, 'filled');
ylabel('Amplitude'); title('Spread Sequence (Transmitted)');
ylim([-0.5 1.5]);

% Apply formatting and save
set(findall(gcf, 'Type', 'axes'), 'Color', 'w', 'XColor', 'k', 'YColor', 'k');
exportgraphics(gcf, 'CDMA_Transmitter.png', 'Resolution', 300);

% --- 4. DESPREADING (RECEIVER) ---
b2 = zeros(1, LD);
k = 1;

for i = 1:LD
    s = 0; % Sum accumulator
    for j = 1:LG
        % XOR incoming spread signal with local Gold Code
        temp = xor(spread(1,k), Goldcode(1,j));
        s = s + temp;
        k = k + 1;
    end
    
    % Decision logic: if sum is 0, original bit was 0. 
    if(s == 0)
        b2(1,i) = 0;
    else
        b2(1,i) = 1;
    end
end

despreaded_signal = b2;

% --- 5. PLOTTING RECEIVER ---
figure('Name', 'CDMA Receiver', 'Color', 'w');

% Recreate pulse shape for the recovered data
pattern = repelem(despreaded_signal, LG);

subplot(3,1,1);
stem(spread, 'filled');
ylabel('Amplitude'); title('Received Spread Sequence');
ylim([-0.5 1.5]);

subplot(3,1,2);
stem(Gold_pulse, 'filled');
ylabel('Amplitude'); title('Local Gold Code (Receiver)');
ylim([-0.5 1.5]);

subplot(3,1,3);
stem(pattern, 'filled');
ylabel('Amplitude'); title('Recovered Data Sequence (Despread)');
ylim([-0.5 1.5]);

% Apply formatting and save
set(findall(gcf, 'Type', 'axes'), 'Color', 'w', 'XColor', 'k', 'YColor', 'k');
exportgraphics(gcf, 'CDMA_Receiver.png', 'Resolution', 300);