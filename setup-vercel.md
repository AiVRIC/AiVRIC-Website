# Vercel Setup Instructions

## Prerequisites
- Docker Desktop running
- GitHub CLI (`gh`) configured
- Vercel account

## Setup Steps

### 1. Get Vercel Token
1. Go to https://vercel.com/account/tokens
2. Click "Create Token"
3. Name it "AIVric Preview Deploy"
4. Copy the token

### 2. Link Vercel Project (Using Docker)

Run this command to link your project to Vercel:
```bash
# Windows Command Prompt or PowerShell
vercel-docker.bat link
```

When prompted:
- Choose "Create a new project"
- Enter a project name (e.g., "aivric-preview")
- Select your Vercel team/account
- Confirm the settings

This will create a `.vercel` folder with your project configuration.

### 3. Get Project and Org IDs

After linking, check the `.vercel/project.json` file:
```bash
type .vercel\project.json
```

You'll see:
- `orgId`: Your VERCEL_ORG_ID
- `projectId`: Your VERCEL_PROJECT_ID

### 4. Add Secrets to GitHub

Run these commands (replace with your actual values):

```bash
# Add Vercel Token
gh secret set VERCEL_TOKEN

# Add Org ID (from .vercel/project.json)
gh secret set VERCEL_ORG_ID

# Add Project ID (from .vercel/project.json)
gh secret set VERCEL_PROJECT_ID
```

### 5. Configure Password Protection

The password protection is already configured in `vercel.json`.
To set/change the password:

1. Go to your Vercel dashboard
2. Select your project
3. Go to Settings → Environment Variables
4. Add `VERCEL_AUTHENTICATION_PASSWORD` with your desired password
5. This password will be required to access the preview site

### 6. Deploy

After setup, push to the `preview` branch to trigger automatic deployment:

```bash
git checkout -b preview
git push -u origin preview
```

## Manual Deployment (Using Docker)

To deploy manually:
```bash
# Windows
vercel-docker.bat deploy --prod
```

## Troubleshooting

If you encounter permission issues:
1. Make sure Docker Desktop is running
2. Ensure the `.vercel` folder exists in your user directory
3. Check that all environment variables are set correctly