#!/usr/bin/env python
import sys
import csv

DATA_ROWS = 10
INDEX_ROWS = 10

def pre_graph():
  print "digraph g {"
  print "rankdir=LR"
  # print "rotate=90"

def post_graph():
  print "}"

def pre_subgraph(sub_id, name):
  print "subgraph cluster%d{" % (sub_id)
  print "label=\"%s\"" % (name)

def post_subgraph():
  print "}"

def create_blocks(u, node_prefix, rows_per_block):
  no_nodes = len(u) // rows_per_block
  if (len(u) % rows_per_block) != 0:
    no_nodes += 1
  j = 0
  blocks = []
  ports = []
  for i in range(no_nodes):
    port_names = {}
    block = []
    block.append("  %s_%d[shape=record,label=\"%s %d\\l|" % (node_prefix, i, node_prefix, i))
    while j < len(u):
      last_name = u[j]['last_name']
      id = u[j]['id']
      port_names[id] = "%s_%d:%d" % (node_prefix, i, id) 
      label_str = "    <%d> (%d) %s\\l" % (id, id, last_name)
      last_label = (j == len(u)-1) or  (((j+1) % rows_per_block) == 0)
      j += 1
      if last_label:
        block.append(label_str)
        break
      else:
        block.append(label_str + '|')
    block.append("  \"];")
    blocks.append(block)
    ports.append(port_names)
  return ports, blocks

# Only interested in the n first and last blocks
def link(src, dst, n):
  link_str = []
  dst_keys = {}
  blocks = len(dst)
  # Find all the visible dst rows
  for i in range(blocks):
    if (i < n) or (i == blocks -1):
      for key in dst[i]:
        dst_keys[key] = i
  blocks = len(src)
  # Find all visible src rows
  for i in range(blocks):
    if (i < n) or (i == blocks -1):
      for key in src[i]:
        if key in dst_keys:
          j = dst_keys[key]
          print "%s -> %s" % (src[i][key], dst[j][key])

# Print only n first and the last block
def print_blocks(blocks, n):
  block_no = 0
  last_no = len(blocks) - 1
  for block in blocks:
    if (block_no < n) or (block_no == last_no):
      for line in block:
        print line
    block_no += 1

def nth_users(users, n):
  user_subset = []
  for i in range(len(users)):
    if (i % n) == 0:
      user_subset.append(users[i])
  return user_subset


def make_level(level, data, level_name, block_size, first_blocks):
  pre_subgraph(level, level_name)
  data_names,data_blocks = create_blocks(data, level_name, DATA_ROWS)
  print_blocks(data_blocks, first_blocks)
  post_subgraph()
  return data_names,data_blocks


def read_users(file_name):
  users = []
  with open(file_name, 'rb') as csvfile:
    u_reader = csv.reader(csvfile)
    for u in u_reader:
      users.append({'id': int(u[0]), 'last_name': u[1]})
  return users


def main(argv):
  if(len(argv) < 3):
    print "usage: %s file-name level" % argv[0]
    exit(1)
  file_name = argv[1]
  level = int(argv[2])
  users = read_users(file_name)
  pre_graph()
  data_names,data_blocks = make_level(0, users, 'Data', DATA_ROWS, 4)
  if level > 0:
    s_users = sorted(users, key=lambda user: user['last_name'])
    index_names,index_blocks = make_level(1, s_users, 'Leaf', INDEX_ROWS, 4)
    if level > 1:
      index1_users = nth_users(s_users, INDEX_ROWS)
      index1_names,index1_blocks = make_level(2, index1_users, 'Index', INDEX_ROWS, 4)
      if level > 2:
        index2_users = nth_users(index1_users, INDEX_ROWS)
        index2_names,index1_blocks = make_level(3, index2_users, 'Root', INDEX_ROWS, 4)

        link(index2_names, index1_names, 4)
      link(index1_names, index_names, 4)
    link(index_names, data_names, 4)

  post_graph()


if __name__ == "__main__":
  main(sys.argv)
