import sys, os, glob
from functions import copy_tree, generate_page

dir_path_static = "./static"
dir_path_public = "./docs"

dir_path_content = "./content"
template_path = "./template.html"

default_basepath = "/"

def main():
    basepath = default_basepath
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    print (f"Using BasePath: {basepath}")

    copy_tree(dir_path_static, dir_path_public, deleteDstFirst=True)

    # Generate pages for all markdown files
    md_files = glob.glob(f"{dir_path_content}/**/*.md", recursive=True)
    for md_file in md_files:
        # Determine the output path by mirroring the directory structure
        rel_path = os.path.relpath(md_file, dir_path_content)
        # Change extension from .md to .html
        output_path = os.path.join(dir_path_public, os.path.splitext(rel_path)[0] + ".html")

        # Create directory structure if it doesn't exist
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        # Generate the HTML page
        generate_page(from_path=md_file, template_path=template_path, dest_path=output_path, basepath=basepath)

if __name__ == "__main__":
    main()
