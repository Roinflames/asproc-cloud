import oci

config = oci.config.from_file()
object_storage = oci.object_storage.ObjectStorageClient(config)

namespace = "axmtlntfagbi"
bucket_name = "bucket-20250928-2036"
object_name = "ejemplo.txt"
download_path = "descargado.txt"

response = object_storage.get_object(namespace, bucket_name, object_name)

with open(download_path, "wb") as f:
    for chunk in response.data.raw.stream(1024 * 1024, decode_content=False):
        f.write(chunk)

print("✅ Archivo descargado en:", download_path)
