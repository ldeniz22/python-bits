#!/usr/bin/python

#**************************************
#
# Purpose: Deletes all files contained older than seven days stored in the FTP folder of a RHEL server. Certified to work on RHEL 6.0.
# Author: Luis de Niz
# Date: 05/15/2014
#
#***************************************

import os, time, sys

root = "/ftproot"
folders_to_exclude = ["folder1", "folder2"]

WEEK_IN_SECS = 7*24*60*60

def cleanup():
	folders_to_walk = os.listdir(root)
	folders_to_walk = [f for f in folders_to_walk if f not in folders_to_exclude ]
	now = time.time()
	for f in folders_to_walk:
		for top_folder, dirs, files in os.walk(os.path.join(root,f),topdown=False,followlinks=False):
			print("- Current folder %s" % top_folder)
			#Walk through each file in the current subdirectory
			for name in files:
                                print("-- Current file %s" % name)
				fullpath = os.path.join(top_folder, name)
				if os.stat(fullpath).st_mtime < (now - WEEK_IN_SECS):
					print("!!!Deleting %s" % fullpath)
					os.remove(fullpath)
			for dir_name in dirs:
                #Check if the subdirectory is empty
                print("-- Current subfolder %s" % dir_name)
				fullpath = os.path.join(top_folder, dir_name)
				try:
					if (os.listdir(fullpath)==[]):
						print("!!!Deleting %s" % fullpath)
						os.rmdir(fullpath)
				except OSError as e:
					# Directoy is not empty cannot be removed.
					print("Exception thrown %s" % e)
					pass

if __name__ == "__main__":
	print("Executing script")
	cleanup()


