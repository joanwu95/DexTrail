"""Render original, two-ink hand-motion teaching diagrams using Pillow.

No source raster is edited. All frames come from explicit link geometry.
Angles are illustrative; these are not measured human or robot joint limits.
"""
from pathlib import Path
from math import sin, cos, pi, atan2, hypot, acos
from functools import lru_cache
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'website/docs/images/knowledge/hand-motions'
W, H, AA = 680, 570, 2
INK = '#223543'
TEAL = '#167d83'
MUTED = '#697d88'
GHOST = '#b9d6d8'
RULE = '#dce4e7'
WHITE = '#ffffff'
FRAMES = 96
DURATION = 80


@lru_cache(None)
def font(size, bold=False, chinese=False):
    name = ('msyhbd.ttc' if bold else 'msyh.ttc') if chinese else ('arialbd.ttf' if bold else 'arial.ttf')
    return ImageFont.truetype(str(Path('C:/Windows/Fonts') / name), round(size * AA))


class Canvas:
    def __init__(self):
        self.im = Image.new('RGB', (W*AA, H*AA), WHITE)
        self.d = ImageDraw.Draw(self.im)

    def line(self, pts, color=INK, width=2):
        self.d.line([(round(x*AA), round(y*AA)) for x, y in pts], fill=color, width=max(1, round(width*AA)), joint='curve')

    def text(self, xy, value, size=18, color=INK, bold=False, center=False, chinese=False):
        self.d.text((round(xy[0]*AA), round(xy[1]*AA)), value, font=font(size,bold,chinese), fill=color, anchor='mt' if center else 'lt')

    def ellipse(self, box, color=TEAL, width=2, fill=None):
        self.d.ellipse(tuple(round(v*AA) for v in box), outline=color, width=round(width*AA), fill=fill)

    def joint(self, p, radius=6, color=TEAL, width=2.5):
        x,y=p
        self.ellipse((x-radius,y-radius,x+radius,y+radius),color,width,WHITE)

    def dashed(self, pts, color=GHOST, width=1.7, dash=7):
        phase=0
        for a,b in zip(pts,pts[1:]):
            length=hypot(b[0]-a[0],b[1]-a[1])
            if length < .01:
                continue
            for step in range(int(length)+1):
                if int((phase+step)/dash)%2 == 0:
                    t=step/length; u=min((step+1)/length,1)
                    self.line([(a[0]+(b[0]-a[0])*t,a[1]+(b[1]-a[1])*t),(a[0]+(b[0]-a[0])*u,a[1]+(b[1]-a[1])*u)],color,width)
            phase += length

    def arrow(self, pts, color=TEAL, width=2.4):
        self.line(pts,color,width)
        a,b=pts[-2:]
        angle=atan2(b[1]-a[1],b[0]-a[0])
        self.line([(b[0]-10*cos(angle-.5),b[1]-10*sin(angle-.5)),b,(b[0]-10*cos(angle+.5),b[1]-10*sin(angle+.5))],color,width)

    def link(self,a,b,radius=9,color=TEAL,width=2.4,ghost=False):
        dx,dy=b[0]-a[0],b[1]-a[1]
        length=hypot(dx,dy)
        if length < 1:
            return
        ux,uy=dx/length,dy/length
        # Capsule with a gap at either end for the joint ring.
        a=(a[0]+ux*8,a[1]+uy*8); b=(b[0]-ux*8,b[1]-uy*8)
        angle=atan2(dy,dx)
        pts=[]
        for i in range(17):
            th=angle+pi/2+pi*i/16
            pts.append((a[0]+radius*cos(th),a[1]+radius*sin(th)))
        for i in range(17):
            th=angle-pi/2+pi*i/16
            pts.append((b[0]+radius*cos(th),b[1]+radius*sin(th)))
        pts.append(pts[0])
        if ghost:
            self.dashed(pts,color,width)
        else:
            self.line(pts,color,width)

    def chain(self,points,color=TEAL,width=2.5,ghost=False,radius=9):
        for a,b in zip(points,points[1:]):
            self.link(a,b,radius,color,width,ghost)
        if not ghost:
            for p in points[:-1]:
                self.joint(p,5,color,width)

    def finish(self):
        return self.im.resize((W,H),Image.Resampling.LANCZOS)


