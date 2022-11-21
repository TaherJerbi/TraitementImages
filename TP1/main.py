fichier = open("zoo.txt", "r")
result = []
tab = []
i = 0
while (i < 3):
    l = fichier.readline()
    if (not (l.startswith("#"))):
        tab.append(l)
        i = i+1
if (tab[0].__contains__('P2') or tab[0].__contains__('P5')):
    (width, height) = tab[1].split()
    pic = fichier.readlines()
    assert len(pic) == int(height)
    for i in range(len(pic)):
        line=pic[i].split()
        assert len(line) == int(width)
        result.append(line)

print(result)
 