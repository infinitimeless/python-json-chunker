import ijson
import json
import os
import argparse

def main():
    parser = argparse.ArgumentParser(description='Split large JSON files into smaller chunks.')
    parser.add_argument('--input', required=True, help='Path to the input JSON file')
    parser.add_argument('--output', required=True, help='Directory to save the output chunks')
    parser.add_argument('--chunk_size', type=int, default=5000, help='Number of JSON objects per chunk')
    args = parser.parse_args()

    input_file = args.input
    output_dir = args.output
    chunk_size = args.chunk_size

    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Initialize chunk number and item count
    chunk_number = 0
    item_count = 0

    # Open the input file and parse it incrementally
    with open(input_file, 'r') as f:
        parser = ijson.items(f, 'item')  # Assumes the JSON is an array of objects
        current_chunk = []
        for item in parser:
            item_count += 1
            print(f"Item {item_count}: {item}")  # See what's being read
            current_chunk.append(item)
            if len(current_chunk) == chunk_size:
                chunk_number += 1
                output_file = os.path.join(output_dir, f'chunk-{chunk_number}.txt')
                with open(output_file, 'w') as outfile:
                    for obj in current_chunk:
                        json.dump(obj, outfile)
                        outfile.write('\n')
                print(f"Written chunk {chunk_number} with {len(current_chunk)} items")
                current_chunk = []
        # Write any remaining objects to the last chunk
        if current_chunk:
            chunk_number += 1
            output_file = os.path.join(output_dir, f'chunk-{chunk_number}.txt')
            with open(output_file, 'w') as outfile:
                for obj in current_chunk:
                    json.dump(obj, outfile)
                    outfile.write('\n')
            print(f"Written chunk {chunk_number} with {len(current_chunk)} items")

    # Final message
    print(f"Finished splitting the file into {chunk_number} chunks.")
    print(f"Total items processed: {item_count}")

if __name__ == '__main__':
    main()