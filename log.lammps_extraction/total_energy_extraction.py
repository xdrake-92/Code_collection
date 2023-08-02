import os
import re
import matplotlib.pyplot as plt
import itertools

def extract_energy(file_path):
    energy = []
    found_start = False

    with open(file_path, 'r') as file:
        lines = file.readlines()

    for line in lines:
        if found_start:  # Check if we have already found the "Step" line
            if line.startswith("Loop"):
                found_start = False  # Reset the flag when a block is complete
            else:
                values = line.split()
                if len(values) >= 4:
                    energy_value = float(values[8])
                    energy.append(energy_value)
        elif line.startswith("Step"):
            found_start = True

    return energy


# Directory containing folders surf_001, surf_002, ..., surf_100
base_directory = '$your_file_name'  

energy_data = []  # List to store energy arrays for each file

# Get all folder names starting with "surf_" and sort them numerically
folder_names = [name for name in os.listdir(base_directory) if re.match(r'surf_\d+', name)]
folder_names.sort(key=lambda x: int(re.search(r'\d+', x).group()))

# Loop through sorted folder names
for folder_name in folder_names:
    folder_path = os.path.join(base_directory, folder_name)

    # Find log.lammps files in the current folder
    log_files = [file for file in os.listdir(folder_path) if file.endswith('log.lammps')]

    if log_files:
        # Process each log.lammps file in the folder
        for log_file in log_files:
          log_file_path = os.path.join(folder_path, log_file)
            energy = extract_energy(log_file_path)
            energy_data.append(energy)

# Plotting the energy data in a single plot
plt.figure(figsize=(6, 4))  # Size of the plot in inches

colors = itertools.cycle(plt.cm.tab20.colors)

for idx, energy in enumerate(energy_data):
    index = list(range(len(energy)))
    color = next(colors)
    plt.plot(index, energy, label=f'Surface {idx+1:03}', color=color)

plt.xlabel('Steps', fontsize=12)
plt.ylabel('Energy', fontsize=12)
#plt.legend(fontsize=10)
plt.grid(True, linestyle='dashed')
plt.tight_layout()  # Adjusts the padding to fit the plot in the figure area

# Customize the appearance of the plot axes and ticks
plt.xticks(fontsize=10)
plt.yticks(fontsize=10)
plt.tick_params(direction='in', length=4)

# Save the plot as a high-resolution image for publication (e.g., PNG, PDF)
plt.savefig('savefilename.pdf', dpi=300, bbox_inches='tight')

# Show the plot on the screen
plt.show()
