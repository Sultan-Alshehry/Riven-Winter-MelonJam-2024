import pygame

import constants


# Define our generic object class
# give it all the properties and methods of pygame.sprite.Sprite
class BaseObject(pygame.sprite.Sprite):

    def __init__(self, sprite, position, object_type, size=(32, 32), hitbox_size=None, animation=None, register=True, offset=None):
        super(BaseObject, self).__init__()
        self.position = position
        self.object_type = object_type
        self.size = size
        if not hitbox_size:
            self.hitbox_size = size
        else:
            self.hitbox_size = hitbox_size
        self.offset = offset

        # creates the visible texture
        self.sprite = pygame.transform.scale(sprite, self.size)
        self.animation = animation
        self.on_animation_finish = self.animation_finished
        self.flip = False

        # creates the "hit-box"
        self.rect = pygame.transform.scale(sprite, self.hitbox_size).get_rect(center=self.position)

        # adds object to a list of objects
        if register:
            self.add_to_game_object_list()

    def add_to_game_object_list(self):
        constants.game.objects.append(self)

    def add_to_game_decoration_list(self):
        constants.game.decorations.append(self)

    def move(self, direction):
        self.position += direction
        self.rect.center = self.position  # Update the rect position

    # updates the sprite
    def update(self):
        pass
        # pygame.sprite.Sprite.update(self)

    # draws the object on the screen
    def draw(self):
        # camera = constants.game.camera
        # if camera.zoom != 1:
        #     constants.game.screen.blit(pygame.transform.scale(self.sprite, (int(self.sprite.get_width() * camera.zoom), int(self.sprite.get_height() * camera.zoom))), (self.rect.topleft - constants.game.camera.position)*camera.zoom)
        # else:
        if self.animation:
            self.sprite = self.animation.get_current_frame(constants.game.time, on_finish=self.on_animation_finish)
        if self.offset:
            constants.game.screen.blit(self.sprite, (self.rect.topleft[0] + self.offset[0], self.rect.topleft[1] + self.offset[1]))
        else:
            constants.game.screen.blit(self.sprite, self.rect.topleft)


    def delete_from_game_object_list(self):
        constants.game.objects.remove(self)

    def play_animation(self, animation):
        self.animation = animation

    def animation_finished(self):
        pass

    def flip_sprite_horiz(self):
        self.sprite = pygame.transform.flip(self.sprite, True, False)
        if self.animation is not None:
            self.animation.flip()
