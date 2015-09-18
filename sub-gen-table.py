#!/usr/bin/env python
import sys
from faker import Factory

ROWS_PER_BLOCK = 10

def gprint(u):
  no_nodes = len(u) // ROWS_PER_BLOCK + 1
  j = 0
  print "digraph g {"
  for i in range(no_nodes):
    print "  subgraph block_%d{" % (i)
    print "    rankdir=TB;"
    print "    node [shape=record];"
    print "    label=\"block %d\"" % (i)
    while j < len(u):
      if (j == len(u)-1) or  (((j+1) % ROWS_PER_BLOCK) == 0):
        print "    node_%d[shape=record,label=\"%s\"];" % (u[j]['id'], u[j]['last_name'])
        j += 1
        break
      else:
        print "    node_%d[shape=record,label=\"%s\"];" % (u[j]['id'], u[j]['last_name'])
      j += 1
    print "}"
  print "}" # Close digraph

def main(argv):
  if(len(argv) < 2):
    print "usage: %s number-of-rows" % argv[0]
    exit(1)
  n = int(argv[1])
  fake = Factory.create()
  users = []
  for i in range(n):
    u = {'id': i, 'last_name': fake.last_name(), 'first_name': fake.first_name()}
    # print "[%d, %s, %s]" % (u['id'], u['last_name'], u['first_name'])
    users.append(u)
  gprint(users)


if __name__ == "__main__":
  main(sys.argv)
