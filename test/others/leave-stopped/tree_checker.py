#!/usr/bin/python2

import os
import sys


def get_thread_status(thread_dir):
	for line in open(os.path.join(thread_dir, "status")).readlines():
		if line.startswith("State:"):
			return line.split(":", 1)[1].strip().split(' ')[0]
	return None


def is_process_stopped(pid):
	tasks_dir = "/proc/{}/task".format(pid)

	for thread_dir in os.listdir(tasks_dir):
		thread_status = get_thread_status(os.path.join(tasks_dir, thread_dir))
		if not thread_status == "T":
			return False

	thread_status = get_thread_status("/proc/{}".format(pid))
	if not thread_status == "T":
		return False

	return True


def check_tree(root_pid):
	if not is_process_stopped(root_pid):
		print "Process with pid {} is not stopped.".format(root_pid)
		return False

	f_children_path = "/proc/{0}/task/{0}/children".format(root_pid)

	with open(f_children_path, "r") as f_children:
		for line in f_children:
			for child_pid in line.strip().split(" "):
				if not check_tree(int(child_pid)):
					return False

	return True


if __name__ == "__main__":
	if not check_tree(sys.argv[1]):
		sys.exit(1)
