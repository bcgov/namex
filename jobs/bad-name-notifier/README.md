# Bad-Name-Notifier

Bad-Name-Notifier is a Python application designed to identify names with special characters in a PostgreSQL database and send email notifications to specified recipients. The application runs as a standalone job, suitable for deployment in OpenShift or similar platforms.

## Features
- Query a PostgreSQL database for names with special characters.
- Filter out names that are not in specific states (e.g., `APPROVED`, `CONDITION`).
- Send email notifications with formatted data to a configurable list of recipients.
- Configurable via environment variables for flexibility.

## Requirements
- Python 3.12+
- PostgreSQL database
- Poetry for dependency management
- OpenShift (for deployment)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/namex.git
   cd jobs/bad-name-notifier

2 ### Install the dependencies
```bash
poetry install
```

3 ### Configure the .env
(see .env.sample)

```bash
eval $(poetry env activate)
```

4 ### Run the job
```bash
python src/bad_name_notifier/app.py
OR: ./run.sh
```

5 ### Run Linting
```bash
poetry run ruff check --fix
```

6 ### Run unit tests
```bash
poetry run pytest
```