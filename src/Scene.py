from abc import ABCMeta, abstractmethod, abstractproperty
from RenderableObject import RenderableObject


class Scene(metaclass=ABCMeta):
    """
    Abstract class for scenes.
    Inherit this class to create a new scene.
    """

    @abstractproperty
    def objects(self) -> [RenderableObject]:
        pass

    @abstractmethod
    def tick(self, ticks):
        for game_object in self.objects:
            game_object.tick(ticks)

    @abstractmethod
    def render(self): pass  # Defined in Engine.py

    def scene_did_start(self):
        """
        Fires when the current scene starts up.
        :return: None
        """
        pass

    def scene_will_start(self):
        """
        Fires right before a scene will start, so the scene has a chance to get it's objects ready.
        :return:
        """
        pass

    def will_chance_scene(self):
        """
        Optional method that will fire if the current scene will change.
        Gives the current scene a chance to clean up.
        :return: None
        """
        pass

    def key_pressed(self, key: str):
        """

        :param key:
        :return:
        """
        pass

    def __init__(self):
        self.objects = []
