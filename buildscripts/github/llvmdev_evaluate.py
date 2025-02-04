#!/usr/bin/env python

import json
import os

event = os.environ.get("GITHUB_EVENT_NAME")
label = os.environ.get("GITHUB_LABEL_NAME")
inputs = os.environ.get("GITHUB_WORKFLOW_INPUT")
changed_files = os.environ.get("ALL_CHANGED_FILES")

flow_file = ".github/workflows/llvmdev_build.yml"
runner_mapping = {
    "linux-64": "ubuntu-24.04",
    "linux-aarch64": "ubuntu-24.04-arm",
    "osx-64": "macos-13",
    "osx-arm64": "macos-14",
    "win-64": "windows-2019",
}

default_include = [
    {   "runner": runner_mapping["linux-64"],
        "platform": "linux-64",
        "recipe": "llvmdev"},
    {
        "runner": runner_mapping["linux-aarch64"],
        "platform": "linux-aarch64",
        "recipe": "llvmdev",
    },
    {
        "runner": runner_mapping["osx-arm64"],
        "platform": "osx-arm64",
        "recipe": "llvmdev",
    },
    {
        "runner": runner_mapping["osx-arm64"],
        "platform": "osx-arm64",
        "recipe": "llvmdev_manylinux",
    },
    {   "runner": runner_mapping["win-64"],
        "platform": "win-64",
        "recipe": "llvmdev"},
    {
        "runner": runner_mapping["win-64"],
        "platform": "win-64",
        "recipe": "llvmdev_manylinux",
    },
]

print(
    f"event: '{event}', label: '{label}', inputs: '{inputs}', changed_files: '{changed_files}'"
)

if event == "pull_request" and changed_files and flow_file in changed_files.split():
    # full matrix build
    include = default_include
elif event == "label":
    # reduced matrix build
    include = default_include[0:1]
elif event == "workflow_dispatch":
    # TBD
    include = {}
else:
    include = {}
matrix = {"include": include}

print(f"matrix:\n {json.dumps(matrix, indent=4)}")

#with open(os.environ["GITHUB_OUTPUT"], "a") as fh:
#    print(f"{matrix}={json.dumps(matrix)}", file=fh)

print(f"::set-output name=matrix::{json.dumps(matrix)}")
