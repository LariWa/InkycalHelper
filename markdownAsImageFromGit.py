import markdown
from html2image import Html2Image
from git import Repo
import os
import time
import re

def markdown_to_image(md_file_path, output_image_path):
    # Read the Markdown file
    with open(md_file_path, 'r') as file:
        md_content = file.read()
    
    # Convert Markdown to HTML
    html_content = markdown.markdown(md_content)
    html_content = re.sub(r'\[\s*\]', '&#x2610;', html_content)
    html_content = html_content.replace('[x]', '&#x2611;')  
    html_with_css = f"""
    <html>
    <head>
    <style>
        body {{
            zoom: 1.5;
            font-family: Arial, sans-serif;
        }}
         ul {{
            list-style-type: none;
        }}
    </style>
    </head>
    <body>
    {html_content}
    </body>
    </html>
    """
    print(html_content)
    # Initialize Html2Image
    hti = Html2Image()
    
    # Use Html2Image to convert HTML to image
    hti.screenshot(html_str=html_with_css, save_as=output_image_path, size=(448, 290))
    
def fetch_markdown_from_repo(repo_url, file_path, local_dir='/home/pi/InkycalHelper/MarkdownRepo'):
    # Clone the repository into the local directory
    if not os.path.exists(local_dir):
        Repo.clone_from(repo_url, local_dir)
    else:
        repo = Repo(local_dir)
        repo.remotes.origin.fetch()
        # Check if there are changes to pull
        remote_commit = repo.git.rev_parse("origin/master")
        local_commit = repo.git.rev_parse("HEAD")
        if remote_commit != local_commit:
            print("There are updates available. Pulling changes...")
            repo.remotes.origin.pull()
        #else: return None

    # Construct the full path to the file
    full_file_path = os.path.join(local_dir, file_path)
    if not os.path.isfile(full_file_path):
      raise FileNotFoundError("The file "+ full_file_path + " does not exist in the repository.")

    return full_file_path   
        

repo_url = 'https://github.com/hansu/notebook'
file_path = 'README.md'
output_image_path = 'MarkdownImage.png'

while True:
    md_file_path = fetch_markdown_from_repo(repo_url, file_path)
    if md_file_path is not None:
        markdown_to_image(md_file_path, output_image_path)
        print("Updated mark down image")
    time.sleep(600) 
