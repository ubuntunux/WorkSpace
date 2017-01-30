# -*- coding: utf-8 -*-
'''
Created on 14 July 2012

@author: Marco Baxemyr
'''
import math

from pygame import sprite
from pygame import Rect
from vector import Vector
import math

from utils import *
from constants import *

class Ball(sprite.Sprite):

    thud_sound = None
    
    def __init__(self, image_surface, position, direction, is_time_distortion_field_active, attached=False, attach_pos=0):
        sprite.Sprite.__init__(self)
        if Ball.thud_sound is None:
            Ball.thud_sound = load_sound("explosion_dull.wav")
            Ball.thud_sound.set_volume(0.25)
        self.image = image_surface
        self.radius = (self.image.get_width() / 2) - 1
        self.density = 1
        self.mass = (4.0 / 3.0) * math.pi * self.radius ** 3 * self.density
        self.speed = 550.
        self.orig_speed = self.speed
        self.is_time_distortion_field_active = is_time_distortion_field_active
        self.rect = Rect(0, 0, self.image.get_width(), self.image.get_height())
        self.move(Vector(position[0], position[1]))
        self.direction = direction.get_normalized()
        self.has_passed_paddle=False
        self.damage = 1
        self.score = 0
        self.combo = 0
        self.combo_length = 0
        self.attached_to_paddle = attached
        self.attach_pos = attach_pos
        
    def update(self, time_passed, paddle, balls, normal_blocks, invulnerable_blocks):
        """
        Moves the ball forward and handles collisions with walls and the passed objects.
        time_passed: the time passed in seconds since last call
        paddle: the paddle sprite
        blocks: the group of the block sprites
        """
        if self.is_time_distortion_field_active() and self.pos.get_y() > 520:
            self.speed = 200.
        else:
            self.speed = self.orig_speed
        
        if self.attached_to_paddle:
            self.keep_on_paddle(paddle)
            return
        
        displacement = Vector(self.direction.get_x() * self.speed * time_passed,
                              self.direction.get_y() * self.speed * time_passed)
        new_pos = self.pos+displacement
        old_pos = self.pos
        
        self.keep_within_bounds(new_pos, old_pos, time_passed)
        
        self.check_and_handle_paddle_collision(paddle, new_pos, old_pos, time_passed)

        self.check_and_handle_ball_collision(balls, new_pos, old_pos, time_passed)
        
        block_collision_new_pos = self.check_and_handle_block_collision(new_pos, old_pos, time_passed, normal_blocks, invulnerable_blocks)
        if block_collision_new_pos:
            self.move(block_collision_new_pos)
            return
        
        self.move(new_pos)
    
    def combo_done(self):
        self.score += self.combo
        self.combo = 0
        self.combo_length = 0
    
    def move(self, position):
        self.pos = position
        self.rect.center = (position.get_x(), position.get_y())
    
    def keep_on_paddle(self, paddle):
        topleft = paddle.rect.topleft
        pos = Vector(topleft[0] + (paddle.rect.width / 4) + (self.attach_pos * (2 * self.radius + 1)), topleft[1] - self.radius)
        self.move(pos)
    
    def keep_within_bounds(self, new_pos, old_pos, time_passed):
        if new_pos.get_x() - self.radius < LEFT_BOUND:
            self.direction = Vector(abs(self.direction.get_x()), self.direction.get_y())
            displacement = Vector(self.direction.get_x() * self.speed * time_passed,
                              self.direction.get_y() * self.speed * time_passed)
            new_pos = old_pos+displacement
        elif new_pos.get_x() + self.radius > RIGHT_BOUND:
            self.direction = Vector(-abs(self.direction.get_x()), self.direction.get_y())
            displacement = Vector(self.direction.get_x() * self.speed * time_passed,
                              self.direction.get_y() * self.speed * time_passed)
            new_pos = old_pos+displacement
        elif new_pos.get_y() - self.radius < 0:
            self.direction = Vector(self.direction.get_x(), abs(self.direction.get_y()))
            displacement = Vector(self.direction.get_x() * self.speed * time_passed,
                              self.direction.get_y() * self.speed * time_passed)
            new_pos = old_pos+displacement
        elif new_pos.get_y() - self.radius > SCREEN_HEIGHT:
            self.combo_done()
            self.kill()
    
    def check_and_handle_paddle_collision(self, paddle, new_pos, old_pos, time_passed):
        if new_pos.get_y() + self.radius >= (PADDLE_HEIGHT_POS) and (new_pos.get_x() + self.radius > paddle.rect.left and new_pos.get_x() - self.radius < paddle.rect.right) and not self.has_passed_paddle:
            offset_from_middle = (new_pos.get_x() - paddle.rect.centerx) / (paddle.rect.width / 2)
            #self.direction = Vector(self.direction.get_x()+offset_from_middle, -abs(self.direction.get_y())).get_normalized()
            self.direction = (Vector(offset_from_middle, min(-abs(self.direction.get_y()), -0.1)).get_normalized() * 0.90 + self.direction * 0.10).get_normalized()
            displacement = Vector(self.direction.get_x() * self.speed * time_passed,
                                  self.direction.get_y() * self.speed * time_passed)
            new_pos = old_pos+displacement
            self.combo_done()
        elif new_pos.get_y() >= paddle.rect.bottom: #- (paddle.rect.height / 2.5):
            self.has_passed_paddle = True

    def check_and_handle_ball_collision(self, balls, new_pos, old_pos, time_passed):
        other_balls = balls.copy()
        other_balls.remove(self)
        for ball in other_balls:
            if ball.attached_to_paddle:
                other_balls.remove(ball)
        collided_balls = sprite.spritecollide(self, other_balls, False, sprite.collide_circle)
        other_balls.empty()
        if collided_balls:
            collided_ball = collided_balls[0] #only collide with one ball
            delta_vector = self.pos - collided_ball.pos
            axis_vector = delta_vector.get_normalized() #collision axis, along which we should apply changes
            self_velocity = (self.direction * self.speed)
            collided_ball_velocity = (collided_ball.direction * collided_ball.speed)
            relative_velocity =  collided_ball_velocity - self_velocity
            if axis_vector:
                relative_velocity_on_axis = axis_vector.dot(relative_velocity)

                if relative_velocity_on_axis > 0.0: #are the balls traveling towards each other?
                    #current velocities along collision axis
                    u1 = axis_vector.dot(self_velocity)
                    u2 = axis_vector.dot(collided_ball_velocity)

                    #calculate new velocities
                    i = self.mass * u1 + collided_ball.mass * u2
                    r = -(u2 - u1)

                    massSum = self.mass + collided_ball.mass
                    v1 = (i - collided_ball.mass * r) / massSum
                    v2 = (i + self.mass * r) /massSum

                    self_velocity = self_velocity + (axis_vector * (-u1 + v1))
                    collided_ball_velocity = collided_ball_velocity + (axis_vector * (-u2 + v2))
                    #self.speed = self_velocity.get_length()
                    #collided_ball.speed = collided_ball_velocity.get_length()
                    self.direction = self_velocity.get_normalized()
                    collided_ball.direction = collided_ball_velocity.get_normalized()

                    displacement = Vector(self.direction.get_x() * self.speed * time_passed,
                                  self.direction.get_y() * self.speed * time_passed)
                    new_pos = old_pos+displacement
                
    
    def check_and_handle_block_collision(self, new_pos, old_pos, time_passed, normal_blocks, invulnerable_blocks):
        self.move(new_pos) #move the sprite forward to be able to check collision with other sprites
        
        blocks = normal_blocks.copy()
        blocks.add(invulnerable_blocks.sprites())
        
        collided_blocks = sprite.spritecollide(self, blocks, False, sprite.collide_rect)
        blocks.empty() #remove all blocks from the temporary group, otherwise the sprites will soon find themselves in thousands of groups
        if collided_blocks:
            top_or_bottom_hit, left_or_right_hit = False, False
            for block in collided_blocks:
                if (old_pos.get_y() < block.rect.centery) and (old_pos.get_x() < (block.rect.right + self.radius)) and (old_pos.get_x() > (block.rect.left - self.radius)):
                    top_or_bottom_hit = True
                if (old_pos.get_y() > block.rect.centery) and (old_pos.get_x() < (block.rect.right + self.radius)) and (old_pos.get_x() > (block.rect.left - self.radius)):
                    top_or_bottom_hit = True
                if (old_pos.get_x() < block.rect.centerx) and (old_pos.get_y() < (block.rect.bottom + self.radius)) and (old_pos.get_y() > (block.rect.top - self.radius)):
                    left_or_right_hit = True
                if (old_pos.get_x() > block.rect.centerx) and (old_pos.get_y() < (block.rect.bottom + self.radius)) and (old_pos.get_y() > (block.rect.top - self.radius)):
                    left_or_right_hit = True
                
                if not (top_or_bottom_hit or left_or_right_hit):
                    #No collision with circle detected
                    pass
                else:
                    self.combo_length += 1
                    score = block.damage(self.damage)
                    self.combo += int(score * (self.combo_length * 0.3)) / int(1 + self.combo_length * 0.1)
                    Ball.thud_sound.play()
                
            
            if top_or_bottom_hit:
                self.direction = Vector(self.direction.get_x(), -self.direction.get_y())
            if left_or_right_hit:
                self.direction = Vector(-self.direction.get_x(), self.direction.get_y())

            displacement = Vector(self.direction.get_x() * self.speed * time_passed,
                                      self.direction.get_y() * self.speed * time_passed)
            return old_pos+displacement
    
    def release_from_paddle(self):
        previously_attached = self.attached_to_paddle
        self.attached_to_paddle = False
        return previously_attached
    
    def is_traveling_down(self):
        return self.direction.get_y() > 0
