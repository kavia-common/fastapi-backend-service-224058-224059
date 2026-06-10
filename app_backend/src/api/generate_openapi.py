import json
import os

from src.api.main import app

# Get the OpenAPI schema
openapi_schema = app.openapi()

# Write to file (app_backend/interfaces/openapi.json)
output_dir = "interfaces"
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, "openapi.json")

with open(output_path, "w", encoding="utf-8") as f:
    json.dump(openapi_schema, f, indent=2, ensure_ascii=False, sort_keys=True)
