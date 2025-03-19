# JSON Chunker

A Python tool for processing and splitting large JSON files into smaller manageable chunks.

## Features

- Split large JSON files into smaller chunks
- Support for projects with document collections
- Robust error handling for malformed JSON
- File analysis capabilities

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/infinitimeless/python-json-chunker.git
   cd python-json-chunker
   ```

2. Create a virtual environment (optional but recommended):
   ```
   python -m venv myenv
   source myenv/bin/activate  # On Windows: myenv\Scripts\activate
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Usage

### Splitting JSON Files

Run the script with the following command:
```
python split_json.py --input path/to/input.json --output path/to/output/ --chunk_size 100
```

- `--input`: Path to the input JSON file.
- `--output`: Directory where the chunk files will be saved.
- `--chunk_size`: Number of document objects per chunk (default: 100).

The script will create files like `chunk-1.txt`, `chunk-2.txt`, etc., each containing up to `chunk_size` document objects.

### Analyzing JSON Files

To analyze the structure of a JSON file:
```
python analyze_json.py path/to/file.json
```

This will provide information about:
- File size
- Number of objects
- Brace/bracket counts
- Sample object structure

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.