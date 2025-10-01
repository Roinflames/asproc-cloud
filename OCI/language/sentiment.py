import oci
from oci.ai_language.ai_service_language_client import AIServiceLanguageClient
from oci.ai_language.models import BatchDetectLanguageSentimentsDetails, TextDocument

# --- Configuración ---
config = oci.config.from_file()
compartment_id = "ocid1.tenancy.oc1..aaaaaaaadriltqxnkhtld6sg5vcfzomkv6qox74g4vsr7aptr6m6cbwmyyda" 

# Textos para analizar
documentos = [
    TextDocument(key="doc1", text="El servicio al cliente fue excelente, resolvieron mi problema rápidamente.", language_code="es"),
    TextDocument(key="doc2", text="Estoy muy decepcionado con la calidad del producto, no lo recomiendo.", language_code="es"),
    TextDocument(key="doc3", text="El paquete llegó a tiempo, pero el embalaje estaba dañado.", language_code="es")
]

# --- Cliente y llamada a la API ---
language_client = AIServiceLanguageClient(config)
batch_details = BatchDetectLanguageSentimentsDetails(
    documents=documentos,
    compartment_id=compartment_id
)

try:
    response = language_client.batch_detect_language_sentiments(
        batch_detect_language_sentiments_details=batch_details
    )
    
    print(response.data)

    # print("Resultados del Análisis de Sentimiento:")
    for doc in response.data.documents:
        if doc.aspects:
            aspect = doc.aspects[0]
            print(f"- Documento '{doc.key}':")
            print(f"  - Sentimiento: {aspect.sentiment}")
            print(
                f"  - Scores -> Positivo: {aspect.scores['Positive']:.2f}, "
                f"Negativo: {aspect.scores['Negative']:.2f}, "
                f"Neutral: {aspect.scores['Neutral']:.2f}"
                f"Neutral: {aspect.scores['Mixed']:.2f}"
            )
            print(f"  - Aspect: {aspect}")
            print("-------------------------------------")

except oci.exceptions.ServiceError as e:
    print(f"Error al llamar al servicio de OCI Language: {e.status} {e.message}")
