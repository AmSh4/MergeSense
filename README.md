# MergeSense

[![CI](https://img.shields.io/badge/ci-passing-brightgreen)](https://github.com/)
[![License](https://img.shields.io/badge/license-MIT-blue)](LICENSE)
[![Issues](https://img.shields.io/badge/issues-0-green)](https://github.com/)

A full-stack engineering analytics platform that analyzes Pull Requests (PRs) using Machine Learning, provides visual dashboards, and integrates with modern developer workflows.

### It helps engineering teams:

- Detect risky PRs before merge.

- Visualize trends in review cycles, risk levels, and team activity.

- Run in a fully containerized environment (Docker / Kubernetes).

---

## Features:

- Interactive Dashboard with charts (React + Recharts + Tailwind).
- ML-Powered PR Risk Analyzer (FastAPI + scikit-learn).

- PostgreSQL + Redis caching for scalable performance.

- Docker Compose & Kubernetes support for easy deployment.

- Pytest-based testing + GitHub Actions CI/CD.
- Clean modular project structure with multiple services.
  
---

## Project Structure:

- https://github.com/AmSh4/MergeSense/new/main

---

## Tech Stack1:

- Frontend: Next.js, TypeScript, Tailwind CSS, Recharts

- Backend: FastAPI, SQLModel, scikit-learn

- Database: PostgreSQL

- Cache: Redis

- Infra: Docker, Kubernetes, GitHub Actions

- Testing: Pytest, React Testing Library

---
## Getting Started:
1. Clone the repo
     
        git clone https://github.com/AmSh4/MergeSense.git
        cd codeflow-insights

2. Run with Docker Compose

- Make sure Docker & Docker Compose are installed.

        docker-compose up --build


`Frontend → http://localhost:3000`

`Backend API → http://localhost:8000/docs`

3. Local Development (without Docker)
- Backend
  
        cd backend
        python3 -m venv .venv
        source .venv/bin/activate
        pip install -r requirements.txt

**Run ML training**

      python ml/train_model.py

**Start FastAPI**

      uvicorn main:app --reload

- Frontend
  
      cd frontend
      npm install
      npm run dev


`App → http://localhost:3000`

---
## Testing

**Run unit tests:**

    cd backend
    pytest -v

---
## Deployment
**Kubernetes**

    kubectl apply -f k8s/

**GitHub Actions CI/CD**

- Runs linting & pytest on PRs.

- Can be extended to build and push Docker images.
---
## Roadmap

- GitHub OAuth to pull real PR data.

- Fine-tune ML model with real PR datasets.
- Mobile-friendly dashboard.

- Multi-tenant support for larger teams.

---
## Kubernetes 
Manifests are provided in `/k8s`. These are basic Deployment + Service manifests for frontend, backend, Postgres, and Redis, intended as a starting point for cluster deployment.

## Files of interest
- `frontend/` — Next.js app with charts and improved UI
- `backend/` — FastAPI app with Postgres + Redis support and enhanced tests
- `k8s/` — Kubernetes manifests (deployments + services)
- `docker-compose.yml` — local dev using Postgres + Redis

## Contributing

Contributions are welcome! 
https://github.com/AmSh4/MergeSense/blob/main/CONTRIBUTING.md

## License

MIT License
