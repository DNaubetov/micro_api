import uuid

from models.pin import Pin, AddPinData, PinControl
from models.plant import Plant, AddPlant
from models.controller import Controller

flower1 = Plant(plant_id=uuid.uuid4(), name='Rose red', capacity=500,
                pin_soil=Pin(pin_num=32),
                pin_pomp=PinControl(pin_num=2))

flower2 = Plant(plant_id=uuid.uuid4(),name='Rose blue', capacity=600,
                pin_soil=Pin(pin_num=36),
                pin_pomp=PinControl(pin_num=4))

# flower3 = Plant(plant_id=uuid.uuid4(), name='Rose white', capacity=700,
#                 pin_soil=Pin(pin_num=34),
#                 pin_pomp=PinControl(pin_num=15))
#
# flower4 = Plant(plant_id=uuid.uuid4(), name='Rose yellow', capacity=800,
#                 pin_soil=Pin(pin_num=35),
#                 pin_pomp=PinControl(pin_num=16))
#
esp32 = Controller(plants_list=[flower1, flower2])
#
#
# a = AddPlant(name='Rose red', capacity=1,
#              pin_soil=Pin(pin_num=32),
#              pin_pomp=PinControl(pin_num=2))
#
# esp32.add_plant(a)

for i in esp32.plants_list:
    print(i.plant_id)