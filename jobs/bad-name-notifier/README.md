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
   git clone https://github.com/your-repo/bad-name-notifier.git
   cd bad-name-notifier
