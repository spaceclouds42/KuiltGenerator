from urllib.request import urlretrieve
from urllib.request import urlopen
import json


def download_gradle_scripts(project_path):
    gradlew = "https://raw.githubusercontent.com/FabricMC/fabric-example-mod/master/gradlew"
    urlretrieve(gradlew, f"{project_path}/gradlew")

    gradlew_bat = "https://raw.githubusercontent.com/FabricMC/fabric-example-mod/master/gradlew.bat"
    urlretrieve(gradlew_bat, f"{project_path}/gradlew.bat")


def download_gradle_wrapper(wrapper_path):
    gradle_wrapper = "https://github.com/FabricMC/fabric-example-mod/blob/master/gradle/wrapper/gradle-wrapper.jar" \
                     "?raw=true"
    urlretrieve(gradle_wrapper, f"{wrapper_path}/gradle-wrapper.jar")

    gradle_wrapper_props = "https://raw.githubusercontent.com/FabricMC/fabric-example-mod/master/gradle/wrapper" \
                           "/gradle-wrapper.properties"
    urlretrieve(gradle_wrapper_props, f"{wrapper_path}/gradle-wrapper.properties")


def download_lgpl(path):
    lgpl = "https://www.gnu.org/licenses/lgpl-3.0.txt"
    urlretrieve(lgpl, f"{path}/LICENSE.md")


def download_apache(path):
    url = "http://www.apache.org/licenses/LICENSE-2.0.txt"
    urlretrieve(url, f"{path}/LICENSE.md")


def download_mozilla(path):
    url = "https://www.mozilla.org/media/MPL/2.0/index.815ca599c9df.txt"
    urlretrieve(url, f"{path}/LICENSE.md")


def download_custom_license(path, url):
    urlretrieve(url, f"{path}/LICENSE.md")


def get_yarn(mc_version):
    with urlopen(f"https://meta.fabricmc.net/v1/versions/loader/{mc_version}") as url:
        data = json.loads(url.read().decode())
        return data[0]["mappings"]["version"]


def get_loader(mc_version):
    with urlopen(f"https://meta.fabricmc.net/v1/versions/loader/{mc_version}") as url:
        data = json.loads(url.read().decode())
        return data[0]["loader"]["version"]


def get_fabric_api(mc_version):
    with urlopen(f"https://api.modrinth.com/api/v1/mod/P7dR8mSH/version") as url:
        data = json.loads(url.read().decode())
        for version in data:
            for mc_ver in version["game_versions"]:
                if mc_ver == mc_version:
                    return version["version_number"]
    return "VERSION_NOT_FOUND"


def get_latest_loom():
    return "0.6-SNAPSHOT"


def download_icon(path):
    icon = "https://github.com/natanfudge/fabric-example-mod-kotlin/raw/master/src/main/resources/assets/modid/icon.png"
    urlretrieve(icon, f"{path}/icon.png")
