
# README: Versioning and Git Tagging Script

## Overview
This Python script automates the process of version management, file commits, and Git tagging for a repository. It generates a version file (`version.h`), commits changes, pushes them to the remote repository, and tags the repository with version information.

## Features
- **Version File Generation:** Creates `version.h` file with metadata like Product version number, Product tag, Product date, and Product time.
- **Interactive Commit Messages:** Prompts the user to input commit messages using their default text editor.
- **Git Tagging:** Tags the repository with an annotated tag containing user-provided details.
- **Push Changes:** Automatically pushes changes and tags to the remote repository.

## Requirements
- Python 3.12
- Git installed and configured
- A writable `Product/DataBase/` directory for the `version.h` file
- Default text editor set via the `EDITOR` environment variable (e.g., `vi`, `nano`, or `notepad`)

## Installation
1. Clone the repository:
   ```bash
   git clone <repository_url>
   ```
2. Navigate to the repository directory:
   ```bash
   cd <repository_directory>
   ```
3. Ensure the required directories (`Product/DataBase/`) exist or will be created by the script.

## Usage
Run the script with the desired version number as an argument:
```bash
python script.py <version_number>
```

### Example
```bash
python script.py 1.0.0
```

### Script Workflow
1. **Version File Creation:**
   - Generates a `version.h` file in the `Product/DataBase/` directory using     `generate_version_file` function.
   - Adds metadata like product name, date, time, tag and version number.

2. **File Commit:**
   - Prompts the user to enter a commit message in a temporary file using `commit_file` function. 
   - Commits the changes to Git.

3. **Push Changes:**
   - Pushes the committed changes to the remote repository using `push_changes` function.

4. **Tagging:**
   - Prompts the user to enter a tag annotation using `tag_repo` function.
   - Creates an annotated Git tag.
   - Pushes the tag to the remote repository.

## Script Details
#### Key Functions
- `run_shell_command(command: str, cwd: str = None) -> str`
  - Executes shell commands and captures output or errors.

- `create_temp_file(pre_stored_text: str) -> str`
  - Creates a temporary file with pre-filled text.

- `get_user_input(pre_stored_text: str, prompt: str) -> str`
  - Opens the default editor for user input.

- `generate_version_file(version: str) -> str`
  - Generates the `version.h` file with version metadata.

- `commit_file(file_path: str, repo_name: str) -> bool`
  - Commits the specified file to Git with a user-provided message.

- `push_changes() -> bool`
  - Pushes committed changes to the remote repository.

- `tag_repo(tag_name: str, version: str, repo_name: str) -> None`
  - Tags the repository with an annotated tag and pushes the tag.

## Code execution flow 

![Image Description](./Screenshot%202025-01-08%20161521.png)


## Error Handling
- Handles errors during shell command execution and file operations.

## Configuration
- Modify `VERSION_FILE_PATH` to set the location of the `version.h` file.
- Update `GIT_REPO_PATH` to specify the Git repository directory if not the current directory.
- Set the `EDITOR` environment variable to specify our preferred text editor.

