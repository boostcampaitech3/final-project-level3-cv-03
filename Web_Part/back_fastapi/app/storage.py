#### cloud storage #####
from google.cloud import storage

def create_new_bucket(bucket_name : str, blob_name : str, path_to_file : str):
    storage_client = storage.Client.from_service_account_json(
        './source/bitcoin-03-8813c851f085.json')
    # 새 bucket 만들기
    new_bucket = storage_client.create_bucket(bucket_name, location="asia-northeast3")
    new_blob = new_bucket.blob(blob_name)
    new_blob.upload_from_filename(path_to_file)
    return

def upload_to_bucket(bucket_name : str, blob_name : str, path_to_file : str):
    storage_client = storage.Client.from_service_account_json('./source/bitcoin-03-8813c851f085.json')
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
    storage_client = storage.Client.from_service_account_json(
        './source/bitcoin-03-8813c851f085.json')
    # 버킷 목록 확인
    # print(list(storage_client.list_buckets()))

    # ('bitcoin_storage', 'models/model.meta', 'model/model.meta')
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.get_blob(blob_name)
    # content = blob.download_as_bytes()

    ##########################test
    refer_bucket = storage_client.get_bucket('bitcoin_reference_images')
    refer_blob = refer_bucket.get_blob('12.jpg')
    # print('버킷 사진 목록', f'https://storage.googleapis.com/bitcoin_reference_images/{refer_blob.name}')

    ##################################
    
    # 디렉토리 지정 시 미리 local에 생성되어 있어야 하고 파일명은 다르게 download하셔도 괜찮습니다.
    blob.download_to_filename(path_to_file)
    # return content
    return "Blob {} downloaded to {}.".format(
            blob_name, path_to_file
        )