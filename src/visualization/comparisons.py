import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import seaborn as sns

'''
This python script contains functions, which are used in the creation of comparison graphs.
Basicaly, the code that would have been often repeated during graph creation has been put here.
'''


def corr_matrix(df, df_name, height=3, width=3, fontsize=20):
    '''
    Visualizes the correlation matrix
    '''
    sns.set_style('whitegrid')
    corr = df.corr()
    mask = np.zeros_like(corr, dtype=bool)
    mask[np.triu_indices_from(mask)] = True
    fig = plt.figure(facecolor='white')
    ax = fig.add_axes([0,0,width,height])
    vmax = np.abs(corr.values[~mask]).max()
    sns.heatmap(corr, mask=mask, cmap='viridis', vmin=-vmax, vmax=vmax,
                square=True, linecolor='black', linewidths=1, ax=ax)
    for i in range(len(corr)):
        ax.text(i+0.5,i+0.5, corr.columns[i], 
                ha='center', va='center', rotation=45, fontsize=fontsize)
        for j in range(i+1, len(corr)):
            s = '{:.3f}'.format(corr.values[i,j])
            ax.text(j+0.5,(i+0.5),s, 
                ha='center', va='center', fontsize=fontsize)
    ax.set_title(f'The correlation matrix for {df_name}', fontsize=fontsize*1.5)
    ax.axis("off")
    plt.show()

def kde_scatter_pairplot(df, df_name, fontsize=20, top=0.2):
    '''
    Visualizes pairplot with 2d kde plots below the diagonal, scatter plots above it and histograms with 1d kde on the diagonal
    '''
    sns.set_style('whitegrid')
    mpl.rcParams['axes.labelsize'] = fontsize
    mpl.rcParams['xtick.labelsize'] = fontsize
    mpl.rcParams['ytick.labelsize'] = fontsize
    fig = sns.PairGrid(df.dropna())
    fig.map_upper(plt.scatter,edgecolor='w',color='purple')
    fig.map_lower(sns.kdeplot,cmap='cool_d',shade=True)
    fig.map_diag(sns.histplot,bins=30,kde=True,color='purple')
    fig.fig.subplots_adjust(top=top)
    fig.fig.suptitle(f'KDE, histograms and scatter plots for {df_name}', fontsize=fontsize*1.5)


def risk_to_return(df, r=4, width=3, height=3, fontsize=20):
    '''
    Visualizes comparison of risk to return ratios. The dataset df must already contain the computed returns per period.
    '''
    area = np.pi*r**2
    fig = plt.figure(facecolor='white')
    ax = fig.add_axes([0,0,width,height])
    ax.scatter(df.mean(),df.std(),s=area)
    ax.set_xlabel('Return', fontsize=fontsize)
    ax.set_ylabel('Risk', fontsize=fontsize)
    ax.tick_params(axis='x', labelsize=fontsize)
    ax.tick_params(axis='y', labelsize=fontsize)
    for la, x, y in zip(df.columns, df.mean(), df.std()):
        ax.annotate(
            la,
            xy=(x,y),xytext=(15,15),
            textcoords='offset points', ha='right', va='bottom', fontsize=fontsize,
            arrowprops=dict(arrowstyle='-', connectionstyle='arc3,rad=-0.3', color='black')
        )
    ax.set_title(f'The risk to return ratios', fontsize=fontsize*1.5)
    plt.show()

def correlation_analysis(df, width=3, height=3, fontsize=20, r=4, top=.95):
    '''
    Shows correlations between prices and returns of assets using the correlation matrix, kde plot, scatter plot, histogram and risk to return ratio.
    The df must be a dataset with assets on x_axis and prices on y_axis
    '''
    rets = df.pct_change()
    print("Prices:")
    print(df.describe())
    print("Returns:")
    print(rets.describe())
    corr_matrix(df, "prices", height=height, width=width, fontsize=fontsize)
    corr_matrix(rets, "returns", height=height, width=width, fontsize=fontsize)
    kde_scatter_pairplot(df, "prices", fontsize=fontsize, top=top)
    kde_scatter_pairplot(rets, "returns", fontsize=fontsize, top=top)
    risk_to_return(rets, r=r, width=width, height=height, fontsize=fontsize)
