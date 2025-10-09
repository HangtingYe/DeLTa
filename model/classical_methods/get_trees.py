import os
import re


def extract_and_rename_trees(input_directory, output_file,data_item,md,ml,tree):
    with open(output_file, 'w') as out_file:
        for root, _, files in os.walk(input_directory):
            for index, file_name in enumerate(files):
                file_path = os.path.join(root, file_name)
                file_ext = os.path.splitext(file_name)[1]
                pattern = rf'RFfull_{data_item}_randfull_md{md}_ml{ml}_tree{tree}_\d+.txt'
                if file_ext == '.txt' and re.search(pattern, file_name):
                    try:
                        with open(file_path, 'r') as file:
                            content = file.read()
                            pattern = re.compile(r"```python(.*?)```", re.DOTALL)
                            matches = pattern.findall(content)
                            for match_index, match in enumerate(matches):
                                name_match = re.search(rf'RFfull_(\w+)_randfull_md(\d+)_ml(\d+)_tree(\d+)_(\d+)', file_name)
                                if name_match:
                                    rand_part = 'full'
                                    md_num = name_match.group(2)
                                    ml_num = name_match.group(3)
                                    num = name_match.group(5)#5
                                    tree_name = f'tree_{rand_part}_md{md_num}_ml{ml_num}_{num}'
                                    print(tree_name)
                                else:
                                    tree_name = f'tree_{index}_{match_index}'
                                new_tree_content = re.sub(r'self\.tree', tree_name, match)
                                out_file.write(f'{new_tree_content}\n\n')
                                print(f'write in {out_file}')
                    except FileNotFoundError:
                        print(f"File not found: {file_path}")
                    except Exception as e:
                        print(f"Error processing file {file_path}: {e}")


if __name__ == "__main__":
 
    data=['']
    mds = []
    mls = []
    tree=[]

    for data_item in data:
        if not os.path.exists(f"trees_mdml/{data_item}"):
            print('data_item')
            os.makedirs(f"trees_mdml/{data_item}")
        for tree_item in tree:
            for md in mds:
                for ml in mls:
                
                    input_directory = f'data/{data_item}/answers'
                    output_file = f'trees_mdml/{data_item}/RFfull_{data_item}_tree{tree_item}_md{md}_ml{ml}.py'
                    extract_and_rename_trees(input_directory, output_file, data_item,md,ml,tree_item)


