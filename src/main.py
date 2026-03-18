from helpers.file_utils import copy_folder_contents, delete_folder_contents, generate_page
from textnode import TextNode, TextType

def main():
    delete_folder_contents('public')
    copy_folder_contents('static', 'public')
    generate_page('content/index.md', 'template.html', 'public/index.html')

if __name__ == "__main__":
    main()

#failing in blockquote and italic  cases on bootdev