def chain(base,lengths,angles):
    pts=[base]
    for length,angle in zip(lengths,angles):
        a=angle*pi/180
        pts.append((pts[-1][0]+length*cos(a),pts[-1][1]+length*sin(a)))
    return pts


def phase(i):
    # Held endpoints and slow, symmetric easing: 7.68 seconds per cycle.
    f=i/FRAMES
    if f < .08:
        return 0,True,True
    if f < .46:
        return (1-cos(pi*(f-.08)/.38))/2,True,False
    if f < .54:
        return 1,False,True
    if f < .92:
        return (1+cos(pi*(f-.54)/.38))/2,False,False
    return 0,True,True


def heading(c,n,title,subtitle):
    c.text((30,24),f'{n:02}',16,TEAL,True)
    c.text((66,20),title,25,INK,True)
    c.text((66,59),subtitle,16,MUTED,chinese=True)
    c.line([(30,92),(650,92)],RULE,1)


def status(c,first,second,outward,hold,cn):
    c.line([(30,466),(650,466)],RULE,1)
    c.text((32,480),first,23,TEAL if outward else MUTED,outward)
    bbox=c.d.textbbox((0,0),second,font=font(23,not outward))
    right=648-(bbox[2]-bbox[0])/AA
    c.text((right,480),second,23,TEAL if not outward else MUTED,not outward)
    c.text((340,515),cn,18,INK,center=True,chinese=True)
    c.text((340,545),'END POSE' if hold else 'MOVING',11,MUTED,center=True)


BASES=[(270,315),(313,306),(356,313),(397,330)]
LENGTHS=[(64,49,35),(75,53,40),(69,49,35),(54,39,29)]


def palm(c):
    c.line([(261,325),(249,346),(240,354),(222,374),(233,409),(265,432),(298,438),(352,438),(386,416),(409,370),(406,344)],MUTED,1.8)
    c.line([(298,438),(298,457)],MUTED,1.8)
    c.line([(352,438),(352,457)],MUTED,1.8)
    c.line([(285,400),(325,388),(372,390)],RULE,1.2)


def resting_fingers(c,angles=None,color=INK):
    angles=angles or [-90]*4
    for base,lens,angle in zip(BASES,LENGTHS,angles):
        c.chain(chain(base,lens,[angle]*3),color,1.5,radius=9)


def static_thumb(c):
    c.chain(chain((254,395),(51,45,31),[-139,-130,-125]),INK,1.5,radius=10)


def finger_abduction(i):
    c=Canvas(); q,out,hold=phase(i)
    heading(c,1,'Abduction / Adduction','手指外展 / 内收 · 掌面视图')
    palm(c); static_thumb(c)
    for base,lens,angle in zip(BASES,LENGTHS,[-90]*4):
        c.chain(chain(base,lens,[angle]*3),GHOST,1.4,True)
    angles=[-90-23*q,-90,-90+14*q,-90+30*q]
    for base,lens,angle in zip(BASES,LENGTHS,angles):
        c.chain(chain(base,lens,[angle]*3))
    c.dashed([(313,118),(313,435)],MUTED,1,5)
    c.text((313,104),'Middle-finger axis',13,MUTED,center=True)
    if not hold:
        for x,y,direction in [(230,169,-1),(417,196,1)]:
            dx=24*direction*(1 if out else -1)
            c.arrow([(x-dx/2,y),(x+dx/2,y)])
    c.text((80,402),'MCP',14,TEAL,True)
    c.line([(126,410),(177,410),(247,329)],MUTED,1)
    status(c,'Abduction','Adduction',out,hold,'张开手指，远离中指轴线' if out else '并拢手指，回到中指轴线附近')
    return c.finish()


