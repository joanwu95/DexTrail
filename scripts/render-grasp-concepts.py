"""Render source-linked DexTrail grasping plates as PNG, SVG and selected GIFs.

All illustrations are constructed from geometry, not edited raster images.
Run with Pillow. --preview produces posters; --only SLUG updates one plate.
Website palette tokens and Windows fonts match the hand-motion edition.
"""
from pathlib import Path
from math import sin, cos, pi, atan2, hypot, acos, exp, sqrt
from functools import lru_cache
from html import escape
import argparse
import json
import re
import zipfile
from PIL import Image, ImageDraw, ImageFont, ImageColor

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'website/docs/images/knowledge/grasp-concepts-dextrail'
CSS = (ROOT / 'website/docs/stylesheets/theme.css').read_text(encoding='utf-8')
def token(name):
    return re.search(r'--atlas-'+name+r':(#[0-9a-fA-F]{6})', CSS).group(1)
PAPER, INK, ACCENT, MUTED, RULE = [token(n) for n in ['paper','ink','accent','muted','line']]
W, H, AA, FRAMES, MS = 960, 720, 2, 80, 80
def tint(color, weight):
    return '#'+''.join(f'{round(a+(b-a)*weight):02x}' for a,b in zip(ImageColor.getrgb(PAPER),ImageColor.getrgb(color)))
GHOST, FILL, RED_FILL = tint(INK,.27), tint(INK,.035), tint(ACCENT,.075)

SOURCES = {
    'form': ('Modern Robotics 12.1.7', 'https://modernrobotics.northwestern.edu/nu-gm-book-resource/12-1-7-form-closure/'),
    'force': ('Modern Robotics 12.2.3', 'https://modernrobotics.northwestern.edu/nu-gm-book-resource/12-2-3-force-closure/'),
    'friction': ('Modern Robotics 12.2.1', 'https://modernrobotics.northwestern.edu/nu-gm-book-resource/12-2-1-friction/'),
    'contacts': ('Modern Robotics 12.1.2: Contact Types', 'https://modernrobotics.northwestern.edu/nu-gm-book-resource/12-1-2-contact-types-rolling-sliding-and-breaking/'),
    'primer': ('Multi-Fingered Robotic Grasping: A Primer', 'https://arxiv.org/pdf/1607.06620'),
    'berkeley': ('UC Berkeley: Introduction to Grasping', 'https://pages.github.berkeley.edu/EECS-106/sp22-site/assets/scribe_notes/scribe_lec_9A.pdf'),
    'caging': ('Mahler et al.: Synthesis of Energy-Bounded Planar Caging', 'https://goldberg.berkeley.edu/pubs/Cage-Grasp-Synthesis-WAFR-accepted-Dec-2016.pdf'),
    'taxonomy': ('Feix et al.: GRASP taxonomy', 'https://www.eng.yale.edu/grablab/pubs/Feix_THMS2016.pdf'),
    'manipulation': ('Northwestern: In-hand Sliding Manipulation', 'https://www.robotics.northwestern.edu/research/topics/dynamic-nonprehensile-manipulation/in-hand-sliding-manipulation.html'),
    'gaiting': ('Shi et al.: Dynamic In-hand Sliding Manipulation', 'https://robotics.northwestern.edu/documents/publications/dynamic-in-hand-sliding-manipulation-tro.pdf'),
    'impedance': ('DLR Hand II: Experiments and Experiences', 'https://www.robotic.dlr.de/fileadmin/robotic/borst/BorstEtAl-ICRA03-HandApplications.pdf'),
    'synergy': ('Adaptive Synergies for the Pisa/IIT SoftHand', 'https://arpi.unipi.it/handle/11568/507072'),
}

@lru_cache(None)
def font(size, bold=False, mono=False, chinese=False):
    filename = 'consola.ttf' if mono else ('msyhbd.ttc' if bold else 'msyh.ttc') if chinese else ('seguisb.ttf' if bold else 'segoeui.ttf')
    return ImageFont.truetype('C:/Windows/Fonts/'+filename,round(size*AA))

