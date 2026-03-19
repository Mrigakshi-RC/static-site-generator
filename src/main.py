import sys

from helpers.file_utils import copy_folder_contents, delete_folder_contents, generate_page, generate_pages_recursive
from textnode import TextNode, TextType

def main():
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"

    delete_folder_contents('docs')
    copy_folder_contents('static', 'docs')
    generate_pages_recursive("content", 'template.html', 'docs', basepath)

if __name__ == "__main__":
    main()

#failing in blockquote and italic  cases on bootdev