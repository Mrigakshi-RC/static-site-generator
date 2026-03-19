from genericpath import isfile
import os
import shutil

from helpers.markdown_to_html import extract_title, markdown_to_html_node


def delete_folder_contents(folder_path):
    if not os.path.exists(folder_path):
        print(f"{folder_path} not found")
        return
    
    for filename in os.listdir(folder_path):
        file_path=os.path.join(folder_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print("Error: ", e)

def copy_folder_contents(source_dir, destination_dir):
    try:
        shutil.copytree(source_dir, destination_dir,dirs_exist_ok=True)
    except Exception as e:
        print(e)

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    md_content, html_content=None, None

    with open(from_path, 'r') as f:
        md_content = f.read()

    with open(template_path, 'r') as f:
        html_content = f.read()

    md_to_html=markdown_to_html_node(md_content).to_html()
    page_title=extract_title(md_content)

    final_html_content=html_content.replace('{{ Title }}', page_title).replace('{{ Content }}', md_to_html).replace('href="/',f'href="{basepath}').replace('src="/',f'src="{basepath}')

    with open(dest_path, "w") as file:
        file.write(final_html_content)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    if dir_path_content==None:
        return
    if os.path.isfile(dir_path_content):
        base_name, _ = os.path.splitext(dest_dir_path)
        generate_page(dir_path_content, template_path, base_name+".html", basepath)
    else:
        for item in os.listdir(dir_path_content):
            content_path=os.path.join(dir_path_content, item)
            dest_path=os.path.join(dest_dir_path, item)
            if os.path.isdir(content_path):
                os.mkdir(dest_path)
            generate_pages_recursive(content_path, template_path, dest_path, basepath)

        
