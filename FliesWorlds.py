from PhysicsObjects import Entity, Material, Spawner, Text
from Suntherland import corner_rectangle, center_rectangle, ramp
from LinAlg import Vector3


def spawner(x, y):
    x += 1
    y += 1
    return Spawner(name="",
                   shape=center_rectangle(20, 20),
                   material=Material(density=0),
                   location=Vector3(x, y, 0),
                   color=(0, 200, 20),
                   affects_force=False,
                   )


def text(x, y, msg):
    x += 1
    y += 1
    return Text(name="",
                text=msg,
                shape=center_rectangle(10, 10),
                material=Material(density=0),
                location=Vector3(x, y, 0),
                color=(30, 30, 30),
                affects_force=False,
                )


def builder(x, y, width, height, color, jump=True):
    name = "builder" if jump else ""
    return Entity(name=name,
                  shape=corner_rectangle(width, height),
                  material=Material(density=0, friction=0.05),
                  color=color,
                  location=Vector3(x, y, 0))


def builder_rotate(x, y, width, height, color):
    x += width / 2
    y += height / 2
    return Entity(name="builder",
                  shape=center_rectangle(width, height),
                  material=Material(density=0, friction=0.05),
                  color=color,
                  location=Vector3(x, y, 0),
                  rvel=0.1)


def ramp_builder(x, y, width, height, color):
    return Entity(name="builder",
                  shape=ramp(width, height),
                  material=Material(density=0, friction=0.01),
                  color=color,
                  location=Vector3(x, y, 0))


def killer(x, y, width, height):
    return Entity(name="killer",
                  shape=corner_rectangle(width, height),
                  material=Material(density=0),
                  color=(255, 0, 0),
                  location=Vector3(x, y, 0),
                  affects_force=False)


def make_world_a():
    dark_color = (20, 20, 20)
    a_safe_color = (191, 6, 249)
    a_object_color = (9, 83, 246)
    return [
        builder(320, 320, 400, 40, a_safe_color),
        builder(320, 460, 320, 40, a_object_color),
        builder(320, 360, 40, 100, a_object_color),
        builder(600, 360, 40, 100, a_object_color),
        # post long jump
        builder(2560, 320, 320, 40, a_safe_color),
        # wall climb
        builder(2840, 360, 40, 440, a_object_color),
        builder(2560, 800, 320, 40, a_object_color),
        # dark wall intro platform
        builder(2400, 600, 160, 40, a_safe_color),
        builder(2360, 640, 40, 160, dark_color, False),
        builder(2400, 800, 160, 40, dark_color, False),
        # stairs
        builder(1920, 680, 160, 40, a_object_color),
        builder(1600, 840, 160, 40, a_object_color),
        # big block
        builder(1480, 640, 80, 480, dark_color, False),
        builder(1280, 840, 160, 40, a_object_color),
        # Enter the maze
        builder(960, 920, 160, 40, a_safe_color),
        builder(840, 960, 80, 480, dark_color, False),
        builder(320, 920, 480, 40, a_object_color),
        builder(320, 1120, 40, 160, a_object_color),
        builder(320, 1480, 480, 40, a_object_color),
        # Exit the maze safe area
        builder(960, 1240, 160, 40, a_safe_color),
        builder(1760, 1240, 160, 40, a_safe_color),
        # The box
        builder(2160, 1120, 160, 40, a_object_color),
        builder(2160, 1320, 160, 40, dark_color, False),
        builder(2120, 1160, 40, 160, dark_color, False),
        builder(2320, 1160, 40, 160, dark_color, False),
        # Elevator
        builder(2560, 1120, 320, 40, a_object_color),
        builder(2560, 1280, 320, 40, a_object_color),
        builder(2560, 1440, 320, 40, a_object_color),
        builder(2560, 1600, 320, 40, a_object_color),
        # tube slide
        builder(2520, 1360, 40, 400, dark_color, False),
        builder(2440, 1560, 40, 320, dark_color, False),
        builder(2240, 1440, 160, 40, a_safe_color),
        # long jump stairs
        builder(2080, 1520, 160, 40, a_object_color),
        builder(1920, 1600, 160, 40, a_object_color),
        builder(1440, 1720, 480, 40, a_object_color),
        # dark and safe spot
        builder(1020, 1720, 240, 40, dark_color, False),
        builder(1280, 1600, 160, 40, a_safe_color),
        # safe spot post jump
        builder(320, 1720, 160, 40, a_safe_color),
        # ceiling practice
        builder(480, 1760, 40, 480, a_object_color),
        builder(320, 2320, 160, 40, dark_color, False),
        builder(480, 2320, 240, 40, a_object_color),
        builder(720, 2320, 40, 40, dark_color, False),
        builder(960, 2320, 160, 40, dark_color, False),
        builder(960, 2080, 160, 40, a_safe_color),
        # spinny
        builder_rotate(1340, 1980, 40, 480, a_object_color),
        # last safe
        builder(1440, 2840, 160, 40, a_safe_color),
        builder(1600, 2840, 480, 40, a_object_color),
    ] + texts + spawners + killers


