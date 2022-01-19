#!/usr/bin/env python3

import os
import requests
from subprocess import check_output
import urllib.request
import wget
from zipfile import ZipFile

def print_seperator():
  print()
  rows, columns = os.popen('stty size', 'r').read().split()
  print("-" * int(columns))
  print()

def init():
  print("Initializing:")
  global version, valid_versions
  temp = str(check_output(["lsb_release", "-sr"]))
  temp = temp.split("\\")
  temp = temp.pop(0)
  temp = temp.split("'")
  temp = temp.pop(1)
  version = str(temp)
  print("Retrieving valid-versions.txt...")
  wget.download("https://raw.githubusercontent.com/ShadityOS/patches/master/valid-versions.txt")
  file = open("valid-versions.txt", "r")
  valid_versions = file.read().splitlines()
  file.close()
  print_seperator()

def get_changelog(version):
  try:
    url = "https://raw.githubusercontent.com/ShadityOS/patches/master/v" + version + "-changelog.txt"
  except:
    os.system("rm valid-versions.txt")
    print("ShadityOS is up to date!")
    print()
    exit()
  file = "v" + version + "-changelog.txt"
  print("Retrieving changelog at: " + url)
  wget.download(url)
  print_seperator()
  temp = open(file, "r")
  for line in temp:
    print(line)
  os.system("rm " + file)

def is_a_valid_version(version):
  if version in valid_versions:
    return True
  else:
    return False

def get_next_version(current_version):
  version_before = False
  for item in valid_versions:
    if version_before == True:
      return item
    if item == current_version:
      version_before = True

def patch(version_to_patch):
  version = get_next_version(version_to_patch)
  get_changelog(version)
  print_seperator()
  if is_a_valid_version(version):
    value = input("Upgrade OS? This may take a while [Y/n]: ")
    print_seperator()
    if value.lower() == "n":
      print("Upgrade Aborted.")
    else:
      install_patch(version) 
  else:
    print("Patch seems to be non-existant!")

def install_patch(version):
  print("Downloading Patch...")
  wget.download("https://github.com/ShadityOS/patches/raw/master/v" + version + "-patch.zip")
  print_seperator()
  file = "v" + version + "-patch.zip"
  with ZipFile(file, "r") as zip:
    print("Extracting Patch...")
    print()
    zip.extractall()
    print("Done!")
  print_seperator()
  print("Installing Patch...")
  print()
  os.system("rm " + file)
  os.system("sh patch.sh")
  print_seperator()
  print("Cleaning Up...")
  print()
  os.system("rm -r media")
  os.system("rm patch.sh")
  print("ShadityOS Patched Successfully!")

init()

patch(version)
os.system("rm valid-versions.txt")
