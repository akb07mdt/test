import subprocess
import os
import tempfile
import re
 
# Paths to scripts and files
VERSION_SCRIPT_PATH = "version.sh"
VERSION_FILE_PATH = os.path.join("Product", "DataBase", "version.h")
GIT_REPO_PATH = "."  # Assuming the repository is in the current directory
 
def run_shell_command(command, cwd=None):
    """Runs a shell command and returns the output."""
    try:
        result = subprocess.run(command, cwd=cwd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        return result.stdout.decode("utf-8").strip()
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.stderr.decode('utf-8')}")
        return None
 
def generate_version_file(version):
    """Executes the version.sh script to generate the version.h file."""
    print(f"Generating version.h by executing version.sh with version: {version}...")
    run_shell_command(f"bash {VERSION_SCRIPT_PATH} {version}")
 
def extract_version_and_tag(version_file_path):
    """Extracts the PRODUCT_TAG and PRODUCT_VERSION from version.h using regex."""
    try:
        with open(version_file_path, 'r') as f:
            content = f.read()
       
        # Use regex to extract the tag and version
        tag_match = re.search(r'#define PRODUCT_TAG\s+"([^"]+)"', content)
        version_match = re.search(r'#define PRODUCT_VERSION\s+"([^"]+)"', content)
 
        tag_name = tag_match.group(1) if tag_match else None
        version = version_match.group(1) if version_match else None
 
        return tag_name, version
    except Exception as e:
        print(f"Error reading {version_file_path}: {e}")
        return None, None
 
def create_tag_annotation(tag_name, version, repo_name, comments):
    """Creates a temporary file and fills it with the tag annotation."""
    try:
        tmp_file = tempfile.mktemp()
        with open(tmp_file, 'w') as f:
            f.write(f"Annotation for tag {tag_name}\n")
            f.write(f"Version: {version}\n")
            f.write(f"Repository: {repo_name}\n\n")
            f.write(comments)
        return tmp_file
    except Exception as e:
        print(f"Error creating temporary file for tag annotation: {e}")
        return None
 
def tag_repo(tmp_file, tag_name):
    """Tags the Git repository with the provided tag name and annotation."""
    try:
        subprocess.run(["git", "tag", "--annotate", "--file", tmp_file, tag_name], check=True, cwd=GIT_REPO_PATH)
        subprocess.run(["git", "push", "origin", tag_name], check=True, cwd=GIT_REPO_PATH)
        print(f"Tag {tag_name} pushed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error during tagging operation: {e}")
 
def main():
    # Step 1: Prompt the user for version and comments
    print("Opening a temporary file for user input...")
    tmp_file = tempfile.mktemp()
    with open(tmp_file, 'w') as f:
        f.write("VERSION= Replace this text with your version number...\n")
        f.write("COMMENTS= Replace this text with your comments...\n")
   
    # Open the file in the default editor for user input
    editor = os.getenv("EDITOR", "notepad" if os.name == "nt" else "vi")
    subprocess.run([editor, tmp_file])
 
    # Read the user input
    with open(tmp_file, 'r') as f:
        lines = f.readlines()
   
    # Extract version and comments
    version = None
    comments = None
    for line in lines:
        if line.startswith("VERSION="):
            version = line.split("=", 1)[1].strip()
        elif line.startswith("COMMENTS="):
            comments = line.split("=", 1)[1].strip()
   
    # Clean up the temporary file
    os.remove(tmp_file)
 
    if not version or not comments:
        print("Error: Version or comments not provided.")
        return
 
    # Step 2: Generate version.h
    generate_version_file(version)
 
    # Step 3: Extract tag and version from version.h
    tag_name, extracted_version = extract_version_and_tag(VERSION_FILE_PATH)
    if not tag_name or not extracted_version:
        print("Failed to extract tag name or version from version.h.")
        return
 
    print(f"Tag Name: {tag_name}")
    print(f"Version: {extracted_version}")
 
    # Step 4: Create the tag annotation
    repo_name = "TM91"  # Hardcoded repository name
    annotation_file = create_tag_annotation(tag_name, extracted_version, repo_name, comments)
    if not annotation_file:
        print("Failed to create tag annotation file.")
        return
 
    # Step 5: Tag the repository
    tag_repo(annotation_file, tag_name)
 
    # Clean up the annotation file
    os.remove(annotation_file)
    print("Annotation file deleted.")
 
