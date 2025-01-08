import subprocess
import os
import tempfile
import re
import sys
import datetime

# Paths to scripts and files
VERSION_FILE_PATH = os.path.join("Product", "DataBase", "version.h")
GIT_REPO_PATH = "."  # Assuming the repository is in the current directory

def run_shell_command(command:str, cwd:str=None)->str:
    """Runs a shell command and returns the output."""
    try:
        result = subprocess.run(command, cwd=cwd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        return result.stdout.decode("utf-8").strip()
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.stderr.decode('utf-8')}")
        return None 

def create_temp_file(pre_stored_text:str)->str:
    """Creates a temporary file with the provided pre-stored text."""
    try:
        tmp_file = tempfile.mktemp() 
        with open(tmp_file, 'w') as f:
            f.write(pre_stored_text)
        return tmp_file
    except Exception as e:
        print(f"Error creating temporary file: {e}")
        return None

def get_user_input(pre_stored_text :str, prompt:str)->str:
    """
    Creates a temporary file, allows the user to edit it, and reads the content.
    :param pre_stored_text: Text to pre-fill in the temp file.
    :param prompt: Prompt to display to the user.
    :return: The content entered by the user.
    """
    print(prompt)
    tmp_file = create_temp_file(pre_stored_text)
    if not tmp_file:
        raise Exception("Failed to create temporary file.")

    # Open the file in the user's default editor
    editor = os.getenv("EDITOR", "notepad" if os.name == "nt" else "vi")
    subprocess.run([editor, tmp_file])

    # Read the user-provided input
    with open(tmp_file, 'r') as f:
        user_input = f.read().strip()

    os.remove(tmp_file)  # Clean up the temp file
    return user_input

def generate_version_file(version: str, repo_name: str) -> str:
    """Generates the version.h file with the product information."""
    if not os.path.exists(VERSION_FILE_PATH):
        open(VERSION_FILE_PATH,"w").close() # create the file
    if os.path.exists(VERSION_FILE_PATH):  
        timestamp = datetime.datetime.now(datetime.timezone.utc)
        prod_date = timestamp.strftime("%Y%m%d")
        prod_time = timestamp.strftime("%H%M%S")
        version_no = version.replace(".", "_")
        prod_ver = f"{repo_name}_{prod_date}_{prod_time}_{version_no}"

        print(f"Product version string is \"{repo_name}_{prod_date}_{prod_time}\"")

        version_content = []
        version_content.append("// @file version.h")
        version_content.append("//")
        version_content.append("// Holds Version Strings for this product.")
        version_content.append("//")
        version_content.append(f"// Use the tag {prod_ver}")
        version_content.append("// to checkout code associated with this version.")
        version_content.append("//")
        version_content.append("")
        version_content.append(f"#define PRODUCT_NAME    {repo_name}")
        version_content.append(f"#define PRODUCT_DATE    {prod_date}")
        version_content.append(f"#define PRODUCT_TIME    {prod_time}")
        version_content.append(f"#define PRODUCT_TAG     {prod_ver}")
        version_content.append(f"#define PRODUCT_VERSION {version}")


        #os.makedirs(os.path.dirname(VERSION_FILE_PATH), exist_ok=True)

        with open(VERSION_FILE_PATH, "w") as f:
            f.write("\n".join(version_content))

        print("Successfully updated version.h file")
        return prod_ver
    else :
        print("Error generating version.h file")
        sys.exit(1)

def commit_file(file_path:str, repo_name:str)->bool:
    """Commits a file to the Git repository with a user-provided commit message."""

    pre_stored_text = f"Replace this text with commit details and then save and exit the editor>\n\nProvide a commit title here for project {repo_name}\n"
    commit_message = get_user_input(pre_stored_text, "Please enter the commit message in the opened text editor.")
    if not commit_message:
        print("Commit message is empty. Exiting.")
        sys.exit(1)

    if os.path.exists(file_path):
        run_shell_command(f"git commit {file_path} -m {commit_message}", cwd=GIT_REPO_PATH)
        print(f"File {file_path} committed successfully!")
        return True
    else :
        print(f"Error during commit operation")
        return False

def push_changes()->bool:
    """Pushes the committed changes to the remote repository."""
    try:
        run_shell_command("git push", cwd=GIT_REPO_PATH)
        print("Changes pushed successfully!")
        return True
    except Exception as e:
        print(f"Error during push operation: {e}")
        return False

def tag_repo(tag_name:str, version:str, repo_name:str)->None:
    """Tags the Git repository with the provided tag name and user-provided annotation."""
    pre_stored_text = f"Annotation for tag {tag_name}\nAssociated with version {version} of product {repo_name}\r\n\r\n <Enter your tag annotation details here>\n"
    tag_comments = get_user_input(pre_stored_text, "Please enter the tag comments.")
    if not tag_comments:
        print("Tag comments are empty. Exiting.")
        sys.exit(1)

    try:
        annotation_file = create_temp_file(tag_comments)
        run_shell_command(f"git tag --annotate --file {annotation_file} {tag_name}", cwd=GIT_REPO_PATH)
        run_shell_command(f"git push origin {tag_name}", cwd=GIT_REPO_PATH)
        print(f"Tag {tag_name} pushed successfully!")
        os.remove(annotation_file)
    except Exception as e:
        print(f"Error during tagging operation: {e}")




def main()->None:
    if len(sys.argv) < 2:
        print("Usage: python script.py <version_number>")
        sys.exit(1)

    version = sys.argv[1]

    repo_name = "TM9101"
    tag_name = generate_version_file(version, repo_name)

    if not commit_file(VERSION_FILE_PATH,repo_name):
        print("Failed to commit version.h. Exiting.")
        return

    if not push_changes():
        print("Failed to push changes. Exiting.")
        return

    tag_repo(tag_name,version,repo_name)

if __name__ == "__main__":
    main()
