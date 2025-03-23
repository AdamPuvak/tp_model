Vysvetlenie jednotlivych suborov:
----------------------------------------

from_database.csv - data ziskane z databazy

sample_data.csv - manualne vytvorene data pripravene na predspracovanie (-> preprocessing.py)

preprocessed_data.csv - predspracovane data (vystup z preprocessing.py)

----------------------------------------


Vysvetlenie features:
----------------------------------------

ATMS - priemerna rychlost touch pohybu (priemer vsetkych TMS)

length - celková vzdialenosť tocuh pohybu (sucet vsetkych ciastkovych pohybov)

accel_? - priemerne zrychlenie na osi "?"
    (? - oznacenie osi (x,y,z))

total_accel - priemerne celkove zrychlenie na vsetkych troch osiach

----------------------------------------