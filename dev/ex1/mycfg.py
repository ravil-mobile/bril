import json
import sys
import os
import argparse
import graphviz

TERMINATORS = ('ret', 'jmp', 'br')


def print_instr(block):
  for item in block:
    print(item)


def form_blocks(instrs):
  blocks = []
  curr_block = []

  for instr in instrs:
    if 'op' in instr:
      # found an instruction
      curr_block.append(instr)

      if instr['op'] in TERMINATORS:
        # found a terminator instruction
        blocks.append(curr_block)
        curr_block = []

    else:
      if 'label' not in instr:
        raise RuntimeError(f'Expected find a label, given {instr}')
      # label is going to start a new block
      curr_block = [instr]
  
  return blocks


def generate_block_map(blocks):
  out = {}
  for block in blocks:
    first_instr = block[0]
    if 'label' in first_instr:
      out[first_instr['label']] = block[1:]
    else:
      new_block_name = f'block_{len(out)}'
      out[new_block_name] = block
  return out


def get_cfg(name2block):
  out = {} 
  for name, block in name2block.items():
      last_instr = block[-1]

      succ = []
      if last_instr['op'] in ('jmp', 'br'):
        succ = last_instr['labels']

      out[name] = succ
  return out


def print_cfg(cfg, name):
  print(f'digraph {name} {{')
  for block_name, successors in cfg.items():
    for successor in successors:
      print(f'  {block_name} -> {successor};')

  print('}')

def mycfg():
  parser = argparse.ArgumentParser(description="Specify Manufacturer and Sub_Arch of the GPU")
  parser.add_argument("-f", "--file", action="store", help="file name", default='none')
  args = parser.parse_args()

  if args.file == 'none':
    prog = json.load(sys.stdin)
  else:
    if not os.path.exists(args.file):
      raise RuntimeError(f'file {args.file} does not exist')

    with open(args.file, 'r') as file:
      prog = json.load(file)

  for function in prog["functions"]:
    blocks = form_blocks(function["instrs"])
    name2block = generate_block_map(blocks)
    cfg = get_cfg(name2block)

    for block in blocks:
      print('=' * 80)
      print_instr(block)

    print_cfg(cfg=cfg, name=function['name'])



if __name__ == '__main__':
  mycfg()