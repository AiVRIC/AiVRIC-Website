# Helper script to run Vercel commands in Docker on Windows

param(
    [Parameter(Position=0, ValueFromRemainingArguments=$true)]
    [string[]]$Arguments
)

docker run --rm -it `
  -v "${pwd}:/app" `
  -v "${env:USERPROFILE}/.vercel:/root/.vercel" `
  -w /app `
  --env VERCEL_TOKEN="${env:VERCEL_TOKEN}" `
  --env VERCEL_ORG_ID="${env:VERCEL_ORG_ID}" `
  --env VERCEL_PROJECT_ID="${env:VERCEL_PROJECT_ID}" `
  aivric-vercel:latest `
  vercel $Arguments