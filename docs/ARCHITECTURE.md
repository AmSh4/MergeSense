# Architecture (high-level)

Frontend (Next.js) <--> Backend (FastAPI) <--> Postgres
                               |
                               V
                             Redis (cache)
                               |
                               V
                        ML model (joblib file)

Run locally: docker-compose up --build
Kubernetes manifests included in /k8s for cluster deployment.
