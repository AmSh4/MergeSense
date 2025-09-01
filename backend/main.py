
from fastapi import FastAPI, HTTPException, BackgroundTasks
from typing import List
from sqlmodel import Field, SQLModel, Session, create_engine, select
from pydantic import BaseModel
import joblib, os, time, json
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import redis

DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///./data/codeflow.db')
REDIS_URL = os.getenv('REDIS_URL', None)

# create engine with postgres compatibility if provided
connect_args = {}
if DATABASE_URL.startswith('sqlite'):
    connect_args = {'check_same_thread': False}

engine = create_engine(DATABASE_URL, echo=False, connect_args=connect_args)

# connect to redis if provided
redis_client = None
if REDIS_URL:
    try:
        redis_client = redis.Redis.from_url(REDIS_URL)
    except Exception as e:
        print('Redis connection warning:', e)

class PullRequest(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    author: str
    lines_changed: int
    files_changed: int
    comments: int
    tests_modified: bool
    created_at: float = time.time()

class PRIn(BaseModel):
    title: str
    author: str
    lines_changed: int
    files_changed: int
    comments: int
    tests_modified: bool

app = FastAPI(title='MergeSense API')

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

@app.on_event('startup')
def on_startup():
    SQLModel.metadata.create_all(engine)

@app.post('/api/prs', response_model=dict)
def create_pr(pr: PRIn):
    with Session(engine) as session:
        pr_obj = PullRequest.from_orm(pr)
        session.add(pr_obj)
        session.commit()
        session.refresh(pr_obj)
    return {'id': pr_obj.id}

@app.get('/api/prs', response_model=List[PullRequest])
def list_prs():
    with Session(engine) as session:
        prs = session.exec(select(PullRequest).order_by(PullRequest.created_at)).all()
    return prs

@app.get('/api/prs/{pr_id}/analyze')
def analyze_pr(pr_id: int):
    # check redis cache first
    cache_key = f"pr_analysis:{pr_id}"
    if redis_client:
        cached = redis_client.get(cache_key)
        if cached:
            return json.loads(cached)
    model_path = os.path.join(os.path.dirname(__file__), 'models', 'pr_risk.joblib')
    if not os.path.exists(model_path):
        raise HTTPException(status_code=404, detail='Model not trained yet. Run ml/train_model.py')
    model = joblib.load(model_path)
    with Session(engine) as session:
        pr = session.get(PullRequest, pr_id)
        if not pr:
            raise HTTPException(status_code=404, detail='PR not found')
        features = [[pr.lines_changed, pr.files_changed, pr.comments, int(pr.tests_modified)]]
        prob = float(model.predict_proba(features)[0][1])
        result = {'pr_id': pr_id, 'risk_score': round(prob, 4)}
        # cache for 60 seconds
        if redis_client:
            try:
                redis_client.setex(cache_key, 60, json.dumps(result))
            except Exception as e:
                print('Redis setex warning', e)
        return result

# Simple SSE for demo (stream increments)
@app.get('/api/stream')
def stream():
    def event_stream():
        i = 0
        while i < 20:
            yield f"data: {{\"time\": {time.time()}, \"value\": {i}}}\n\n"
            time.sleep(1)
            i += 1
    return StreamingResponse(event_stream(), media_type='text/event-stream')
