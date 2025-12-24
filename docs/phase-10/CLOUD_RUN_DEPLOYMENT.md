# Cloud Run Deployment Guide

This guide walks through deploying the cloud producer to Google Cloud Run with Cloud Scheduler.

---

## Prerequisites

1. ✅ GCP project created (`today-in-emojis`)
2. ✅ Cloud Storage bucket created (`today-in-emojis-assets`)
3. ✅ Firestore database created
4. ✅ Service account created with credentials
5. ✅ Local testing passed

---

## Architecture

```
Cloud Scheduler (6 triggers/day)
    ↓
Cloud Run Job (executes on trigger)
    ↓
Cloud Producer (Python + TypeScript)
    ↓
Cloud Storage (images) + Firestore (editions)
```

---

## Step 1: Enable Required APIs

```bash
# Set your project
gcloud config set project today-in-emojis

# Enable required APIs
gcloud services enable \
    cloudbuild.googleapis.com \
    run.googleapis.com \
    cloudscheduler.googleapis.com \
    artifactregistry.googleapis.com
```

---

## Step 2: Create Artifact Registry Repository

This is where your Docker images will be stored.

```bash
# Create repository
gcloud artifacts repositories create today-in-emojis \
    --repository-format=docker \
    --location=us-central1 \
    --description="Docker images for Today in Emojis cloud producer"

# Verify creation
gcloud artifacts repositories list --location=us-central1
```

---

## Step 3: Build and Push Docker Image

### Option A: Build Locally and Push

```bash
# Configure Docker to use Artifact Registry
gcloud auth configure-docker us-central1-docker.pkg.dev

# Build the image
docker build -f Dockerfile.cloud-producer \
    -t us-central1-docker.pkg.dev/today-in-emojis/today-in-emojis/cloud-producer:latest \
    .

# Push to Artifact Registry
docker push us-central1-docker.pkg.dev/today-in-emojis/today-in-emojis/cloud-producer:latest
```

### Option B: Build in Cloud (Recommended - no local Docker needed)

```bash
# Build using Cloud Build
gcloud builds submit \
    --tag us-central1-docker.pkg.dev/today-in-emojis/today-in-emojis/cloud-producer:latest \
    --timeout=20m \
    -f Dockerfile.cloud-producer \
    .
```

**Note:** Cloud Build is recommended because:
- No need for Docker Desktop locally
- Builds in the cloud (faster, consistent)
- Automatically pushed to Artifact Registry

---

## Step 4: Store Secrets in Secret Manager

Your OpenAI API key needs to be stored securely.

```bash
# Enable Secret Manager API
gcloud services enable secretmanager.googleapis.com

# Create secret for OpenAI API key
echo -n "your-actual-openai-api-key-here" | \
    gcloud secrets create openai-api-key \
    --data-file=- \
    --replication-policy="automatic"

# Grant service account access to the secret
gcloud secrets add-iam-policy-binding openai-api-key \
    --member="serviceAccount:today-in-emojis-producer@today-in-emojis.iam.gserviceaccount.com" \
    --role="roles/secretmanager.secretAccessor"
```

---

## Step 5: Create Cloud Run Job

Cloud Run Jobs run to completion and exit (perfect for our producer).

```bash
# Create the job
gcloud run jobs create cloud-producer \
    --image=us-central1-docker.pkg.dev/today-in-emojis/today-in-emojis/cloud-producer:latest \
    --region=us-central1 \
    --service-account=today-in-emojis-producer@today-in-emojis.iam.gserviceaccount.com \
    --set-env-vars="GOOGLE_CLOUD_PROJECT=today-in-emojis,CLOUD_STORAGE_BUCKET=today-in-emojis-assets,CLOUD_STORAGE_REGION=us-central1,FIRESTORE_DATABASE=(default),FIRESTORE_COLLECTION=editions,CLOUD_DRY_RUN=false,CLOUD_MODE=parallel,ASSET_RETENTION_DAYS=30,ESSENCE_CADENCE_N=6,ESSENCE_TEMPERATURE=0.7,ESSENCE_FALLBACK_EMOJI=🌍" \
    --set-secrets="OPENAI_API_KEY=openai-api-key:latest" \
    --max-retries=1 \
    --task-timeout=10m \
    --memory=2Gi \
    --cpu=2
```

