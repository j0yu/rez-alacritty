# -*- coding: utf-8 -*-

name = "alacritty"

# Vendor packages: <vendor_version>+local.<our_version>
__version__ = "0.4.3"
version = __version__ + "+local.1.0.0"

description = "A cross-platform, GPU-accelerated terminal emulator."

authors = ["Joseph Yu"]

variants = [
    ["platform-linux", "arch-x86_64"],
    # ["platform-macos", "arch-x86_64"],
    # ["platform-windows", "arch-x86"],
    # ["platform-windows", "arch-x86_64"],
]

tools = ["alacritty"]
# @late()
# def tools():
#     import os
#     bin_path = os.path.join(str(this.root), 'bin')
#     executables = []
#     for item in os.listdir(bin_path):
#         path = os.path.join(bin_path, item)
#         if os.access(path, os.X_OK) and not os.path.isdir(path):
#             executables.append(item)
#     return executables

build_command = r"""
set -euf -o pipefail

# Setup: curl "{CURL_FLAGS}" ...
# Show progress bar if output to terminal, else silence
declare -a CURL_FLAGS
CURL_FLAGS=("-L")
[ -t 1 ] && CURL_FLAGS+=("-#") || CURL_FLAGS+=("-sS")

cp "$REZ_BUILD_SOURCE_PATH"/Dockerfile \
    "$REZ_BUILD_SOURCE_PATH"/install-dependencies \
    "$REZ_BUILD_SOURCE_PATH"/entrypoint \
    "$REZ_BUILD_PATH"/

IIDFILE=$(mktemp "$REZ_BUILD_PATH"/DockerImageXXXXXX)
docker build --iidfile="$IIDFILE" --build-arg "VERSION={version}" "$REZ_BUILD_PATH"
# Successfully built 7f40cc613be9
# docker: Error response from daemon: No such image: sha256:0c305c5dfdf96edb2c3b0a66d0aa610ee267fc9d954b7d35801c58568674516d.


if [[ $REZ_BUILD_INSTALL -eq 1 ]]
then
    RUN_ARGS=("--env" "INSTALL_PATH=$REZ_BUILD_INSTALL_PATH")
    [ -t 1 ] && RUN_ARGS+=("-it") || :
    RUN_ARGS+=("$(cat $IIDFILE)")

    CONTAINER_ID=$(docker create "{RUN_ARGS}")
    docker start -ia "$CONTAINER_ID"
    docker cp "$CONTAINER_ID":"$REZ_BUILD_INSTALL_PATH"/. "$REZ_BUILD_INSTALL_PATH"
    docker rm "$CONTAINER_ID"
fi
""".format(
    version=__version__, CURL_FLAGS="${{CURL_FLAGS[@]}}", RUN_ARGS="${{RUN_ARGS[@]}}"
)


def commands():
    """Commands to set up environment for ``rez env alacritty``"""
    import os

    env.PATH.append(os.path.join("{root}", "bin"))
    env.XDG_DATA_DIRS.append(os.path.join("{root}", "share"))
