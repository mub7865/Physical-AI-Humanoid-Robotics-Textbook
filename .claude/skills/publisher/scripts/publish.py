import subprocess
import os

def publish_site():
    """
    Builds the Docusaurus site and deploys it to GitHub Pages using the
    pre-configured 'deploy' script in package.json.
    """
    book_directory = "book/"
    print("Starting Docusaurus deployment process...")

    # Step 1: Build the site
    print(f"Running 'npm run build' in '{book_directory}'...")
    try:
        subprocess.run(
            ["npm", "run", "build"],
            check=True,
            cwd=book_directory,
            capture_output=True, # Capture output to show on error
            text=True
        )
        print("Docusaurus site built successfully.")
    except subprocess.CalledProcessError as e:
        print("\n--- ERROR: Failed to build Docusaurus site. ---")
        print(f"Exit Code: {e.returncode}")
        print("\n--- STDOUT ---")
        print(e.stdout)
        print("\n--- STDERR ---")
        print(e.stderr)
        print("\nDeployment failed at build step.")
        return

    # Step 2: Deploy the site
    print(f"\nRunning 'npm run deploy' in '{book_directory}'...")
    try:
        # Note: The 'docusaurus deploy' command requires a GIT_USER environment variable
        # for non-interactive deployment. Ensure it is set in the execution environment.
        # Example: GIT_USER=<your-github-username> npm run deploy
        subprocess.run(
            ["npm", "run", "deploy"],
            check=True,
            cwd=book_directory,
            capture_output=True, # Capture output to show on error
            text=True
        )
        print("\n--- SUCCESS: Site deployed successfully to GitHub Pages! ---")
        print("It might take a few minutes for the changes to appear live.")

    except subprocess.CalledProcessError as e:
        print("\n--- ERROR: Failed to deploy Docusaurus site. ---")
        print(f"Exit Code: {e.returncode}")
        print("\n--- STDOUT ---")
        print(e.stdout)
        print("\n--- STDERR ---")
        print(e.stderr)
        print("\nDeployment failed. Please check the error message above.")
        print("Tip: Make sure the GIT_USER environment variable is set and you have the correct permissions for the repository.")

if __name__ == "__main__":
    publish_site()
