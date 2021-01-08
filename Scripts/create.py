import sprite as sp
import grid as gr
import location as lo
import panel_entity as pe
import entity as en
import controller as co
import controllable_entity as ce
import button as bu
import battle_entity as be
import pygame

def sprite(path, scale):
    return sp.Sprite(path, scale)

def location(x, y, raw_x, raw_y, offset_x, offset_y):
    return lo.Location(x, y, raw_x, raw_y, offset_x, offset_y)

def entity(sprite, location):
    return en.Entity(sprite, location)

def battle_entity(sprite, location, is_blue, max_health):
    return be.BattleEntity(sprite, location, is_blue, max_health)

def panel_entity(sprite, location, is_blue):
    return pe.PanelEntity(sprite, location, is_blue)

def grid(rows, columns, scale, space_between_tiles):
    return gr.Grid(rows, columns, scale, space_between_tiles)

def controllable_entity(sprite, location, is_blue, controller, max_health):
    return ce.ControllableEntity(sprite, location, is_blue, controller, max_health)

def controller():
        return co.Controller(
            bu.Button('Left', pygame.K_LEFT),
            bu.Button('Right', pygame.K_RIGHT),
            bu.Button('Up', pygame.K_UP),
            bu.Button('Down', pygame.K_DOWN))

def alt_controller():
        return co.Controller(
            bu.Button('Left', pygame.K_a),
            bu.Button('Right', pygame.K_d),
            bu.Button('Up', pygame.K_w),
            bu.Button('Down', pygame.K_s))