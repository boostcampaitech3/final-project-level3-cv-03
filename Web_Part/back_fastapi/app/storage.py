from google.cloud import storage

def create_new_bucket(bucket_name : str, blob_name : str, path_to_file : str):
    # 새 bucket 만들기
    new_bucket = storage_client.create_bucket(bucket_name, location="asia-northeast3")
    new_blob = new_bucket.blob(blob_name)
    new_blob.upload_from_filename(path_to_file)
    return

def upload_to_bucket(bucket_name : str, blob_name : str, path_to_file : str):
    # 버킷 목록 확인
    #print(list(storage_client.list_buckets()))
    
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.upload_from_filename(path_to_file)
    
    # 접근권한 public으로 설정
    # blob.make_public()
    
    # 접근권한 public 시, 파일 url 만들어주기
    # url = blob.public_url
    # return url
    return 

def download_from_bucket(bucket_name : str, blob_name : str, path_to_file : str):
    storage_client = storage.Client()
    # 버킷 목록 확인
    # print(list(storage_client.list_buckets()))
    bucket = storage_client.bucket(bucket_name)
    print(storage_client.list_buckets())
    blob = bucket.blob(blob_name)
    blob.download_to_filename(path_to_file)
    # return content
    return "Blob {} downloaded to {}.".format(
            blob_name, path_to_file
        )