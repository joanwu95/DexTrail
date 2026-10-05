"""DexTrail editorial edition of the hand motion diagrams.

Uses anatomical motion schematics with flat projected spatial geometry,
typography, spacing and palette. All animation frames are drawn from geometry.
Website tokens are read from theme.css so regeneration follows the site palette.
"""
from pathlib import Path
import importlib.util
import re
from math import sin, cos, pi, atan2, hypot, sqrt
from functools import lru_cache
from PIL import Image, ImageDraw, ImageFont, ImageColor

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('hand_motion_geometry', ROOT/'scripts/render-hand-motions.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
CSS = (ROOT/'website/docs/stylesheets/theme.css').read_text(encoding='utf-8')


def token(name):
    match = re.search(r'--atlas-'+name+r':(#[0-9a-fA-F]{6})', CSS)
    if not match:
        raise ValueError(f'Missing website token: atlas-{name}')
    return match.group(1)


PAPER, PANEL, INK, ACCENT, MUTED, RULE = [token(n) for n in ['paper','panel','ink','accent','muted','line']]


def tint(color, weight):
    a,b=ImageColor.getrgb(PAPER),ImageColor.getrgb(color)
    return tuple(round(x+(y-x)*weight) for x,y in zip(a,b))


GHOST = tint(INK,.26)
LINK_FILL = tint(INK,.025)
ACTIVE_FILL = tint(ACCENT,.075)
OUT = ROOT/'website/docs/images/knowledge/hand-motions-dextrail'
W,H,AA = 800,680,2
FRAMES,DURATION = 96,80
COLORS = {m.WHITE:PAPER,m.INK:INK,m.TEAL:ACCENT,m.MUTED:MUTED,m.RULE:RULE,m.GHOST:GHOST}


@lru_cache(None)
def face(size,semibold=False,chinese=False,mono=False):
    name = ('msyhbd.ttc' if semibold else 'msyh.ttc') if chinese else ('seguisb.ttf' if semibold else 'segoeui.ttf')
    if mono:
        name='consola.ttf'
    return ImageFont.truetype(str(Path('C:/Windows/Fonts')/name),round(size*AA))


class EditorialCanvas:
    def __init__(self):
        self.im=Image.new('RGB',(W*AA,H*AA),PAPER)
        self.d=ImageDraw.Draw(self.im)
        self.diagram=False

    def pos(self,p):
        # Enlarged illustration stage, separated from editorial typography.
        x,y=p
        return (x*1.12+16,y*1.12+30) if self.diagram else (x,y)

    def color(self,color):
        return COLORS.get(color,color) if isinstance(color,str) else color

    def line(self,pts,color=INK,width=2):
        pts=[self.pos(p) for p in pts]
        self.d.line([(round(x*AA),round(y*AA)) for x,y in pts],fill=self.color(color),width=max(1,round(width*AA)),joint='curve')
        # Round line caps make a visibly smoother engineering drawing.
        r=width*AA/2
        for x,y in (pts[0],pts[-1]):
            self.d.ellipse((x*AA-r,y*AA-r,x*AA+r,y*AA+r),fill=self.color(color))

    def text(self,xy,value,size=18,color=INK,bold=False,center=False,chinese=False,mono=False):
        xy=self.pos(xy)
        self.d.text((round(xy[0]*AA),round(xy[1]*AA)),value,font=face(size,bold,chinese,mono),fill=self.color(color),anchor='mt' if center else 'lt')

    def ellipse(self,box,color=ACCENT,width=2,fill=None):
        a=self.pos(box[:2]);b=self.pos(box[2:])
        self.d.ellipse(tuple(round(v*AA) for v in (*a,*b)),outline=self.color(color),width=round(width*AA),fill=self.color(fill) if fill else None)

    def joint(self,p,radius=6,color=ACCENT,width=2):
        x,y=p
        self.ellipse((x-radius,y-radius,x+radius,y+radius),color,min(width,2),PAPER)
        # A tiny hub strengthens the pivot's reading without a bulky badge.
        if color in (m.TEAL,ACCENT):
            self.ellipse((x-1.35,y-1.35,x+1.35,y+1.35),color,1,color)

    def dashed(self,pts,color=GHOST,width=1.2,dash=7):
        phase=0
        for a,b in zip(pts,pts[1:]):
            length=hypot(b[0]-a[0],b[1]-a[1])
            if length < .01:
                continue
            for step in range(int(length)+1):
                if int((phase+step)/dash)%2==0:
                    t=step/length;u=min((step+1)/length,1)
                    self.line([(a[0]+(b[0]-a[0])*t,a[1]+(b[1]-a[1])*t),(a[0]+(b[0]-a[0])*u,a[1]+(b[1]-a[1])*u)],color,min(width,1.3))
            phase += length

    def arrow(self,pts,color=ACCENT,width=2):
        self.line(pts,color,min(width,2))
        a,b=pts[-2:];angle=atan2(b[1]-a[1],b[0]-a[0])
        self.line([(b[0]-9*cos(angle-.43),b[1]-9*sin(angle-.43)),b,(b[0]-9*cos(angle+.43),b[1]-9*sin(angle+.43))],color,min(width,2))

    def link(self,a,b,radius=9,color=ACCENT,width=2,ghost=False):
        length=hypot(b[0]-a[0],b[1]-a[1])
        if length < 1:
            return
        if ghost:
            # One dashed centerline instead of a pile of ghost capsules.
            self.dashed([a,b],GHOST,1.15,6)
            return
        ux,uy=(b[0]-a[0])/length,(b[1]-a[1])/length
        nx,ny=-uy,ux
        angle=atan2(uy,ux)
        ra=(radius+2)*.86;rb=(radius+2)*.76
        a=(a[0]+ux*ra,a[1]+uy*ra);b=(b[0]-ux*rb,b[1]-uy*rb)
        span=max(1,length-ra-rb)
        # Tapered rounded bands reach the pivot instead of floating as
        # separate ovals. The joints are drawn last over the meeting ends.
        pts=[]
        for j in range(17):
            th=angle+pi/2+pi*j/16
            pts.append((a[0]+ra*cos(th),a[1]+ra*sin(th)))
        for j in range(1,17):
            t=j/16;r=ra+(rb-ra)*t+1.8*sin(pi*t)
            pts.append((a[0]+ux*span*t-nx*r,a[1]+uy*span*t-ny*r))
        for j in range(1,17):
            th=angle-pi/2+pi*j/16
            pts.append((b[0]+rb*cos(th),b[1]+rb*sin(th)))
        for j in range(15,0,-1):
            t=j/16;r=ra+(rb-ra)*t+1.8*sin(pi*t)
            pts.append((a[0]+ux*span*t+nx*r,a[1]+uy*span*t+ny*r))
        mapped=[self.pos(p) for p in pts]
        active=color in (m.TEAL,ACCENT)
        self.d.polygon([(round(x*AA),round(y*AA)) for x,y in mapped],fill=ACTIVE_FILL if active else LINK_FILL)
        self.line(pts+[pts[0]],INK if active else MUTED,2 if active else 1.55)
        # Short center axis, quiet enough to stay behind the mechanism.
        self.line([(a[0]+ux*span*.25,a[1]+uy*span*.25),(a[0]+ux*span*.75,a[1]+uy*span*.75)],tint(INK,.18),.65)

    def chain(self,points,color=ACCENT,width=2,ghost=False,radius=9):
        for a,b in zip(points,points[1:]):
            self.link(a,b,radius,color,width,ghost)
        if not ghost:
            for p in points[:-1]:
                self.joint(p,4.9,color,1.9)

    def polygon(self,pts,fill=LINK_FILL,color=MUTED,width=1.5):
        self.d.polygon([(round(x*AA),round(y*AA)) for x,y in map(self.pos,pts)],fill=fill)
        self.line(pts,color,width)

    def finish(self):
        return self.im.resize((W,H),Image.Resampling.LANCZOS)


def bezier(a,b,c,d,n=18):
    return [((1-t)**3*a[0]+3*(1-t)**2*t*b[0]+3*(1-t)*t*t*c[0]+t**3*d[0],(1-t)**3*a[1]+3*(1-t)**2*t*b[1]+3*(1-t)*t*t*c[1]+t**3*d[1]) for t in [j/n for j in range(n+1)]]


def palm(c):
    # Subtle coherent palm surface, smooth thumb web and curved heel.
    points=[(261,325)]
    for controls in [
        ((261,325),(250,339),(254,356),(235,361)),
        ((235,361),(212,366),(222,391),(244,411)),
        ((244,411),(271,439),(280,438),(300,438)),
        ((300,438),(319,441),(341,441),(352,438)),
        ((352,438),(389,426),(409,381),(406,344)),
    ]:
        points += bezier(*controls)[1:]
    # Close at the finger bases with a light connecting contour.
    top=[(406,344),(405,335),(397,324),(385,332),(374,324),(356,307),(344,316),(332,308),(313,300),(299,310),(287,313),(270,309),(261,325)]
    c.polygon(points+top,LINK_FILL,MUTED,1.25)
    c.line([(298,438),(298,457)],MUTED,1.25)
    c.line([(352,438),(352,457)],MUTED,1.25)
    curve=bezier((274,394),(301,379),(345,380),(380,389))
    c.line(curve,tint(INK,.18),.7)


def heading(c,n,title,subtitle):
    c.diagram=False
    c.text((34,23),f'DEXTRAIL / MOTION {n:02}',12,ACCENT,mono=True)
    c.text((34,51),title,29,INK,False)
    c.text((35,93),subtitle,15,MUTED,chinese=True)
    c.line([(34,127),(766,127)],RULE,1)
    c.diagram=True


def status(c,first,second,outward,hold,cn):
    c.diagram=False
    c.line([(34,576),(766,576)],RULE,1)
    c.text((36,591),first,24,ACCENT if outward else MUTED,outward)
    box=c.d.textbbox((0,0),second,font=face(24,not outward))
    right=764-(box[2]-box[0])/AA
    c.text((right,591),second,24,ACCENT if not outward else MUTED,not outward)
    # The underline carries the state as well as color.
    word=first if outward else second
    box=c.d.textbbox((0,0),word,font=face(24,True))
    length=(box[2]-box[0])/AA
    x=36 if outward else right
    c.line([(x,627),(x+length,627)],ACCENT,1.5)
    c.text((400,643),cn,17,INK,center=True,chinese=True)


def add3(a,b):
    return tuple(x+y for x,y in zip(a,b))


def mul3(v,s):
    return tuple(x*s for x in v)


def unit3(v):
    length=sqrt(sum(x*x for x in v))
    return tuple(x/length for x in v)


class HandView:
    """Orthographic spatial geometry rendered only as flat linework.

    The palm is in z=0, fingers extend along +y, and +z is palmar.
    No lighting, depth shading, textures or perspective scaling are used.
    """
    bases=[(-46,118,0),(-5,127,0),(34,118,0),(68,100,0)]
    lengths=[(67,48,32),(76,54,36),(70,49,31),(54,39,26)]
    cmc=(-56,27,0)
    thumb_lengths=(59,49,36)

    def __init__(self,c,yaw=35,pitch=32,scale=1.35,origin=(455,531)):
        self.c=c;self.yaw=yaw*pi/180;self.pitch=pitch*pi/180
        self.scale=scale;self.origin=origin
        c.diagram=False

    def project(self,p):
        x,y,z=p
        u=cos(self.yaw)*x-sin(self.yaw)*z
        v=sin(self.yaw)*sin(self.pitch)*x+cos(self.pitch)*y+cos(self.yaw)*sin(self.pitch)*z
        return (self.origin[0]+self.scale*u,self.origin[1]-self.scale*v)

    def chain(self,base,lengths,direction):
        points=[base];direction=unit3(direction)
        for length in lengths:
            points.append(add3(points[-1],mul3(direction,length)))
        return points

    def link(self,a,b,radius=10,active=False,ghost=False):
        if ghost:
            self.c.dashed([self.project(a),self.project(b)],GHOST,1.1,6)
            return
        delta=tuple(y-x for x,y in zip(a,b))
        direction=unit3(delta)
        # Stable local width axis avoids incorrect planar bending of a
        # finger undergoing actual spatial rotation.
        seed=(1,0,0) if abs(direction[0])<.85 else (0,0,1)
        dot=sum(x*y for x,y in zip(seed,direction))
        side=unit3(tuple(x-dot*y for x,y in zip(seed,direction)))
        ra,rb=radius*.88,radius*.76
        start=add3(a,mul3(direction,ra));end=add3(b,mul3(direction,-rb))
        points=[]
        for j in range(17):
            t=pi*j/16
            points.append(add3(add3(start,mul3(side,ra*cos(t))),mul3(direction,-ra*sin(t))))
        for j in range(1,17):
            t=pi*j/16
            points.append(add3(add3(end,mul3(side,-rb*cos(t))),mul3(direction,rb*sin(t))))
        outline=[self.project(p) for p in points]
        self.c.polygon(outline+[outline[0]],PAPER,INK if active else MUTED,2.1 if active else 1.4)
        self.c.line([self.project(add3(a,mul3(delta,.32))),self.project(add3(a,mul3(delta,.7)))],tint(INK,.18),.65)

    def finger(self,points,active=False,ghost=False,radius=10):
        for a,b in zip(points,points[1:]):
            self.link(a,b,radius,active,ghost)
        if not ghost:
            for p in points[:-1]:
                self.c.joint(self.project(p),4.6,ACCENT if active else MUTED,1.7)

    def palm(self):
        # Smooth Catmull-Rom boundary sampled in the palm plane.
        knots=[(-56,27),(-64,59),(-54,103),(-46,117),(-28,110),(-5,125),(14,110),(34,116),(51,102),(68,98),(74,55),(61,14),(38,-5),(-22,-5),(-48,5)]
        boundary=[]
        for j,p1 in enumerate(knots):
            p0,p2,p3=knots[(j-1)%len(knots)],knots[(j+1)%len(knots)],knots[(j+2)%len(knots)]
            for k in range(12):
                t=k/12
                xy=tuple(.5*((2*p1[a])+(-p0[a]+p2[a])*t+(2*p0[a]-5*p1[a]+4*p2[a]-p3[a])*t*t+(-p0[a]+3*p1[a]-3*p2[a]+p3[a])*t*t*t) for a in range(2))
                boundary.append(self.project((*xy,0)))
        # An unshaded, thin back edge makes the oblique palm plane legible
        # without adding lighting or a volumetric rendered appearance.
        back=[self.project((x,y,-9)) for x,y in knots[10:]+knots[:2]]
        self.c.line(back,tint(INK,.32),1)
        for x,y in [knots[10],knots[12],knots[13],knots[0]]:
            self.c.line([self.project((x,y,0)),self.project((x,y,-9))],tint(INK,.32),1)
        self.c.polygon(boundary+[boundary[0]],PAPER,MUTED,1.6)
        for x in (-22,38):
            self.c.line([self.project((x,-5,0)),self.project((x,-12,0))],MUTED,1.3)
        seam=[self.project((*p,0)) for p in bezier((-37,43),(-11,62),(19,65),(48,59))]
        self.c.line(seam,tint(INK,.18),.7)

    def fixed_fingers(self,skip=None):
        for j,(base,lengths,dx) in enumerate(zip(self.bases,self.lengths,[-.06,0,.05,.14])):
            if j!=skip:
                self.finger(self.chain(base,lengths,(dx,1,0)))

    def thumb(self,q=0,active=False,ghost=False):
        a=q*78*pi/180
        # Palmar abduction rotates the first metacarpal OUT of z=0.
        direction=(-.2*cos(a),.9798*cos(a),sin(a))
        points=self.chain(self.cmc,self.thumb_lengths,direction)
        self.finger(points,active,ghost,11)
        return points


def palmar_abduction(i):
    c=EditorialCanvas();q,out,hold=m.phase(i)
    heading(c,4,'Palmar abduction','拇指掌侧外展 / 内收 · 完整手掌斜视线稿')
    view=HandView(c)
    # A quiet dashed plane surrounds the palm, so the moving thumb can
    # be read against an explicit spatial plane rather than guessed.
    plane=[view.project(p) for p in [(-73,1,0),(83,1,0),(83,130,0),(-73,130,0),(-73,1,0)]]
    c.dashed(plane,GHOST,.9,8)
    view.palm();view.fixed_fingers()
    view.thumb(0,ghost=True)
    points=view.thumb(q,active=True)
    pivot=view.project(view.cmc);tip=view.project(points[-1])
    c.text((78,283),'Thumb',18,INK)
    c.line([(140,295),(186,295),tip],MUTED,1)
    c.text((590,414),'Palm plane',16,MUTED)
    palm_target=view.project((83,76,0))
    c.line([(589,439),(561,453),palm_target],MUTED,1)
    c.text((259,551),'CMC',14,ACCENT,True)
    c.line([(300,558),pivot],MUTED,1)
    # A synchronized side view disambiguates palmar from radial abduction.
    # The palm edge stays horizontal; the thumb rises above that edge.
    c.text((84,337),'Side view',14,MUTED)
    c.line([(88,455),(246,455)],MUTED,1.5)
    c.line([(88,461),(246,461)],GHOST,.9)
    c.text((181,472),'Palm edge',12,MUTED)
    side_base=(112,455)
    side_angle=q*78*pi/180
    side_points=[side_base]
    for length in view.thumb_lengths:
        x,y=side_points[-1]
        side_points.append((x+.7*length*cos(side_angle),y-.7*length*sin(side_angle)))
    c.dashed([side_base,(side_base[0]+.7*sum(view.thumb_lengths),455)],GHOST,1.1,5)
    for a,b in zip(side_points,side_points[1:]):
        c.line([a,b],ACCENT,3)
    for point in side_points[:-1]:
        c.joint(point,2.5,ACCENT,1.2)
    c.text((84,511),'Lift out of',16,ACCENT)
    c.text((84,535),'the palm plane',16,ACCENT)
    # Arrow follows the actual thumb-tip sweep, rather than a generic
    # arc disconnected from a recognizable hand.
    sweep=[]
    for j in range(30):
        a=(.12+.78*j/29)*78*pi/180
        end=add3(view.cmc,mul3(unit3((-.2*cos(a),.9798*cos(a),sin(a))),sum(view.thumb_lengths)))
        u,v=view.project(end)
        sweep.append((u-14,v-15))
    if not hold:
        c.arrow(sweep if out else sweep[::-1],ACCENT,1.8)
    status(c,'Abduction','Adduction',out,hold,'手掌与其余四指固定；拇指抬离掌面' if out else '手掌与其余四指固定；拇指落回掌面附近')
    return c.finish()


def circumduction(i):
    c=EditorialCanvas()
    heading(c,6,'Circumduction','食指环转 · 完整手掌斜视线稿')
    view=HandView(c,yaw=-18,pitch=45,scale=1.6,origin=(442,541))
    view.palm();view.fixed_fingers(skip=0)
    # The resting thumb is opened radially for an unmistakable whole-hand
    # silhouette; it does not participate in the animated index motion.
    view.finger(view.chain(view.cmc,view.thumb_lengths,(-.7,.714,0)),radius=11)
    base=view.bases[0];lengths=view.lengths[0]
    bend,cone=21*pi/180,18*pi/180
    axis=(0,cos(bend),sin(bend))
    u=(1,0,0);v=(0,-sin(bend),cos(bend))
    def direction(theta):
        return add3(mul3(axis,cos(cone)),add3(mul3(u,sin(cone)*cos(theta)),mul3(v,sin(cone)*sin(theta))))
    def tip_at(theta):
        return view.project(add3(base,mul3(direction(theta),sum(lengths))))
    orbit=[tip_at(2*pi*j/120) for j in range(121)]
    c.dashed(orbit,GHOST,1.2,6)
    theta=2*pi*i/FRAMES
    points=view.chain(base,lengths,direction(theta))
    view.finger(points,active=True)
    tip=view.project(points[-1]);pivot=view.project(base)
    c.joint(tip,3.4,ACCENT,1.8)
    trail=[tip_at(theta-.75+.75*j/24) for j in range(25)]
    c.arrow(trail,ACCENT,2)
    c.text((77,237),'Index finger',18,INK)
    point=view.project(points[2])
    c.line([(174,253),(228,253),point],MUTED,1)
    c.text((558,149),'Fingertip',16,ACCENT)
    c.text((558,173),'draws a circle',16,ACCENT)
    c.line([(558,202),(535,202),tip],MUTED,1)
    c.text((106,470),'Fixed MCP',16,ACCENT)
    c.line([(195,484),(267,484),pivot],MUTED,1)
    c.text((572,453),'Other fingers',14,MUTED)
    c.text((572,477),'stay still',14,MUTED)
    c.line([(34,576),(766,576)],RULE,1)
    c.text((400,591),'Circumduction',24,ACCENT,center=True)
    c.text((400,643),'食指指根不移位，指尖绕圈；其余手指保持不动',17,INK,center=True,chinese=True)
    return c.finish()


def gif(frames,path):
    # Keep website colors exact and add antialias shades from shared samples.
    sample=Image.new('RGB',(W*4,H*2),PAPER)
    for j,index in enumerate([0,12,24,36,48,60,72,84]):
        sample.paste(frames[index].resize((W,H)),((j%4)*W,(j//4)*H))
    quant=sample.quantize(colors=96,method=Image.Quantize.MEDIANCUT)
    palette=quant.getpalette()
    for j,color in enumerate([PAPER,INK,ACCENT,MUTED,RULE]):
        palette[j*3:j*3+3]=list(ImageColor.getrgb(color))
    quant.putpalette(palette)
    indexed=[im.quantize(palette=quant,dither=Image.Dither.NONE) for im in frames]
    indexed[0].save(path,save_all=True,append_images=indexed[1:],duration=DURATION,loop=0,optimize=True,disposal=1)


def overview(all_frames,index):
    width,height=1840,1220
    sheet=Image.new('RGB',(width,height),PAPER)
    d=ImageDraw.Draw(sheet)
    d.text((34,20),'DEXTRAIL / KINEMATICS',fill=ACCENT,font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',14))
    d.text((34,47),'Hand motions',fill=INK,font=ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',36))
    d.text((317,61),'手部运动',fill=MUTED,font=ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',20))
    d.text((1200,64),'砖红：运动关节与方向    虚线：参考姿态 / 轨迹',fill=MUTED,font=ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',17))
    d.line((34,104,width-34,104),fill=RULE,width=1)
    for j,frames in enumerate(all_frames):
        panel=frames[index].resize((584,496),Image.Resampling.LANCZOS)
        sheet.paste(panel,(28+(j%3)*600,126+(j//3)*520))
    for x in (619,1219):
        d.line((x,142,x,1123),fill=RULE,width=1)
    d.line((34,1162,width-34,1162),fill=RULE,width=1)
    d.text((34,1180),'Anatomical motion schematic',fill=MUTED,font=ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',16))
    d.text((1260,1180),'指掌平面与运动轴已作示意简化',fill=MUTED,font=ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',15))
    return sheet


def main():
    import argparse
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--preview',action='store_true',help='Render one overview frame for visual inspection')
    args=parser.parse_args()
    OUT.mkdir(parents=True,exist_ok=True)
    m.Canvas=EditorialCanvas
    m.heading=heading
    m.status=status
    m.palm=palm
    renderers=m.RENDERERS[:3]+[
        ('thumb-palmar-abduction-adduction',palmar_abduction),
        m.RENDERERS[4],
        ('finger-circumduction',circumduction),
    ]
    if args.preview:
        frames=[[render(32)] for _,render in renderers]
        overview(frames,0).save(OUT/'hand-motions-overview-preview.png')
        for slug,render in renderers:
            render(32).save(OUT/f'{slug}.png')
        print('Preview rendered',flush=True)
        return
    all_frames=[]
    for slug,render in renderers:
        frames=[render(i) for i in range(FRAMES)]
        gif(frames,OUT/f'{slug}.gif')
        frames[32].save(OUT/f'{slug}.png')
        contact=Image.new('RGB',(W*3,H*2),PAPER)
        for j,i in enumerate([0,24,44,48,72,92]):
            contact.paste(frames[i],((j%3)*W,(j//3)*H))
        contact.save(OUT/f'{slug}-review.png')
        all_frames.append(frames)
        print(f'Rendered {slug}',flush=True)
    sheets=[overview(all_frames,i) for i in range(FRAMES)]
    gif(sheets,OUT/'hand-motions-overview.gif')
    sheets[32].save(OUT/'hand-motions-overview.png')
    print(f'Output: {OUT}',flush=True)


if __name__=='__main__':
    main()
