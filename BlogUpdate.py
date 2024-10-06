import os
from datetime import datetime

blog_file = "Blog.html"
txt_folder = "./txt_files"

def create_blog_post(file_path):
    """Create an HTML blog post from a .txt file."""
    with open(file_path, 'r') as f:
        content = f.read()

    title = os.path.basename(file_path).replace('.txt', '')
    current_date = datetime.now().strftime('%b %d, %Y')

    new_post = f"""
    <div class="card">
        <h2>{title}</h2>
        <h5>{current_date}</h5>
        <p>{content}</p>
    </div>
    """
    return new_post

def get_most_recent_txt_file(folder):
    """Find the most recent .txt file in the folder."""
    txt_files = [os.path.join(folder, f) for f in os.listdir(folder) if f.endswith('.txt')]

    if not txt_files:
        return None

    # Get the most recent .txt file based on last modification time
    most_recent_file = max(txt_files, key=os.path.getmtime)
    return most_recent_file

def update_blog():
    """Update the blog HTML file with the most recent .txt post."""
    most_recent_file = get_most_recent_txt_file(txt_folder)

    if most_recent_file is None:
        print("No .txt files found in the folder.")
        return

    # Read the existing blog HTML file
    with open(blog_file, 'r') as f:
        blog_html = f.read()

    # Create a new blog post from the most recent .txt file
    new_post = create_blog_post(most_recent_file)

    # Insert the new post into the blog HTML file before the closing </div> tag
    blog_html = blog_html.replace('</div>', new_post + '</div>', 1)

    # Write the updated HTML back to the file
    with open(blog_file, 'w') as f:
        f.write(blog_html)

    print(f"Blog updated with the most recent file: {os.path.basename(most_recent_file)}")

if __name__ == '__main__':
    update_blog()
