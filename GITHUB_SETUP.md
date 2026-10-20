# Publish Clear Flow to GitHub

This source archive is prepared for a new Git repository. It intentionally does not include a `.git` directory or credentials.

## 1. Create an empty GitHub repository

On GitHub, create a repository named `Clear-Flow`. For the simplest first push, do not initialize it with a README, license, or `.gitignore` because those files already exist in this project.

## 2. Initialize and push from the project directory

Run these commands in PowerShell from the extracted `Clear-Flow` directory. Replace the example remote URL with the URL of your repository.

```powershell
git init -b main
git add .
git status
git commit -m "Initial Clear Flow release"
git remote add origin https://github.com/YOUR-USERNAME/Clear-Flow.git
git push -u origin main
```

Review `git status` before committing. The `.gitignore` excludes virtual environments, local secrets, caches, generated training outputs, and build artifacts while keeping source files and legitimate data files eligible for version control.

## 3. After pushing

- Check the **Actions** tab for package-build, test, and pre-commit workflows.
- The SUMO-based integration tests require SUMO and `SUMO_HOME`; see `README.md` and `CONTRIBUTING.md`.
- The documentation workflow publishes to the `gh-pages` branch. Enable GitHub Pages for that branch if you want the site published.
- The package-build workflow does not publish to PyPI automatically. Configure a trusted publisher only when you are ready to distribute a package.