class Canvas:
    """One scene, simultaneously recorded as vector primitives and rasterized."""
    def __init__(self, plate):
        self.plate=plate
        self.im=Image.new('RGB',(W*AA,H*AA),PAPER)
        self.d=ImageDraw.Draw(self.im)
        self.svg=[f'<rect width="{W}" height="{H}" fill="{PAPER}"/>']
        self.text_boxes=[]
        self.text((34,23),f'DEXTRAIL / GRASP {plate["number"]:02}',12,ACCENT,mono=True)
        self.text((34,51),plate['title'],29)
        self.text((35,95),plate['subtitle'],15,MUTED)
        self.line([(34,129),(W-34,129)],RULE,1)

    def line(self, points, color=INK, width=1.8, dashed=False):
        if dashed:
            phase=0
            for a,b in zip(points,points[1:]):
                length=hypot(b[0]-a[0],b[1]-a[1])
                if not length: continue
                for step in range(int(length)+1):
                    if int((phase+step)/7)%2==0:
                        t=step/length;u=min((step+1)/length,1)
                        p=(a[0]+(b[0]-a[0])*t,a[1]+(b[1]-a[1])*t)
                        q=(a[0]+(b[0]-a[0])*u,a[1]+(b[1]-a[1])*u)
                        self.d.line([(round(x*AA),round(y*AA)) for x,y in [p,q]],fill=color,width=max(1,round(width*AA)))
                phase+=length
        else:
            self.d.line([(round(x*AA),round(y*AA)) for x,y in points],fill=color,width=max(1,round(width*AA)),joint='curve')
            radius=width*AA/2
            for x,y in (points[0],points[-1]):
                self.d.ellipse((x*AA-radius,y*AA-radius,x*AA+radius,y*AA+radius),fill=color)
        coords=' '.join(f'{x:.2f},{y:.2f}' for x,y in points)
        dash=' stroke-dasharray="7 7"' if dashed else ''
        self.svg.append(f'<polyline points="{coords}" fill="none" stroke="{color}" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round"{dash}/>')

    def polygon(self, points, fill=FILL, color=INK, width=1.6):
        self.d.polygon([(round(x*AA),round(y*AA)) for x,y in points],fill=fill)
        self.line(points+[points[0]],color,width)
        coords=' '.join(f'{x:.2f},{y:.2f}' for x,y in points)
        self.svg.append(f'<polygon points="{coords}" fill="{fill}" stroke="{color}" stroke-width="{width}" stroke-linejoin="round"/>')

    def circle(self, center, radius, color=INK, width=1.6, fill=PAPER, ry=None):
        x,y=center;ry=radius if ry is None else ry
        self.d.ellipse(((x-radius)*AA,(y-ry)*AA,(x+radius)*AA,(y+ry)*AA),fill=fill,outline=color,width=max(1,round(width*AA)))
        self.svg.append(f'<ellipse cx="{x:.2f}" cy="{y:.2f}" rx="{radius:.2f}" ry="{ry:.2f}" fill="{fill}" stroke="{color}" stroke-width="{width}"/>')

    def text(self, point, value, size=18, color=INK, center=False, bold=False, mono=False):
        x,y=point;cn=bool(re.search('[\u3400-\u9fff]',value))
        face=font(size,bold,mono,cn)
        anchor='mt' if center else 'lt'
        self.d.text((round(x*AA),round(y*AA)),value,font=face,fill=color,anchor=anchor)
        bbox=self.d.textbbox((round(x*AA),round(y*AA)),value,font=face,anchor=anchor)
        self.text_boxes.append((value,tuple(v/AA for v in bbox)))
        family='Consolas, monospace' if mono else 'Segoe UI, Microsoft YaHei, sans-serif'
        self.svg.append(f'<text x="{x:.2f}" y="{y+size:.2f}" font-size="{size}" fill="{color}" font-family="{family}" font-weight="{600 if bold else 400}" text-anchor="{"middle" if center else "start"}">{escape(value)}</text>')

    def arrow(self, a, b, color=ACCENT, width=2, head=9):
        self.line([a,b],color,width)
        theta=atan2(b[1]-a[1],b[0]-a[0])
        self.line([(b[0]-head*cos(theta-.43),b[1]-head*sin(theta-.43)),b,(b[0]-head*cos(theta+.43),b[1]-head*sin(theta+.43))],color,width)

    def arc(self, center, radius, start, end, color=ACCENT, width=1.7, arrow=True, ry=None):
        x,y=center;ry=radius if ry is None else ry
        points=[(x+radius*cos(start+(end-start)*i/40),y+ry*sin(start+(end-start)*i/40)) for i in range(41)]
        self.line(points,color,width)
        if arrow:self.arrow(points[-3],points[-1],color,width,8)

    def leader(self, points):self.line(points,MUTED,1)
    def joint(self,p,active=False,r=4):
        self.circle(p,r,ACCENT if active else MUTED,1.5)
        if active:self.circle(p,1.2,ACCENT,1,ACCENT)

    def link(self,a,b,radius=10,active=False):
        length=hypot(b[0]-a[0],b[1]-a[1])
        if length<2:return
        ux,uy=(b[0]-a[0])/length,(b[1]-a[1])/length
        nx,ny=-uy,ux;angle=atan2(uy,ux)
        ra,rb=radius*.88,radius*.76
        aa=(a[0]+ux*ra,a[1]+uy*ra);bb=(b[0]-ux*rb,b[1]-uy*rb)
        points=[(aa[0]+ra*cos(angle+pi/2+pi*i/16),aa[1]+ra*sin(angle+pi/2+pi*i/16)) for i in range(17)]
        points += [(bb[0]+rb*cos(angle-pi/2+pi*i/16),bb[1]+rb*sin(angle-pi/2+pi*i/16)) for i in range(17)]
        self.polygon(points,PAPER,INK if active else MUTED,2 if active else 1.4)
        self.line([(a[0]+ux*length*.32,a[1]+uy*length*.32),(a[0]+ux*length*.7,a[1]+uy*length*.7)],GHOST,.65)

    def chain(self,points,active=False,radius=10):
        for a,b in zip(points,points[1:]):self.link(a,b,radius,active)
        for p in points[:-1]:self.joint(p,active)

    def footer(self,caption,scope=None):
        self.line([(34,622),(W-34,622)],RULE,1)
        self.text((W/2,640),caption,18,center=True)
        self.text((34,690),scope or self.plate['scope'],12,MUTED)
        value=self.plate['source_short']
        width=self.d.textlength(value,font=font(12))/AA
        self.text((W-34-width,690),value,12,MUTED)

    def finish(self):return self.im.resize((W,H),Image.Resampling.LANCZOS)
    def save_svg(self,path):
        desc=escape(self.plate['alt'])
        title=escape(self.plate['title'])
        head=f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" style="max-width:100%;height:auto" role="img" aria-labelledby="title desc"><title id="title">{title}</title><desc id="desc">{desc}</desc>'
        path.write_text(head+'\n'+'\n'.join(self.svg)+'\n</svg>',encoding='utf-8')

def smooth(x):return .5-.5*cos(pi*max(0,min(1,x)))
def cycle(t):return (1-cos(2*pi*t))/2
def polar(p,r,a):return (p[0]+r*cos(a),p[1]+r*sin(a))
def smooth_boundary(knots):
    points=[]
    for j,p1 in enumerate(knots):
        p0,p2,p3=knots[(j-1)%len(knots)],knots[(j+1)%len(knots)],knots[(j+2)%len(knots)]
        for k in range(10):
            t=k/10
            points.append(tuple(.5*(2*p1[a]+(-p0[a]+p2[a])*t+(2*p0[a]-5*p1[a]+4*p2[a]-p3[a])*t*t+(-p0[a]+3*p1[a]-3*p2[a]+p3[a])*t*t*t) for a in range(2)))
    return points
def box(c,cx,cy,w,h,color=INK,fill=FILL,angle=0):
    pts=[(-w/2,-h/2),(w/2,-h/2),(w/2,h/2),(-w/2,h/2)]
    pts=[(cx+x*cos(angle)-y*sin(angle),cy+x*sin(angle)+y*cos(angle)) for x,y in pts]
    c.polygon(pts,fill,color)
    return pts
def sphere(c,p,r,angle=0,mark=True):
    c.circle(p,r,INK,1.8,FILL)
    if mark:
        c.line([p,polar(p,r*.67,angle)],GHOST,1)
        c.circle(polar(p,r*.74,angle),3,ACCENT,1,ACCENT)
def contact(c,p):c.circle(p,3.5,ACCENT,1.5,PAPER)
def cone(c,p,angle,length=82,mu=.5):
    a=atan2(mu,1)
    c.polygon([p,polar(p,length,angle-a),polar(p,length,angle+a)],RED_FILL,GHOST,1)
    c.line([p,polar(p,length*1.08,angle)],MUTED,1,dashed=True)
def pad(c,p,n,scale=1):
    # A stationary support lies outside the body, opposite the inward normal.
    x,y=p;nx,ny=n;tx,ty=-ny,nx
    pts=[(x+tx*16*scale,y+ty*16*scale),(x-tx*16*scale,y-ty*16*scale),(x-tx*16*scale-nx*24*scale,y-ty*16*scale-ny*24*scale),(x+tx*16*scale-nx*24*scale,y+ty*16*scale-ny*24*scale)]
    c.polygon(pts,PAPER,MUTED,1.6)
    for d in [-10,0,10]:
        p1=(x+tx*d*scale-nx*24*scale,y+ty*d*scale-ny*24*scale)
        p2=(p1[0]+tx*8*scale-nx*10*scale,p1[1]+ty*8*scale-ny*10*scale)
        c.line([p1,p2],GHOST,1)
def spring(c,a,b,color=MUTED,width=1.4,turns=8,dashed=False):
    dx,dy=b[0]-a[0],b[1]-a[1];length=hypot(dx,dy)
    nx,ny=-dy/length,dx/length
    points=[a,(a[0]+dx*.1,a[1]+dy*.1)]
    for i in range(turns*2+1):
        t=.15+.7*i/(turns*2)
        side=7 if i%2==0 else -7
        points.append((a[0]+dx*t+nx*side,a[1]+dy*t+ny*side))
    points += [(a[0]+dx*.9,a[1]+dy*.9),b]
    c.line(points,color,width,dashed)
def ik(base,target,l1,l2,sign=1):
    dx,dy=target[0]-base[0],target[1]-base[1];distance=hypot(dx,dy)
    if not abs(l1-l2)+1e-5<distance<l1+l2-1e-5:
        raise ValueError(f'Unreachable schematic finger: {distance:.2f} for {l1},{l2}')
    angle=atan2(dy,dx)+sign*acos((l1*l1+distance*distance-l2*l2)/(2*l1*distance))
    return [base,polar(base,l1,angle),target]
