from enum import Enum

class Trait(Enum):
    def __new__(cls, *args, **kwds):
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = value
        return obj

    def __init__(self, seq):
        self.seq = seq
        
    REPRODUCTIVE_DRIVE = 1      #Will to reproduce
    
    #ow fertile I am. Affected by -> Age, Sex, Ability to Reproduce
    FERTILITY = 2               
    SPEED = 11                  #How fast I move
    AGILITY = 12                #How agile I am
    RESISTENCE = 14             #My resistance
    VISUAL_RANGE = 20           #How far I see
    SENSE_RANGE = 21
    MATE_SELECTION = 22
    PARENTAL_CARE = 23
    ARMOR = 30
    CAMOUFLAGE = 31
    COUNTER_ATTACK = 32
    DEFENSIVE_WILLINGNESS = 33
    AGRESSIVINESS = 40
    STRENGTH = 41
    LOUDNESS = 50
    SIGNAL_RANGE = 51
    ENCODING_COMPLEXITY = 52
    DECODING_COMPLEXITY = 53
    PRECISE_COMMUNICATION = 54
    SCAVENGING_EFFICIENCE = 60
    RESOURCE_STORAGE = 61
    METABOLIC_RATE = 70
    BASE_NEED_FOR_ENERGY = 71
    STARVATION_RESISTENCY = 72
    LEADERSHIP = 80
    OBEDIENCY = 81
    
    