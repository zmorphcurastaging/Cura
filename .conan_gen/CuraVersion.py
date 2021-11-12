import os

CuraAppDisplayName = os.getenv("CURA_APP_DISPLAY_NAME", "Cura")
CuraVersion = os.getenv("CURA_VERSION", "master")
CuraBuildType = os.getenv("CURA_BUILD_TYPE", "")
CuraDebugMode = True
CuraCloudAPIRoot = os.getenv("CURA_CLOUD_API_ROOT", "https://api.ultimaker.com")
CuraCloudAccountAPIRoot = os.getenv("CURA_CLOUD_ACCOUNT_API_ROOT", "https://account.ultimaker.com")
CuraDigitalFactoryURL = os.getenv("CURA_DIGITAL_FACTORY_URL", "https://digitalfactory.ultimaker.com")
