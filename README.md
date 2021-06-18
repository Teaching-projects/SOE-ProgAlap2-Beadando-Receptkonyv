# SOE-ProgAlap2-Beadando-Receptkonyv
Polgar Teodora

A program egy receptfüzetet mutat be, ahol a meglévő receptek mellé lehet gyűjteni újakat. 
A program elinítása után megjelenik egy grafikus felület. A bal oldalon található 3 gomb: naptár, receptkezelő, valamint egy exit gomb.
## Naptár:
A naptár részben egy naptárt találunk. Felül a két nyíllal a keresett hónapot érhetjük el.
 Az egyik napra rákattintva – ahol egy kis jel található -  a bal oldalon megjelenik a dátum, valamint az ételek neve, amit főzni  szeretnék aznap. Az étel nevére rákattintva megjelenik az étel képe, hozzávalói, valamint az elkészítésének a menete.
Az egyik napra rákattintva bal oldalon megjelenik a dátum, valamint egy „Uj EVENT“ gomb, melyre kattintva új felületet kapunk. Itt ki lehet választani a „+“ jellel a meglévő receptek közül azt az ételt, melyet el szeretnék készíteni az adott napon. A „-“ jelre kattintva pedig el lehet távolítani azt az ételt, amelyet még sem szeretnék elkészíteni. A „SAVE“ gombra kattintva pedig elmentődik az étel neve.
## Receptkezelő: 
A „Receptkezelo“ gomb megnyomása után láthatóvá válnak az eddig megadott receptek. Az egyikre rákattintva megjelenik az étel képe, hozzávalói, valamint elkészítésének menete. Lehet hozzáadni új recepteket is az „UJ RECEPT“ gomb megnyomásával. Meg lehet adni az étel nevét, majd a + gomb megnyomásával ki lehet  választani alapanyogokat a meglévő alapanyagok közül, vagy új alapanyogak is fel lehet venni. Mennyiségüket is meg lehet adni (mennyiseg, suly, terfogat). A „Kesz vagyok, Mentes!“ gombbal lehet elmenteni az új recepteket.
## Exit: 
Kilépés a grafikus felületből. 
## Plot
A „diagram.py“ elindítása után láthatóvá válik egy diagram, amely azt ábrázolja, hogy melyik étel, mennyi idő alatt készül el, percben megadva. A „diagram.png“ az elkésztett oszlopdiagram képe.

A „Kepek“ben találhatóak az ételek képei, a „Recepek“ben pedig az eddigi receptek, valamint ide lesznek elmentve az új receptek is. 
A „hozzavalok_db.json“ – ben találhatóak az eddigi hozzávalók a mértékegységeikkel.
A „mertekegysegek_db.json“ – ben találhatóak a mennyiség, a súly és a térfogat mértékegységei.
Az "event_db.json" - ben találhatóak a naptár részben elmentett ételek nevei, amelyeket el szeretnék  készíteni az adott napon.
