# CLAUDE.md - AiVRIC Website Repository

This file provides guidance to Claude Code (claude.ai/code) when working with this repository.

## IMPORTANT: Branch Strategy

This repository uses a **specific branch strategy**. You are currently on the **`main`** branch, which contains **ONLY documentation**.

### Branch Structure

- **`main`** (THIS BRANCH - Documentation Only)
  - Contains: README.md, CLAUDE.md, .gitignore, .github/
  - Purpose: Repository documentation and contribution guidelines
  - **NO website files should be on this branch**

- **`gh-pages`** (Website Content Branch)
  - Contains: ALL website HTML, CSS, JavaScript, assets
  - Purpose: Deployed to http://aivric.com via GitHub Pages
  - **ALL website development work happens here**

## If You Need to Work on Website Files

**STOP!** You are on the wrong branch. Follow these steps:

1. **Switch to the gh-pages branch**:
   ```bash
   git checkout gh-pages
   ```

2. **Read the CLAUDE.md file on gh-pages** for website-specific instructions:
   ```bash
   # After switching to gh-pages
   cat CLAUDE.md
   ```

3. **Work on website files** (HTML, CSS, JS, images, etc.) on the `gh-pages` branch

4. **Submit pull requests to `gh-pages`**, NOT to main

## What Can You Do on the Main Branch?

The `main` branch is ONLY for:

- Updating README.md (contribution guidelines, project overview)
- Updating this CLAUDE.md file (branch strategy, documentation)
- Updating .gitignore
- Managing .github/ workflows (if needed)

## Common Scenarios

### Scenario: User asks to update website content/HTML/CSS/images

**Action**: Inform the user you need to switch to `gh-pages` branch, then:
```bash
cd "AiVRIC WebSite"
git checkout gh-pages
```

### Scenario: User asks to update README or contribution guidelines

**Action**: You're on the correct branch (main). Proceed with updates.

### Scenario: User asks to work on website but you're not sure which branch

**Action**: Default to `gh-pages` for ANY website-related work.

## Repository Context

- **Project**: AiVRIC Platform - Enterprise security operations platform
- **Website**: http://aivric.com
- **Repository**: https://github.com/AiVRIC/AiVRIC-Website
- **Deployment**: GitHub Pages serves from `gh-pages` branch
- **Parent Repo**: Part of AiVRIC-Platform meta-repository (submodule)

## Quick Reference

```bash
# Check current branch
git branch --show-current

# Switch to gh-pages for website work
git checkout gh-pages

# Switch to main for documentation updates
git checkout main

# List all branches
git branch -a
```

## Related Documentation

- **README.md** (on this branch): Full contribution guidelines
- **README.md on gh-pages**: Website-specific documentation
- **CLAUDE.md on gh-pages**: Website development guidelines
- **AiVRIC Platform CLAUDE.md**: Parent repository context

---

**Remember**:
- Main branch = Documentation only
- gh-pages branch = All website files
- When in doubt, use `gh-pages` for website work!