def fingertip_chain(base,target,normal,l1=135,l2=100,last=22,sign=1):
    pre=(target[0]+normal[0]*last,target[1]+normal[1]*last)
    return ik(base,pre,l1,l2,sign)+[target]

def form_closure(c,t):
    center=(340,374);a=112
    box(c,*center,2*a,2*a)
    contacts=[((-a,a/2),(1,0)),((a,-a/2),(-1,0)),((a/2,-a),(0,1)),((-a/2,a),(0,-1))]
    for i,((x,y),n) in enumerate(contacts):
        p=(center[0]+x,center[1]+y);pad(c,p,n);contact(c,p)
        c.arrow(p,(p[0]+n[0]*48,p[1]+n[1]*48),ACCENT,1.7)
        c.text((p[0]-29*n[0]-5,p[1]-29*n[1]-24),f'C{i+1}',14,MUTED)
    c.text((620,248),'Fixed contacts',22)
    c.text((620,292),'No translation',18,MUTED)
    c.text((620,324),'No rotation',18,MUTED)
    c.text((620,377),'Friction is not required',17,ACCENT)
    c.text((620,429),'Normal wrench matrix N',16,MUTED)
    c.text((620,465),'rank(N) = 3',18,mono=True)
    c.text((620,497),'N [1,1,1,1] = 0',17,mono=True)
    c.text((340,533),'4 frictionless point contacts',17,MUTED,center=True)
    c.footer('固定接触的几何约束，同时阻止平移和转动')

def force_closure(c,t):
    cx,cy=340,375
    box(c,cx,cy,190,170)
    for x,n in [(cx-95,1),(cx+95,-1)]:
        c.chain([(x-110*n,460),(x-75*n,392),(x-8*n,cy)],radius=15)
        cone(c,(x,cy),0 if n==1 else pi,85,.55)
        contact(c,(x,cy));c.arrow((x,cy),(x+n*60,cy),ACCENT,2)
    c.arrow((cx+10,cy-45),(cx+10,cy+45),ACCENT)
    c.arc((cx,cy),57,-pi*.75,pi*.35)
    c.text((619,230),'Frictional contacts',22)
    c.text((619,283),'Counter force',18,MUTED)
    c.text((619,316),'Counter moment',18,MUTED)
    c.text((619,383),'All planar wrench directions',17,ACCENT)
    c.text((619,440),'Force limits still matter',17,MUTED)
    c.text((cx,541),'Two opposed contacts + friction',17,MUTED,center=True)
    c.footer('接触力与摩擦共同提供抗扰能力；图中为平面模型')

def friction_cone(c,t):
    for j,cx in enumerate([260,710]):
        p=(cx,441)
        c.line([(cx-145,441),(cx+145,441)],INK,1.5)
        c.circle((cx,463),24,MUTED,1.6,PAPER,ry=20)
        cone(c,p,-pi/2,192,.5)
        contact(c,p)
        theta=-pi/2+(.2 if j==0 else .67)
        endpoint=polar(p,176,theta)
        c.arrow(p,endpoint,ACCENT if j==0 else MUTED,2)
        c.text((cx,195),'Inside cone' if j==0 else 'Outside cone',21,center=True)
        c.text((cx,520),'Static force feasible' if j==0 else 'Static demand infeasible',18,ACCENT,center=True)
        c.text((cx,552),'|ft| ≤ μ fn' if j==0 else '|ft| > μ fn',19,center=True,mono=True)
        if j==1:c.arrow((cx-40,480),(cx+40,480),ACCENT)
    c.footer('静摩擦有上限：切向力需求超出摩擦锥时，无法保持静止')

def antipodal_grasp(c,t):
    for j,cx in enumerate([258,712]):
        cy=385;r=91;sphere(c,(cx,cy),r,mark=False)
        angles=[pi,0] if j==0 else [-3*pi/4,-pi/4]
        points=[polar((cx,cy),r,a) for a in angles]
        for p,a in zip(points,angles):
            n=(-cos(a),-sin(a));pad(c,p,n,.8)
            cone(c,p,a+pi,90,.5);contact(c,p)
        c.line([(points[0][0]-34,points[0][1]),(points[1][0]+34,points[1][1])],INK,1.5,dashed=True)
        c.text((cx,198),'Antipodal' if j==0 else 'Not antipodal',23,center=True)
        c.text((cx,524),'Line inside both cones' if j==0 else 'Line outside the cones',18,ACCENT,center=True)
    c.footer('平面双点接触：接触连线位于两侧摩擦锥内部')

def caging(c,t):
    # A 50-unit gate is narrower than the 104-unit disk diameter.
    left,right,top,bottom=295,662,225,550
    c.line([(right,355),(right,top),(left,top),(left,bottom),(right,bottom),(right,405)],INK,3)
    for x,y in [(left,top),(left,bottom),(right,top),(right,bottom)]:c.joint((x,y),False,5)
    x=478+75*sin(2*pi*t);y=385+62*sin(4*pi*t)
    sphere(c,(x,y),52,2*pi*t)
    c.line([(348,386),(606,386)],GHOST,1,dashed=True)
    c.arrow((610,380),(648,380),ACCENT)
    c.text((714,335),'Narrow gate',18)
    c.text((714,365),'Object cannot pass',16,MUTED)
    c.leader([(710,401),(685,401),(662,380)])
    c.text((66,281),'Room to move',20)
    c.text((66,316),'No escape path',18,ACCENT)
    c.leader([(195,350),(238,350),(295,350)])
    c.text((478,578),'Fixed cage · moving object',17,MUTED,center=True)
    c.footer('物体仍可平移和转动，但无法从固定围笼中逃脱')

def contact_models(c,t):
    for j,cx in enumerate([177,480,783]):
        name=['Frictionless point','Frictional point','Soft-finger patch'][j]
        c.text((cx,189),name,21,center=True)
        c.polygon([(cx-95,412),(cx,355),(cx+95,412),(cx,467)],FILL,MUTED,1.4)
        c.chain([(cx-50,259),(cx-32,313),(cx,398)],radius=13)
        if j<2:contact(c,(cx,398))
        else:c.circle((cx,398),24,ACCENT,1.5,RED_FILL,ry=9)
        c.arrow((cx,398),(cx,316),ACCENT)
        c.text((cx+10,329),'fn',14,MUTED,mono=True)
        if j>=1:
            c.arrow((cx,398),(cx+63,430),ACCENT,1.5)
            c.arrow((cx,398),(cx-63,430),ACCENT,1.5)
        if j==2:c.arc((cx,398),37,.1,1.85*pi,ACCENT,1.6,True,ry=14)
        c.text((cx,513),['Normal force','Normal + tangent','Also torsional moment'][j],17,center=True)
        c.text((cx,545),['1 component','3 components','4 components'][j],16,MUTED,center=True)
    c.footer('接触模型决定能够传递哪些力与力矩')

