% Core computation for iterative prefactor alpha

parpool(60);

numperitem = 2000;
totalpdb = 60;

existing_files = []; % To keep track of the file numbers that exist

% Determine which files exist
for i = 1:totalpdb
    filename = sprintf('data_arrays%d.mat', i);
    if exist(filename, 'file')
        existing_files = [existing_files, i]; % Store the file number that exists
    end
end

% Calculate the number of existing files
num_existing_files = length(existing_files);

disp(['Number of existing files: ', num2str(num_existing_files)])

% Create the 'arrays' variable with the required dimensions
arrays = zeros(numperitem * num_existing_files, 27584);

% Load the existing files into 'arrays'
for i = 1:num_existing_files
    filename = sprintf('data_arrays%d.mat', existing_files(i));
    temp = load(filename);
    arrays((i - 1) * numperitem + 1 : i * numperitem, :) = temp.da;
end

clear temp

disp(arrays(:, 1))

B = cov(arrays);

amean = mean(arrays, 1);

clear arrays

Amedian = median(amean);

Bmedian = median(abs(B), 'all');

Bcond = cond(B);

save('cocond.txt', "Amedian", "Bmedian", 'Bcond', "-ascii");

hfexp = importdata('hfexp.mat');

minus_term = amean - hfexp;

error = sum(abs(minus_term)) / sum(hfexp);
save('errorel.txt', "error", "-ascii");

tic
Bpinv = pinv(B);
toc

alpha = -0.06 + Bpinv * minus_term';

phaamean = mean(abs(alpha));
phamean = mean(alpha);

alpha_output=1;
alphaname1 = sprintf('alpha%d.mat', alpha_output);
alphaname2 = sprintf('alpha%d.txt', alpha_output);
save(alphaname1, 'alpha');
save(alphaname2, 'phaamean', 'phamean', 'alpha', "-ascii");

delete(gcp('nocreate'));

