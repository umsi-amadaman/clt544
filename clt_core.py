"""Python port of Bobby Madamanchi's CLT_ShinyApp.R, with correct mixture SE."""
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import stats
NAMES=('Normal','Uniform','Gamma','Bimodal')
BLUE='#3333B2';ORANGE='#BD6110'
def simulate(n=25,repetitions=1000,mu=68.,sd=3.,separation=1.2,seed=1):
    if not 1<=n<=500 or not 5<=repetitions<=5000 or sd<=0 or not 0<=separation<=3:
        raise ValueError('Use n=1..500, repetitions=5..5000, positive base SD, separation=0..3.')
    rng=np.random.default_rng(seed);shape=(repetitions,n)
    # Same population definitions as the original R app. SD denotes base spread.
    samples={
        'Normal':rng.normal(mu,sd,shape),
        'Uniform':rng.uniform(mu-sd*np.sqrt(3),mu+sd*np.sqrt(3),shape),
        'Gamma':mu+(rng.gamma(4,3,shape)-12)*(sd/6),
        'Bimodal':mu+rng.choice([-1,1],size=shape)*separation*sd+rng.normal(0,sd/2,shape)}
    actual_sd={name:sd for name in NAMES}
    actual_sd['Bimodal']=np.sqrt((separation*sd)**2+(sd/2)**2)
    rows=[]
    for name,a in samples.items():
        rows.append({'Population':name,'Mean':mu,'Population SD':actual_sd[name],
            'Expected SE':actual_sd[name]/np.sqrt(n),'Observed SD of means':a.mean(axis=1).std(ddof=1)})
    return {'samples':samples,'summary':pd.DataFrame(rows),'n':n,'repetitions':repetitions,
            'mu':mu,'sd':sd,'separation':separation,'seed':seed}
def density(name,x,result):
    mu,sd,sep=result['mu'],result['sd'],result['separation']
    if name=='Normal':return stats.norm.pdf(x,mu,sd)
    if name=='Uniform':return stats.uniform.pdf(x,mu-sd*np.sqrt(3),2*sd*np.sqrt(3))
    if name=='Gamma':return stats.gamma.pdf((x-(mu-2*sd))/(sd/6),4,scale=3)/(sd/6)
    return .5*stats.norm.pdf(x,mu-sep*sd,sd/2)+.5*stats.norm.pdf(x,mu+sep*sd,sd/2)
def plot_rows(result,rows=('population','samples','means','pooled'),names=NAMES,overlay=True):
    rows=list(rows);names=list(names)
    fig,axs=plt.subplots(len(rows),len(names),figsize=(3.5*len(names),3.5*len(rows)),squeeze=False)
    mu,sd=result['mu'],result['sd'];xs=np.linspace(mu-5*sd,mu+5*sd,1400)
    labels={'population':'Population density','samples':'First 12 samples; orange = mean','means':'One mean per sample','pooled':'All individual observations pooled'}
    for i,row in enumerate(rows):
      for j,name in enumerate(names):
        ax=axs[i,j];a=result['samples'][name];means=a.mean(axis=1)
        if row=='population':
            ax.fill_between(xs,density(name,xs,result),color=BLUE,alpha=.25);ax.plot(xs,density(name,xs,result),color=BLUE)
        elif row=='samples':
            for k,vals in enumerate(a[:12]):
                ax.scatter(vals,np.full(len(vals),k),s=7,color=BLUE,alpha=.25)
                ax.plot([means[k]]*2,[k-.38,k+.38],color=ORANGE,lw=2)
            ax.invert_yaxis();ax.set_ylabel('Sample number')
        elif row=='means':
            ax.hist(means,bins=35,density=True,color=ORANGE,alpha=.7)
            if overlay:
                popsd=float(result['summary'].set_index('Population').loc[name,'Population SD'])
                ax.plot(xs,stats.norm.pdf(xs,mu,popsd/np.sqrt(result['n'])),color='black',lw=1.5)
        else:
            ax.hist(a.ravel(),bins=50,density=True,color='#92C5DE',alpha=.8)
            ax.plot(xs,density(name,xs,result),color=BLUE,lw=1.5)
        ax.axvline(mu,color='gray',ls=':',lw=1)
        ax.set_xlim(xs[0],xs[-1]);ax.set_title(f'{name}\n{labels[row]}',fontsize=14)
        ax.tick_params(labelsize=12)
        ax.spines[['top','right']].set_visible(False)
        if row!='samples':ax.set_ylabel('Density')
        if i==len(rows)-1:ax.set_xlabel('Value' if row!='means' else 'Sample mean')
    fig.suptitle(f"n = {result['n']} observations per sample · {result['repetitions']:,} repetitions",fontsize=13)
    fig.tight_layout(rect=(0,0,1,.96));return fig