if __name__ == "__main__":
    main()




 ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 
import subprocess
import os
import tempfile
import re
import sys

# Paths to scripts and files
VERSION_SCRIPT_PATH = "version.sh"
VERSION_FILE_PATH = os.path.join("Product", "DataBase", "version.h")
GIT_REPO_PATH = "."  # Assuming the repository is in the current directory

def run_shell_command(command, cwd=None):
    """Runs a shell command and returns the output."""
    try:
        result = subprocess.run(command, cwd=cwd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        return result.stdout.decode("utf-8").strip()
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.stderr.decode('utf-8')}")
        return None

def generate_version_file(version):
    """Executes the version.sh script to generate the version.h file."""
    print(f"Generating version.h with version: {version}...")
    run_shell_command(f"bash {VERSION_SCRIPT_PATH} {version}")

def extract_version_and_tag(version_file_path):
    """Extracts the PRODUCT_TAG and PRODUCT_VERSION from version.h using regex."""
    try:
        with open(version_file_path, 'r') as f:
            content = f.read()
        
        # Use regex to extract the tag and version
        tag_match = re.search(r'#define PRODUCT_TAG\s+"([^"]+)"', content)
        version_match = re.search(r'#define PRODUCT_VERSION\s+"([^"]+)"', content)

        tag_name = tag_match.group(1) if tag_match else None
        version = version_match.group(1) if version_match else None

        return tag_name, version
    except Exception as e:
        print(f"Error reading {version_file_path}: {e}")
        return None, None

def add_commit_push(file_path):
    """Adds, commits, and pushes a file to the Git repository."""
    try:
        # Add the file to staging
        run_shell_command(f"git add {file_path}", cwd=GIT_REPO_PATH)

        # Create a temporary file for commit message
        tmp_file = tempfile.mktemp()
        repo_name = "TM91"  # Replace with your repository name
        with open(tmp_file, 'w') as f:
            f.write("<Replace this text with commit details and then save and exit the editor>\n\n")
            f.write(f"Provide a commit title here for project {repo_name}\n")
           
        # Open the file in the default editor for user input
        editor = os.getenv("EDITOR", "notepad" if os.name == "nt" else "vi")
        subprocess.run([editor, tmp_file])

        # Read the user-provided commit message
        with open(tmp_file, 'r') as f:
            comments = f.read().strip()

        # Commit the changes
        run_shell_command(f"git commit -m \"{comments}\"", cwd=GIT_REPO_PATH)

        # Push the commit
        run_shell_command("git push", cwd=GIT_REPO_PATH)
        print("version.h committed and pushed successfully!")
        return True
    except Exception as e:
        print(f"Error during add/commit/push operation: {e}")
        return False

def tag_repo(tag_name, version, repo_name, comments):
    """Tags the Git repository with the provided tag name and annotation."""
    try:
        # Create the tag annotation in a temporary file
        annotation_file = tempfile.mktemp()
        with open(annotation_file, 'w') as f:
            f.write(comments)

        # Create and push the tag
        run_shell_command(f"git tag --annotate --file {annotation_file} {tag_name}", cwd=GIT_REPO_PATH)
        run_shell_command(f"git push origin {tag_name}", cwd=GIT_REPO_PATH)
        print(f"Tag {tag_name} pushed successfully!")
        os.remove(annotation_file)
    except Exception as e:
        print(f"Error during tagging operation: {e}")

