import json
import os
import argparse

def main():
    parser = argparse.ArgumentParser(description='Split large JSON files into smaller chunks.')
    parser.add_argument('--input', required=True, help='Path to the input JSON file')
    parser.add_argument('--output', required=True, help='Directory to save the output chunks')
    parser.add_argument('--chunk_size', type=int, default=100, help='Number of document objects per chunk')
    args = parser.parse_args()

    input_file = args.input
    output_dir = args.output
    chunk_size = args.chunk_size

    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Initialize chunk number and item count
    chunk_number = 0
    doc_count = 0
    current_chunk = []

    try:
        # Load and process the file
        with open(input_file, 'r') as f:
            try:
                # Parse the JSON as an array of projects
                projects = json.load(f)
                
                # Go through each project and extract documents
                for project in projects:
                    if 'docs' in project and isinstance(project['docs'], list):
                        for doc in project['docs']:
                            # Add project metadata to each document
                            doc['project_uuid'] = project.get('uuid', '')
                            doc['project_name'] = project.get('name', '')
                            doc['creator'] = project.get('creator', {})
                            
                            # Add to current chunk
                            current_chunk.append(doc)
                            doc_count += 1
                            
                            # When chunk is full, write to file
                            if len(current_chunk) >= chunk_size:
                                chunk_number += 1
                                output_file = os.path.join(output_dir, f'chunk-{chunk_number}.txt')
                                with open(output_file, 'w') as outfile:
                                    for item in current_chunk:
                                        json.dump(item, outfile)
                                        outfile.write('\n')
                                print(f"Written chunk {chunk_number} with {len(current_chunk)} documents")
                                current_chunk = []
                    else:
                        print(f"Warning: Project {project.get('name', 'unnamed')} does not have docs or docs is not a list")
            
            except json.JSONDecodeError as e:
                print(f"Error parsing JSON: {str(e)}")
                print("Trying line by line parsing...")
                
                # Reset file position
                f.seek(0)
                
                # Try to read line by line
                for line in f:
                    try:
                        if line.strip() in ['[', ']', ',']:
                            continue
                            
                        # Remove trailing comma if any
                        if line.rstrip().endswith(','):
                            line = line.rstrip()[:-1]
                            
                        # Parse the line as a JSON object
                        project = json.loads(line)
                        
                        if 'docs' in project and isinstance(project['docs'], list):
                            for doc in project['docs']:
                                # Add project metadata to each document
                                doc['project_uuid'] = project.get('uuid', '')
                                doc['project_name'] = project.get('name', '')
                                doc['creator'] = project.get('creator', {})
                                
                                # Add to current chunk
                                current_chunk.append(doc)
                                doc_count += 1
                                
                                # When chunk is full, write to file
                                if len(current_chunk) >= chunk_size:
                                    chunk_number += 1
                                    output_file = os.path.join(output_dir, f'chunk-{chunk_number}.txt')
                                    with open(output_file, 'w') as outfile:
                                        for item in current_chunk:
                                            json.dump(item, outfile)
                                            outfile.write('\n')
                                    print(f"Written chunk {chunk_number} with {len(current_chunk)} documents")
                                    current_chunk = []
                    except json.JSONDecodeError:
                        print(f"Warning: Could not parse line as JSON: {line[:100]}...")
    
    except Exception as e:
        print(f"Error processing file: {str(e)}")
    
    # Write any remaining documents to the last chunk
    if current_chunk:
        chunk_number += 1
        output_file = os.path.join(output_dir, f'chunk-{chunk_number}.txt')
        with open(output_file, 'w') as outfile:
            for item in current_chunk:
                json.dump(item, outfile)
                outfile.write('\n')
        print(f"Written chunk {chunk_number} with {len(current_chunk)} documents")

    # Final message
    print(f"Finished splitting the file into {chunk_number} chunks.")
    print(f"Total documents processed: {doc_count}")

if __name__ == '__main__':
    main()