**Explanation:**
- `--image`: Docker image from Artifact Registry
- `--service-account`: Uses the service account we created
- `--set-env-vars`: Environment variables (non-secret)
- `--set-secrets`: Mounts secrets from Secret Manager
- `--max-retries=1`: Retry once if it fails
- `--task-timeout=10m`: Max 10 minutes per run
- `--memory=2Gi`: 2GB RAM (needed for Playwright)
- `--cpu=2`: 2 vCPUs (speeds up image generation)

---

## Step 6: Test Manual Execution

Before setting up the schedule, test the job manually:

```bash
# Execute the job
gcloud run jobs execute cloud-producer --region=us-central1

# Watch logs
gcloud run jobs executions logs tail \
    --region=us-central1 \
    --job=cloud-producer
```

Check:
1. Job completes successfully (exit code 0)
2. Image uploaded to Cloud Storage
3. Edition written to Firestore
4. No errors in logs

---

## Step 7: Create Cloud Scheduler Jobs (6x per day)

Now set up the automated schedule - 6 triggers per day.

### Normal Posts (5x/day)

```bash
# Post 1: Midnight UTC
gcloud scheduler jobs create http cloud-producer-00 \
    --location=us-central1 \
    --schedule="0 0 * * *" \
    --time-zone="UTC" \
    --uri="https://us-central1-run.googleapis.com/apis/run.googleapis.com/v1/namespaces/today-in-emojis/jobs/cloud-producer:run" \
    --http-method=POST \
    --oauth-service-account-email=today-in-emojis-producer@today-in-emojis.iam.gserviceaccount.com

# Post 2: 4am UTC
gcloud scheduler jobs create http cloud-producer-04 \
    --location=us-central1 \
    --schedule="0 4 * * *" \
    --time-zone="UTC" \
    --uri="https://us-central1-run.googleapis.com/apis/run.googleapis.com/v1/namespaces/today-in-emojis/jobs/cloud-producer:run" \
    --http-method=POST \
    --oauth-service-account-email=today-in-emojis-producer@today-in-emojis.iam.gserviceaccount.com

# Post 3: 8am UTC
gcloud scheduler jobs create http cloud-producer-08 \
    --location=us-central1 \
    --schedule="0 8 * * *" \
    --time-zone="UTC" \
    --uri="https://us-central1-run.googleapis.com/apis/run.googleapis.com/v1/namespaces/today-in-emojis/jobs/cloud-producer:run" \
    --http-method=POST \
    --oauth-service-account-email=today-in-emojis-producer@today-in-emojis.iam.gserviceaccount.com

# Post 4: Noon UTC
gcloud scheduler jobs create http cloud-producer-12 \
    --location=us-central1 \
    --schedule="0 12 * * *" \
    --time-zone="UTC" \
    --uri="https://us-central1-run.googleapis.com/apis/run.googleapis.com/v1/namespaces/today-in-emojis/jobs/cloud-producer:run" \
    --http-method=POST \
    --oauth-service-account-email=today-in-emojis-producer@today-in-emojis.iam.gserviceaccount.com

# Post 5: 4pm UTC
gcloud scheduler jobs create http cloud-producer-16 \
    --location=us-central1 \
    --schedule="0 16 * * *" \
    --time-zone="UTC" \
    --uri="https://us-central1-run.googleapis.com/apis/run.googleapis.com/v1/namespaces/today-in-emojis/jobs/cloud-producer:run" \
    --http-method=POST \
    --oauth-service-account-email=today-in-emojis-producer@today-in-emojis.iam.gserviceaccount.com

# Post 6: 8pm UTC (Essence post - 6th of the day)
gcloud scheduler jobs create http cloud-producer-20 \
    --location=us-central1 \
    --schedule="0 20 * * *" \
    --time-zone="UTC" \
    --uri="https://us-central1-run.googleapis.com/apis/run.googleapis.com/v1/namespaces/today-in-emojis/jobs/cloud-producer:run" \
    --http-method=POST \
    --oauth-service-account-email=today-in-emojis-producer@today-in-emojis.iam.gserviceaccount.com
```

