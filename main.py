import matplotlib.pyplot as plt
from matplotlib import animation
from matplotlib.patches import Circle, Arrow

import numpy as np

from particles import Particles
from rotor import Rotor

rotor = Rotor()
particles = Particles(rotor=rotor)

fig = plt.figure()
subplot_shape = (2,4)
ax = plt.subplot2grid(subplot_shape, (0,0), rowspan=2, colspan=3)
ax_cumulative_theta = plt.subplot2grid(subplot_shape, (0,3) )
ax_cumulative_theta.xaxis.set_ticks([])

ax_cumulative_v_theta = plt.subplot2grid(subplot_shape, (1,3) )

plt.tight_layout()

ax_main_objs = []
cumulative_plot = None
cumulative_v_plot = None

def init():
    global ax_main_objs
    global cumulative_plot
    global cumulative_v_plot

    ax.clear()
    for s in ['top', 'bottom', 'left', 'right']:
        ax.spines[s].set_linewidth(2)
    ax.set_aspect('equal', 'box')
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.xaxis.set_ticks([])
    ax.yaxis.set_ticks([])
    ax.scatter([rotor.fixed_point[0]], [rotor.fixed_point[1]], marker='o', color='black', s=5)

    ax_cumulative_theta.clear()
    ax_cumulative_v_theta.clear()

    ax_main_objs = []
    for particle in particles.particles:
        circle = Circle(
            xy=(particle.x, particle.y),
            radius=particle.radius
        )
        ax.add_patch(circle)
        ax_main_objs.append(circle)
    rotor_line = plt.Line2D(
        (rotor.fixed_point[0], rotor.free_point[0]),
        (rotor.fixed_point[1], rotor.free_point[1]),
        color='black',
        alpha=1,
        lw=0.5
    )
    ax.add_line(rotor_line)
    ax_main_objs.append(rotor_line)

    cumulative_plot = ax_cumulative_theta.plot(
        rotor.theta_history
    )[0]
    ax_cumulative_theta.set_ylim(-np.pi, np.pi)
    ax_cumulative_theta.axhline(0, ls='--', c='k')
    ax_cumulative_theta.set(title='Rotor Angle')
    ax_cumulative_theta.xaxis.set_ticks([])

    cumulative_v_plot = ax_cumulative_v_theta.plot(
        rotor.v_theta_history
    )[0]
    ax_cumulative_v_theta.axhline(0, ls='--', c='k')
    ax_cumulative_v_theta.set(title='Rotor Speed')
    ax_cumulative_v_theta.xaxis.set_ticks([])
    ax_cumulative_v_theta.yaxis.set_ticks([])

    return ax_main_objs + [cumulative_plot, ax_cumulative_theta] + [cumulative_v_plot, ax_cumulative_v_theta]


def animate(i):
    print(i)
    particles.step()
    for i, p in enumerate(particles.particles):
        ax_main_objs[i].center = (p.x, p.y)
    ax_main_objs[-1].set_data(
        (rotor.fixed_point[0], rotor.free_point[0]),
        (rotor.fixed_point[1], rotor.free_point[1])
    )
    
    history_len = len(rotor.theta_history)
    history_x = list(range(history_len))

    cumulative_plot.set_data(
        history_x,
        rotor.theta_history
    )
    ax_cumulative_theta.set_xlim(0, history_len + 1)

    cumulative_v_plot.set_data(
        history_x,
        rotor.v_theta_history
    )
    ax_cumulative_v_theta.set_xlim(0, history_len + 1)
    ax_cumulative_v_theta.set_ylim(min(0, min(rotor.v_theta_history)*1.1), max(rotor.v_theta_history)*1.1+1e-9)


    return ax_main_objs + [cumulative_plot, ax_cumulative_theta] + [cumulative_v_plot, ax_cumulative_v_theta]


def save_animation(anim, save, filename='movie.mp4'):
    if save:
        Writer = animation.writers['ffmpeg']
        writer = Writer(fps=30, bitrate=1800)
        anim.save(filename, writer=writer)
    else:
        plt.show()


def do_animation(save=False, interval=1, filename='collision.mp4'):
    try:
        anim = animation.FuncAnimation(
            fig,
            animate,
            init_func=init,
            frames=1_000,
            interval=interval,
            blit=False
        )
    finally:
        save_animation(anim, save, filename)


do_animation(save=True)
