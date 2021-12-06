# TODO: add constellation support.

from abc import ABC, abstractmethod, abstractproperty


class GrpgCharacterBase(ABC):
    """
    Represents the RPG character that you actually 
    play in the game.

    not the character from genshin.
    """

    def __init__(self):
        pass



    # @abstractmethod
    # def get_id(self):
    #     """
    #     returns the character's id
    #     equivalent to character's id from hoyolab api
    #     """
    #     pass

    @abstractmethod
    def invoke_auto(self):
        """
        objective: invokes the character's Auto(Normal) Attack 
        """
        pass

    

    @abstractmethod
    def invoke_charge(self):
        """
        invokes the character's Charge Attack."""
        pass

    @abstractmethod
    def invoke_skill(self):
        """
        invokes the character's Elemental Skill.
        """
        pass

    @abstractmethod
    def invoke_burst(self):
        """
        invokes the character's Elemental Burst.
        """
        pass

    @abstractmethod
    def take_field():
        """
        character switches on-field
        """

    @abstractmethod
    def leave_field():
        """
        character switches off-field
        """

    @abstractmethod
    def get_hp(self):
        """returns character's current hp"""

    # @abstractmethod
    # def get_hp(self):
    #     """
    #     get the remaining hp of the character.
    #     """
    #     pass

    # @abstractmethod
    # def get_buffs(self):
    #     """
    #     returns all the active buffs present on the character.
    #     """
    #     pass

    # @abstractmethod
    # def get_debuffs(self):
    #     """
    #     returns all the active debuffs present on the character.
    #     """
    #     pass


