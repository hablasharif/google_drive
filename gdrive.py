name: Python Runner

on:
  workflow_dispatch:

jobs:
  run:
    runs-on: ubuntu-latest

    env:
      URLS: |
        https://bbbb.c2629860576b18c4e67abfd4deeaa712.r2.cloudflarestorage.com/file.zip?X-Amz-Signature=abc

    steps:
      - name: Checkout Repository
        uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install Requirements
        run: |
          if [ -f requirements.txt ]; then
            pip install -r requirements.txt
          fi

      - name: Find and Run Python File
        run: |
          PY_FILE=$(find . -type f -name "*.py" | head -n 1)

          if [ -z "$PY_FILE" ]; then
            echo "No Python file found"
            exit 1
          fi

          echo "Running: $PY_FILE"

          python "$PY_FILE"

      - name: Upload Downloads
        uses: actions/upload-artifact@v4
        with:
          name: downloaded-files
          path: downloads/
          if-no-files-found: ignore
