from helpers.file_utils import copy_folder_contents, delete_folder_contents, generate_page, generate_pages_recursive
from textnode import TextNode, TextType

def main():
    delete_folder_contents('public')
    copy_folder_contents('static', 'public')
    generate_pages_recursive('content', 'template.html', 'public')

if __name__ == "__main__":
    main()

#failing in blockquote and italic  cases on bootdev