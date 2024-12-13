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
   ```

2. Install dependencies using Poetry:
   ```bash
   poetry install
   ```

3. Set up the `.env` file for local development:
   ```env
   NAMEX_DATABASE_HOST=
   NAMEX_DATABASE_NAME=namex
   NAMEX_DATABASE_PASSWORD=yourpassword
   NAMEX_DATABASE_PORT=5432
   NAMEX_DATABASE_USERNAME=yourusername
   EMAIL_RECIPIENTS=eve.deng@gov.bc.ca
   SMTP_SERVER=apps.smtp.gov.bc.ca
   SMTP_USER=namex@noreply.github.com
   ```

4. Activate the virtual environment:
   ```bash
   poetry shell
   ```

5. Run the application locally:
   ```bash
   ./run.sh
   ```

## Configuration

The application uses environment variables for configuration. These can be set in the `.env` file for local development or directly in the environment for production.

### Required Environment Variables

| Variable               | Description                              |
|------------------------|------------------------------------------|
| `NAMEX_DATABASE_HOST`  | Hostname of the PostgreSQL database      |
| `NAMEX_DATABASE_NAME`  | Name of the PostgreSQL database          |
| `NAMEX_DATABASE_PORT`  | Port for the PostgreSQL database         |
| `NAMEX_DATABASE_USERNAME` | Username for the PostgreSQL database   |
| `NAMEX_DATABASE_PASSWORD` | Password for the PostgreSQL database   |
| `EMAIL_RECIPIENTS`     | Comma-separated list of email recipients |
| `SMTP_SERVER`          | SMTP server address                     |
| `SMTP_USER`            | Sender email address                    |

## Deployment

### Running Locally
To test the application locally:
1. Ensure the `.env` file is correctly configured.
2. Run the following command:
   ```bash
   python app.py
   ```

### Running in OpenShift
1. Create a Kubernetes/OpenShift secret for sensitive data like `SMTP_USER`:
   ```bash
   oc create secret generic smtp-credentials --from-literal=SMTP_USER=namex@noreply.github.com
   ```

2. Deploy the application as a job with environment variables and secrets configured in your deployment YAML:
   ```yaml
   env:
     - name: EMAIL_RECIPIENTS
       value:
   envFrom:
     - secretRef:
         name: smtp-credentials
   ```

3. Build and push the Docker image to your registry.

4. Deploy the job:
   ```bash
   oc apply -f deployment.yaml
   ```

## Development

### Debugging
Use VSCode for debugging:
1. Add a `launch.json` configuration for Flask.
2. Set breakpoints in the code.
3. Run the debugger.

### Testing
Ensure the database and email services are accessible. You can write unit tests for the services in the `services` directory.

## File Structure

```
.
├── app.py              # Main application file
├── config.py           # Configuration handling
├── services/           # Contains database and email service logic
│   ├── database_service.py
│   ├── email_service.py
├── requirements.txt    # Dependencies for manual pip installs
├── pyproject.toml      # Poetry dependency management
├── run.sh              # Shell script for running the app
└── README.md           # Project documentation
```

## License
This project is licensed under the Apache License 2.0. See the `LICENSE` file for details.

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request.

## Contact
For questions or support, please contact `eve.deng@gov.bc.ca`.
