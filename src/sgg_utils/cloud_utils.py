def access_secret_version(project_id, secret_id, version_id):
    from google.cloud import secretmanager
    # Create the Secret Manager client.
    client = secretmanager.SecretManagerServiceClient()

    # Build the resource name of the secret version.
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"

    # Access the secret version.
    response = client.access_secret_version(request={"name": name})

    # Return the decoded payload.
    return response.payload.data.decode('UTF-8')


def list_to_cloud_storage(bucket_name, list_of_dict, filename, timestamp=False, timeout=300):
    from google.cloud import storage
    import json
    import time
    from google.cloud.storage.retry import DEFAULT_RETRY

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    if timestamp:
        from datetime import datetime
        filename = filename.split('.')[0]
        filename = f'{filename}_{datetime.now().strftime("%Y%m%d%H%M%S")}.json'
    blob = bucket.blob(filename)
    modified_retry = DEFAULT_RETRY.with_deadline(500.0)
    modified_retry = modified_retry.with_delay(initial=1.5, multiplier=1.2, maximum=45.0)
    blob.upload_from_string('\n'.join(json.dumps(item) for item in list_of_dict), timeout=timeout, retry=modified_retry)
    return f'File {filename} uploaded to {bucket_name}.'