def flexion(i):
    c=Canvas();q,out,hold=phase(i)
    heading(c,2,'Flexion / Extension','手指屈曲 / 伸展 · 单指侧视图')
    # Palm runs left from MCP; flexion bends into its palmar side below.
    c.line([(90,245),(252,245),(275,261),(254,288),(92,288)],MUTED,1.8)
    c.text((128,255),'Palm',16,MUTED)
    base=(274,255); lengths=(106,76,54)
    c.chain(chain(base,lengths,[0,0,0]),GHOST,1.4,True,radius=12)
    pts=chain(base,lengths,[70*q,70*q+90*q,70*q+90*q+55*q])
    c.chain(pts,radius=12)
    for label,p in zip(['MCP','PIP','DIP'],pts[:-1]):
        c.text((p[0],p[1]-30),label,13,TEAL,True,center=True)
    c.text((540,215),'Straight',14,MUTED)
    c.text((126,323),'Palmar side',14,MUTED)
    if not hold:
        ang0,ang1=(5,58) if out else (58,5)
        arc=[(274+158*cos(a*pi/180),255+158*sin(a*pi/180)) for a in [ang0+(ang1-ang0)*j/25 for j in range(26)]]
        c.arrow(arc)
    status(c,'Flexion','Extension',out,hold,'指关节弯曲，指尖向掌侧卷入' if out else '指关节展开，弯曲的手指伸直')
    return c.finish()


def opposition(i):
    c=Canvas();q,out,hold=phase(i)
    heading(c,3,'Opposition / Reposition','拇指对掌 / 复位 · 掌面投影')
    palm(c)
    # A flexed index finger presents a target pad to the thumb.
    target=chain(BASES[0],LENGTHS[0],[-100,-190,-270])[-1]
    for j,(base,lens) in enumerate(zip(BASES,LENGTHS)):
        pts=chain(base,lens,[-100,-190,-270] if j==0 else [-90]*3)
        c.chain(pts,INK,1.5,radius=9)
    # Explicit thumb endpoint poses; shape-preserving inverse kinematics
    # keeps proximal and distal link lengths constant in this projection.
    base=(254,395)
    mcp=chain(base,(54,),[-139+27*q])[-1]
    start=chain(chain(base,(54,),[-139])[-1],(48,34),[-125,-118])[-1]
    tip=(start[0]+(target[0]-start[0])*q,start[1]+(target[1]-start[1])*q)
    # These are projection lengths. The axial-rotation pad inset below
    # explains the additional out-of-plane component explicitly.
    distance=hypot(tip[0]-mcp[0],tip[1]-mcp[1])
    axis=atan2(tip[1]-mcp[1],tip[0]-mcp[0])
    bend=acos(max(-1,min(1,(48**2+distance**2-34**2)/(2*48*distance))))
    midpoint=(mcp[0]+48*cos(axis-bend),mcp[1]+48*sin(axis-bend))
    ghost=chain(base,(54,48,34),[-139,-125,-118])
    c.chain(ghost,GHOST,1.4,True,radius=10)
    c.chain([base,mcp,midpoint,tip],radius=10)
    # Pad direction: small flat ellipse, then broad contact surface.
    rx=3+7*q
    c.ellipse((tip[0]-rx,tip[1]-5,tip[0]+rx,tip[1]+5),TEAL,2)
    c.text((64,229),'Index pad',14,MUTED)
    c.line([(133,242),(163,260),target],MUTED,1)
    c.text((76,419),'CMC',14,TEAL,True)
    c.line([(117,425),(187,425),base],MUTED,1)
    c.text((455,156),'Thumb pad',16,INK,True)
    c.text((455,181),'turns to face',14,MUTED)
    c.text((455,201),'the index pad',14,MUTED)
    # Flat inset denotes axial rotation rather than portraying a false
    # pure in-plane abduction as opposition.
    cx,cy=504,266
    c.ellipse((cx-34,cy-34,cx+34,cy+34),GHOST,1.5)
    ang=(-65+65*q)*pi/180
    c.line([(cx-25*cos(ang),cy-25*sin(ang)),(cx+25*cos(ang),cy+25*sin(ang))],TEAL,4)
    arc=[(cx+43*cos(a),cy+43*sin(a)) for a in [-1.3+j*.045 for j in range(26)]]
    if not hold:
        c.arrow(arc if out else arc[::-1],TEAL,1.8)
    c.text((504,323),'Axial rotation',13,MUTED,center=True)
    c.text((466,383),'Abduction + flexion',13,MUTED)
    c.text((466,404),'+ axial rotation',13,MUTED)
    status(c,'Opposition','Reposition',out,hold,'拇指指腹转向并接近食指指腹' if out else '拇指离开对掌姿态，回到原位')
    return c.finish()


