from init import *

class ItemNameEntry:
    def __init__(self, data):
        self.nameOffset = int.from_bytes(data[:2], 'little')
        self.descOffset = int.from_bytes(data[2:], 'little')
        self.name = ''
        self.desc = ''

def load(path, cp):
    fs = fileio.FileStream(path)

    minOffset = fs.ReadUShort()
    offsets = [minOffset]

    while fs.Position < minOffset:
        offsets.append(fs.ReadUShort())

    data = []

    for index, offset in enumerate(offsets):
        fs.Position = offset
        entry = ItemNameEntry(fs.Read(4))

        fs.Position = entry.nameOffset
        entry.name = fs.ReadMultiByte(cp)

        fs.Position = entry.descOffset
        entry.desc = fs.ReadMultiByte(cp)

        data.append(entry)

    return data

def main():
    os.chdir(os.path.dirname(__file__))

    cn = load(os.path.join(GAME_CN_PATH, 'ED6_DT02\\T_ITEM2 ._DT'), 'GBK')
    en = load(os.path.join(GAME_EN_PATH, 'ED6_DT02\\T_ITEM2 ._DT'), 'SHIFTJIS')

    assert len(cn) == len(en)

    fs = fileio.FileStream('T_ITEM2 ._DT', 'wb')

    fs.Position = len(en) * 2
    offsets = []

    for index, entry in enumerate(en):
        offsets.append(fs.Position)

        if entry.name and not cn[index].name:
            raise

        if entry.desc and not cn[index].desc:
            raise

        name = cn[index].name.encode('GBK') + b'\x00'
        desc = cn[index].desc.encode('GBK') + b'\x00'

        fs.WriteUShort(fs.Position + 4)                 # name offset
        fs.WriteUShort(fs.Position + 2 + len(name))     # desc offset
        fs.Write(name)
        fs.Write(desc)

    fs.Position = 0
    for offset in offsets:
        fs.WriteUShort(offset)

    load('T_ITEM2 ._DT', 'GBK')

if __name__ == '__main__':
    Try(main)
