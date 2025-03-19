# JSON Chunker

A Python script to split large JSON files into smaller chunks using `ijson` for memory-efficient parsing.

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

3. Install the required package:
   ```
   pip install ijson
   ```
   Or use the requirements file:
   ```
   pip install -r requirements.txt
   ```

## Usage

Run the script with the following command:
```
python split_json.py --input path/to/input.json --output path/to/output/ --chunk_size 5000
```

- `--input`: Path to the large JSON file.
- `--output`: Directory where the chunk files will be saved.
- `--chunk_size`: Number of JSON objects per chunk (default: 5000).

The script will create files like `chunk-1.txt`, `chunk-2.txt`, etc., each containing up to `chunk_size` JSON objects.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.