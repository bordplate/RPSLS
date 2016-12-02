from abc import ABCMeta, abstractmethod

from RenderableObject import RenderableObject


class Scene(metaclass=ABCMeta):
    """
    Abstract class for scenes.
    Inherit this class to create a new scene.
    """

    objects = []  # type: [RenderableObject]

    width = 0
    height = 0

    @abstractmethod
    def tick(self, ticks: int):
        """
        Passes on ticks from game engine to all objects we want to have on screen.
        :param ticks: Current engine tick count. Used to animate with different frequencies.
        :return: None
        """
        for game_object in self.objects:
            game_object.tick(ticks)

    def change_scene(self, scene):
        """
        A method that the engine overwrites with a function that changes from this scene to a specified scene.
        :param scene: A scene to be changed to.
        :return: None
        """
        pass

    def scene_will_start(self):
        """
        Fires right before a scene will start, so the scene has a chance to get it's objects ready.
        When this function is called by the engine, all Engine-setup for the scenes should have finished.
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
        """
        Removes a given object from the scene
        :param scene_object: The object that should be removed from the scene.
        :return: None
        """
        for obj in self.objects:
            if obj == scene_object:
                self.objects.remove(obj)

    def __init__(self):
        """
        Initiates objects as empty, to make sure no scenes start with objects already being drawn.
        """
        self.objects = []
