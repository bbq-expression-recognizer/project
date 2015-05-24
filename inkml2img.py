from PIL import Image
import xml.etree.ElementTree as ET
from os import listdir
from os.path import isfile, join
from tex2label import Mapper

inkmlpath = 'inkml'
imgpath = 'imgall'
listfile = open(join(imgpath, 'listfile.txt'), 'w')
img_x = 28
img_y = 28
margin = 4
density = 32
mapper = Mapper('texsyms.txt')
for f in [f for f in listdir(inkmlpath) if isfile(join(inkmlpath, f))]:
    if not f.endswith('.inkml'):
        continue
    print 'Processing', f, '...'

    # find traces and trace groups
    tree = ET.parse(join(inkmlpath, f))
    root = tree.getroot()
    traces = []
    traceGroup = None
    for child in root:
        if child.tag.endswith('trace'):
            traces.append(child)
        elif child.tag.endswith('traceGroup'):
            traceGroup = child

    # convert trace elements to coordinate lists
    coord = []
    for trace in traces:
        coord.append([[float(a) for a in a.split()] for a in trace.text.split(',')])

    # group traces and get symbol
    sym = []
    tex = []
    for child in traceGroup:
        if child.tag.endswith('traceGroup'):
            tmp = []
            for child in child:
                if child.tag.endswith('traceView'):
                    tmp.append(int(child.get('traceDataRef')))
                if child.tag.endswith('annotation'):
                    tex.append(child.text)
            sym.append(tmp)

    for i in xrange(len(sym)):
        if mapper.tex2label(tex[i]) is None:
            continue
        traceref = sym[i]
        min_x = max_x = coord[sym[i][0]][0][0]
        min_y = max_y = coord[sym[i][0]][0][1]
        for j in traceref:
            for x, y in coord[j]:
                min_x = min(min_x, x)
                max_x = max(max_x, x)
                min_y = min(min_y, y)
                max_y = max(max_y, y)
        # pass one point trace
        if min_x == max_x and min_y == max_y:
            continue
        # prevent divide-by-zero
        if min_x == max_x:
            max_x = max_x + 1
        if min_y == max_y:
            max_y = max_y + 1
        x_scale = img_x / (max_x - min_x)
        y_scale = img_y / (max_y - min_y)
        if x_scale > y_scale:
            mx = (max_x + min_x) / 2
            dx = (max_x - min_x) / 2
            max_x = mx + dx / y_scale * x_scale
            min_x = mx - dx / y_scale * x_scale
        else:
            my = (max_y + min_y) / 2
            dy = (max_y - min_y) / 2
            max_y = my + dy / x_scale * y_scale
            min_y = my - dy / x_scale * y_scale

        img = Image.new('L', (img_x, img_y), 255)
        px = img.load()
        for j in traceref:
            for k in xrange(1, len(coord[j])):
                prevx = coord[j][k - 1][0]
                prevy = coord[j][k - 1][1]
                nextx = coord[j][k][0]
                nexty = coord[j][k][1]
                for t in xrange(density):
                    x = prevx + (nextx - prevx) * t / density
                    y = prevy + (nexty - prevy) * t / density
                    mx = (x - min_x) / (max_x - min_x) * (img_x - 2 * margin) + margin
                    my = (y - min_y) / (max_y - min_y) * (img_y - 2 * margin) + margin
                    px[round(mx), round(my)] = 0
        imgname = str(mapper.tex2label(tex[i])) + "_" + f.rstrip('.inkml') + '_%d.png' % i
        img.save(join(imgpath, imgname))
        listfile.write(imgname + ' ' + str(mapper.tex2label(tex[i])) + '\n')
listfile.close()
