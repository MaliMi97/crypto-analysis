import matplotlib.pyplot as plt
import pandas as pd

'''
This python script contains functions, which are used in the creation of line graphs.
Basicaly, the code that would have been often repeated during graph creation has been put here.
'''


def background(width=2, height=2, fontsize=40):
    '''
    Makes preparation for plotting. Returns the tuple (figure, ax, ax_background)
    '''
    fig = plt.figure(facecolor='white')
    ax = fig.add_axes([0,0,width,height])
    ax_background = ax.twinx()
    ax_background.tick_params(axis='y', labelsize=fontsize)
    ax.set_xlabel('time', fontsize=fontsize)
    ax.tick_params(axis='x', labelsize=fontsize)
    return (fig, ax, ax_background)


def with_price_in_background(time, price, width=2, height=2, fontsize=40):
    '''
    Makes a figure with twin y axes called ax, ax_background and puts the data called price in ax_background. Returns the tuple (figure, ax, ax_background)
    '''
    fig, ax, ax_background = background(width, height, fontsize)
    ax_background.plot(time,price,color='black')
    ax_background.set_ylabel('price', fontsize=fontsize)
    ax_background.semilogy()
    return (fig, ax, ax_background)

def impermanent_loss_vis(df, x, y, width=2, height=2, fontsize=40):
    '''
    Takes the data frame from function impermanent_loss in functions.impermanent_loss module as an input and plots the impermanent loss.
    '''
    fig = plt.figure(facecolor='white')
    ax = fig.add_axes([0,0,width,height])
    s = pd.concat([df['to x'],df['to y'],df['to 50/50']])
    plt.ylim(min(s)-0.1,max(s)+0.1)
    ax.set_ylabel('price', fontsize=fontsize)
    ax.tick_params(axis='y', labelsize=fontsize)
    ax.set_xlabel('time', fontsize=fontsize)
    ax.tick_params(axis='x', labelsize=fontsize)
    aux = [0 for i in range(len(df['time']))]
    ax.plot(df['time'], aux, color='black')
    ax.plot(df['time'], df['to x'], label=f"to {x}")
    ax.plot(df['time'], df['to y'], label=f"to {y}")
    ax.plot(df['time'], df['to 50/50'], label=f"to 50/50")
    ax.plot([df['time'].loc[0],df['time'].loc[len(df)-1]],[1,1])
    ax.legend(fontsize=fontsize)
    plt.show()