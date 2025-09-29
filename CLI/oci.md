[DOCS](https://docs.oracle.com/en-us/iaas/Content/API/SDKDocs/cliinstall.htm#InstallingCLI__windows)
[Troubleshooting](https://chatgpt.com/share/68da83c2-d428-8008-9dc7-2988b9bc2075)
[OCI Python SDK](https://github.com/oracle/oci-python-sdk/releases)

## Este método no termina de forma exitosa, al menos el paso 1
# 🔹 1. Instalar la OCI CLI en Windows
```bash
python -m venv %USERPROFILE%\oci-cli-venv
%USERPROFILE%\oci-cli-venv\Scripts\activate
pip install oci-cli
```
# 🔹 2. Configurar la CLI
```bash
oci setup config
```
# 🔹 3. Probar la instalación
```bash
oci os ns get
oci os bucket list --compartment-id <OCID_DEL_COMPARTIMENTO>
oci os bucket list --compartment-id ocid1.tenancy.oc1..aaaaaaaadriltqxnkhtld6sg5vcfzomkv6qox74g4vsr7aptr6m6cbwmyyda
```
# 🔹 4. Hacerlo global (opcional)
Si quieres que oci se reconozca desde cualquier consola sin activar el venv:
- Agrega la ruta C:\Users\<TU_USUARIO>\oci-cli-venv\Scripts al PATH de Windows.
- Reinicia la consola.