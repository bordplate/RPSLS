from abc import ABCMeta, abstractmethod
from RenderableObject import RenderableObject


class Scene(metaclass=ABCMeta):
    """
    Abstract class for scenes.
    Inherit this class to create a new scene.
    """

    objects = []  # type: [RenderableObject]

    @abstractmethod
    def tick(self, ticks):
        for game_object in self.objects:
            game_object.tick(ticks)

    # TODO: Check if this method ever gets used in a scene.
    @abstractmethod
    def render(self): pass  # Defined in Engine.py

    def change_scene(self, scene):
        pass

    def scene_did_start(self):
        """
        Fires when the current scene starts up.
        :return: None
        """
        pass

    def scene_will_start(self):
        """
        Fires right before a scene will start, so the scene has a chance to get it's objects ready.
        :return: None
        """
        pass

    def will_change_scene(self):
        """
        Optional method that will fire if the current scene will change.
        Gives the current scene a chance to clean up.
        :return: None
        """
        pass

    def key_pressed(self, key: str):
        """
        Fires if a key has been pressed.
        :param key: Key pressed as a string. 'F' for the key F, KEY_UP for arrow-key up
        :return: None
        """
        pass

    def add_objects(self, objects: [RenderableObject]):
        """
        Add renderable objects to the screen.
        :param objects: A list containing multiple RenderableObject
        :return: None
        """
        self.objects += objects

        for scene_object in objects:
            scene_object.scene = self

    def remove_object(self, scene_object: RenderableObject):
        for obj in self.objects:
            if obj == scene_object:
                self.objects.remove(obj)

    def __init__(self):
        self.objects = []
