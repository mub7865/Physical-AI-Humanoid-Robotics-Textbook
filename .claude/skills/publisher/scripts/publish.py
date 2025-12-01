import subprocess
import os

def publish_site():
    print("Building Docusaurus site...")
    try:
        subprocess.run(["npm", "run", "build"], check=True, cwd="book/")
        print("Docusaurus site built successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error building Docusaurus site: {e}")
        return

    print("Deploying to GitHub Pages...")
    try:
        # Placeholder for git deployment logic
        # This typically involves committing the build output and pushing to a specific branch (e.g., gh-pages)
        # For a full implementation, consider using gh-pages package or specific git commands.
        # Example:
        # subprocess.run(["git", "add", "-f", "book/build"], check=True)
        # subprocess.run(["git", "commit", "-m", "Deploy to GitHub Pages"], check=True)
        # subprocess.run(["git", "push", "origin", "gh-pages"], check=True)
        print("Deployment logic would go here. (e.g., git add, commit, push to gh-pages branch)")
        print("Site deployed successfully (placeholder).")
    except subprocess.CalledProcessError as e:
        print(f"Error deploying to GitHub Pages: {e}")

if __name__ == "__main__":
    publish_site()