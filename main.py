from re import sub
from re import search
from string import capwords
from time import sleep

import inputs
import fetcher
import generator


def main():
    this_version = "1.0.1"
    latest_version = fetcher.get_latest_of_this()
    print("FabriKGenerator, the simplest way to generate a Fabric Kotlin mod")
    print(f"Using version {this_version}")
    if latest_version != this_version:
        print(f"There's a newer version! Download v{latest_version} for the latest features")
        sleep(2)

    print()

    # Inputs
    mc = inputs.minecraft_version()
    fabric = inputs.fabric_api()
    mixins = inputs.mixins()
    maven_group = inputs.maven_group()
    modid = inputs.archives_base_name()
    mod_name = capwords(sub("-", " ", modid))
    mod_version = inputs.mod_version()
    print()

    flk_name = fetcher.get_kotlin()
    kotlin_version = search(""".+kotlin\.(.+)""", flk_name).group(1)
    flk_version = flk_name
    kx_ser_version = inputs.kx_ser_version()
    print("Fetching Kotlin versions...\n")

    mod_license = inputs.mod_license()

    print()
    print(f"Generating {mod_name} ({maven_group}.{modid}) v{mod_version}")

    print(f"MC version {mc}", end="")
    if fabric:
        print(f" with fabric api version {fetcher.get_fabric_api(mc)}")
    else:
        print()

    print(f"Kotlin version {kotlin_version}")
    print(f"Fabrik-Language-Kotlin version {flk_version}")
    if kx_ser_version == "":
        print()
    else:
        print(f"Kotlinx serialization version {kx_ser_version}")

    print(f"Using {mod_license} license")
    print()

    generator.generate_project(
        mc=mc,
        uses_fabric=fabric,
        use_mixins=mixins,
        maven=maven_group,
        modid=modid,
        name=mod_name,
        version=mod_version,
        kt_ver=kotlin_version,
        flk_ver=flk_version,
        kx_ver=kx_ser_version,
        mod_license=mod_license
    )


if __name__ == "__main__":
    main()
