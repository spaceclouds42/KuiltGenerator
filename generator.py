from os import getcwd
from os.path import join
from os import mkdir
from os import makedirs
from os import chdir
from time import sleep
from re import sub
from json import dumps

import content
import fetcher


def generate_project(mc, uses_fabric, use_mixins, maven, modid, name, version, kt_ver, flk_ver, kx_ver, mod_license):
    path = join(getcwd(), name)
    mkdir(path)
    chdir(path)
    print(f"Created directory {path}")

    maven = sub("-", "_", maven)

    generate_static_gradle_files(path)
    generate_license(path, mod_license)
    generate_readme(path, name)
    generate_gitignore(path)
    generate_gradle_props(path, mc, uses_fabric, maven, modid, version, kt_ver, flk_ver, kx_ver)
    generate_build_script(path, kx_ver, uses_fabric)
    generate_src(path, mc, maven, modid, name, mod_license, flk_ver)
    sleep(.5)


def generate_static_gradle_files(path):
    fetcher.download_gradle_scripts(path)

    settings = open("settings.gradle", "w")
    settings.write(content.settings_gradle_content)
    settings.close()

    wrapper_path = join(path, "gradle/wrapper")
    makedirs(wrapper_path)
    fetcher.download_gradle_wrapper(wrapper_path)


def generate_license(path, mod_license):
    if mod_license.lower() == "lgpl":
        fetcher.download_lgpl(path)
    elif mod_license.lower() == "apache":
        fetcher.download_apache(path)
    elif mod_license.lower() == "mozilla":
        fetcher.download_mozilla(path)
    elif mod_license.startswith("https"):
        fetcher.download_custom_license(path, mod_license)
    else:
        print("Your license is not currently supported")


def generate_readme(path, name):
    readme = open(f"{path}/README.md", "w")
    readme.write(f"### {name}")
    readme.close()


def generate_gradle_props(path, mc, uses_fabric, maven, modid, version, kt_ver, flk_ver, kx_ver):
    props = open(f"{path}/gradle.properties", "a")
    props.write(
        f"""kotlin.code.style=official
org.gradle.jvmargs=-Xmx1G

# Fabric Properties
# Check these on https://modmuss50.me/fabric.html
minecraft_version={mc}
yarn_mappings={fetcher.get_yarn(mc)}
loader_version={fetcher.get_loader(mc)}

"""
    )

    if uses_fabric:
        props.write(f"# Fabric API\nfabric_version={fetcher.get_fabric_api(mc)}")

    props.write(
        f"""
loom_version={fetcher.get_latest_loom()}

# Mod Properties
mod_version={version}
maven_group={maven}
archives_base_name={modid}

# Kotlin
kotlin_version={kt_ver}
fabric_kotlin_version={flk_ver}
"""
    )

    if not kx_ver == "":
        props.write(f"kx_ser_version={kx_ver}")

    props.close()


def generate_gitignore(path):
    ignore = open(f"{path}/.gitignore", "w")
    ignore.write(content.gitignore)
    ignore.close()


def generate_src(path, mc, maven, modid, name, mod_license, flk_version):
    flattened_id = sub("-", "_", modid)
    src_path = join(path, "src/main")
    makedirs(src_path)

    package_path = sub("\\.", "/", maven)

    java_path = join(src_path, f"java/{package_path}/{flattened_id}/mixin")
    makedirs(java_path)

    kt_path = join(src_path, f"kotlin/{package_path}/{flattened_id}")
    makedirs(kt_path)
    generate_common_kt(kt_path, f"{maven}.{flattened_id}")

    resource_path = join(src_path, "resources")
    mkdir(resource_path)
    generate_mod_json(resource_path, mc, maven, modid, name, mod_license, flk_version)
    generate_mixin_json(resource_path, flattened_id, f"{maven}.{flattened_id}.mixin")
    print("Finalizing..")
    assets_path = join(resource_path, f"assets/{flattened_id}")
    makedirs(assets_path)
    fetcher.download_icon(assets_path)


def generate_mod_json(path, mc, maven, modid, name, mod_license, flk_version):
    print("Generating fabric.mod.json, will require user input to complete (you can leave any of them blank)")

    description = input(f"Description of {name}: ")
    author = input("Author: ")
    home = input("Homepage: ")
    source = input("Source Code Link: ")
    issues = input("Issues Page: ")

    if mod_license.startswith("https"):
        license_name = input("Custom license detected; Please enter license name: ")
    else:
        license_name = mod_license

    side = input("Environment (client/server/*): ").lower()
    if side != "client" and side != "server":
        side = "*"
    flattened_id = sub("-", "_", modid)

    json = {
        "schemaVersion": 1,
        "id": modid,
        "version": "${version}",
        "name": name,
        "description": description,
        "authors": [
            author
        ],
        "contact": {
            "homepage": home,
            "sources": source,
            "issues": issues
        },
        "license": license_name,
        "icon": f"assets/{flattened_id}/icon.png",
        "environment": side,
        "entrypoints": {
            "main": [
                {
                    "value": f"{maven}.{flattened_id}.Common::INSTANCE"
                }
            ]
        },
        "mixins": [
            f"{flattened_id}.mixins.json"
        ],
        "depends": {
            "fabricloader": ">=0.7.1",
            "fabric": "*",
            "fabric-language-kotlin": f">={flk_version}",
            "minecraft": f"^{mc}"
        }
    }

    mod = open(f"{path}/fabric.mod.json", "w")
    mod.write(dumps(json, indent=2))
    mod.close()


