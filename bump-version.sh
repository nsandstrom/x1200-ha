#!/bin/bash

# Function to bump the version
bump_version() {
  local version=$1
  local part=$2

  IFS='.' read -r -a parts <<< "$version"

  case $part in
    major)
      parts[0]=$((parts[0] + 1))
      parts[1]=0
      parts[2]=0
      ;;
    minor)
      parts[1]=$((parts[1] + 1))
      parts[2]=0
      ;;
    patch|*)
      parts[2]=$((parts[2] + 1))
      ;;
  esac

  echo "${parts[0]}.${parts[1]}.${parts[2]}"
}

# Path to the manifest.json file
manifest_path="custom_components/x1200/manifest.json"

# Read the current version from manifest.json
current_version=$(grep '"version":' "$manifest_path" | sed -E 's/.*"version": "([^"]+)".*/\1/')

# Determine the part to bump (patch by default)
part=${1:-patch}

# Get the new version
new_version=$(bump_version "$current_version" "$part")

# Update the version in manifest.json
sed -i '' -E "s/\"version\": \"$current_version\"/\"version\": \"$new_version\"/" "$manifest_path"

# Stage the manifest.json file
git add "$manifest_path"

# Commit the changes with the new version number in the message
git commit -m "version to $new_version"

# Create and push a git tag with the new version number
git tag "$new_version"
git push origin "$new_version"