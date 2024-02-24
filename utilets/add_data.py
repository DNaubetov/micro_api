from models.pin import Pin
from models.plant import Plant, AddPlant
from models.controller import Controller

flower1 = Plant(name='Rose red', capacity=500,
                pin_soil=Pin(pin_num=32, pin_type='d', pin_value=False),
                pin_pomp=Pin(pin_num=2, pin_type='a', pin_value=None))

flower2 = Plant(name='Rose blue', capacity=600,
                pin_soil=Pin(pin_num=33, pin_type='d', pin_value=False),
                pin_pomp=Pin(pin_num=4, pin_type='a', pin_value=None))

flower3 = Plant(name='Rose white', capacity=700,
                pin_soil=Pin(pin_num=34, pin_type='d', pin_value=False),
                pin_pomp=Pin(pin_num=15, pin_type='a', pin_value=None))

flower4 = Plant(name='Rose yellow', capacity=800,
                pin_soil=Pin(pin_num=35, pin_type='d', pin_value=False),
                pin_pomp=Pin(pin_num=16, pin_type='a', pin_value=None))

esp32 = Controller(plants_list=[flower1, flower2, flower3, flower4])


a = AddPlant(name='Rose red', capacity=1,
             pin_soil=Pin(pin_num=32, pin_type='d', pin_value=False),
             pin_pomp=Pin(pin_num=2, pin_type='a', pin_value=None))


esp32.update_plant(esp32.plants_list[0].plant_id, a)

print(esp32.plants_list, sep='\n')


esp32.add_plant(a)
esp32.add_plant(a)
esp32.add_plant(a)
esp32.add_plant(a)

print(*esp32.plants_list[-3:-1], sep='\n')