def palmar_abduction(i):
    c=Canvas();q,out,hold=phase(i)
    heading(c,4,'Palmar abduction','拇指掌侧外展 / 内收 · 手掌侧视图')
    # Edge-on palm: thumb rotates anteriorly out of the palm plane.
    c.line([(88,374),(202,374),(438,374),(532,374)],MUTED,2)
    c.line([(88,398),(202,398),(438,398),(532,398)],MUTED,1.5)
    c.text((490,412),'Palm plane',14,MUTED,center=True)
    base=(221,374)
    rest=chain(base,(73,56,38),[0]*3)
    c.chain(rest,GHOST,1.4,True,radius=10)
    pts=chain(base,(73,56,38),[-78*q]*3)
    c.chain(pts,radius=10)
    c.text((193,421),'CMC',14,TEAL,True)
    c.line([(213,415),base],MUTED,1)
    c.arrow([(491,311),(491,191)],MUTED,1.4)
    c.text((491,157),'Out of palm plane',14,MUTED,center=True)
    c.text((101,329),'Wrist',14,MUTED)
    if not hold:
        arc=[(221+118*cos(a*pi/180),374-118*sin(a*pi/180)) for a in [10+j*2.3 for j in range(29)]]
        c.arrow(arc if out else arc[::-1])
    status(c,'Abduction','Adduction',out,hold,'拇指抬离手掌平面，向掌侧展开' if out else '拇指落回手掌平面附近')
    return c.finish()


def radial_abduction(i):
    c=Canvas();q,out,hold=phase(i)
    heading(c,5,'Radial abduction','拇指桡侧外展 / 内收 · 掌面视图')
    palm(c); resting_fingers(c)
    base=(254,395)
    rest=chain(base,(62,52,36),[-94]*3)
    c.chain(rest,GHOST,1.4,True,radius=10)
    pts=chain(base,(62,52,36),[-94-51*q]*3)
    c.chain(pts,radius=10)
    c.text((99,418),'CMC',14,TEAL,True)
    c.line([(138,426),(203,426),base],MUTED,1)
    if not hold:
        arc=[(254+174*cos(a*pi/180),395+174*sin(a*pi/180)) for a in [-96-j*1.7 for j in range(29)]]
        c.arrow(arc if out else arc[::-1])
    c.text((452,245),'In the',16,MUTED)
    c.text((452,268),'palm plane',16,MUTED)
    status(c,'Abduction','Adduction',out,hold,'拇指在手掌平面内，远离食指张开' if out else '拇指在手掌平面内，向食指靠回')
    return c.finish()


