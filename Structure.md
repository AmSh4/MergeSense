    MergeSense/
    │
    ├── frontend/                 # Next.js + Tailwind UI
    │   ├── components/           # Reusable UI components
    │   │   └── PRChart.tsx
    │   ├── pages/                # Dashboard pages (index, PR details)
    │   │   └── dashboard.tsx
    │   ├── styles/               # Static assets
    │   │   └──globals.css
    │   └── package.json
    │
    ├── backend/               
    │   ├── models/               # SQLModel schemas
    │   │   └── _init_.py
    │   ├── ml/                   # Training & saved ML model
    │   │   └── train_model.py
    │   ├── tests/                # Pytest unit tests
    │   │   └── test_api.py
    │   └── main.py
    │
    ├── k8s/                      # Kubernetes manifests
    │   ├── backend-deployment.yaml
    │   ├── redis.yaml
    │   ├── frontend-deployment.yaml
    │   └── postgress.yaml
    │
    ├── docker-compose.yml        # Local dev setup (Frontend, Backend, DB, Redis)
    ├── README.md
    ├── .github
    ├── LICENSE
    └── docs/
        └── ARCHITECTURE.md       # System overview