def wrench(c,t):
    box(c,331,388,198,148)
    origin=(331,388);p=(430,314)
    contact(c,p);c.circle(origin,3,MUTED,1,MUTED)
    c.line([origin,p],GHOST,1,dashed=True)
    c.arrow(p,(430,214),ACCENT)
    c.text((450,233),'Force F',19,ACCENT)
    c.arc(origin,58,pi*.7,-pi*.65,ACCENT)
    c.text((222,481),'Moment about O',18,MUTED)
    c.text((305,408),'O',15,MUTED)
    c.text((371,361),'r',17,MUTED,mono=True)
    c.text((614,251),'Wrench',24)
    c.text((614,308),'w = [ F ; τ ]',26,mono=True)
    c.text((614,367),'τ = r × F',24,mono=True)
    c.text((614,429),'3 force components',18,MUTED)
    c.text((614,461),'3 moment components',18,MUTED)
    c.footer('力旋量同时描述力与力矩；力矩取决于参考点 O')

def grasp_matrix(c,t):
    cx,cy=260,375
    box(c,cx,cy,156,156)
    for i,x in enumerate([cx-78,cx+78]):
        contact(c,(x,cy));pad(c,(x,cy),(1 if i==0 else -1,0))
        c.arrow((x,cy),(x+(60 if i==0 else -60),cy),ACCENT)
        c.arrow((x,cy),(x,cy-67),MUTED,1.4)
        c.text((x-18,cy+27),f'C{i+1}',16,MUTED)
    c.text((cx,526),'C1 = (−a,0)   C2 = (a,0)',17,MUTED,center=True,mono=True)
    c.text((503,230),'Contact forces → object wrench',20)
    c.text((503,284),'w = G f',27,ACCENT,mono=True)
    for j,value in enumerate(['[ 1   0   1   0 ]','[ 0   1   0   1 ]','[ 0  −a   0   a ]']):c.text((548,346+j*36),value,24,mono=True)
    c.text((503,473),'f = [fx1, fy1, fx2, fy2]',18,mono=True)
    c.text((503,507),'w = [Fx, Fy, Mz]',18,mono=True)
    c.text((503,553),'Forces must obey contact constraints',16,MUTED)
    c.footer('抓取矩阵把各接触力，汇总成物体的合力与合力矩')

def internal_force(c,t):
    for j,cx in enumerate([260,710]):
        box(c,cx,381,150,150)
        force=45+20*j
        pad(c,(cx-75,381),(1,0));pad(c,(cx+75,381),(-1,0))
        c.arrow((cx-75,381),(cx-75+force,381),ACCENT,2+j)
        c.arrow((cx+75,381),(cx+75-force,381),ACCENT,2+j)
        c.text((cx,213),'Gentle squeeze' if j==0 else 'Stronger squeeze',21,center=True)
        c.text((cx,505),'Net wrench = 0',20,center=True,mono=True)
    c.text((W/2,564),'G f_int = 0',22,ACCENT,center=True,mono=True)
    c.footer('对向挤压力彼此抵消；增加内力并不改变物体的合力旋量')

def gws_polygon(mu=.5):
    # Zero moment requires equal tangential forces at the two contacts.
    # With 0 <= fn_i <= 1, |Fy| <= 2 mu (1 - |Fx|).
    return [(-1,0),(0,-2*mu),(1,0),(0,2*mu)]
def axes(c,p,rx=170,ry=170,labels=('Fx','Fy')):
    c.arrow((p[0]-rx,p[1]),(p[0]+rx,p[1]),MUTED,1.1,6)
    c.arrow((p[0],p[1]+ry),(p[0],p[1]-ry),MUTED,1.1,6)
    c.text((p[0]+rx-8,p[1]+12),labels[0],15,MUTED,mono=True)
    c.text((p[0]+12,p[1]-ry-10),labels[1],15,MUTED,mono=True)
def grasp_wrench_space(c,t):
    box(c,215,360,114,114)
    for x,n in [(158,1),(272,-1)]:
        pad(c,(x,360),(n,0));cone(c,(x,360),0 if n==1 else pi,54)
        contact(c,(x,360));c.arrow((x,360),(x+40*n,360),ACCENT)
    c.text((215,465),'0 ≤ fn1, fn2 ≤ 1',17,center=True,mono=True)
    c.text((215,498),'μ = 0.5',17,center=True,mono=True)
    c.arrow((354,365),(427,365),MUTED,1.5)
    center=(680,368)
    poly=[(center[0]+145*x,center[1]-145*y) for x,y in gws_polygon()]
    c.polygon(poly,RED_FILL,ACCENT,1.8)
    axes(c,center,170,149)
    c.circle(center,3,INK,1,INK)
    c.text((680,177),'Feasible wrench set',22,center=True)
    c.text((680,570),'Exact planar slice: Mz = 0',17,center=True)
    c.footer('给定接触、摩擦与力预算后，抓取可产生的力旋量集合')

def inscribed_radius(points):
    best=None
    for a,b in zip(points,points[1:]+points[:1]):
        dx,dy=b[0]-a[0],b[1]-a[1]
        u=max(0,min(1,-(a[0]*dx+a[1]*dy)/(dx*dx+dy*dy)))
        p=(a[0]+u*dx,a[1]+u*dy);r=hypot(*p)
        if best is None or r<best[0]:best=(r,p)
    return best
def grasp_quality(c,t):
    polys=[[(140,0),(35,65),(-120,54),(-120,-62),(65,-54)],[(132*cos(2*pi*i/6),132*sin(2*pi*i/6)) for i in range(6)]]
    for j,(cx,poly) in enumerate(zip([260,710],polys)):
        center=(cx,382)
        c.polygon([(cx+x,382+y) for x,y in poly],FILL,MUTED,1.6)
        r,foot=inscribed_radius(poly)
        c.circle(center,r,ACCENT,1.8,RED_FILL)
        axes(c,center,172,145,('w1','w2'))
        c.arrow(center,(cx+foot[0],382+foot[1]),ACCENT,1.8,7)
        c.text((cx,196),'Grasp A' if j==0 else 'Grasp B',22,center=True)
        c.text((cx,549),'Smaller worst-case margin' if j==0 else 'Larger worst-case margin',17,center=True)
    c.text((480,582),'εA < εB',20,ACCENT,center=True,mono=True)
    c.footer('同一力预算和归一化下，最不利方向的抗扰余量越大越好')

def disturbance_state(t):
    # Displace, release, observe, then explicitly reset for the next loop.
    if t<.16:return smooth(t/.16), 'Displace'
    if t<.82:return 1,'Release'
    return 1-smooth((t-.82)/.18),'Reset'
def stable_response(dt,decay,frequency):
    # Exact homogeneous damped response to release at zero velocity.
    return exp(-decay*dt)*(cos(frequency*dt)+(decay/frequency)*sin(frequency*dt))
def equilibrium_stability(c,t):
    q,state=disturbance_state(t)
    for j,cx in enumerate([258,712]):
        if state=='Release':
            dt=(t-.16)/.66
            dx=65*stable_response(dt,5.8,11) if j==0 else 65
        elif state=='Reset' and j==0:dx=65*stable_response(1,5.8,11)*q
        else:dx=65*q
        c.line([(cx-143,457),(cx+148,457)],MUTED,1.4)
        c.line([(cx,290),(cx,477)],GHOST,1,dashed=True)
        c.text((cx,195),'Asymptotically stable' if j==0 else 'Neutral equilibrium',21,center=True)
        if j==0:
            pad(c,(cx-132,390),(1,0))
            spring(c,(cx-132,385),(cx+dx-34,385),MUTED)
            c.text((cx-138,509),'Restoring force + damping',17,MUTED)
        else:c.text((cx-138,509),'No restoring force',17,MUTED)
        box(c,cx+dx,413,68,88)
        if state=='Displace':c.arrow((cx+dx-24,272),(cx+dx+37,272),ACCENT)
        c.text((cx,552),'Returns toward reference' if j==0 else 'Stays displaced',17,ACCENT,center=True)
    c.text((480,581),state,17,MUTED,center=True)
    c.footer('初始都处于平衡；受扰动后的恢复行为不同')

