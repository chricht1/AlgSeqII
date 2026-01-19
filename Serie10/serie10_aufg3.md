# Aufgabe 10.3

Im Vorlesungsskript sind die rekursiven Berechnungsvorschriften für die Berechnung der Matrizen W, V und WM gegeben.

Die Matrix WM an (i,j) hängt von V an (i,j) ab, die anderen Matrizen hängen aber nur von Einträgen der anderen Matrizen an Positionen (i',j') mit i < i' < j' < j ab. Daher könnte man zunächst für jede Position (i,j) im Zuker-Algorithmus, zuerst V_ij und dann entweder WM_ij oder W_ij berechnen. Die Positionen (i,j) könnte man analog zum Nussinov rekursiv mit (i,j)=(1,L) beginnend in einem Baum, der durch die Rekursionsvorschrift gebildet wird, von dessen Blättern hin zur Wurzel berechnen.