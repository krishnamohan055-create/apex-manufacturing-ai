@echo off
REM Deploy ApexMfg AI to Google Cloud Run (Windows)
echo ==========================================================
echo  Deploying ApexMfg AI to Google Cloud Run
echo ==========================================================

set SERVICE_NAME=apexmfg-ai
set REGION=us-central1

echo Enabling Google Cloud APIs...
call gcloud services enable run.googleapis.com artifactregistry.googleapis.com firestore.googleapis.com cloudbuild.googleapis.com

echo Building and deploying container to Cloud Run...
call gcloud run deploy %SERVICE_NAME% --source . --platform managed --region %REGION% --allow-unauthenticated --port 8080 --memory 1Gi --cpu 1

echo ==========================================================
echo  DEPLOYMENT COMPLETE!
echo  Copy the HTTPS Service URL and paste it into the Hackathon submission form.
echo ==========================================================
pause
