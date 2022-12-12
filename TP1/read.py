from turtle import title


tab = [['9', '10', '6', '29', '45'], ['3', '50', '19',
                                      '60', '65'], ['28', '240', '23', '29', '33']]
typ = "P2"
max = 255
height = len(tab)
width = len(tab[0])
title = "chien"
f = open("chien.pgm", "a")
f.write(typ)
f.write('\n')
f.write( f"# chien.pgm nbre de ligne = {height} nbre de colonne = {width}")
f.write('\n')
f.write(str(max))
f.write('\n')
for line in tab:
    f.write(' '.join([str(elem) for elem in line]))
    f.write('\n')
f.close()
