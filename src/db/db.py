import json

# Saving the sounds dictionary to a file
def save_sounds_to_file(sounds, filename="sounds.json"):
    with open(filename, 'w') as json_file:
        json.dump(sounds, json_file, indent=4)

# Loading the sounds dictionary from a file
def load_sounds_from_file(filename="sounds.json"):
    try:
        with open(filename, 'r') as json_file:
            return json.load(json_file)
    except FileNotFoundError:
        return []  # Return an empty list if the file doesn't exist
