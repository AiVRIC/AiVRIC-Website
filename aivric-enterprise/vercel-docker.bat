@echo off
REM Helper script to run Vercel commands in Docker on Windows

docker run --rm -it ^
  -v "C:\Repos\AIVric://app" ^
  -v "%USERPROFILE%\.vercel://root/.vercel" ^
  -w "//app" ^
  --env VERCEL_TOKEN=%VERCEL_TOKEN% ^
  --env VERCEL_ORG_ID=%VERCEL_ORG_ID% ^
  --env VERCEL_PROJECT_ID=%VERCEL_PROJECT_ID% ^
  aivric-vercel:latest ^
  vercel %*