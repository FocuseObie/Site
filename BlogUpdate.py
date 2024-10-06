import os
from datetime import datetime
import subprocess
import docx

blog_file = "Blog.html"
docx_folder = "./docx_files"  # Folder to hold the .docx files

def extract_text_from_docx(file_path):
    """Extract text from .docx file and preserve basic formatting, including lists."""
    doc = docx.Document(file_path)
    full_text = []
    inside_list = False

    for para in doc.paragraphs:
        # Check for bullet points (list items)
        if para.style.name.startswith('List'):
            # If we're entering a list, start the <ul> tag
            if not inside_list:
                full_text.append("<ul>")
                inside_list = True
            full_text.append(f"<li>{para.text}</li>")
        else:
            # If we were inside a list and encounter a non-list paragraph, close the list
            if inside_list:
                full_text.append("</ul>")
                inside_list = False

            # Preserve headings, bold, and italic formatting
            if para.style.name.startswith('Heading'):
                full_text.append(f"<h2>{para.text}</h2>")
            elif para.runs and para.runs[0].bold:
                full_text.append(f"<b>{para.text}</b>")
            elif para.runs and para.runs[0].italic:
                full_text.append(f"<i>{para.text}</i>")
            else:
                full_text.append(f"<p>{para.text}</p>")
    
    # If the document ends inside a list, close the list
    if inside_list:
        full_text.append("</ul>")

    return "\n".join(full_text)

def create_blog_post(file_path):
    """Create an HTML blog post from a .docx file."""
    content = extract_text_from_docx(file_path)
    title = os.path.basename(file_path).replace('.docx', '')
    current_date = datetime.now().strftime('%b %d, %Y')

    new_post = f"""
    <div class="card">
        <h2>{title}</h2>
        <h5>{current_date}</h5>
        {content}
    </div>
    """
    return new_post

def get_most_recent_docx_file(folder):
    """Find the most recent .docx file in the folder."""
    docx_files = [os.path.join(folder, f) for f in os.listdir(folder) if f.endswith('.docx')]

    if not docx_files:
        return None

    # Get the most recent .docx file based on last modification time
    most_recent_file = max(docx_files, key=os.path.getmtime)
    return most_recent_file

def update_blog():
    """Update the blog HTML file with the most recent .docx post."""
    most_recent_file = get_most_recent_docx_file(docx_folder)

    if most_recent_file is None:
        print("No .docx files found in the folder.")
        return False

    # Read the existing blog HTML file
    with open(blog_file, 'r') as f:
        blog_html = f.read()
        print("Blog file read successfully.")

    # Create a new blog post from the most recent .docx file
    new_post = create_blog_post(most_recent_file)

    # Insert the new post into the blog HTML file at the correct placeholder
    blog_html = blog_html.replace('<div class="leftcolumn" id="blog">', f'<div class="leftcolumn" id="blog">\n{new_post}', 1)

    # Write the updated HTML back to the file
    with open(blog_file, 'w') as f:
        f.write(blog_html)
        print(f"Blog file updated with the most recent file: {os.path.basename(most_recent_file)}")

    return True

def git_commit_and_push():
    """Commit and push changes to GitHub."""
    try:
        # Check if there are changes to commit
        result = subprocess.run(['git', 'status', '--porcelain'], capture_output=True, text=True)

        # If there are changes, stage and commit them
        if result.stdout.strip():
            subprocess.run(['git', 'add', 'Blog.html'], check=True)
            subprocess.run(['git', 'commit', '-m', 'Update blog with new posts'], check=True)
            subprocess.run(['git', 'push'], check=True)
            print("Changes committed and pushed to GitHub.")
        else:
            print("No changes to commit.")
    except subprocess.CalledProcessError as e:
        print(f"Error during git operation: {e}")

if __name__ == '__main__':
    # First update the blog
    if update_blog():
        # Then commit and push to GitHub if the blog was updated
        git_commit_and_push()
