import string

from selenium.webdriver.remote.webelement import WebElement

class CharProp:
    def __init__(self, value, dataState, slot_chance, non_chances_slot, webElement):
        self.value = value
        self.dataState = dataState
        self.webElement = webElement
        self.slot_chances = []
        self.non_chances_slots = []
        if slot_chance is not None:
            self.slot_chances.append(slot_chance)
        if non_chances_slot is not None:
            self.non_chances_slots.append(non_chances_slot)
        
    def setSlotChance(self, slotChance):
        self.slot_chances.append(slotChance)

    def setNonSlotChance(self, nonSlotChance):
        self.non_chances_slots.append(nonSlotChance)

    def setDataState(self, dataState):
        self.dataState = dataState

    def toPrint(self):
        print('value:'+self.value)
        print('dataState:'+self.dataState)
        if self.slot_chances:
            print(str(self.slot_chances)[1:-1])
        if self.non_chances_slots:
            print(str(self.non_chances_slots)[1:-1])
