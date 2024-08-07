# Define project name and directory
param (
    [string]$projectName = "C:\Users\micha\Dropbox\DistributionBoardNetworkScripts\distnet",
    [string]$pythonVersion = "python"  # or "python3" depending on your setup
)

# Create project directory
$projectPath = $projectName
New-Item -ItemType Directory -Path $projectPath -Force

# Navigate to project directory
Set-Location -Path $projectPath

# Create a virtual environment
Write-Output "Creating virtual environment..."
& $pythonVersion -m venv venv

# Activate the virtual environment
Write-Output "Activating virtual environment..."
& .\venv\Scripts\Activate.ps1

# Upgrade pip
Write-Output "Upgrading pip..."
pip install --upgrade pip

# Install required packages
Write-Output "Installing required packages..."
$requirements = @(
    "json"
)
foreach ($package in $requirements) {
    pip install $package
}

# Create a basic directory structure
Write-Output "Creating directory structure..."
$directories = @("src", "tests")
foreach ($dir in $directories) {
    New-Item -ItemType Directory -Path $dir -Force
}

# Create a basic README file
Write-Output "Creating README file..."
$readmePath = Join-Path -Path $projectPath -ChildPath "README.md"
Set-Content -Path $readmePath -Value "# $projectName`n`nThis project generates an electrical distribution network in a building."

# Create a .gitignore file
Write-Output "Creating .gitignore file..."
$gitignorePath = Join-Path -Path $projectPath -ChildPath ".gitignore"
Set-Content -Path $gitignorePath -Value "venv/`n__pycache__/`n*.pyc`n"

# Create an initial Python script
Write-Output "Creating initial Python script..."
$scriptPath = Join-Path -Path $projectPath -ChildPath "src\main.py"
$scriptContent = @'
import json
import random

class ElectricalNetworkGenerator:
    def __init__(self, num_roots, num_levels, num_children_per_node):
        self.num_roots = num_roots
        self.num_levels = num_levels
        self.num_children_per_node = num_children_per_node
        self.node_id = 1

    def generate_board(self, level):
        board = {
            "id": self.node_id,
            "name": f"DistributionBoard{self.node_id}",
            "circuits": [],
            "phase": random.choice(["Single-phase", "Three-phase"])
        }
        current_id = self.node_id
        self.node_id += 1

        if level < self.num_levels:
            num_children = random.randint(1, self.num_children_per_node)
            for _ in range(num_children):
                child_board = self.generate_board(level + 1)
                circuit_type = random.choice(["Single-phase", "Three-phase"])
                board["circuits"].append({
                    "circuit_type": circuit_type,
                    "downstream_board": child_board
                })
        
        return board

    def generate_network_data(self):
        network_data = []
        for _ in range(self.num_roots):
            root_board = self.generate_board(1)
            network_data.append(root_board)
        return network_data

def main():
    # Parameters
    num_roots = 2
    num_levels = 3
    num_children_per_node = 3

    # Generate Electrical Distribution Network data
    generator = ElectricalNetworkGenerator(num_roots, num_levels, num_children_per_node)
    network_data = generator.generate_network_data()

    # Convert to JSON format
    network_json = json.dumps(network_data, indent=4)
    print(network_json)

if __name__ == "__main__":
    main()
'@
Set-Content -Path $scriptPath -Value $scriptContent

Write-Output "Python project setup complete."
