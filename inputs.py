def minecraft_version():
    return input("minecraft_version: ")


def fabric_api():
    return True


def mixins():
    return True


def maven_group():
    return input("maven_group: ")


def archives_base_name():
    return input("archives_base_name: ")


def mod_version():
    return input("mod_version: ")


def kotlin_version():
    return input("kotlin_version: ")


def flk_version():
    return input("fabric-kotlin-version: ")


def kx_ser_version():
    if input("use kotlinx (y/n) ").lower().startswith("y"):
        return input("kx_ser_version: ")
    else:
        return ""


def mod_license():
    switch = {
        "lgpl": "LGPL",
        "apache": "Apache",
        "mozilla": "Mozilla"
    }
    user_input = input("Choose your license (if not listed, provide link)\n - LGPL\n - Apache\n - Mozilla\n: ")
    if user_input.startswith("https"):
        return user_input
    else:
        return switch.get(user_input.lower(), "INVALID")
