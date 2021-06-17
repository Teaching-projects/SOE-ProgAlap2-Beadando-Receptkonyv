import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['figure.figsize'] = (50,20) 
plt.rcParams.update({'font.size': 5}) 



x = np.array(["Almas Kevert", "Babgulyas", "Csokis Muffin","Fokhagymaleves", "Gyumolcsleves", "Halaszle", "Husleves", "Krumplis Teszta", "Lasagne", "Meggyes Retes", "Palacsinta", "Rakott Krumpli", "Spagetti", "Turogomboc", "Zoldbabos Rizs"])
y = np.array([40, 100, 25, 30, 20, 100, 195, 60, 90, 35, 35, 90, 30, 25, 35])

plt.bar(x,y)
plt.xlabel('Ételek')
plt.ylabel('Elkészítési idő')
plt.title('Ételek elkésztísi ideje')
plt.legend()
plt.show()