def circumduction(i):
    c=Canvas()
    heading(c,6,'Circumduction','环转 · 单指运动轨迹的平面投影')
    # Oblique orthographic projection of a cone: fixed MCP and distal tip
    # traces an ellipse. This is a planar diagram of a spatial motion.
    base=(337,396); theta=2*pi*i/FRAMES
    cx,cy=337,207;rx,ry=130,56
    orbit=[(cx+rx*cos(a),cy+ry*sin(a)) for a in [2*pi*j/120 for j in range(121)]]
    c.dashed(orbit,GHOST,1.8)
    for a in [0,pi/2,pi,3*pi/2]:
        end=(cx+rx*cos(a),cy+ry*sin(a))
        c.dashed([base,end],GHOST,1.2)
    c.line([(284,405),(280,443),(393,443),(390,405)],MUTED,1.8)
    tip=(cx+rx*cos(theta),cy+ry*sin(theta))
    pts=[(base[0]+(tip[0]-base[0])*s,base[1]+(tip[1]-base[1])*s) for s in [0,.45,.77,1]]
    c.chain(pts,radius=11)
    trail=[(cx+rx*cos(theta-0.8+j*.04),cy+ry*sin(theta-0.8+j*.04)) for j in range(21)]
    c.arrow(trail,TEAL,3)
    c.joint(tip,4,TEAL,2)
    c.text((337,130),'Fingertip path',14,MUTED,center=True)
    c.text((117,388),'Fixed MCP',14,TEAL,True)
    c.line([(199,397),(271,397),base],MUTED,1)
    c.text((529,272),'Not axial',14,MUTED,center=True)
    c.text((529,292),'twisting',14,MUTED,center=True)
    c.line([(30,466),(650,466)],RULE,1)
    c.text((340,480),'Circumduction',23,TEAL,True,center=True)
    c.text((340,515),'指根相对固定，指尖沿环形路径运动',18,INK,center=True,chinese=True)
    c.text((340,546),'Flexion + abduction + extension + adduction',12,MUTED,center=True)
    return c.finish()


RENDERERS=[
    ('finger-abduction-adduction',finger_abduction),
    ('finger-flexion-extension',flexion),
    ('thumb-opposition-reposition',opposition),
    ('thumb-palmar-abduction-adduction',palmar_abduction),
    ('thumb-radial-abduction-adduction',radial_abduction),
    ('finger-circumduction',circumduction),
]


def gif(frames,path):
    # One palette across all frames prevents colors from flickering.
    sample=Image.new('RGB',(W*4,H*2),WHITE)
    for j,index in enumerate([0,12,24,36,48,60,72,84]):
        sample.paste(frames[index].resize((W,H)),((j%4)*W,(j//4)*H))
    palette=sample.quantize(colors=64,method=Image.Quantize.MEDIANCUT)
    indexed=[im.quantize(palette=palette,dither=Image.Dither.NONE) for im in frames]
    indexed[0].save(path,save_all=True,append_images=indexed[1:],duration=DURATION,loop=0,optimize=True,disposal=1)


def main():
    OUT.mkdir(parents=True,exist_ok=True)
    all_frames=[]
    for slug,render in RENDERERS:
        frames=[render(i) for i in range(FRAMES)]
        gif(frames,OUT/f'{slug}.gif')
        frames[32].save(OUT/f'{slug}.png')
        all_frames.append(frames)
        print(f'Rendered {slug}',flush=True)
    # A compact overview; individual files preserve annotation legibility.
    overview=[]
    ow,oh=1800,1120
    for i in range(FRAMES):
        sheet=Image.new('RGB',(ow,oh),WHITE)
        draw=ImageDraw.Draw(sheet)
        draw.text((28,18),'HAND MOTIONS / 手部运动',fill=INK,font=ImageFont.truetype('C:/Windows/Fonts/msyhbd.ttc',30))
        draw.text((28,63),'Teal: moving links   |   Thin ink: reference structure   |   Dashed: reference pose / path',fill=MUTED,font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',18))
        for j,frames in enumerate(all_frames):
            panel=frames[i].resize((580,486),Image.Resampling.LANCZOS)
            sheet.paste(panel,(20+(j%3)*600,108+(j//3)*494))
        draw.line((600,112,600,1090),fill=RULE,width=1)
        draw.line((1200,112,1200,1090),fill=RULE,width=1)
        overview.append(sheet)
    gif(overview,OUT/'hand-motions-overview.gif')
    overview[32].save(OUT/'hand-motions-overview.png')
    # Contact sheets make endpoint/direction inspection possible without
    # relying on the image viewer to play GIFs.
    for slug,frames in zip([s for s,_ in RENDERERS],all_frames):
        contact=Image.new('RGB',(W*3,H*2),WHITE)
        for j,index in enumerate([0,24,44,48,72,92]):
            contact.paste(frames[index],((j%3)*W,(j//3)*H))
        contact.save(OUT/f'{slug}-review.png')
    print(f'Output: {OUT}',flush=True)


if __name__=='__main__':
    main()
