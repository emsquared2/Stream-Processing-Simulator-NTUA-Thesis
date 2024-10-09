# Stream Processing Simulator

*A simulator developed for stream processing as part of the NTUA thesis.*

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Running the simulator](#running-the-simulator)
- [Example Usage](#example-usage)
- [Configuration](#configuration)
- [Contributing](#contributing)
- [License](#license)
- [Contact Information](#contact-information)

## Introduction

The **Stream Processing Simulator** is a tool designed to simulate stream processing systems for research and educational purposes. Developed as part of a thesis project at the National Technical University of Athens (NTUA), it aims to provide insights into the performance and behavior of stream processing architectures.

## Features

- Simulate various stream processing scenarios
- Modular and extensible architecture
- Support for different data scenarios
- Support for custom operators and processing elements
- Fully configurable topology
- Performance metrics
- Scalability testing
- Partition Strategy testing

## Installation

### Prerequisites

- Python 3.8 or higher
- Required Python packages listed in `requirements.txt`

### Steps

1. **Clone the repository**
   ```console
   git clone https://github.com/emsquared2/Stream-Processing-Simulator-NTUA-Thesis.git
   ```

2. Navigate to the project directory
    ```console
   cd Stream-Processing-Simulator-NTUA-Thesis
    ```

3. Install the required packages:
    ```console
    pip install -r requirements.txt
    ```

### Running the Simulator

To run a simulation, use the following command:

```sh
python main.py --config <path/to/config.json> [--key_gen <path/to/generated_key.json>] [--stream <path/to/pre-existing_key.json>] [--logs <path/to/logs_directory>]
```

#### Command-Line Options

- `--config CONFIG`: Path to the configuration file. (Required)
- `--key_gen KEY_GEN`: Path to the generated key stream file. (Mutually required with `--stream`. Either `--key_gen` or `--stream` must be provided.)
- `--stream STREAM`: Path to the pre-existing key stream file. (Mutually required with `--key_gen`. Either `--key_gen` or `--stream` must be provided.)
- `--logs LOGS`: Path to the directory for storing generated logs. (Optional)

### Example Usage

An example to run the simulator with a given configuration file:

```sh
python main.py --config config/example_config.json --key_gen input/stream.txt --logs logs/
```

### Configuration

The configuration file is a JSON file that defines the topology of the stream processing system. Below is an example configuration:

```json
{
    "topology": {
        "stages": [
            {
                "id": 0,
                "type": "stateless",
                "nodes": [
                    {
                        "id": 0,
                        "type": "key_partitioner",
                        "throughput": 1000,
                        "operation_type": "StatelessOperation",
                        "strategy": {
                            "name": "hashing"
                        }
                    }                    
                ]
            },
            {
                "id": 1,
                "type": "stateful",
                "nodes": [
                    {
                        "id": 1,
                        "type": "stateful",
                        "throughput": 1000,
                        "operation_type": "Sorting",
                        "window_size": 5,
                        "slide": 2
                    },
                    {
                        "id": 2,
                        "type": "stateful",
                        "throughput": 1000,
                        "operation_type": "Sorting",
                        "window_size": 5,
                        "slide": 2
                    }
                ]
            },
            {
                "id": 2,
                "type": "stateless",
                "nodes": [
                    {
                        "id": 3,
                        "type": "key_partitioner",
                        "throughput": 1000,
                        "operation_type": "StatelessOperation",
                        "strategy": {
                            "name": "hashing"
                        }
                    },
                    {
                        "id": 4,
                        "type": "key_partitioner",
                        "throughput": 1000,
                        "operation_type": "StatelessOperation",
                        "strategy": {
                            "name": "hashing"
                        }
                    }
                ]
            },
            {
                "id": 3,
                "type": "stateful",
                "nodes": [
                    {
                        "id": 5,
                        "type": "stateful",
                        "throughput": 1000,
                        "operation_type": "Aggregation",
                        "window_size": 5,
                        "slide": 2
                    }
                ]
            }
        ]
    }
}
```

The configuration file describes the system topology with multiple stages and nodes, specifying node types, throughput, operations, partitioning strategies, and window configurations.

### Key Components

- **Stages**: Each stage contains one or more nodes of the same type.
- **Nodes**: Nodes can be either stateless or stateful, and each has a specific role such as key partitioning, worker node (computational node and aggregator node.
- **Operation**: The operation each worker node is implementing.
- **Partition Strategies**: Strategies like hashing can be used to partition keys across nodes.

## Contributing

Contributions are welcome! Here are some ways you can contribute:

1. **Report Issues**: If you find any bugs or have suggestions for improvements, please open an issue.
2. **Submit Pull Requests**: If you want to contribute code, fork the repository, create a new branch, make your changes, and submit a pull request.
3. **Documentation**: Help improve the documentation by adding more examples, clarifying existing sections, or translating content.
4. **Feature Requests**: Suggest new features that can make the simulator more useful.

Before submitting a pull request, please ensure that:
- Your code follows the existing style and conventions.
- You have tested your changes thoroughly.
- You include a description of the changes made and the purpose of the modification.

Feel free to reach out if you have questions or need help getting started.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact Information

For any questions or inquiries, please contact:

| Name                  | Email                                               | GitHub                                         |
|-----------------------|-----------------------------------------------------|------------------------------------------------|
| **Alexandros Ionitsa**| [alexandros.ionitsa@gmail.com](mailto:alexandros.ionitsa@gmail.com) | [alexion](https://github.com/alexion)          |
| **Emmanouil Emmanouilidis**  | [manosemmanouilidis05@gmail.com](mailto:manosemmanouilidis05@gmail.com) | [emsquared2](https://github.com/emsquared2)    |
| **Nikolaos Chalvantzis**        | [nchalv@cslab.ece.ntua.gr](mailto:nchalv@cslab.ece.ntua.gr) | [nchalv](https://github.com/nchalv)  |
