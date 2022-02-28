import pygame
import math
pygame.init()

WIDTH, HEIGHT = 800, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Planet Simulation")
background = pygame.image.load('background.png')

#sunimg = pygame.image.load('sun.png')


White = (248,254,255)
Yellow = (250,232,150)
Blue = (173,216,230)
Red = (211,125,16)
Dark_Grey = (80, 79, 81)
LightOrange = (241,170,80)


#to write the distances from sun:

FONT = pygame.font.SysFont("comic sans", 16)


class Planet:

    AU = 149.6e6 * 1000
    G = 6.67428e-11
    SCALE = 250 / AU      #1AU = 100 pixels
    Timestep = 3600 * 24    #1 day

    def __init__(self, x, y, radius, colour, mass):
        self.x = x
        self.y = y
        self.radius = radius
        self.colour = colour
        self.mass = mass
        #self.image = image

        self.orbit = []   #keeps track of all the points the plants has hit to draw the circle
        self.sun = False
        self.distance_to_sun = 0

        self.x_vel = 0
        self.y_vel = 0

    def draw(self, win):
        x = self.x * self.SCALE + WIDTH / 2
        y = self.y * self.SCALE + HEIGHT / 2

        if len(self.orbit) > 2:
            updated_points = []
            for point in self.orbit:
                x, y = point
                x = x * self.SCALE + WIDTH/2
                y = y * self.SCALE + HEIGHT / 2
                updated_points.append((x, y))

            pygame.draw.lines(win, self.colour, False, updated_points, 2)


        pygame.draw.circle(win, self.colour, (x, y), self.radius)


        if not self.sun:
            distance_text = FONT.render(f"{round(self.distance_to_sun/1000, 1)}km", 1, White)
            win.blit(distance_text, (x - distance_text.get_width()/2, y - distance_text.get_height()/2))



    def attraction(self, other):
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y

        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

        if other.sun:
            self.distance_to_sun = distance

        force = self.G * self.mass * other.mass / distance ** 2
        theta = math.atan2(distance_y, distance_x)
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force
        return force_x, force_y

    def update_position(self, planets):
        total_fx = total_fy = 0
        for planet in planets:
            if self == planet:
                    continue

            fx, fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy

        self.x_vel += total_fx / self.mass * self.Timestep
        self.y_vel += total_fy / self.mass * self.Timestep

        self.x += self.x_vel * self.Timestep
        self.y += self.y_vel * self.Timestep
        self.orbit.append((self.x, self.y))




def main():
        run = True
        clock = pygame.time.Clock()
        #WIN.fill(White)
        #pygame.display.update() - dont want it white


        sun = Planet(0, 0, 30, Yellow, 1.98892*10**30)
        sun.sun = True
        earth = Planet(-1 * Planet.AU, 0, 16, Blue, 5.9742 * 10 ** 24)
        earth.y_vel = 29.783 * 1000
        mars = Planet(-1.524 * Planet.AU, 0, 12, Red, 6.39 * 10 ** 23)
        mars.y_vel = 24.007 * 1000
        mercury = Planet(0.387 * Planet.AU, 0, 8, Dark_Grey, 3.3 * 10 ** 23)
        mercury.y_vel = -47.4 * 1000
        venus = Planet(0.723 * Planet.AU, 0, 14,LightOrange, 4.8685 * 10**24)
        venus.y_vel = -35.02 * 1000

        planets = [sun, earth, mars, mercury, venus]

        while run:
            clock.tick(60)  #updates loop max 60x per sec so our code isnt going too fast
            #WIN.fill((0, 0, 0))
            WIN.blit(background, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            for planet in planets:
                #now call the update position method funtion on all planets to get them to move

                planet.update_position(planets)
                planet.draw(WIN)



            pygame.display.update()

        pygame.quit()


main()