def make_world_b():
    dark_color = (20, 20, 20)
    b_safe_color = (191, 6, 249)
    b_object_color = (246, 172, 9)
    return [
        # Spawn Box
        builder(320, 320, 400, 40, b_safe_color),
        # First platforms
        builder(800, 320, 160, 40, b_object_color),
        builder(1120, 320, 320, 40, b_object_color),
        # wall obstacle
        builder(1480, 400, 80, 160, b_object_color),
        # running jump
        builder(1600, 320, 440, 40, b_object_color),
        builder(2560, 320, 320, 40, b_safe_color),
        # dark wall intro platform
        builder(2400, 600, 160, 40, b_safe_color),
        # stairs
        builder(2080, 600, 160, 40, b_object_color),
        builder(1760, 760, 160, 40, b_object_color),
        # enter the maze
        builder(960, 920, 160, 40, b_safe_color),
        builder(840, 960, 80, 480, dark_color, False),
        builder(480, 960, 40, 160, b_object_color),
        builder(480, 1280, 40, 160, b_object_color),
        # Exit the maze safe area
        builder(960, 1240, 160, 40, b_safe_color),
        # Long jumps
        builder(1120, 1240, 160, 40, b_object_color),
        builder(1440, 1400, 160, 40, b_object_color),
        builder(1760, 1240, 160, 40, b_safe_color),
        # Elevator
        builder(2560, 1040, 320, 40, b_object_color),
        builder(2560, 1200, 320, 40, b_object_color),
        builder(2560, 1360, 320, 40, b_object_color),
        builder(2560, 1520, 320, 40, b_object_color),
        builder(2560, 1680, 320, 40, b_object_color),
        # tube slide
        builder(2520, 1360, 40, 400, dark_color, False),
        builder(2440, 1560, 40, 320, dark_color, False),
        builder(2240, 1440, 160, 40, b_safe_color),
        # safe spot
        builder(1280, 1600, 160, 40, b_safe_color),
        # long jump
        builder(480, 1720, 320, 40, b_object_color),
        builder(320, 1720, 160, 40, b_safe_color),
        # ceiling practice
        builder(760, 2320, 200, 40, b_object_color),
        builder(320, 2320, 160, 40, dark_color, False),
        builder(680, 2320, 80, 40, dark_color, False),
        builder(960, 2320, 160, 40, dark_color, False),
        builder(960, 2080, 160, 40, b_safe_color),
        # spinny
        builder_rotate(1080, 2420, 40, 480, b_object_color),
        # last safe
        builder(1440, 2840, 160, 40, b_safe_color),
        builder(2560, 2840, 160, 40, b_object_color),
        # last block
        builder(3000, 2880, 40, 160, b_object_color),
    ] + spawners + texts + killers


killers = [
        killer(0, 0, 3200, 160),
        killer(0, 160, 160, 2880),
        killer(0, 3040, 3200, 160),
        killer(3040, 160, 160, 2720),
]

spawners = [
    spawner(2720, 400),
    spawner(1040, 1000),
    spawner(1040, 1320),
    spawner(1840, 1320),
    spawner(2320, 1520),
    spawner(400, 1800),
    spawner(1040, 2160),
    spawner(1520, 2920),
]

texts = [
    text(480, 370, "You've been trapped! Use your left and right arrow keys to move..."),
    text(560, 370, "Thankfully you can use your down arrow key to change the map whenever you get stuck..."),
    text(700, 370, "You can jump with the up arrow key..."),
    text(940, 370, "Double-jump by pressing the up arrow key again while airborne..."),
    text(1400, 370, "You can even double-jump after falling off a platform..."),
    text(2000, 370, "You can hold your spacebar to zoom out for a better view..."),
    text(2020, 370, "You might need a running start for this jump..."),
    text(2650, 370, "Jump into a green square to set your spawnpoint..."),
    text(2800, 370, "You can repeatedly jump into walls and ceilings to move up or around them..."),
    text(2440, 650, "Dark walls cannot be jumped on, unless you still have a double-jump available..."),
]
