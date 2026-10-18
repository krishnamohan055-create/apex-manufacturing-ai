#!/usr/bin/env bash
# Deploy ApexMfg AI to Google Cloud Run in 1 Command
# Run this inside Google Cloud Shell or any terminal with gcloud installed.

set -e

SERVICE_NAME="apexmfg-ai"
REGION="${GCP_REGION:-us-central1}"
PROJECT_ID="$(gcloud config get-value project 2>/dev/null)"

echo "=========================================================="
echo " Deploying ApexMfg AI to Google Cloud Run"
echo " Project: ${PROJECT_ID}"
echo " Region:  ${REGION}"
echo " Service: ${SERVICE_NAME}"
echo "=========================================================="

# Check if project is set
if [ -z "$PROJECT_ID" ]; then
    echo "ERROR: No active GCP project found. Run 'gcloud config set project YOUR_PROJECT_ID' first."
    exit 1
fi

# Enable required Google Cloud APIs
echo "--> Enabling required GCP APIs (Cloud Run, Artifact Registry, Firestore)..."
gcloud services enable run.googleapis.com \
    artifactregistry.googleapis.com \
    firestore.googleapis.com \
    cloudbuild.googleapis.com

# Deploy directly from source
echo "--> Building and deploying container to Cloud Run..."
gcloud run deploy "$SERVICE_NAME" \
    --source . \
    --platform managed \
    --region "$REGION" \
    --allow-unauthenticated \
    --port 8080 \
    --memory 1Gi \
    --cpu 1 \
    --min-instances 0 \
    --max-instances 5 \
    --set-env-vars="GCP_PROJECT=${PROJECT_ID}"

echo ""
echo "=========================================================="
echo " DEPLOYMENT SUCCESSFUL!"
echo " Copy the Service URL above and paste it into your"
echo " Hackathon 'Prototype Link Deployed on GCP or Cloud run' field!"
echo "=========================================================="
