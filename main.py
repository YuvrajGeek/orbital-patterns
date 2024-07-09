import svgwrite
import pygame, sys
import math
import os
from datetime import datetime

planets = {}
count = 0

pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Orbit Visualizer")

width = screen.get_width()
height = screen.get_height()
fps = pygame.time.Clock()
counter = 0
centre = (width//2,height//2)
show_axes = False
paused = False

lines = []
circles = []

def lines_to_svg(lines, output_file):
    # Create an SVG drawing
    dwg = svgwrite.Drawing(output_file, profile='full', size=(width, height))

    # Add a black background
    dwg.add(dwg.rect(insert=(0, 0), size=(width, height), fill=svgwrite.rgb(0, 0, 0, '%')))

    # Add a circle
    for radius in circles:
        dwg.add(dwg.circle(center=centre, r=radius, fill='none', stroke=svgwrite.rgb(100, 100, 100, '%'), stroke_width=1))
        
    # Iterate over the list of lines and add them to the SVG
    for line in lines:
        start, end = line
        dwg.add(dwg.line(start=start, end=end, stroke=svgwrite.rgb(100, 100, 100, '%'), stroke_width=1))  # White line

    # Save the drawing to the file
    dwg.save()

def from_centre(x,y):
    return (centre[0]+x,centre[1]-y)

def render():
    screen.fill((0, 0, 0))
    
    for planet in planets.values():
        planet["angle"] = planet["angle"] + planet["omega"]
        planet["x"] = planet["a"] * math.cos(planet["angle"]) # New x
        planet["y"] = planet["a"] * math.sin(planet["angle"]) # New y
        pygame.draw.circle(
            screen,
            (5, 255, 230),
            center=from_centre(planet["x"],planet["y"]),
            radius=5,
            width=25
        )
        pygame.draw.circle(
            screen,
            (0, 79, 71),
            center=centre,
            radius=planet["a"],
            width=1
        )

    if count > 1:
        for i in range(1,count):
            pygame.draw.line(
                screen,
                (255, 255, 255),
                from_centre(planets[f"{i}"]["x"], planets[f"{i}"]["y"]),
                from_centre(planets[f"{i+1}"]["x"], planets[f"{i+1}"]["y"])
            )

        for k in range(1,count):
            if counter%6 == 0:
                lines.append(
                    (from_centre(planets[f"{k}"]["x"], planets[f"{k}"]["y"]),
                     from_centre(planets[f"{k+1}"]["x"], planets[f"{k+1}"]["y"]))
                )
        for j in lines:
            pygame.draw.line(
                screen,
                (255,255,255),
                j[0],j[1]
            )

    if show_axes == True:
        pygame.draw.line(
            screen,
            (0,255,0),
            (0, height//2),
            (width, height//2)
        )
        pygame.draw.line(
            screen,
            (0,255,0),
            (width//2, 0),
            (width//2, height)
        )
        pygame.draw.line(
            screen,
            (255,0,0),
            centre,
            pygame.mouse.get_pos()
        )
    pygame.draw.circle(
        screen,
        (253, 184, 19),
        center=centre,
        radius=25,
        width=65
    )
    pygame.draw.circle(
        screen,
        (5, 255, 230),
        center=pygame.mouse.get_pos(),
        radius=5,
        width=25
    )
    pygame.draw.circle(
        screen,
        (0, 79, 71),
        center=centre,
        radius=math.sqrt((centre[0]-pygame.mouse.get_pos()[0])**2 + (centre[1]-pygame.mouse.get_pos()[1])**2),
        width=1
    )
    font = pygame.font.SysFont("monospace", 15)
    radius_display = font.render(f"Radius: {round(math.sqrt((centre[0]-pygame.mouse.get_pos()[0])**2 + (centre[1]-pygame.mouse.get_pos()[1])**2))}", 1, (255,255,255))
    mouse_pos = pygame.mouse.get_pos()
    ang = math.atan2(
        centre[1]-mouse_pos[1], mouse_pos[0]-centre[0]
    )
    angledisplay = font.render(f"Angle: {round(math.degrees(ang))}", 1, (255,255,255))
    screen.blit(radius_display, mouse_pos)
    screen.blit(angledisplay, (mouse_pos[0], mouse_pos[1]+20))


while True:
    counter += 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_q]:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                if not os.path.isdir("images"):
                    os.makedirs("images")
                lines_to_svg(lines, f"images/{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.svg");
                pygame.image.save(screen, f"images/{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.png")
            if event.key == pygame.K_a:
                show_axes = not show_axes
            if event.key == pygame.K_p:
                paused = not paused
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            count += 1
            rad = math.sqrt((centre[0]-mouse_pos[0])**2 + (centre[1]-mouse_pos[1])**2)
            ang_vel = math.sqrt(1/rad**3)*90
            ang = math.atan2(
                centre[1]-mouse_pos[1], mouse_pos[0]-centre[0]
            )
            planets[str(count)] = {
                "a":rad,
                "angle":ang,
                "omega":ang_vel,
                "x":pygame.mouse.get_pos()[0],
                "y":pygame.mouse.get_pos()[1],
            }
            circles.append(rad)
    if not paused:
      render()
    pygame.display.update()
    fps.tick(60)