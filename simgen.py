import json
import random

def load_config(config_file):
    with open(config_file, 'r') as file:
        config = json.load(file)
    return config

def generate_keystream(config):
    steps = config["steps"]
    num_keys = config["number of keys"]
    arrival_rate = config["arrival rate"]
    
    keys = [f"key{i}" for i in range(1, num_keys + 1)]
    stream = []
    
    for _ in range(steps):
        line = random.choices(keys, k=arrival_rate)
        stream.append(' '.join(line))
    
    return stream

def write_output(stream, output_file):
    with open(output_file, 'w') as file:
        for line in stream:
            file.write(line + "\n")

def main(config_file, output_file):
    config = load_config(config_file)
    stream = generate_keystream(config)
    write_output(stream, output_file)

if __name__ == "__main__":
    config_file = "config.json"  
    output_file = "stream_output.txt"  
    
    main(config_file, output_file)
