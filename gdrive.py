import os
import sys
import subprocess
from pathlib import Path
from urllib.parse import urlparse, unquote

# ─────────────────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────────────────

URLS = os.environ.get("URLS", "")

DOWNLOAD_DIR = Path("downloads")

# ─────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────

def log(msg):
    print(msg)


def install_requirements():

    packages = [
        "gdown",
        "requests"
    ]

    subprocess.run(
        [sys.executable, "-m", "pip", "install", "-q"] + packages,
        check=True
    )


def get_filename_from_url(url):

    parsed = urlparse(url)

    filename = os.path.basename(parsed.path)

    filename = unquote(filename)

    if not filename:
        filename = "downloaded_file"

    return filename


def download_normal_url(url):

    import requests

    filename = get_filename_from_url(url)

    output_path = DOWNLOAD_DIR / filename

    log(f"Downloading: {filename}")

    headers = {
        "User-Agent": (
            "Mozilla/5.0"
        )
    }

    with requests.get(
        url,
        stream=True,
        headers=headers,
        timeout=60
    ) as r:

        r.raise_for_status()

        total = int(
            r.headers.get("content-length", 0)
        )

        downloaded = 0

        with open(output_path, "wb") as f:

            for chunk in r.iter_content(
                chunk_size=1024 * 1024
            ):

                if chunk:

                    f.write(chunk)

                    downloaded += len(chunk)

                    if total > 0:

                        percent = (
                            downloaded / total
                        ) * 100

                        print(
                            f"\r{percent:.1f}% ",
                            end=""
                        )

    print()
    log(f"Saved: {output_path}")


def download_google_drive(url):

    import gdown

    # Folder
    if (
        "folders/" in url
        or "drive/folders/" in url
    ):

        folder_output = (
            DOWNLOAD_DIR / "gdrive_folder"
        )

        folder_output.mkdir(exist_ok=True)

        gdown.download_folder(
            url=url,
            output=str(folder_output),
            quiet=False,
            remaining_ok=True
        )

    # Single file
    else:

        gdown.download(
            url=url,
            output=str(DOWNLOAD_DIR),
            fuzzy=True,
            quiet=False
        )


def process_links():

    if not URLS.strip():

        log("No URLs provided")
        sys.exit(1)

    DOWNLOAD_DIR.mkdir(exist_ok=True)

    links = [
        x.strip()
        for x in URLS.splitlines()
        if x.strip()
    ]

    log(f"Total URLs: {len(links)}")

    for idx, url in enumerate(links, 1):

        log("\n" + "=" * 70)
        log(f"[{idx}/{len(links)}]")
        log(url)
        log("=" * 70)

        try:

            # ─── GOOGLE DRIVE ───
            if (
                "drive.google.com" in url
            ):

                download_google_drive(url)

            # ─── NORMAL DIRECT FILE ───
            else:

                download_normal_url(url)

            log("Completed")

        except Exception as e:

            log(f"Failed: {e}")


# ─────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────

def main():

    install_requirements()

    process_links()

    log("\nAll downloads completed")


if __name__ == "__main__":
    main()
