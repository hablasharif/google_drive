name: Universal Downloader

on:
  workflow_dispatch:

jobs:
  download:
    runs-on: ubuntu-latest

    env:
      URLS: |


        https://bbbb.c2629860576b18c4e67abfd4deeaa712.r2.cloudflarestorage.com/file.zip?X-Amz-Signature=abc

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Run Downloader
        run: |
          python downloader.py

      - name: Upload Files
        uses: actions/upload-artifact@v4
        with:
          name: downloaded-files
          path: downloads/
