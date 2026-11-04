#!/usr/bin/env python3

import logging
import subprocess
import sys
import time

import requests

# Configure logging - streams to GCP Cloud Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

# Health check configuration
SOLR_HOST = "localhost"
SOLR_PORT = 8983
SOLR_BASE_URL = f"http://{SOLR_HOST}:{SOLR_PORT}"
CHECK_INTERVAL = 300  # Run checks every 5 minutes

# Role detection (leader/follower)
ROLE = subprocess.getoutput("curl -fs http://metadata.google.internal/computeMetadata/v1/instance/attributes/role -H 'Metadata-Flavor: Google' 2>/dev/null").strip()

if ROLE not in ("leader", "follower"):
    logger.error(f"Failed to detect role from GCP metadata. Got: '{ROLE}'. Exiting.")
    sys.exit(1)

CORE = "name_request" if ROLE == "leader" else "name_request_follower"

logger.info(f"Health check monitoring starting (ROLE={ROLE}, CORE={CORE}, CHECK_INTERVAL={CHECK_INTERVAL}s)")


def check_command(cmd, description):
    """Execute a shell command and return True if successful."""
    try:
        result = subprocess.call(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        success = result == 0
        logger.info(f"Check '{description}': {'✓ PASS' if success else '✗ FAIL'}")
        return success, None
    except Exception as e:
        logger.error(f"Check '{description}' error: {e}")
        return False, str(e)


def check_docker():
    """Verify Docker container is running via Docker Engine API."""
    try:
        result = subprocess.run(
            ["curl", "-sf", "--unix-socket", "/var/run/docker.sock",
             "http://localhost/containers/solr-container/json"],
            capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0:
            import json
            state = json.loads(result.stdout).get("State", {})
            running = state.get("Running", False)
            if running:
                logger.info("Check 'Docker container running': ✓ PASS")
                return True, None
            else:
                status = state.get("Status", "unknown")
                logger.info("Check 'Docker container running': ✗ FAIL")
                return False, f"solr-container status: {status}"
        else:
            logger.info("Check 'Docker container running': ✗ FAIL")
            return False, "solr-container not found"
    except Exception as e:
        logger.error(f"Check 'Docker container running' error: {e}")
        return False, str(e)


def check_solr_query():
    """Verify Solr search functionality works."""
    try:
        response = requests.get(
            f"{SOLR_BASE_URL}/solr/{CORE}/select",
            params={"q": "*:*", "rows": "0"},
            timeout=5
        )
        if response.status_code == 200:
            logger.info(f"Check 'Solr query ({CORE})': ✓ PASS")
            return True, None
        else:
            return False, f"HTTP {response.status_code}"
    except requests.exceptions.RequestException as e:
        logger.error(f"Check 'Solr query ({CORE})': ✗ FAIL - {e}")
        return False, str(e)


def check_disk_usage():
    """Verify disk usage is below 90%."""
    try:
        cmd = "df -h /home | awk 'NR==2 {gsub(/%/,\"\", $5); print $5}'"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=5)
        
        if result.returncode != 0:
            return False, "Failed to check disk"
        
        usage = int(result.stdout.strip())
        
        if usage > 90:
            logger.warning(f"Check 'Disk usage': ✗ FAIL - {usage}% (threshold: 90%)")
            return False, f"Disk usage {usage}% exceeds 90%"
        else:
            logger.info(f"Check 'Disk usage': ✓ PASS ({usage}%)")
            return True, None
    except Exception as e:
        logger.error(f"Check 'Disk usage': ✗ ERROR - {e}")
        return False, str(e)


def run_monitoring_loop():
    """Continuously run health checks and log results."""
    logger.info("Starting monitoring loop...")
    
    checks = [
        ("Docker container", check_docker),
        ("Solr query", check_solr_query),
        ("Disk usage", check_disk_usage),
    ]
    
    while True:
        try:
            failures = []
            
            for check_name, check_func in checks:
                success, error = check_func()
                if not success:
                    failures.append(f"{check_name}: {error or 'failed'}")
            
            if failures:
                logger.warning(f"HEALTH CHECK FAILED: {'; '.join(failures)}")
            else:
                logger.info("HEALTH CHECK PASSED: All checks healthy")
            
            time.sleep(CHECK_INTERVAL)
        except Exception as e:
            logger.error(f"Monitoring loop error: {e}", exc_info=True)
            time.sleep(CHECK_INTERVAL)


# Entry point
if __name__ == "__main__":
    run_monitoring_loop()