def hand(c,cx,cy,s=1,pose='open',q=0,active=False):
    def p(x,y):return (cx+x*s,cy+y*s)
    knots=[(-70,-28),(-82,-61),(-69,-125),(-55,-145),(-30,-133),(-5,-150),(21,-133),(45,-142),(65,-124),(88,-120),(100,-66),(73,-8),(38,8),(-25,8),(-59,-7)]
    c.polygon(smooth_boundary([p(*v) for v in knots]),PAPER,MUTED,1.5)
    c.line([p(-24,8),p(-24,26)],MUTED,1.3);c.line([p(38,8),p(38,26)],MUTED,1.3)
    if pose=='power':box(c,cx,cy-117*s,57*s,220*s,MUTED,FILL)
    fingers=[]
    for j,(x,y,L) in enumerate([(-55,-145,(68,46,30)),(-5,-150,(80,54,33)),(45,-142,(73,50,31)),(88,-120,(57,39,27))]):
        if pose=='power':
            coords=[(x,y),(x*.72,y-44),(x*.38,y-28),(24 if x>0 else -24,y+10)]
        elif pose=='precision' and j==0:coords=[(-55,-145),(-30,-175),(-15,-205),(-28,-215)]
        else:
            a=-pi/2+([-10,-3,7,17][j]*q*pi/180)
            coords=[(x,y)]
            for length in L:coords.append((coords[-1][0]+length*cos(a),coords[-1][1]+length*sin(a)))
        points=[p(*v) for v in coords];c.chain(points,active,s*9);fingers.append(points)
    if pose=='precision':coords=[(-70,-28),(-105,-93),(-99,-163),(-76,-215)]
    elif pose=='lateral':coords=[(-70,-28),(-117,-120),(-107,-185),(-77,-225)]
    elif pose=='power':coords=[(-70,-28),(-90,-83),(-59,-119),(-26,-131)]
    else:
        coords=[(-70,-28)];a=(-137-28*q)*pi/180
        for length in [49,40,29]:coords.append((coords[-1][0]+length*cos(a),coords[-1][1]+length*sin(a)))
    thumb=[p(*v) for v in coords];c.chain(thumb,active,s*10)
    if pose=='precision':
        sphere(c,p(-52,-215),24*s,-pi/3)
        for xy in [(-28,-215),(-76,-215)]:contact(c,p(*xy))
    if pose=='lateral':
        box(c,*p(-72,-218),10*s,81*s,MUTED,FILL)
        c.circle(p(-72,-272),14*s,MUTED,1.4,PAPER)
        for y in [-205,-191]:c.line([p(-72,y),p(-58,y)],MUTED,2)
        contact(c,p(-77,-225))
    return fingers,thumb

def grasp_types(c,t):
    for j,(cx,pose) in enumerate(zip([169,482,795],['power','precision','lateral'])):
        c.text((cx,191),['Power grasp','Precision grasp','Intermediate grasp'][j],21,center=True)
        hand(c,cx,551,.89,pose)
        c.text((cx,586),['Tool handle','Fingertip pinch','Lateral pinch'][j],17,MUTED,center=True)
    c.footer('抓取姿态可按力量、精度需求，以及接触部位区分')

def virtual_finger(c,t):
    hand(c,473,554,1.12,'power')
    c.text((66,226),'VF 1',23,ACCENT)
    c.text((66,264),'Palm',19)
    c.leader([(150,298),(225,298),(425,483)])
    c.text((698,226),'VF 2',23,ACCENT)
    c.text((698,264),'Four fingers',19)
    c.leader([(696,299),(653,299),(541,379)])
    c.text((709,406),'One functional unit',17,MUTED)
    c.text((709,434),'Similar force direction',16,MUTED)
    c.footer('将协同施力的多个手指，视为一个功能性的“虚拟手指”')

def manipulation_scene(c,angle=0,gait=0):
    # Complete hand, three active fingers and two resting fingers.
    knots=[(320,535),(317,505),(350,487),(383,484),(414,499),(455,503),(493,489),(535,498),(571,484),(605,474),(621,526),(594,574),(551,602),(390,602),(345,570)]
    c.polygon(smooth_boundary(knots),PAPER,MUTED,1.5)
    c.line([(392,602),(392,614)],MUTED,1.2);c.line([(550,602),(550,614)],MUTED,1.2)
    c.chain([(535,498),(544,393),(549,331),(552,293)])
    c.chain([(605,474),(620,390),(629,339),(635,311)],radius=9)
    center=(430,345);radius=63
    sphere(c,center,radius,angle-pi/2)
    bases=[(355,490),(455,505),(320,535)]
    angles=[210*pi/180+angle,330*pi/180+angle,150*pi/180+angle]
    targets=[]
    for j,(base,a) in enumerate(zip(bases,angles)):
        if j==0 and gait:
            a=210*pi/180+gait*35*pi/180
            lift=20*sin(pi*gait)
        else:lift=0
        normal=(cos(a),sin(a));target=polar(center,radius+lift,a)
        points=fingertip_chain(base,target,normal,sign=-1 if j!=1 else 1)
        c.chain(points,True,11 if j==2 else 10)
        if lift<2:contact(c,target)
        else:c.circle(target,4,GHOST,1.3,PAPER)
        targets.append(target)
    return center,targets

def in_hand_manipulation(c,t):
    angle=.46*sin(2*pi*t)
    center,targets=manipulation_scene(c,angle)
    start,end=-pi/2-.55,-pi/2+.55
    if cos(2*pi*t)<0:start,end=end,start
    c.arc(center,87,start,end,ACCENT,arrow=abs(cos(2*pi*t))>1e-6)
    c.text((77,224),'Object reorientation',20)
    c.text((77,260),'Palm stays fixed',17,MUTED)
    c.leader([(240,294),(286,294),(367,345)])
    c.text((689,429),'Fingers coordinate',18)
    c.text((689,462),'Object moves in the hand',16,MUTED)
    c.footer('改变物体相对于手掌的姿态，而不移动整只手')

def gait_state(t):
    if t<.12:return 0,'Hold'
    if t<.58:return smooth((t-.12)/.46),'Lift → move → contact'
    if t<.72:return 1,'New contact'
    if t<.95:return 1-smooth((t-.72)/.23),'Return step'
    return 0,'Hold'
def finger_gaiting(c,t):
    q,state=gait_state(t)
    center,targets=manipulation_scene(c,0,q)
    route=[polar(center,63+20*sin(pi*x),210*pi/180+x*35*pi/180) for x in [i/50 for i in range(51)]]
    c.line(route,GHOST,1.2,True)
    c.text((73,225),'One finger steps',21)
    c.text((73,264),state,16,ACCENT)
    c.leader([(215,300),(278,300),targets[0]])
    c.text((687,426),'Two contacts support',18)
    c.text((687,460),'the stationary object',17,MUTED)
    c.footer('一指松开、换位、重新接触；其他手指继续支撑物体')

