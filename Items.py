import pygame

TILE_SIZE=40

#load images
mulberry_img = pygame.image.load("Images/Food/mulberry.png")
peanuts_img = pygame.image.load("Images/Food/peanuts.png")
raspberry_img = pygame.image.load("Images/Food/raspberry.png")


item_boxes={
  'Mulberry'  : mulberry_img,
  'Peanuts'  : peanuts_img,
  'Raspberry' : raspberry_img,
}

class Item(pygame.sprite.Sprite):
  def __init__ (self, item_type, x, y):
    pygame.sprite.Sprite.__init__(self)
    self.item_type = item_type
    self.image=item_boxes[self.item_type]
    self.rect=self.image.get_rect()
    self.rect.midtop = (x+TILE_SIZE//2,y+(TILE_SIZE-self.image.get_height()))
    
  def update(self, player):
    #check if the player has picked up the box
    if pygame.sprite.collide_rect(self, player):
      #check what kind of box it was
      if self.item_type == 'Mulberry':
        player.mulberry+=2
        print("Mulberry")
      if self.item_type == 'Peanuts':
        player.peanuts+=5
        print("Peanuts")
      if self.item_type == 'Raspberry':
        player.raspberry+=3
        print("Raspberry")

      #delete the item box
      self.kill()