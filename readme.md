# How to Commit New Files to GitHub

This guide explains how to commit new files to a GitHub repository using Git.

## Prerequisites

- Git is installed on your system.
- You have a GitHub account.
- You have cloned the repository to your local machine.

## Steps to Commit New Files

1. **Navigate to the Repository**
   ```bash
   cd /path/to/your/repository
   ```

2. **Add the New Files**
   Use the `git add` command to stage the new files for commit.
   ```bash
   git add <file1> <file2>
   ```
   To add all new files:
   ```bash
   git add .
   ```

3. **Check the Status**
   Verify the files are staged for commit.
   ```bash
   git status
   ```

4. **Commit the Changes**
   Use the `git commit` command to commit the staged files. Include a meaningful commit message.
   ```bash
   git commit -m "Add new files"
   ```

5. **Push the Changes**
   Push the committed changes to the remote repository on GitHub.
   ```bash
   git push origin <branch-name>
   ```
   Replace `<branch-name>` with the name of the branch you are working on (e.g., `main` or `master`).

## Example

```bash
cd /path/to/your/repository
git add newfile.py
git status
git commit -m "Add new Python script"
git push origin main
```

## Notes

- Always pull the latest changes from the remote repository before committing new files:
  ```bash
  git pull origin <branch-name>
  ```
- Resolve any merge conflicts if they arise.

For more information, refer to the [Git documentation](https://git-scm.com/doc).
