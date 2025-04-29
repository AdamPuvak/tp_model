1. Spust get_data_from_database.py
2. Spust split_from_db.py
3. Spust preprocessing.py - pozor cd TEST v terminali, nahrad aj nazvy podla toho ktore data chces
4. merge_data_vzors.py ich mergne dokopy 

5. modelIsUserOwnerOfData.py overuje ci sa jedna o daneho pouzivatela resp. patria tieto data tomu uzivatelovi ? true / false 

vyhladaj #ZMENIT v model.py tam vies menit vstupne udaje (POZOR 2x aj vstup aj vystup model nazov)

v ./ folderi je optimized_xgb_model.pkl (2min trening) to je z model.py (potom je este jeden model v old.py, rychle trenovanie s rovnakou uspesnostou)