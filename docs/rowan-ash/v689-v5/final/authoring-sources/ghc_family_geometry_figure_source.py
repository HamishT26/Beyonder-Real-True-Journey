from pathlib import Path
import hashlib,html,json,os
from fractions import Fraction

BANK=Path(__file__).parent
os.environ['MPLCONFIGDIR']=str(BANK/'plot-cache')
os.environ['PYTHONDONTWRITEBYTECODE']='1'
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
BASE=Path('D:/GHC-Archives/worktrees/rowan-ash-main/docs/rowan-ash/v689-v5')
OUT=BASE/'final';FIG=OUT/'figures';FIG.mkdir(exist_ok=True)
receipt=json.loads((BASE/'x2/interpretation-receipt.json').read_bytes())
baton=json.loads((OUT/'baton-module-index.json').read_bytes())
navy='#163449';teal='#1d7a74';rust='#a44332';muted='#506675'
plt.rcParams.update({'font.size':11,'axes.labelcolor':navy,'text.color':navy,'axes.edgecolor':'#b8c8cf','svg.fonttype':'none'})
fig,axes=plt.subplots(1,3,figsize=(11.8,3.45),gridspec_kw={'width_ratios':[1,1,1.55]})
points=[(0,0),(1,0),(.5,.86)]
for ax,filled,title,beta in [(axes[0],False,'Unfilled loop',1),(axes[1],True,'Filled triangle',0)]:
    ax.add_patch(Polygon(points,closed=True,facecolor='#d5ece7' if filled else 'white',edgecolor=teal if filled else navy,linewidth=2.4))
    for i,(x,y) in enumerate(points):
        ax.scatter([x],[y],s=40,color=navy,zorder=3)
        ax.text(x,y+(.08 if i==2 else -.13),str(i),ha='center',va='center',fontsize=10)
    ax.set_title(title,fontweight='bold',fontsize=12,pad=14)
    ax.text(.5,-.34,r'$\beta_1 = '+str(beta)+'$',ha='center',fontsize=16,color=teal)
    ax.set_xlim(-.22,1.22);ax.set_ylim(-.52,1.08);ax.set_aspect('equal');ax.axis('off')
curve=receipt['euler_energy_ratio_curve'];x=[float(Fraction(r['step'])) for r in curve];y=[float(Fraction(r['energy_ratio'])) for r in curve]
ax=axes[2];ax.axvspan(0,1,color='#d5ece7',alpha=.8);ax.plot(x,y,color=navy,lw=2.6)
ax.axhline(1,color=muted,lw=1,ls='--');ax.scatter([1.5],[4],color=rust,zorder=4,s=40)
ax.annotate('step 1.5: energy x4',(1.5,4),xytext=(.63,3.65),fontsize=10,color=rust,arrowprops={'arrowstyle':'-','color':rust})
ax.set(xlim=(0,1.56),ylim=(-.15,4.3),xlabel='Explicit Euler step',ylabel='Energy after / energy before')
ax.set_title('A large step can add energy',fontweight='bold',fontsize=12,pad=12)
ax.spines[['top','right']].set_visible(False);ax.grid(axis='y',alpha=.18)
fig.suptitle('Finite models: the declared structure and assumptions matter',fontsize=14,fontweight='bold',y=1.02)
fig.tight_layout(w_pad=2)
fig.savefig(FIG/'finite-geometry.png',dpi=190,bbox_inches='tight',facecolor='white')
fig.savefig(FIG/'finite-geometry.svg',bbox_inches='tight',facecolor='white',metadata={'Date':'2026-09-10'})
plt.close(fig)

print(json.dumps({'figure_png':str(FIG/'finite-geometry.png'),'status':'RENDERED'}),flush=True)
