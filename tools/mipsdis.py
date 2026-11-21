"""Desensamblador MIPS (R5900) mínimo para leer el ejecutable de Eternal Ring.
Uso: python3 -I mipsdis.py SLES_500.51 DESDE HASTA   (direcciones virtuales en hex)
"""
import struct, sys

R = ['zero','at','v0','v1','a0','a1','a2','a3','t0','t1','t2','t3','t4','t5','t6','t7',
     's0','s1','s2','s3','s4','s5','s6','s7','t8','t9','k0','k1','gp','sp','fp','ra']
BASE = 0x100000 - 0x1000  # vaddr - offset en el archivo

def s16(x): return x - 0x10000 if x & 0x8000 else x

SPECIAL = {0x20:'add',0x21:'addu',0x22:'sub',0x23:'subu',0x24:'and',0x25:'or',0x26:'xor',0x27:'nor',
           0x2a:'slt',0x2b:'sltu',0x2c:'dadd',0x2d:'daddu',0x2e:'dsub',0x2f:'dsubu',0x0a:'movz',0x0b:'movn',
           0x04:'sllv',0x06:'srlv',0x07:'srav',0x14:'dsllv',0x16:'dsrlv',0x17:'dsrav'}
SHIFT = {0x00:'sll',0x02:'srl',0x03:'sra',0x38:'dsll',0x3a:'dsrl',0x3b:'dsra',0x3c:'dsll32',0x3e:'dsrl32',0x3f:'dsra32'}
MEM = {0x20:'lb',0x21:'lh',0x23:'lw',0x24:'lbu',0x25:'lhu',0x27:'lwu',0x37:'ld',0x1e:'lq',
       0x28:'sb',0x29:'sh',0x2b:'sw',0x3f:'sd',0x1f:'sq',0x31:'lwc1',0x39:'swc1',0x1a:'ldl',0x1b:'ldr',0x2c:'sdl',0x2d:'sdr',0x22:'lwl',0x26:'lwr',0x2a:'swl',0x2e:'swr'}
IMM = {0x08:'addi',0x09:'addiu',0x0a:'slti',0x0b:'sltiu',0x0c:'andi',0x0d:'ori',0x0e:'xori',0x18:'daddi',0x19:'daddiu'}
BR = {0x04:'beq',0x05:'bne',0x14:'beql',0x15:'bnel',0x06:'blez',0x07:'bgtz',0x16:'blezl',0x17:'bgtzl'}

def dis(w, pc):
    op = w >> 26; rs = (w >> 21) & 31; rt = (w >> 16) & 31; rd = (w >> 11) & 31; sa = (w >> 6) & 31
    imm = w & 0xffff; fn = w & 63
    if w == 0: return 'nop'
    if op == 0:
        if fn in SHIFT: return f'{SHIFT[fn]} {R[rd]}, {R[rt]}, {sa}'
        if fn in SPECIAL: return f'{SPECIAL[fn]} {R[rd]}, {R[rs]}, {R[rt]}'
        if fn == 0x08: return f'jr {R[rs]}'
        if fn == 0x09: return f'jalr {R[rd]}, {R[rs]}'
        if fn in (0x18, 0x19, 0x1a, 0x1b): return f"{['mult','multu','div','divu'][fn-0x18]} {R[rs]}, {R[rt]}"
        if fn in (0x10, 0x12): return f"{'mfhi' if fn == 0x10 else 'mflo'} {R[rd]}"
        if fn == 0x0f: return 'sync'
        return f'special.{fn:02x}'
    if op == 1:
        names = {0: 'bltz', 1: 'bgez', 2: 'bltzl', 3: 'bgezl', 0x10: 'bltzal', 0x11: 'bgezal'}
        return f"{names.get(rt, 'regimm')} {R[rs]}, 0x{pc + 4 + s16(imm) * 4:x}"
    if op in (2, 3): return f"{'j' if op == 2 else 'jal'} 0x{((pc + 4) & 0xf0000000) | ((w & 0x3ffffff) << 2):x}"
    if op in BR:
        if op in (6, 7, 0x16, 0x17): return f'{BR[op]} {R[rs]}, 0x{pc + 4 + s16(imm) * 4:x}'
        return f'{BR[op]} {R[rs]}, {R[rt]}, 0x{pc + 4 + s16(imm) * 4:x}'
    if op == 0x0f: return f'lui {R[rt]}, 0x{imm:x}'
    if op in IMM:
        v = imm if op in (0x0c, 0x0d, 0x0e) else s16(imm)
        return f'{IMM[op]} {R[rt]}, {R[rs]}, {hex(v)}'
    if op in MEM:
        reg = f'f{rt}' if op in (0x31, 0x39) else R[rt]
        return f'{MEM[op]} {reg}, {hex(s16(imm))}({R[rs]})'
    if op == 0x11: return f'cop1 {w:08x}'
    if op == 0x1c: return f'mmi {w:08x}'
    return f'.word 0x{w:08x}'

def main():
    d = open(sys.argv[1], 'rb').read()
    a, b = int(sys.argv[2], 16), int(sys.argv[3], 16)
    for pc in range(a, b, 4):
        w = struct.unpack_from('<I', d, pc - BASE)[0]
        print(f'{pc:08x}: {w:08x}  {dis(w, pc)}')

if __name__ == '__main__':
    main()
