import os

def process_file(file_path):
    replacements = {
        'cracks': '0',
        'patholes': '1',
    }
    
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    modified_lines = []
    for line in lines:
        parts = line.split()
        
        if not parts:
            continue
        
        # ✅ Skip if already converted
        if parts[0].isdigit():
            modified_lines.append(line)
            continue
        
        class_name = parts[0].strip().lower()
        
        if class_name in replacements:
            parts[0] = replacements[class_name]
        
        modified_lines.append(' '.join(parts) + '\n')
    
    with open(file_path, 'w') as file:
        file.writelines(modified_lines)

def process_folder(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.txt'):
                file_path = os.path.join(root, file)
                process_file(file_path)

main_folder = r'D:\\pathole\\dataset'

for subfolder in ['train', 'test', 'val']:
    folder_path = os.path.join(main_folder, subfolder)
    if os.path.exists(folder_path):
        process_folder(folder_path)
    else:
        print(f"Folder not found: {folder_path}")

print("✅ Processing complete.")