def finger_pad(c):
    c.chain([(176,530),(259,491),(337,455),(412,448)],False,17)
    c.polygon([(398,425),(583,425),(598,435),(595,454),(573,469),(409,469),(398,459)],PAPER,MUTED,1.5)
    c.line([(408,425),(580,425)],INK,2)
    c.text((587,487),'Finger pad',17,MUTED)
def contact_motion(c,t,rolling=True):
    x=480+36*sin(2*pi*t);r=65;angle=(x-480)/r if rolling else 0
    finger_pad(c);sphere(c,(x,360),r,pi/2+angle);contact(c,(x,425))
    velocity=cos(2*pi*t)
    moving=abs(velocity)>1e-6
    sign=1 if velocity>=0 else -1
    if moving:c.arrow((x-35*sign,244),(x+35*sign,244),ACCENT)
    c.text((685,244),'Object translates',20)
    c.text((685,283),'and rotates' if rolling else 'without rotating',19)
    c.text((685,366),'v_contact = 0' if rolling else ('v_relative ≠ 0' if moving else 'v_relative = 0'),19,ACCENT,mono=True)
    c.text((685,407),'No slip at contact' if rolling else 'Contact slips along pad',16,MUTED)
    if moving:
        if rolling:c.arc((x,360),44,-1.6,-1.6+sign*1.3,ACCENT)
        else:c.arrow((x-28*sign,432),(x+28*sign,432),ACCENT,1.7)
    c.footer('物体边转动边移动，接触处没有相对滑动' if rolling else '物体沿指腹滑动；受控滑动可以用于调整物体位置')
def rolling(c,t):contact_motion(c,t,True)
def sliding(c,t):contact_motion(c,t,False)

def pivoting(c,t):
    pivot=(378,472);angle=(-52+18*sin(2*pi*t))*pi/180
    c.chain([(212,549),(285,530),pivot],False,17)
    length=236;center=polar(pivot,length/2,angle)
    box(c,*center,length,47,INK,FILL,angle)
    c.circle(pivot,7,ACCENT,2,PAPER)
    c.circle(pivot,2,ACCENT,1,ACCENT)
    start,end=-70*pi/180,-34*pi/180
    if cos(2*pi*t)<0:start,end=end,start
    c.arc(pivot,217,start,end,ACCENT,1.6,arrow=abs(cos(2*pi*t))>1e-6)
    c.text((82,252),'Fixed pivot',21)
    c.leader([(190,287),(241,287),pivot])
    c.text((666,245),'Object rotates',21)
    c.text((666,283),'about the contact',18,MUTED)
    c.footer('接触支点保持不动，物体围绕这个支点转动')

def compliance(c,t):
    q=cycle(t);dy=42*q;contact_y=378+dy
    base=(250,529);target=(568,contact_y+28)
    points=ik(base,(target[0]-72,target[1]),155,135,sign=-1)+[target]
    c.chain(points,True,16)
    c.polygon([(516,contact_y),(606,contact_y),(615,contact_y+13),(605,contact_y+32),(518,contact_y+32)],PAPER,INK,1.6)
    box(c,564,contact_y-42,102,84)
    c.arrow((564,218),(564,290+40*q),ACCENT,2+q)
    c.text((588,241),'Load F',18,ACCENT)
    c.line([(501,378),(633,378)],GHOST,1,True)
    c.arrow((650,378),(650,contact_y),ACCENT,1.5,6)
    c.text((676,385),'Deflection δ',19)
    c.text((76,262),'Compliant finger',21)
    c.text((76,302),'Yields under load',18,MUTED)
    c.text((78,345),'F = K δ',24,mono=True)
    c.footer('受力时允许变形或让位；卸载后恢复参考姿态')

def impedance_control(c,t):
    q,state=disturbance_state(t)
    if state=='Release':dx=58*stable_response((t-.16)/.66,5,10)
    elif state=='Reset':dx=58*stable_response(1,5,10)*q
    else:dx=58*q
    x=546+dx
    c.line([(546,207),(546,457)],GHOST,1,True)
    c.text((546,173),'Reference',16,MUTED,center=True)
    spring(c,(294,317),(x-56,317),GHOST,1.4,dashed=True)
    # A parallel damper marks the desired virtual damping.
    c.line([(294,371),(383,371)],GHOST,1.2,True)
    c.line([(383,356),(417,356),(417,386),(383,386)],GHOST,1.2,True)
    c.line([(404,359),(404,383)],GHOST,1.2)
    c.line([(404,371),(x-56,371)],GHOST,1.2,True)
    c.text((329,260),'Virtual K, D',18,MUTED)
    box(c,x,355,112,124)
    c.chain(ik((250,475),(x-56,413),175,160,-1),False,16)
    c.circle((x-56,413),3.5,ACCENT,1.5)
    if state=='Displace':c.arrow((x+22,233),(x+84,233),ACCENT)
    c.text((704,291),'External disturbance',18)
    c.text((704,330),'Controlled response',18,ACCENT)
    c.text((704,369),state,16,MUTED)
    box(c,465,550,410,70,MUTED,PAPER)
    c.text((465,532),'Impedance controller',20,center=True)
    c.text((465,565),'M δ¨ + D δ˙ + K δ = Fext',18,center=True,mono=True)
    c.footer('设定受力与运动之间的期望关系：虚拟质量、弹簧和阻尼')

def underactuation(c,t):
    q=cycle(t);early=min(q/.55,1);late=max(0,(q-.55)/.45)
    base=(320,520);a=(-82+42*early)*pi/180
    elbow=polar(base,150,a);end=polar(elbow,130,(-154+64*late)*pi/180)
    sphere(c,(415,516),45,-.7)
    c.circle((180,516),31,MUTED,1.8,PAPER)
    c.text((180,508),'M',21,center=True)
    c.line([(211,516),base,elbow,end],ACCENT,1.2)
    c.chain([base,elbow,end],True,13)
    c.line([base,elbow,end],ACCENT,1.05)
    start,end=-2.1,-.4+q*1.5
    if t>.5:start,end=end,start
    c.arc((180,516),40,start,end,ACCENT,1.3,arrow=abs(sin(2*pi*t))>1e-6)
    c.arc(elbow,15,-2.2,.2,GHOST,1.2,False)
    if q>.55:
        contact(c,(385,482))
        c.text((658,294),'First link stops',20,ACCENT)
        c.text((658,333),'Second keeps moving',18)
        c.leader([(658,371),(610,371),(385,482)])
    else:
        c.text((658,294),'One motor pulls',20)
        c.text((658,333),'Two joints respond',18,MUTED)
    c.text((72,219),'1 input',24,ACCENT)
    c.text((72,261),'2 joint DOFs',22)
    c.text((72,306),'Tendon + passive joint',17,MUTED)
    c.footer('一个驱动输入带动多个自由度；接触改变关节的运动分配')

def synergy(c,t):
    q=cycle(t);hand(c,475,557,1.03,q=q,active=True)
    c.text((75,217),'One synergy coordinate',20)
    c.text((75,257),'s',26,ACCENT,mono=True)
    c.line([(78,317),(259,317)],GHOST,3)
    c.circle((78+181*q,317),6,ACCENT,1.5,PAPER)
    c.text((75,344),'Together',16,MUTED)
    c.text((211,344),'Spread',16,MUTED)
    c.text((720,237),'Many joint angles',20)
    c.text((720,284),'q = q0 + S s',20,mono=True)
    c.text((720,342),'Coordinated posture',17,ACCENT)
    c.footer('用少数协同变量组织多个关节；示例为手指张开与收拢')