---

## Step 8: Test Scheduler

Trigger one scheduler job manually to test:

```bash
# Trigger the midnight job
gcloud scheduler jobs run cloud-producer-00 --location=us-central1

# Watch logs
gcloud run jobs executions logs tail \
    --region=us-central1 \
    --job=cloud-producer
```

---

## Step 9: Monitor

### View Scheduled Jobs

```bash
gcloud scheduler jobs list --location=us-central1
```

### View Job Executions

```bash
gcloud run jobs executions list --job=cloud-producer --region=us-central1
```

### View Logs

```bash
# Real-time logs
gcloud run jobs executions logs tail \
    --region=us-central1 \
    --job=cloud-producer

# Logs in Cloud Console
# https://console.cloud.google.com/logs/query
```

---

## Updating the Job

When you make code changes:

```bash
# 1. Rebuild image
gcloud builds submit \
    --tag us-central1-docker.pkg.dev/today-in-emojis/today-in-emojis/cloud-producer:latest \
    -f Dockerfile.cloud-producer \
    .

# 2. Update the job to use new image
gcloud run jobs update cloud-producer \
    --region=us-central1 \
    --image=us-central1-docker.pkg.dev/today-in-emojis/today-in-emojis/cloud-producer:latest
```

---

## Cost Estimation

**Cloud Run Job:**
- $0.00002400 per vCPU-second
- $0.00000250 per GiB-second
- ~5 minutes per run = 300 seconds
- 6 runs/day × 30 days = 180 runs/month
- Estimated: ~$5-10/month

**Cloud Scheduler:**
- $0.10 per job per month
- 6 jobs = $0.60/month

**Cloud Storage:**
- $0.020 per GB/month
- ~5MB per image × 180 images/month = ~1GB
- Estimated: ~$0.02/month

**Firestore:**
- $0.18 per 100K reads
- $0.18 per 100K writes
- 180 writes/month = minimal cost

**Total: ~$6-11/month**

---

## Troubleshooting

### Job fails with "permission denied"
- Check service account has Storage Object Admin + Cloud Datastore User roles
- Verify secret access is granted

### Job times out
- Increase `--task-timeout` to 15m or 20m
- Check if Playwright is slow (might need more CPU)

### Image generation fails
- Check fonts are installed in Dockerfile
- Verify ImageMagick/Playwright dependencies

### Scheduler doesn't trigger
- Check scheduler job status: `gcloud scheduler jobs describe cloud-producer-00 --location=us-central1`
- Check Cloud Run job exists and is in the same region

---

## Next Steps

After deployment:
1. Monitor for 24 hours to ensure all 6 jobs run successfully
2. Check Cloud Storage for all 6 images per day
3. Check Firestore for all 6 editions per day
4. Verify essence post is created as the 6th post
5. Run for 7-14 days in parallel with GitHub workflow
6. Compare quality and correctness
7. Proceed to Step 2 (Cutover Instagram to cloud)

---

## Cleanup (if needed)

To remove everything:

```bash
# Delete scheduler jobs
gcloud scheduler jobs delete cloud-producer-00 --location=us-central1
gcloud scheduler jobs delete cloud-producer-04 --location=us-central1
gcloud scheduler jobs delete cloud-producer-08 --location=us-central1
gcloud scheduler jobs delete cloud-producer-12 --location=us-central1
gcloud scheduler jobs delete cloud-producer-16 --location=us-central1
gcloud scheduler jobs delete cloud-producer-20 --location=us-central1

# Delete Cloud Run job
gcloud run jobs delete cloud-producer --region=us-central1

# Delete Docker images
gcloud artifacts docker images delete \
    us-central1-docker.pkg.dev/today-in-emojis/today-in-emojis/cloud-producer:latest

# Delete repository
gcloud artifacts repositories delete today-in-emojis --location=us-central1
```
