import oci

# Cargar configuración desde ~/.oci/config
config = oci.config.from_file()

# Cliente de Object Storage
object_storage = oci.object_storage.ObjectStorageClient(config)

# Datos de tu bucket
namespace = "axmtlntfagbi"   # el que te apareció en la consulta
bucket_name = "bucket-20250928-2036"

# Archivo local y nombre en el bucket
file_path = "ejemplo.txt"
object_name = "ejemplo.txt"

with open(file_path, "rb") as f:
    obj = object_storage.put_object(
        namespace,
        bucket_name,
        object_name,
        f
    )

print("✅ Archivo subido:", obj)