def adaptive_synergy(c,t):
    q=cycle(t);a=min(q/.52,1);b=min(q/.92,1)
    left=(241+109*a,337);right=(669-89*b,347)
    box(c,465,358,230,168)
    lchain=ik((231,521),left,128,113,-1)
    rchain=ik((750,521),right,132,116,1)
    delta=21*max(0,b-a)
    motor=(480,572)
    c.circle(motor,25,MUTED,1.6,PAPER);c.text((480,563),'M',20,center=True)
    junction=(480,509)
    ends=[(388,509+delta),(572,509-delta)]
    c.line([ends[0],junction,ends[1]],MUTED,2)
    c.line([(480,547),junction],ACCENT,1.4)
    for endpoint,chain in zip(ends,[lchain,rchain]):
        c.line([endpoint,chain[0],chain[1],chain[2]],ACCENT,1.1)
        c.chain(chain,True,12)
        c.line(chain,ACCENT,1.05)
        spring(c,(endpoint[0],endpoint[1]-16),(endpoint[0],endpoint[1]-55),GHOST,1.1,4)
    if q>=.52:contact(c,left)
    if q>=.92:contact(c,right)
    c.text((60,221),'Common drive',21)
    c.text((60,262),'Compliant branches',18,MUTED)
    c.text((692,222),'Adapts after contact',20,ACCENT)
    c.text((692,265),'First branch holds',17)
    c.text((692,295),'Other branch continues',17)
    c.footer('共享输入与顺应结构，让各手指在接触后适应物体形状')

def plate(slug,title,subtitle,caption,animated,source,scope,renderer,alt):
    return dict(slug=slug,title=title,subtitle=subtitle,caption=caption,animated=animated,source_keys=source,scope=scope,render=renderer,alt=alt)
PLANAR='Planar teaching model · geometry and loads are schematic'
SPATIAL='Spatial teaching model · schematic contact geometry'
PLATES=[
    plate('form-closure','Form closure','形封闭 · 固定接触的几何约束','几何约束',False,['form'],PLANAR,form_closure,'四个固定无摩擦接触约束平面方块，阻止平移与转动。'),
    plate('force-closure','Force closure','力封闭 · 接触力与摩擦提供抗扰方向','接触与摩擦',False,['force'],PLANAR,force_closure,'两个对向摩擦接触的平面夹持示例，显示摩擦锥、合力和力矩。'),
    plate('friction-cone','Friction cone','摩擦锥 · 静摩擦允许的接触力范围','静摩擦范围',False,['friction'],SPATIAL,friction_cone,'两个摩擦锥截面对比：锥内需求可静态实现，锥外需求不可维持静止。'),
    plate('antipodal-grasp','Antipodal grasp','对向抓取 · 接触连线与摩擦锥','对向接触',False,['berkeley','force'],PLANAR,antipodal_grasp,'平面模型中，接触连线在两个摩擦锥内部和外部的对比。'),
    plate('caging','Caging','笼式约束 · 可以活动，但不能逃脱','有限活动空间',True,['caging'],PLANAR,caging,'圆形物体在固定围笼内部平移转动，无法穿过比物体直径小的开口。'),
    plate('contact-models','Contact models','接触模型 · 无摩擦点、摩擦点与软指接触','可传递的力与力矩',False,['primer','force'],SPATIAL,contact_models,'三个接触模型分别允许法向力、法向加切向力，以及额外的法向扭转力矩。'),
    plate('wrench','Wrench','力旋量 · 力与力矩的统一描述','力与力矩',False,['primer'],SPATIAL,wrench,'偏心作用力相对参考点 O 产生力矩，右侧列出力旋量组成。'),
    plate('grasp-matrix','Grasp matrix','抓取矩阵 · 从接触力到物体力旋量','接触力映射',False,['primer'],PLANAR,grasp_matrix,'显示两个对称接触的位置，以及将四个接触力分量映射成 Fx、Fy、Mz 的具体矩阵。'),
    plate('internal-force','Internal force','抓取内力 · 挤压与物体运动解耦','抵消的夹持力',False,['berkeley'], 'Internal-force component only · external loads omitted',internal_force,'对向共线挤压力增大，但其合力与合力矩仍为零。'),
    plate('grasp-wrench-space','Grasp wrench space','抓取力旋量空间 · 给定预算下的可行受力集合','可行力旋量集合',False,['primer','friction'], 'Planar Mz = 0 slice · normalized forces; not full spatial GWS',grasp_wrench_space,'在双指摩擦接触与每指法向力不超过一的预算下，展示零力矩切片的精确可行菱形。'),
    plate('grasp-quality','Grasp quality','抓取质量 · 最不利方向的抗扰余量','抗扰余量',False,['primer'], 'Illustrative normalized 2D section · not the full 6D metric',grasp_quality,'同一归一化与预算下，比较两个示意力旋量截面的原点中心内切圆半径。'),
    plate('equilibrium-stability','Equilibrium & stability','平衡与稳定性 · 初始平衡不等于受扰后恢复','受扰响应',True,['primer','impedance'], '1D explanatory model · neutral versus asymptotically stable',equilibrium_stability,'同时移开两个初始平衡的物体并释放：有恢复力与阻尼的物体回位，中性物体保持偏移；重置阶段标明。'),
    plate('grasp-types','Power, precision & intermediate','抓取类型 · 包握、指尖捏取与侧向捏持','三种握持方式',False,['taxonomy'], 'Schematic hand postures · classification follows GRASP taxonomy',grasp_types,'完整五指手分别包握工具柄、指尖捏小球和侧向捏钥匙。'),
    plate('virtual-finger','Virtual finger','虚拟手指 · 多个接触作为功能单元','协同施力单元',False,['taxonomy'], 'Palm opposition example · functional grouping, not anatomy',virtual_finger,'包握中手掌作为虚拟手指一，四个协同手指作为虚拟手指二。'),
    plate('in-hand-manipulation','In-hand manipulation','手内操作 · 物体相对于手掌改变姿态','手内重定位',True,['manipulation'],PLANAR,in_hand_manipulation,'完整手掌保持固定，三个手指协同使带方向标记的圆形物体往复转动。'),
    plate('finger-gaiting','Finger gaiting','指间换步 · 解除接触、移动与重新接触','接触重配置',True,['gaiting'], 'Planar model · supporting contacts assumed adequately frictional',finger_gaiting,'完整手掌中的食指离开物体、沿弧线换位再接触；两个对向支撑接触保持固定。'),
    plate('rolling','Rolling','滚动 · 接触处没有相对滑动','无滑动的滚动',True,['manipulation','contacts'], '2D rolling kinematics · dx = R dθ; schematic finger pad',rolling,'物体边移动边转动，材料标记随转动改变位置；角度与平移满足无滑动滚动关系。'),
    plate('sliding','Sliding','滑动 · 物体相对于指腹移动','受控滑动',True,['manipulation','contacts'], '2D sliding kinematics · orientation fixed in this example',sliding,'物体保持方向不变沿静止指腹往复滑动，接触处显示相对运动箭头。'),
    plate('pivoting','Pivoting','绕支点转动 · 接触位置保持固定','固定支点',True,['manipulation'], '2D kinematic example · pivot fixed in the world frame',pivoting,'长条物体围绕手指上的固定支点往复转动，弧线显示端部轨迹。'),
    plate('compliance','Compliance','顺应性 · 受力变形与卸载恢复','受力让位',True,['impedance'], 'Quasistatic linear compliance example · F = K δ',compliance,'加载时物体和指腹下移，手指随之变形，卸载后回到参考姿态。'),
    plate('impedance-control','Impedance control','阻抗控制 · 设定期望的力与运动关系','期望动态响应',True,['impedance'], '1D virtual mass–spring–damper · model, not controller simulation',impedance_control,'外部扰动使接触物体偏移，随后按虚拟弹簧阻尼响应回位；显示阻抗关系。'),
    plate('underactuation','Underactuation','欠驱动 · 独立输入少于机械自由度','少输入、多自由度',True,['synergy'], 'Conceptual tendon mechanism · motion distribution is prescribed',underactuation,'一台电机牵引二自由度手指，近端连杆接触后停止，远端关节继续运动。'),
    plate('synergy','Postural synergy','姿态协同 · 少数变量组织多关节动作','协调动作模式',True,['synergy'], 'Illustrative spread synergy · not a measured human principal synergy',synergy,'一个滑块变量同时协调完整五指手的张开与收拢。'),
    plate('adaptive-synergy','Adaptive synergy','自适应协同 · 共享驱动与接触后的适应','接触后适应',True,['synergy'], 'Functional linkage schematic · no product-specific transmission claim',adaptive_synergy,'共享电机驱动两个顺应分支，一侧先接触后保持，另一侧继续闭合直到接触。'),
]
for i,p in enumerate(PLATES,1):
    p['number']=i
    p['source_short']={'form':'Modern Robotics','force':'Modern Robotics','friction':'Modern Robotics','primer':'Grasping Primer','berkeley':'UC Berkeley','caging':'Mahler et al.','taxonomy':'Feix et al.','manipulation':'Northwestern Robotics','gaiting':'Shi et al.','impedance':'DLR Hand II','synergy':'Pisa/IIT SoftHand'}[p['source_keys'][0]]

