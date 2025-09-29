En OCI Functions, el flujo es así:

🔹 Pasos previos que necesitas hacer

Crear un repositorio en OCIR (Oracle Cloud Infrastructure Registry):

Ve a: Developer Services > Container Registry.

Crea un repository con el nombre que quieras (por ejemplo fn-repo).

Este repositorio va a almacenar la imagen de tu función en formato Docker.

Instalar OCI CLI y Fn Project (si no lo tienes):

Las funciones en OCI se desarrollan y empacan con Fn Project CLI.

Desde tu máquina local debes instalar fn y loguearte contra OCIR.

fn create context <context-name> --provider oracle
fn update context oracle.compartment-id <ocid-compartment>
fn update context api-url https://functions.<region>.oraclecloud.com
fn update context registry <region-key>.ocir.io/<tenancy-namespace>/<repo-name>


Construir y subir la imagen de tu función:

Dentro de la carpeta de tu función (ejemplo en Python):

fn init --runtime python fn-hello
cd fn-hello
fn -v deploy --app <nombre-de-tu-app>


Este comando construye la imagen, la sube a OCIR y la conecta con la aplicación de Functions que creaste.

Volver a Create Function en la consola:

Ahora sí, cuando abras la pantalla, en Repository aparecerá el repositorio que creaste en OCIR.

Y en Image, se desplegarán las imágenes que subiste con fn deploy.