
"""Small script to create a synthetic PR dataset and train a simple classifier.
Run this locally to produce `backend/models/pr_risk.joblib` which the API uses.
"""
import os, csv, random, joblib
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score
import numpy as np

OUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'models')
os.makedirs(OUT_DIR, exist_ok=True)
csv_out = os.path.join(os.path.dirname(__file__), '..', 'datasets', 'prs.csv')

# generate small synthetic dataset
random.seed(42)
rows = []
for i in range(600):
    lines = random.randint(1, 2000)
    files = max(1, int(lines / random.uniform(20,200)))
    comments = random.randint(0, 40)
    tests = random.choice([0,1])
    # label: risky if many lines + files + no tests + many comments (synthetic)
    risk = 1 if (lines>800 or (files>10 and tests==0) or comments>20) else 0
    rows.append([lines, files, comments, tests, risk])

# save dataset
os.makedirs(os.path.dirname(csv_out), exist_ok=True)
with open(csv_out, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['lines_changed','files_changed','comments','tests_modified','risky'])
    writer.writerows(rows)

# train model
X = np.array([[r[0], r[1], r[2], r[3]] for r in rows])
y = np.array([r[4] for r in rows])
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
clf = LogisticRegression(max_iter=1000)
clf.fit(X_train, y_train)
probs = clf.predict_proba(X_test)[:,1]
auc = roc_auc_score(y_test, probs)
print('Trained model AUC:', auc)
joblib.dump(clf, os.path.join(OUT_DIR, 'pr_risk.joblib'))
print('Saved model to models/pr_risk.joblib')