def main():
    # Check if version number is provided as a command-line argument
    if len(sys.argv) < 2:
        print("Usage: python script.py <version_number>")
        sys.exit(1)
    
    version = sys.argv[1]
    repo_name = "TM91"  # Replace with your repository name

    # Step 1: Generate version.h
    generate_version_file(version)

    # Step 2: Add, commit, and push version.h
    if not add_commit_push(VERSION_FILE_PATH):
        print("Failed to commit version.h. Exiting.")
        return

    # Step 3: Extract tag name and version
    tag_name, extracted_version = extract_version_and_tag(VERSION_FILE_PATH)
    if not tag_name or not extracted_version:
        print("Failed to extract tag name or version from version.h. Exiting.")
        return

    print(f"Tag Name: {tag_name}")
    print(f"Version: {extracted_version}")

    # Step 4: Perform tagging
    try:
        tmp_file = tempfile.mktemp()
        with open(tmp_file, 'w') as f:
            f.write(f"Annotation for tag {tag_name}\r\n")
            f.write(f"Associated with version {extracted_version} of product {repo_name}\r\n\r\n")
            f.write("<Provide tag annotation details and then save and exit the editor>\n")

        # Open the temporary file in the default editor for user input
        editor = os.getenv("EDITOR", "notepad" if os.name == "nt" else "vi")
        subprocess.run([editor, tmp_file])

        # Read the user-provided comments
        with open(tmp_file, 'r') as f:
            comments = f.read().strip()

        os.remove(tmp_file)

        if not comments:
            print("Tag annotation comments not provided. Exiting.")
            return

        tag_repo(tag_name, extracted_version, repo_name, comments)
    except Exception as e:
        print(f"Error handling temporary file for tagging: {e}")

if __name__ == "__main__":
    main()











--------------------------------------------------------------------------------------------------------------------------------------------------

import subprocess
import os
import tempfile
import re
import sys
import datetime

# Paths to scripts and files
VERSION_FILE_PATH = os.path.join("Product", "DataBase", "version.h")
GIT_REPO_PATH = "."  # Assuming the repository is in the current directory

def run_shell_command(command, cwd=None):
    """Runs a shell command and returns the output."""
    try:
        result = subprocess.run(command, cwd=cwd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        return result.stdout.decode("utf-8").strip()
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.stderr.decode('utf-8')}")
        return None

def generate_version_file(version:str)->str:
    """
    Generates the version.h file with the product information.
    This replaces the functionality of the version.sh script.
    """
    try:
        # Generate timestamp and product details
        timestamp = datetime.datetime.now(datetime.timezone.utc)
        repo_name = "TM9101"  # Replace with your repository name
        prod_date = timestamp.strftime("%Y%m%d")
        prod_time = timestamp.strftime("%H%M%S")
        version_no = version.replace(".", "_")
        prod_ver = f"{repo_name}_{prod_date}_{prod_time}_{version_no}"

        # Print product version string (informational)
        print(f"Product version string is \"{repo_name}_{prod_date}_{prod_time}\"")

        # Generate version.h content
        version_content = []
        version_content.append("// @file version.h")
        version_content.append("// @file version.h")
        version_content.append("// @file version.h")
        version_content.append("// @file version.h")

        version_content = f"""\
// @file version.h
//
// Holds Version Strings for this product.
//
// Use the tag {prod_ver}
//   to checkout code associated with this version.
//

#define PRODUCT_NAME    "{repo_name}"
#define PRODUCT_DATE    "{prod_date}"
#define PRODUCT_TIME    "{prod_time}"
#define PRODUCT_TAG     "{prod_ver}"
#define PRODUCT_VERSION "{version}"

"""

        # Ensure the directory exists
        os.makedirs(os.path.dirname(VERSION_FILE_PATH), exist_ok=True)

        # Write the content to version.h
        with open(VERSION_FILE_PATH, "w") as f:
            f.write(version_content)
        
        print("Successfully updated version.h file")
        #print("Remember to rebuild before committing!")
        
        return prod_ver  # Return the tag name for further use
    except Exception as e:
        print(f"Error generating version.h file: {e}")
        sys.exit(1)

def extract_version_and_tag(version_file_path):
    """Extracts the PRODUCT_TAG and PRODUCT_VERSION from version.h using regex."""
    try:
        with open(version_file_path, 'r') as f:
            content = f.read()
        
        # Use regex to extract the tag and version
        tag_match = re.search(r'#define PRODUCT_TAG\s+"([^"]+)"', content)
        version_match = re.search(r'#define PRODUCT_VERSION\s+"([^"]+)"', content)

        tag_name = tag_match.group(1) if tag_match else None
        version = version_match.group(1) if version_match else None

        return tag_name, version
    except Exception as e:
        print(f"Error reading {version_file_path}: {e}")
        return None, None

