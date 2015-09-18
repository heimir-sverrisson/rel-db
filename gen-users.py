#!/usr/bin/env python
import sys
import csv
from faker import Factory

def generate_users(n):
  fake = Factory.create()
  users = []
  for i in range(n):
    u = {'id': i, 'last_name': fake.last_name()}
    users.append(u)
  return users

def write_users(users, file_name):
  with open(file_name, 'wb') as csvfile:
    user_writer = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)
    for u in users:
      user_writer.writerow([u['id'], u['last_name']])
  
def main(argv):
  if(len(argv) < 2):
    print "usage: %s file-name number-of-rows" % argv[0]
    exit(1)
  n = int(argv[2])
  file_name = argv[1]
  users = generate_users(n)
  write_users(users, file_name)


if __name__ == "__main__":
  main(sys.argv)
