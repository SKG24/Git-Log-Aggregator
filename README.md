# Git‑Based Log Aggregator

A Git‑first, Python‑driven log aggregation and analysis tool designed to turn messy, scattered logs into versioned, auditable data—while helping you learn Git properly (branches, hooks, CI) through a real DevOps‑style project.

## Project Goals

### This project has two primary goals:

- Learn Git deeply and correctly
- Branch‑based development
- Meaningful commits
- Project‑managed Git hooks
- CI validation with GitHub Actions
- Realistic DevOps workflows

### Build a practical log aggregation pipeline

- Collect logs from files, directories, or glob patterns
- Normalize timestamps and severity
- Store logs in a Git‑tracked structure
- Analyze logs and auto‑generate summaries
- Optionally auto‑commit generated results

## Core Idea

- Treat logs as versioned data, not disposable files.
- Instead of overwriting logs or letting them rot:
- Each run aggregates and normalizes logs
- Outputs are saved into a Git repository
- Git history becomes a timeline of system behavior
- You can diff logs, trace errors historically, and experiment safely on branches


## Features
- Collect logs from:
    - Single files
    - Directories (recursive)
    - Glob patterns (**/*.log)

- Normalize:
    - Timestamps → ISO‑8601 (UTC or local time)
    - Severity → ERROR | WARN | INFO
    - Missing timestamps → auto‑injected

- Store:
    - Daily log files:
    - data/logs/YYYY-MM-DD_<source>.log

- Analyze:
    - Error / Warning / Info counts
    - Daily reports:
    - data/reports/summary-YYYY-MM-DD.txt

- Git integration:
    - Versioned Git hooks
    - Optional Python‑driven git add & git commit
    - CI checks ensure repo hygiene

## Repository Structure
```

git-log-aggregator/
├── .githooks/                
│   ├── pre_commit
│   ├── post_commit
│   ├── prepare_commit_msg
│   └── README.md
├── .github/workflows/
│   └── ci.yml                 
├── scripts/
│   └── install_git_hooks.sh   
├── src/
│   └── aggregator/
│       ├── __init__.py
│       ├── cli.py             
│       ├── config.py          
│       ├── collect.py        
│       ├── normalize.py       
│       ├── store.py           
│       ├── analyze.py         
│       └── gitops.py          
├── tests/                     
├── data/
│   ├── logs/                  
│   └── reports/               # tested result in included
├── config/
│   ├── aggregator.json        
│   └── aggregator.override.json 
├── requirements.txt
└── README.md
```

## Setup

1. Clone
```
git clone https://github.com/<your-username>/git-log-aggregator.git
cd git-log-aggregator

```

2. Create Virtual Environment
```

python -m venv .venv
source .venv/Scripts/activate   # Git Bash (Windows)
pip install -r requirements.txt
```

3. Install git hooks
```
./scripts/install_git_hooks.sh
```

4.  Configuration
```
{
  "sources": [
    "C:\\\\Users\\\\User.Name\\\\logs",
    "/var/log/**/*.log"
  ],
  "normalize_timestamp": "UTC",
  "timezone": "Asia/Kolkata",
  "output_dir": "data/logs",
  "report_dir": "data/reports",
  "commit_message_format": "logs: add {date} aggregated logs"
}
```

## How to use
1. Show help -> python -m aggregator --help
2. Run full pipeline -> python -m aggregator run
3. Run and auto commit result -> python -m aggregator run --commit

This will:

1. Collect logs
2. Normalize them
3. Store daily log files
4. Generate summary report
5. Commit outputs to Git (optional)

## Git WOrkflow used
```
main
 ├─ feat/cli
 |
 ├─ feat/config
 |
 ├─ feat/collect
 |
 ├─ feat/normalize
 |
 ├─ feat/store
 |
 ├─ feat/analyze
 |
 ├─ feat/gitops
 |
 └─ feat/pipeline
 ```