def add_commit_push(file_path):
    """Adds, commits, and pushes a file to the Git repository."""
    try:
        # Add the file to staging
        run_shell_command(f"git add {file_path}", cwd=GIT_REPO_PATH)

        # Create a temporary file for commit message
        tmp_file = tempfile.mktemp()
        repo_name = "TM91"  # Replace with your repository name
        with open(tmp_file, 'w') as f:
            f.write("<Replace this text with commit details and then save and exit the editor>\n\n")
            f.write(f"Provide a commit title here for project {repo_name}\n")

        # Open the file in the default editor for user input
        editor = os.getenv("EDITOR", "notepad" if os.name == "nt" else "vi")
        subprocess.run([editor, tmp_file])

        # Read the user-provided commit message
        with open(tmp_file, 'r') as f:
            comments = f.read().strip()

        # Commit the changes
        run_shell_command(f"git commit -m \"{comments}\"", cwd=GIT_REPO_PATH)

        # Push the commit
        run_shell_command("git push", cwd=GIT_REPO_PATH)
        print("version.h committed and pushed successfully!")
        return True
    except Exception as e:
        print(f"Error during add/commit/push operation: {e}")
        return False

def tag_repo(tag_name, comments):
    """Tags the Git repository with the provided tag name and annotation."""
    try:
        # Create the tag annotation in a temporary file
        annotation_file = tempfile.mktemp()
        with open(annotation_file, 'w') as f:
            f.write(comments)

        # Create and push the tag
        run_shell_command(f"git tag --annotate --file {annotation_file} {tag_name}", cwd=GIT_REPO_PATH)
        run_shell_command(f"git push origin {tag_name}", cwd=GIT_REPO_PATH)
        print(f"Tag {tag_name} pushed successfully!")
        os.remove(annotation_file)
    except Exception as e:
        print(f"Error during tagging operation: {e}")

def main():
    # Check if version number is provided as a command-line argument
    if len(sys.argv) < 2:
        print("Usage: python script.py <version_number>")
        sys.exit(1)
    
    version = sys.argv[1]
    repo_name = "TM91"  # Replace with your repository name

    # Step 1: Generate version.h
    tag_name = generate_version_file(version)

    # Step 2: Add, commit, and push version.h
    if not add_commit_push(VERSION_FILE_PATH):
        print("Failed to commit version.h. Exiting.")
        return

    # Step 3: Extract tag name and version
    tag_name, extracted_version = extract_version_and_tag(VERSION_FILE_PATH)
    if not tag_name or not extracted_version:
        print("Failed to extract tag name or version from version.h. Exiting.")
        return

    print(f"Tag Name: {tag_name}")
    print(f"Version: {extracted_version}")

    # Step 4: Perform tagging
    try:
        tmp_file = tempfile.mktemp()
        with open(tmp_file, 'w') as f:
            f.write(f"Annotation for tag {tag_name}\n")
            f.write(f"Associated with version {extracted_version} of product {repo_name}\r\n\r\n")
            f.write("<Provide tag annotation details and then save and exit the editor>\n")

        # Open the temporary file in the default editor for user input
        editor = os.getenv("EDITOR", "notepad" if os.name == "nt" else "vi")
        subprocess.run([editor, tmp_file])

        # Read the user-provided comments
        with open(tmp_file, 'r') as f:
            comments = f.read().strip()

        os.remove(tmp_file)

        if not comments:
            print("Tag annotation comments not provided. Exiting.")
            return

        tag_repo(tag_name, comments)
    except Exception as e:
        print(f"Error handling temporary file for tagging: {e}")

if __name__ == "__main__":
    main()