def scene(p,t):
    c=Canvas(p);p['render'](c,t)
    for value,box in c.text_boxes:
        if not (-.5<=box[0] and box[2]<=W+.5 and box[1]>=0 and box[3]<=H+.5):
            raise ValueError(f'Text outside {p["slug"]}: {value}: {box}')
    return c

def gif(frames,path):
    # Build a shared palette so stationary paper and ink do not flicker.
    sample=Image.new('RGB',(W*4,H*2),PAPER)
    for j,k in enumerate([0,10,20,30,40,50,60,70]):sample.paste(frames[k],((j%4)*W,(j//4)*H))
    palette=sample.quantize(colors=96,method=Image.Quantize.MEDIANCUT)
    indexed=[im.quantize(palette=palette,dither=Image.Dither.NONE) for im in frames]
    indexed[0].save(path,save_all=True,append_images=indexed[1:],duration=MS,loop=0,optimize=True,disposal=1)

def export_plate(p,preview=False):
    c=scene(p,.28)
    c.finish().save(OUT/(p['slug']+'.png'))
    c.save_svg(OUT/(p['slug']+'.svg'))
    if p['animated'] and not preview:
        frames=[scene(p,i/FRAMES).finish() for i in range(FRAMES)]
        gif(frames,OUT/(p['slug']+'.gif'))
        review=Image.new('RGB',(W*3,H*2),PAPER)
        for j,k in enumerate([0,12,24,40,56,72]):review.paste(frames[k],((j%3)*W,(j//3)*H))
        review.save(OUT/(p['slug']+'-review.png'))
    print(f'Rendered {p["slug"]}',flush=True)

def build_overviews():
    # Review sheets are images, never standalone website pages.
    full=Image.new('RGB',(1920,2160),PAPER)
    for j,p in enumerate(PLATES):
        with Image.open(OUT/(p['slug']+'.png')) as im:
            full.paste(im.resize((480,360),Image.Resampling.LANCZOS),((j%4)*480,(j//4)*360))
    full.save(OUT/'grasp-concepts-overview.png')
    for group in range(4):
        sheet=Image.new('RGB',(1440,1620),PAPER)
        for j,p in enumerate(PLATES[group*6:group*6+6]):
            with Image.open(OUT/(p['slug']+'.png')) as im:
                sheet.paste(im.resize((720,540),Image.Resampling.LANCZOS),((j%2)*720,(j//2)*540))
        sheet.save(OUT/f'grasp-concepts-sheet-{group+1:02}.png')

def manifest_and_bundle():
    records=[]
    for p in PLATES:
        records.append({k:p[k] for k in ['number','slug','title','subtitle','animated','scope','alt']} | {
            'width':W,'height':H,'duration_ms':FRAMES*MS if p['animated'] else None,
            'files':[p['slug']+'.png',p['slug']+'.svg']+([p['slug']+'.gif'] if p['animated'] else []),
            'sources':[{'title':SOURCES[k][0],'url':SOURCES[k][1]} for k in p['source_keys']],
        })
    data={'edition':'DexTrail grasp concepts','palette':{'paper':PAPER,'ink':INK,'accent':ACCENT},'assets':records}
    (OUT/'manifest.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (OUT/'README.txt').write_text('''DexTrail grasp concept assets

24 concept plates, including 12 animated processes. All plates have PNG and
SVG versions; animated plates also have GIF versions. Individual plates are
960 × 720. GIF loops last 6.4 seconds. The palette matches the website:
warm paper, charcoal and brick red; no shading or lighting.

Use SVG for scalable figures, PNG for static embedding, and GIF when the
sequence helps explain the concept. Offer the same-name PNG when reduced
motion is requested. These files do not create a standalone website page.

`manifest.json` lists filenames, Chinese alt text, primary sources, and the
teaching assumptions for every plate. The diagrams are explanatory models,
not measurements, product mechanism drawings, or validated robot dynamics.

The project renderer is `scripts/render-grasp-concepts.py`; it reads the
project theme CSS and uses Pillow and Windows fonts. The ZIP contains assets
and their metadata, while the renderer stays in the project repository.
''',encoding='utf-8')
    archive=OUT/'grasp-concepts-dextrail.zip'
    with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
        for r in records:
            for name in r['files']:z.write(OUT/name,name)
        z.write(OUT/'manifest.json','manifest.json')
        z.write(OUT/'grasp-concepts-overview.png','grasp-concepts-overview.png')
        z.write(OUT/'README.txt','README.txt')

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--preview',action='store_true')
    parser.add_argument('--only',nargs='+',choices=[p['slug'] for p in PLATES])
    args=parser.parse_args();OUT.mkdir(parents=True,exist_ok=True)
    for p in PLATES:
        if args.only is None or p['slug'] in args.only:export_plate(p,args.preview)
    if all((OUT/(p['slug']+'.png')).exists() for p in PLATES):build_overviews()
    if not args.preview and all((OUT/(p['slug']+('.gif' if p['animated'] else '.png'))).exists() for p in PLATES):manifest_and_bundle()

if __name__=='__main__':main()
