import json
import random

class ElectricalNetworkGenerator:
    def __init__(self, num_roots, num_levels, num_children_per_node):
        self.num_roots = num_roots
        self.num_levels = num_levels
        self.num_children_per_node = num_children_per_node
        self.node_id = 1
        self.boards = []

    def generate_board(self, level, position, parent_phase, parent_id=None):
        if parent_phase == "Single-phase":
            str_board_phase = "Single-phase"
        else: 
            #str_board_phase = random.choice(["Single-phase", "Three-phase"])
            str_board_phase = "Three-phase"
        board = {
            "node_id": self.node_id,
            "parent_node_id": parent_id,
            "name": f"DistributionBoard: Level: {level}",
            "circuits": [],
            "phase": str_board_phase
        }
        str_print = (f"Dist Board(indent{level}) fed from cct {position}, phase-{str_board_phase}")
        print(Indent(str_print, 10*level))
        
        current_id = self.node_id
        self.node_id += 1

        if level < self.num_levels:
            num_of_ccts = 6
            num_children = random.randint(1, self.num_children_per_node)
            for cct_index in range(num_of_ccts):
                if str_board_phase == "Three-phase":
                    circuit_type = random.choice(["Single-phase", "Three-phase"])
                else:
                    circuit_type = "Single-phase"
                if circuit_type =="Three-phase":
                    lst_cct_phases = ["L1", "L2", "L3"]
                else:
                    lst_cct_phases = ["S"]

                for str_cct_phase in lst_cct_phases:
                    circuit = {
                        "circuit_number": cct_index,
                        "circuit_phase": str_cct_phase,
                        "circuit_type": circuit_type,
                        "child_node_id": None
                    }
                    str_print = (f"circuit-{cct_index} phase-{str_cct_phase}")
                    print(Indent(str_print, 10*level))
                    board["circuits"].append(circuit)
                
                
                if num_children > 0:
                    print(Indent("|  ", 10*level))
                    print(Indent("_______", 10*level))
                    child_board = self.generate_board(level + 1, cct_index, str_board_phase, current_id)
                    circuit["child_node_id"] = child_board["node_id"]

                board["circuits"].append(circuit)

        self.boards.append(board)
        return board

    def generate_network_data(self):
        for root_position in range(self.num_roots):
            self.generate_board(1, str(root_position), "Three-phase")
        return self.boards

def Indent(char, num_indents):
    """
    Function to indent a character by a specified number of spaces.

    :param char: The character to be printed.
    :param num_indents: The number of spaces to indent the character.
    :return: A string with the specified number of spaces followed by the character.
    """
    return " " * num_indents + char

def charprint(char, num_times):
    """
    Function to print a character a specified number of times.
    
    :param char: The character to be printed.
    :param num_times: The number of times to print the character.
    """
    print(char * num_times)

def main():
    # Parameters
    num_roots = 1
    num_levels = 3
    num_children_per_node = 3

    # Generate Electrical Distribution Network data
    generator = ElectricalNetworkGenerator(num_roots, num_levels, num_children_per_node)
    network_data = generator.generate_network_data()

    # Convert to JSON format
    network_json = json.dumps(network_data, indent=4)

    # Print JSON to console (optional)
    # print(network_json)

    # Write JSON to a file
    with open('network_data.json', 'w') as json_file:
        json.dump(network_data, json_file, indent=4)

if __name__ == "__main__":
    main()
