import os
import time
import argparse
from openai import OpenAI
import openai

def parse_arguments():
    parser = argparse.ArgumentParser(description="OpenAI API query script")
    parser.add_argument('--base_rule_path', type=str,help="Base path for prompt files")
    parser.add_argument('--rule_path', type=str,help="Path to the prompt file")
    parser.add_argument('--target_answer_path', type=str,help="Path to save the results")
    return parser.parse_args()

def query_openai(file_path, num_queries=10, max_retries=5, retry_delay=5):
    """
    Query OpenAI API with content from a prompt file
    
    Parameters:
        file_path: Path to the file containing prompt content
        num_queries: Number of queries to perform
        max_retries: Maximum number of retries for failed requests
        retry_delay: Delay between retries in seconds
    
    Returns:
        List of query results
    """
    # Initialize OpenAI client
    client = OpenAI(api_key="<sk-xxx>")
    results = []
    
    for i in range(num_queries):
        retries = 0
        while retries < max_retries:
            try:
                # Read prompt content
                with open(file_path, 'r', encoding='utf-8') as file:
                    prompt_content = file.read().strip()
                
                # Call OpenAI API
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "user", "content": prompt_content}]
                )
                
                results.append(response.choices[0].message.content)
                break
                
            except (openai.InternalServerError, Exception) as e:
                print(f"Error: {e}, retrying {retries + 1}/{max_retries}...")
                retries += 1
                time.sleep(retry_delay)
        
        if retries == max_retries:
            print(f"Query {i + 1} exceeded maximum retries, skipping...")
    
    return results

def main():
    args = parse_arguments()
    
    # Construct input file path
    input_file = os.path.join(args.base_rule_path, args.rule_path)
    
    # Execute query (default: 10 query)
    results = query_openai(input_file, num_queries=10)
    
    # Save results
    for idx, result in enumerate(results):
        # Construct output filename
        file_name = f"{os.path.splitext(args.rule_path)[0]}_{idx}.txt"
        output_file = os.path.join(args.target_answer_path, file_name)
        
        # Write result to file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(result)
        
        print(f"Result {idx} saved to: {output_file}")

if __name__ == "__main__":
    main()

    