def generate_mixin_json(path, modid, mixin_package):
    json = {
        "required": True,
        "package": mixin_package,
        "compatibilityLevel": "JAVA_8",
        "mixins": [

        ],
        "injectors": {
            "defaultRequire": 1
        }
    }

    mod = open(f"{path}/{modid}.mixins.json", "a")
    mod.write(dumps(json, indent=2))
    mod.close()


def generate_common_kt(path, package):
    common = open(f"{path}/Common.kt", "w")
    common.write(f"package {package}")
    common.write(
        """

import net.fabricmc.api.ModInitializer

object Common : ModInitializer {
    override fun onInitialize() {
        println("Hello World")
    }
}

"""
    )

    common.close()


def generate_build_script(path, kx_ver, uses_fabric):
    script = open(f"{path}/build.gradle", "a")
    script.write(
        """plugins {
    id \"fabric-loom\" version \"$loom_version\"
    id \"maven-publish\"
    id \"org.jetbrains.kotlin.jvm\" version \"$kotlin_version\"
"""
    )

    if not kx_ver == "":
        script.write("    id \"org.jetbrains.kotlin.plugin.serialization\" version \"$kotlin_version\"\n")

    script.write(
        """    id \"org.jetbrains.dokka\" version \"$kotlin_version\"
}

sourceCompatibility = JavaVersion.VERSION_1_8
targetCompatibility = JavaVersion.VERSION_1_8

archivesBaseName = project.archives_base_name
version = project.mod_version
group = project.maven_group

minecraft {
    
}

repositories {
    maven { url = "http://maven.fabricmc.net/" }
    maven { url = "https://dl.bintray.com/kotlin/kotlin-eap" }
    maven { url = "https://dl.bintray.com/kotlin/dokka" }
    mavenCentral()
}

dependencies {
    // To change the versions see the gradle.properties file
    minecraft "com.mojang:minecraft:${project.minecraft_version}"
    mappings "net.fabricmc:yarn:${project.yarn_mappings}:v2"
    modImplementation "net.fabricmc:fabric-loader:${project.loader_version}"
"""
    )

    if uses_fabric:
        script.write(
            """
    // Fabric API
    modImplementation "net.fabricmc.fabric-api:fabric-api:${project.fabric_version}"
"""
        )

    script.write(
        """
    // Kotlin
    modImplementation "net.fabricmc:fabric-language-kotlin:${project.fabric_kotlin_version}"
"""
    )

    if not kx_ver == "":
        script.write(
            "    implementation \"org.jetbrains.kotlinx:kotlinx-serialization-core:${project.kx_ser_version}\"\n"
        )

    script.write(
        """    implementation "org.jetbrains.kotlin:kotlin-stdlib-jdk8"

    // PSA: Some older mods, compiled on Loom 0.2.1, might have outdated Maven POMs.
    // You may need to force-disable transitiveness on them.
}

processResources {
    inputs.property "version", project.version

    from(sourceSets.main.resources.srcDirs) {
        include "fabric.mod.json"
        expand "version": project.version
    }

    from(sourceSets.main.resources.srcDirs) {
        exclude "fabric.mod.json"
    }
}

// ensure that the encoding is set to UTF-8, no matter what the system default is
// this fixes some edge cases with special characters not displaying correctly
// see http://yodaconditions.net/blog/fix-for-java-file-encoding-problems-with-gradle.html
tasks.withType(JavaCompile) {
    options.encoding = "UTF-8"
}

// Loom will automatically attach sourcesJar to a RemapSourcesJar task and to the "build" task
// if it is present.
// If you remove this task, sources will not be generated.
task sourcesJar(type: Jar, dependsOn: classes) {
    classifier = "sources"
    from sourceSets.main.allSource
}

jar {
    from "LICENSE"
}

// configure the maven publication
publishing {
    publications {
        mavenJava(MavenPublication) {
            // add all the jars that should be included when publishing to maven
            artifact(remapJar) {
                builtBy remapJar
            }
            artifact(sourcesJar) {
                builtBy remapSourcesJar
            }
        }
    }

    // select the repositories you want to publish to
    repositories {
        // uncomment to publish to the local maven
        // mavenLocal()
    }
}

compileKotlin.kotlinOptions.jvmTarget = "1.8"
compileKotlin {
    kotlinOptions {
        jvmTarget = "1.8"
    }
}
compileTestKotlin {
    kotlinOptions {
        jvmTarget = "1.8"
    }
}
"""
    )

    script.close()
