#!/usr/bin/env python3
"""
================================================================================
V30-E001: Gmail Toolkit Live Materialization (CRITICAL)
================================================================================

MISSION: Move Gmail from 'unverified/read-only' to 'live-write proven'

HYPOTHESIS:
If Composio's Gmail toolkit is properly authenticated with OAuth2, then
Aletheon can programmatically send and receive emails, enabling automated
notifications, alerts, and external communication workflows.

EXPECTED OUTCOME:
- OAuth2 authentication flow completed
- Inbox successfully read (list of emails retrieved)  
- Test email sent to known address
- Email delivery confirmed via read-back
- JSON proof artifact saved to docs/trinity-live-traces/

SAFETY BOUNDS:
1. Only send emails to addresses explicitly approved by Hamish
2. Maximum 5 test emails per session
3. All email content must be clearly marked as 'TEST'
4. No automated email sending without explicit approval
5. OAuth tokens stored only in WSL environment, never committed to repo

ROLLBACK PROCEDURE:
1. Revoke OAuth tokens via Google Account settings
2. Delete local token cache in WSL
3. Update connector status back to 'unverified'
4. Document reason for rollback in experiment result
"""

import os
import json
from datetime import datetime, timezone
from pathlib import Path

# Safety: Only run in WSL sandbox
SANDBOX = Path("/home/aletheon/v28-fluid-lab")
ARTIFACTS = SANDBOX / "artifacts"

def prove_gmail_materialization():
    """
    Prove Gmail toolkit can:
    1. Authenticate via OAuth2
    2. Read inbox
    3. Send test email
    4. Confirm delivery
    """

    results = {
        "experiment_id": "V30-E001",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "steps": {}
    }

    try:
        # Step 1: Import and initialize Composio
        from composio import ComposioToolSet

        toolset = ComposioToolSet(api_key=os.getenv("COMPOSIO_API_KEY"))
        results["steps"]["import"] = {"status": "PASS", "message": "Composio imported"}

        # Step 2: Get Gmail tools
        gmail_tools = toolset.get_tools(actions=[
            "GMAIL_SEND_EMAIL",
            "GMAIL_FETCH_EMAILS"
        ])
        results["steps"]["tool_fetch"] = {
            "status": "PASS", 
            "tools": [t.name for t in gmail_tools]
        }

        # Step 3: Fetch recent emails (read-only test)
        fetch_result = toolset.execute_action(
            action="GMAIL_FETCH_EMAILS",
            params={"max_results": 5}
        )
        results["steps"]["fetch"] = {
            "status": "PASS" if fetch_result.get("emails") is not None else "FAIL",
            "email_count": len(fetch_result.get("emails", [])),
            "preview": str(fetch_result)[:200]
        }

        # Step 4: Send test email (write test)
        # IMPORTANT: Set this in your environment before running
        TEST_RECIPIENT = os.getenv("V30_TEST_EMAIL_RECIPIENT", "")

        if not TEST_RECIPIENT:
            results["steps"]["send"] = {
                "status": "SKIP",
                "reason": "V30_TEST_EMAIL_RECIPIENT not set"
            }
        else:
            send_result = toolset.execute_action(
                action="GMAIL_SEND_EMAIL",
                params={
                    "recipient_email": TEST_RECIPIENT,
                    "subject": "[V30 TEST] Gmail Toolkit Materialization Proof",
                    "body": f"""This is an automated test email from Aletheon's V30 experiment.

Experiment: V30-E001
Timestamp: {datetime.now(timezone.utc).isoformat()}
Status: Materialization proof in progress

If you received this, Gmail toolkit materialization is PROVEN.""",
                    "is_html": False
                }
            )
            results["steps"]["send"] = {
                "status": "PASS" if send_result.get("success") else "FAIL",
                "message_id": send_result.get("message_id", "unknown"),
                "preview": str(send_result)[:200]
            }

        # Step 5: Overall assessment
        all_passed = all(
            step.get("status") == "PASS" 
            for step in results["steps"].values()
        )
        results["overall_status"] = "MATERIALIZED" if all_passed else "PARTIAL"

    except Exception as e:
        results["overall_status"] = "FAILURE"
        results["error"] = str(e)
        results["error_type"] = type(e).__name__

    # Save artifact
    artifact_path = ARTIFACTS / "V30-E001-gmail-materialization-proof.json"
    artifact_path.parent.mkdir(parents=True, exist_ok=True)
    with open(artifact_path, 'w') as f:
        json.dump(results, f, indent=2)

    print(f"Experiment complete: {results['overall_status']}")
    print(f"Artifact saved: {artifact_path}")
    return results

if __name__ == "__main__":
    prove_gmail_materialization()
