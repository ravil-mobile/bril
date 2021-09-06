import json
import sys

TERMINATORS = ('ret', 'jmp', 'br')

def form_blocks(instrs):
  curr_block = []
  blocks = []

  for instr in instrs:
    if 'op' in instr:
      # an actual instruction
      curr_block.append(instr)
      if instr['op'] in TERMINATORS:
        yield curr_block
        curr_block = []

    else:
      # label
      yield curr_block
      curr_block = [instr]
  
  yield curr_block

def block_map(blocks):
  out = {}
  for block in blocks:
    first_insrt = block[0]
    if 'label' in first_insrt:
      out[first_insrt['label']] = block[1:]
    else:
      new_block_name = f'block_{len(out)}'
      out[new_block_name] = block
  return out

def get_cfg(name2block):
  out = {} 
  for name, block in name2block.items():
      last_instr = block[-1]
      if 'jmp' in last_instr:
        out[name] = None
      print(block)
  return None


def mycfg():
  prog = json.load(sys.stdin)
  for function in prog["functions"]:
    name2block = block_map(form_blocks(function["instrs"]))
    cfg = get_cfg(name2block)
    print(cfg)

if __name__ == '__main__':
  mycfg()