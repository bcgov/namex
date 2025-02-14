# Bad-designation-Notifier

Bad-designation-Notifier is a Python application designed to identify designations does not matching request types in a PostgreSQL database and send email notifications to specified recipients. The application runs as a standalone job, suitable for deployment in OpenShift or similar platforms.

## Features
- Query a PostgreSQL database for designations in the names with request type in 'FR','LL','LP','XLL','XLP'.
- Filter out designations that are not in specific states (e.g., 'CANCELLED','EXPIRED','PENDING_DELETION','REJECTED').
- Send email notifications with formatted data to a configurable list of recipients.
- Configurable via environment variables for flexibility.
- to update reciepts, check the environment variable EMAIL_RECIPIENTS in YAML.

## Requirements
- Python 3.12+
- PostgreSQL database
- Poetry for dependency management
- OpenShift (for deployment)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/bad-designation-notifier.git
   cd bad-designation-notifier
