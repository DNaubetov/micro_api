import uuid

from models.pin import PinData, PinDataPost, PinControl
from models.plant import Plant, AddPlant
from models.controller import Controller

flower1 = Plant(plant_id=uuid.uuid4(), name='Цветок 1', capacity=10000,
                pin_soil=PinData(pin_num=36),
                pin_pomp=PinControl(pin_num=15), num_p=1)

flower2 = Plant(plant_id=uuid.uuid4(), name='Цветок 2', capacity=20000,
                pin_soil=PinData(pin_num=39),
                pin_pomp=PinControl(pin_num=2), num_p=2)

flower3 = Plant(plant_id=uuid.uuid4(), name='Цветок 3', capacity=20000,
                pin_soil=PinData(pin_num=34),
                pin_pomp=PinControl(pin_num=4), num_p=3)

flower4 = Plant(plant_id=uuid.uuid4(), name='Цветок 4', capacity=20000,
                pin_soil=PinData(pin_num=32),
                pin_pomp=PinControl(pin_num=16), num_p=4)

flower5 = Plant(plant_id=uuid.uuid4(), name='Цветок 5', capacity=10000,
                pin_soil=PinData(pin_num=33),
                pin_pomp=PinControl(pin_num=17), num_p=5)
#
esp32 = Controller(plants_list=[flower1, flower2, flower3, flower4, flower5])
