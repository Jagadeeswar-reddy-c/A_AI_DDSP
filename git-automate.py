import subprocess
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(message)s")

def run_git_command(command):
    """Runs a Git command and handles errors gracefully."""
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        logging.warning(f"Git command failed: {result.stderr}")
    return result

def automate_git():
    """Automates Git workflow."""
    # Add all changes respecting .gitignore
    run_git_command(['git', 'add', '--all'])

    # Get commit message
    commit_message = input("Enter commit message: ").strip()
    if not commit_message:
        logging.error("Commit message cannot be empty!")
        return

    # Commit changes
    run_git_command(['git', 'commit', '-m', commit_message])

    # Pull latest changes
    run_git_command(['git', 'pull', '--rebase'])

    # Push changes
    result = run_git_command(['git', 'push'])
    if result.returncode == 0:
        logging.info("Changes successfully pushed!")
    else:
        logging.error(f"Failed to push changes: {result.stderr}")

if __name__ == "__main__":
    automate_git()