#!/bin/bash -l
#$ -cwd

# Function to create directory, copy files, and run the command
run_command() {
  dir_name=$1
  mkdir -p "$dir_name"
  cp system.prm7 "$dir_name/system.prm7"
  cp system.rst7 "$dir_name/system.rst7"
#   cp equilibration_npt.mdp "$dir_name/equilibration_npt.mdp"
#   cp equilibration_nvt.mdp "$dir_name/equilibration_nvt.mdp"
#   cp minimisation.mdp "$dir_name/minimisation.mdp"
#   cp production.mdp "$dir_name/production.mdp"
#   cp run_acpype_gromacs.sh "$dir_name/run_acpype_gromacs.sh"
  
  # Replace "your_command" with the actual command you want to run
  cd "$dir_name" && bash ~/GROMACS_template/run_acpype_gromacs.sh -t 16 > "output.txt" 2>&1
}

# Directory names
dir_names=("r1" "r2" "r3")

# Run the function for each directory in parallel
for dir_name in "${dir_names[@]}"; do
  run_command "$dir_name" &
done

# Wait for all background jobs to complete
wait