-----------------------
def extract_version_and_tag(version_file_path):
    """Extracts the PRODUCT_TAG and PRODUCT_VERSION from version.h using regex."""
    try:
        with open(version_file_path, 'r') as f:
            content = f.read()

        tag_match = re.search(r'#define PRODUCT_TAG\s+"([^"]+)"', content)
        version_match = re.search(r'#define PRODUCT_VERSION\s+"([^"]+)"', content)

        tag_name = tag_match.group(1) if tag_match else None
        version = version_match.group(1) if version_match else None

        return tag_name, version
    except Exception as e:
        print(f"Error reading {version_file_path}: {e}")
        return None, None


----------------------------------------------------------------------------------------------------
import subprocess
import os
import tempfile
import re
import sys
import datetime

# Paths to scripts and files
VERSION_FILE_PATH = os.path.join("Product", "DataBase", "version.h")
GIT_REPO_PATH = "."  # Assuming the repository is in the current directory

def run_shell_command(command, cwd=None):
    """Runs a shell command and returns the output."""
    try:
        result = subprocess.run(command, cwd=cwd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        return result.stdout.decode("utf-8").strip()
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.stderr.decode('utf-8')}")
        return None

def create_temp_file(pre_stored_text):
    """Creates a temporary file with the provided pre-stored text."""
    try:
        tmp_file = tempfile.mktemp()
        with open(tmp_file, 'w') as f:
            f.write(pre_stored_text)
        return tmp_file
    except Exception as e:
        print(f"Error creating temporary file: {e}")
        return None

def get_user_input(pre_stored_text, prompt):
    """
    Creates a temporary file, allows the user to edit it, and reads the content.
    :param pre_stored_text: Text to pre-fill in the temp file.
    :param prompt: Prompt to display to the user.
    :return: The content entered by the user.
    """
    try:
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
    except Exception as e:
        print(f"Error getting user input: {e}")
        sys.exit(1)

def generate_version_file(version: str) -> str:
    """Generates the version.h file with the product information."""
    try:
        timestamp = datetime.datetime.now(datetime.timezone.utc)
        repo_name = "TM9101"
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



        os.makedirs(os.path.dirname(VERSION_FILE_PATH), exist_ok=True)

        with open(VERSION_FILE_PATH, "w") as f:
            f.write("\n".join(version_content))

        print("Successfully updated version.h file")
        return prod_ver
    except Exception as e:
        print(f"Error generating version.h file: {e}")
        sys.exit(1)

def commit_file(file_path,repo_name):
    """Commits a file to the Git repository with a user-provided commit message."""

    pre_stored_text = f"Replace this text with commit details and then save and exit the editor>\n\nProvide a commit title here for project {repo_name}\n"
    commit_message = get_user_input(pre_stored_text, "Please enter the commit message in the opened text editor.")
    if not commit_message:
        print("Commit message is empty. Exiting.")
        sys.exit(1)
    # try:
    #     run_shell_command(f"git commit {file_path} -m \"{commit_message}\"", cwd=GIT_REPO_PATH)
    #     print(f"File {file_path} committed successfully!")
    #     return True
    # except Exception as e:
    #     print(f"Error during commit operation: {e}")
    #     return False
    if os.path.exists(file_path):
        run_shell_command(f"git commit {file_path} -m \"{commit_message}\"", cwd=GIT_REPO_PATH)
        print(f"File {file_path} committed successfully!")
        return True
    else :
        print(f"Error during commit operation")
        return False

def push_changes():
    """Pushes the committed changes to the remote repository."""
    try:
        run_shell_command("git push", cwd=GIT_REPO_PATH)
        print("Changes pushed successfully!")
        return True
    except Exception as e:
        print(f"Error during push operation: {e}")
        return False

def tag_repo(tag_name,version,repo_name):
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


def main():
    if len(sys.argv) < 2:
        print("Usage: python script.py <version_number>")
        sys.exit(1)

    version = sys.argv[1]

    tag_name = generate_version_file(version)
    repo_name = "TM9101"
    if not commit_file(VERSION_FILE_PATH,repo_name):
        print("Failed to commit version.h. Exiting.")
        return

    if not push_changes():
        print("Failed to push changes. Exiting.")
        return

    tag_repo(tag_name,version,repo_name)

if __name__ == "__main__":
    main()

