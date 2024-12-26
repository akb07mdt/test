import subprocess
import os
import tempfile
import shutil

# Set paths
GIT_REPO_PATH = "git_learn"  # Update this with your actual repo path
VERSION_SCRIPT_PATH = os.path.join(GIT_REPO_PATH, "version.sh")
VERSION_FILE_PATH = os.path.join(GIT_REPO_PATH, "Product", "DataBase", "version.h")

def run_shell_command(command, cwd=None):
    """Runs a shell command and returns the output."""
    try:
        result = subprocess.run(command, cwd=cwd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        return result.stdout.decode("utf-8")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.stderr.decode('utf-8')}")
        return None

def generate_version_file():
    """Executes the version.sh script to generate the version.h file."""
    print("Generating version.h by executing version.sh...")
    run_shell_command(f"bash {VERSION_SCRIPT_PATH}")

def extract_version_and_tag():
    """Extracts PRODUCT_TAG and PRODUCT_VERSION from version.h."""
    if not os.path.exists(VERSION_FILE_PATH):
        print(f"Error: {VERSION_FILE_PATH} does not exist.")
        return None, None
    
    tag_name, version = None, None
    with open(VERSION_FILE_PATH, "r") as file:
        for line in file:
            if line.startswith("#define PRODUCT_TAG"):
                tag_name = line.split("\"")[1].strip()
            elif line.startswith("#define PRODUCT_VERSION"):
                version = line.split("\"")[1].strip()
    return tag_name, version

def create_tag_annotation(tag_name, version, repo_name):
    """Creates a temporary file and fills it with the tag annotation."""
    try:
        tmp_file = tempfile.mktemp()
        with open(tmp_file, "w") as f:
            f.write(f"Annotation for tag {tag_name}\n")
            f.write(f"Associated with version {version} of product {repo_name}\n\n")
            f.write("<Provide tag annotation details and then save and exit the editor>")
        return tmp_file
    except Exception as e:
        print(f"Error creating temporary file for tag annotation: {e}")
        return None

def edit_tag_annotation(tmp_file):
    """Opens the temporary file in the default editor for user input."""
    try:
        editor = shutil.which("notepad") if os.name == "nt" else "vi"
        subprocess.run([editor, tmp_file], check=True)
        return True
    except Exception as e:
        print(f"Error opening editor: {e}")
        return False

def tag_repo(tmp_file, tag_name):
    """Tags the Git repository with the provided tag name and annotation."""
    try:
        subprocess.run(["git", "tag", "--annotate", "--file", tmp_file, tag_name], check=True, cwd=GIT_REPO_PATH)
        subprocess.run(["git", "push", "origin", tag_name], check=True, cwd=GIT_REPO_PATH)
        print(f"Tag {tag_name} pushed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error during tagging operation: {e}")

def main():
    # Generate version.h
    generate_version_file()
    
    # Extract the tag name and version from version.h
    tag_name, version = extract_version_and_tag()
    if not tag_name or not version:
        print("Failed to extract tag name or version from version.h.")
        return

    print(f"Tag Name: {tag_name}")
    print(f"Version: {version}")

    # Create the tag annotation file
    repo_name = "TM91"  # Hardcoded repo name
    tmp_file = create_tag_annotation(tag_name, version, repo_name)
    if not tmp_file:
        print("Failed to create temporary file for tag annotation.")
        return

    # Ask the user to provide the annotation details in the editor
    print("Please provide the tag annotation in the editor...")
    if not edit_tag_annotation(tmp_file):
        print("Error: Failed to edit tag annotation.")
        return

    # Check if the annotation was modified before saving
    with open(tmp_file, "r") as f:
        annotation = f.read()
        if "<Provide tag annotation details and then save and exit the editor>" in annotation:
            print("Error: Tag annotation was not modified.")
            return

    # Tag the repository and push the tag
    tag_repo(tmp_file, tag_name)

    # Clean up the temporary file
    os.remove(tmp_file)

if __name__ == "__main__":
    main()
