#!/bin/bash
cd /home/kavia/workspace/code-generation/fastapi-backend-service-224058-224059/app_backend
source venv/bin/activate
flake8 .
LINT_EXIT_CODE=$?
if [ $LINT_EXIT_CODE -ne 0 ]; then
  exit 1
fi

