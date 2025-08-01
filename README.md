# Bike Point Data Extraction and Upload Pipeline

## Overview

This repository contains two Python scripts that work together to extract live bike point data from the Transport for London (TfL) API and upload the extracted JSON files to an AWS S3 bucket.

- `output_json_api.py`: Queries the TfL BikePoint API, performs validation on the response, and saves the data as timestamped JSON files in a local `data` directory.
- `s3_upload_api.py`: Uploads the JSON files from the `data` directory to a specified AWS S3 bucket folder and removes local files upon successful upload.

Both scripts are required to be run sequentially to complete the full extract-and-upload cycle.

Additionally, this repository includes a GitHub Actions workflow file (`bike-point-extract-and-load.yml`) to automate the extraction and upload process on demand or via schedule.

---

## Features

- **Robust API extraction with retry logic:**  
  Retries up to 3 times on API errors, network issues, or invalid data, with delays between attempts.

- **Data validation:**  
  Confirms the API returns JSON, checks minimum data length, and verifies data freshness based on timestamps.

- **Timestamped file output:**  
  Saves API responses as uniquely named JSON files in the `data/` folder using the current datetime.

- **AWS S3 upload with connection testing:**  
  Validates AWS credentials and connection before attempting uploads.

- **Safe local cleanup:**  
  Deletes JSON files locally only after successful upload to avoid data loss.

- **GitHub Actions workflow:**  
  Automates running extraction and upload scripts in a controlled CI environment.

---

## Repository Structure

```env
├── output_json_api.py # Extracts and saves bike point data from TfL API
├── s3_upload_api.py # Uploads JSON files from data/ directory to AWS S3
├── bike-point-extract-and-load.yml # GitHub Actions workflow automation
├── requirements.txt # Python dependencies
└── data/ # Directory where JSON files are saved and read from
```

---

## Environment Variables

Create a `.env` file or set the following environment variables before running the scripts:

access_key=<your_aws_access_key_id>
secret_key=<your_aws_secret_access_key>
AWS_BUCKET_NAME=<your_s3_bucket_name>
region=<your_aws_region> # e.g., us-east-1

The upload script uses these variables to authenticate AWS requests and target the correct S3 bucket.

---

## How It Works

### 1. `output_json_api.py`

- Requests data from TfL’s BikePoint API.
- Retries up to 3 times on failure, with 2-second wait intervals.
- Validates the response is JSON and contains sufficient data (>50 entries).
- Checks the freshness of the data based on the latest `modified` timestamp inside additional properties.
- Saves the JSON response locally with a filename formatted as `YYYY-MM-DD__HH-MM-SS.json` under the `data/` directory.
- Prints status messages detailing success or specific errors.

### 2. `s3_upload_api.py`

- Tests AWS connection using STS to verify credentials and permissions.
- Scans the `data/` directory for `.json` files.
- For each file: uploads it to the `bike-point/` folder inside the specified S3 bucket.
- Deletes each local file after successful upload.
- Prints detailed status messages about each upload and any errors.

---

## GitHub Actions Workflow

The included `bike-point-extract-and-load.yml` defines a GitHub Actions workflow that:

- Checks out the repository.
- Sets up Python 3.11.
- Installs dependencies listed in `requirements.txt`.
- Runs the extraction script (`output_json_api.py`).
- Runs the upload script (`s3_upload_api.py`) with AWS credentials injected via GitHub Secrets.

This workflow can be triggered manually (`workflow_dispatch`) or scheduled by uncommenting and configuring the cron schedule.

---

## Error Handling and Limitations

- The extraction script handles network/API errors, invalid JSON, and stale data with retries and informative messages.
- Upload script verifies AWS connectivity before uploading but will not retry failed uploads.
- If uploads fail, local files remain in the `data/` directory for manual intervention.
- No logging framework; output is via console prints.
- Ensure your AWS credentials have proper permissions for STS and S3 upload actions.

---

## Security Considerations

- Store your AWS credentials and other sensitive environment variables securely (e.g., `.env` file excluded from version control or GitHub Secrets).
- Use least-privilege IAM policies for your AWS keys to minimize risk.

---

## Contribution

Contributions to improve error handling, add logging, or enhance automation are welcome. Please open issues or pull requests as needed.

---

## License

This project is provided "as-is" without warranty. Use at your own risk.
