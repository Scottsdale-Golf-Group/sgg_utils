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


def list_to_cloud_storage(bucket_name, list_of_dict, filename, timestamp=False):
    from google.cloud import storage
    import json
    import time
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    if timestamp:
        from datetime import datetime
        filename = filename.split('.')[0]
        filename = f'{filename}_{datetime.now().strftime("%Y%m%d%H%M%S")}.json'
    blob = bucket.blob(filename)
    for _ in range(5):  # Retry up to 5 times
        try:
            print("Uploading file...attempt ", _+1 )
            # Your existing code here...
            blob.upload_from_string('\n'.join(json.dumps(item) for item in list_of_dict))
            break  # If the upload succeeds, break out of the loop
        except ConnectionError:
            print("ConnectionError occurred. Retrying...")
            time.sleep(5) 
    return f'File {filename} uploaded to {bucket_name}.'