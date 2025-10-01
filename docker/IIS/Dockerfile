# Usa una imagen base de Windows con IIS
FROM mcr.microsoft.com/windows/servercore:ltsc2022

# Instala IIS
RUN powershell -Command "Install-WindowsFeature -name Web-Server"

# Expone el puerto 80
EXPOSE 80

# Establece el comando por defecto
CMD ["cmd.exe"]
