"""Sync source-reviewed DLR records into the site tables (2026-10-30)."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DATE='2026-10-30'
def read(name):return json.loads((ROOT/'data'/f'{name}.json').read_text(encoding='utf-8'))
def write(name,data):
 path=ROOT/'data'/f'{name}.json'
 if name=='sensing-audits':
  raw=path.read_text(encoding='utf-8')
  key='    "dlr-hand-ii": '
  block=json.dumps(data['hands']['dlr-hand-ii'],ensure_ascii=False,indent=2).replace('\n','\n    ')
  start=raw.find(key)
  if start>=0:
   value_start=start+len(key)
   _,length=json.JSONDecoder().raw_decode(raw[value_start:])
   raw=raw[:value_start]+block+raw[value_start+length:]
  else:
   end=raw.rfind('\n  }')
   raw=raw[:end]+',\n'+key+block+raw[end:]
  assert json.loads(raw)==data
  path.write_text(raw,encoding='utf-8')
 else:
  path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
base='https://www.dlr.de/de/rm/forschung/robotersysteme/hande/hand-ii'
i='https://www.dlr.de/en/rm/research/robotic-systems/hands/dlr-hand-i-1998'
hit='https://www.dlr.de/en/rm/research/robotic-systems/hands/dlr-hit-hand-ii'
paper='https://elib.dlr.de/55786/1/LiuHong-Multisensory_Five-Finger_Dexterous_Hand-IROS.pdf'
repo='https://github.com/eaa3/dlr_hit_hand_ii'
def source(title,url,**extra):return dict(title=title,url=url,**extra)
spec=source('DLR Hand II 官方数据表',base+'/data-sheet-of-dlr-hand-ii')
comm=source('DLR Hand II 官方通信架构',base+'/communication-architecture-of-dlr-hand-ii')
sensor=source('DLR Hand II 官方传感器说明',base+'/sensors-of-dlr-hand-ii')
control=source('DLR Hand II 官方控制说明',base+'/control')
rl=source('Sievers 等 · 手内操作与 PyBullet，2022','https://arxiv.org/abs/2204.03698')
def main():
 audits=read('sensing-audits')
 audits['hands']['dlr-hand-ii']=dict(
  version='四指 DLR Hand II · 官方数据表与传感器网页；历史配置',checked_on=DATE,
  sources=dict(spec={**spec,'locator':'Sensoren eines einzelnen Fingers'},sensor={**sensor,'locator':'Drehmoment / Positions / Geschwindigkeit Sensoren'},comm={**comm,'locator':'Kommunikationsprotokoll Ebene'}),
  channels=[])
 channels=audits['hands']['dlr-hand-ii']['channels']
 common=dict(status='documented',rate='整手通信周期 1 ms；不据此推断单个传感器的机械带宽。',calibration='通信说明记录逐指 EEPROM 存储标定参数；本轮未进行实物标定或精度评定。',configuration='官方历史 Hand II 配置；存量设备修订应另核对。',sources=['spec','sensor','comm'])
 channels.append(dict(**common,id='position',stage='joint',label='关节位置',tag='position-sensing',quantity='每指三个关节角读数。',location='关节端导电塑料电位器。',output='官方列角分辨率约 0.1°；不是绝对测角精度。',control='关节位置与阻抗控制反馈。',boundary='中末节耦合；有角度反馈不等于每个外形关节可独立驱动。'))
 channels.append(dict(**common,id='motor-position',stage='motor',label='电机位置与速度',quantity='每指三路电机位置 / 转速反馈。',location='电机内模拟霍尔传感器；传感网页说明每电机两个霍尔元件。',output='霍尔周期内插位置，速度由位置信号求导；不是直接测量外部接触力。',control='电机换相及运动控制。',boundary='电机角与关节角测量位置不同，传动弹性不能忽略。'))
 channels.append(dict(**common,id='joint-torque',stage='joint',label='关节转矩',tag='force-sensing',tag_label='关节转矩感知',quantity='每指三个主动轴的关节转矩。',location='关节端应变计测量结构。',output='转矩物理量；已读网页未给统一精度与串扰数值。',control='转矩反馈、阻抗与力控制。',boundary='关节转矩不是指尖六维力 / 力矩，也不是压力分布图。'))
 channels.append(dict(**common,id='fingertip-wrench',stage='contact',label='指尖六维力与力矩',tag='force-sensing',tag_label='指尖六维力感知',quantity='指尖合力 Fx、Fy、Fz 及力矩 Mx、My、Mz。',location='数据表列每指一个指尖六维单元。',output='传感网页列每方向 30 N、150 mN·m、12 bit；2004 论文给不同力矩量程，正文分别记录。',control='接触合力 / 力矩反馈；具体控制研究可能只使用关节传感。',boundary='六维合力单元不提供表面逐点触觉图；量程与位数不等于测量精度。'))
 write('sensing-audits',audits)
 articles=read('engineering-articles')
 for article in articles:
  if article['id']=='sensing-chain' and 'dlr-hand-ii' not in article['hand_ids']:
   article['hand_ids'].append('dlr-hand-ii')
 write('engineering-articles',articles)
 metrics=read('research-metrics')
 m=metrics['dlr-hand-ii']
 m.update(year=2001,transmission='hybrid-transmission',source=base)
 m['facts']=dict(company='德国航空航天中心 · DLR',country='德国',fingers=4,weight='1.8 kg（整手）',dimensions='约 300 × 150 × 150 mm',application='Justin 双手操作、多指抓握与控制研究',product_status='研究平台；2001 首次公开展示，当前供货状态未核实')
 m['audit']['checked_on']=DATE
 m['audit']['sources']=[source('官方设计与执行器计数',base+'/design-construction-of-dlr-hand-ii',kind='official'),{**spec,'kind':'official'}]
 m['audit']['facts']['materials']='铝制开放骨架；注塑塑料外壳'
 m['audit']['explanation']='四指各三主动轴与三个无刷电机；掌部另有一个有刷电机经丝杠同时调整第一、第四指。合计 13 主动自由度、13 电机。中末节 1:1 耦合；手指包含同步带、谐波减速与差动锥齿轮，地图按混合传动记录。'
 m['scope']=m['audit']['explanation']
 metrics['dlr-hand-i']['facts'].update(weight='1.8 kg（四指手体；控制箱另重 1.6 kg）')
 metrics['dlr-hit-hand-ii']['facts'].update(country='中国 / 德国',dimensions='单指总长 169.1 mm、基部宽 24.66 mm（2008 论文）；非整手尺寸')
 metrics['dlr-hit-hand-ii']['audit']=dict(checked_on=DATE,explanation='五个相同手指各三主动轴，共 15 轴和 15 电机；中末节钢丝 1:1 耦合。论文角度采用 Table III 的 D-H 约定，第三方 URDF 需独立核对。',gaps={},sources=[source('DLR/HIT Hand II 官方技术数据',hit,kind='official')],facts=dict(materials='铝制开放骨架；注塑塑料外壳'))
 write('research-metrics',metrics)
 kin=read('hand-kinematics')
 k=kin['dlr-hand-ii']
 k.update(checked_on=DATE,scope='四指 DLR Hand II · 官方数据表',summary='四指各 3 主动轴，掌部另 1 构形轴，共 13 DoF；中末节 1:1 耦合。',drive='12 个指内无刷电机加 1 个掌部有刷电机。指内采用同步带、100:1 谐波减速与基关节差动锥齿轮；近端同步带 1.2:1，中节 2:1。掌部通过丝杠联动第一、第四指。',ranges='官方数据表给出以下手指运动范围；中末节范围相同且 1:1 耦合，不能当作两个独立输入。角度符号沿用原表。',range_rows=[['每指','基关节屈伸','Extension / Flexion',-55,75],['每指','基关节展收','Abduction / Adduction',-37,37],['每指','中节与末节屈伸','1:1 耦合',-20,105]],gaps='掌部构形轴角度范围、标定零位及存量硬件修订仍待核实；手指范围、材料和连杆长度已有官方数据。',sources=[spec,source('DLR Hand II 官方设计',base+'/design-construction-of-dlr-hand-ii')],basic=dict(fingers=4,weight='1.8 kg（整手）',dimensions='约 300 × 150 × 150 mm',materials='铝制开放骨架；注塑塑料外壳'))
 k['capability']=dict(kind='原始论文 · 实机与仿真分别记录',text='2022 工作展示掌心向下、不依赖相机的方块连续旋转，单次超过 46 圈；使用关节角及控制误差历史与底层转矩控制。该任务结果不代表任意物体成功率。',source=rl['url'])
 k=kin['dlr-hand-i'];k['checked_on']=DATE
 k.setdefault('basic',{})['weight']='1.8 kg（手体；控制箱另重 1.6 kg）'
 k['gaps']='手体完整尺寸、结构材料、逐轴限位与零位、标定及长期可靠性仍待核实；1.8 kg 手体质量与 11 N 指尖力已有官方记录。'
 k=kin['dlr-hit-hand-ii'];k['checked_on']=DATE
 k['scope']='DLR/HIT Hand II · IROS 2008 原型 / Table III'
 k['ranges']='采用论文 Table III 的 D-H 角定义：θ1、θ2 为基部两轴，θ3、θ4 为耦合的指间轴。θ4 是随动关节；表中角度不自动等同第三方 URDF 的零位与软限位。'
 k['range_rows']=[['每指','θ1','论文 D-H 轴',0,90],['每指','θ2','论文 D-H 轴',-20,20],['每指','θ3','主动指间轴',0,90],['每指','θ4','1:1 耦合随动',0,90]]
 k['basic']['dimensions']='单指总长 169.1 mm、基部宽 24.66 mm（2008 论文）；非整手尺寸'
 k['gaps']='整手完整外形、各存量硬件修订、标定精度、第三方模型许可和运行兼容性待核实；重量、指节尺寸及论文关节范围已有证据。'
 write('hand-kinematics',kin)
 support=read('platform-support')
 s=support['dlr-hand-ii'];s['checked_on']=DATE
 s['hardware'].update(summary=kin['dlr-hand-ii']['summary'],drive=kin['dlr-hand-ii']['drive'],integration='系统页列 24 V DC（20 A）；历史数据表区分电机电源与电子器件 50 V / 20 kHz 电源。外部为四根电源线、八根串行通信线，定制快换连接；不能仅凭 24 V 记录重建接线。',sources=[spec,source('DLR Hand II 系统页',base)])
 s['sdk'].update(status='已有公开接口资料',language='历史控制软件架构已公开说明；未核实可安装的官方 SDK 及语言接口。',environment='双 PowerPC VME 板、VxWorks；FPGA 串行通信链路 10 Mbit/s。',api='官方说明传感与执行器更新周期 1 ms，已实现关节 / 笛卡尔 / 物体阻抗及力控；2022 研究另采用 10 Hz 策略、1 kHz 实机底层。',compatibility='以上是历史系统与具体研究配置；不代表现代 PC、ROS 或通用 SDK 可直接接入。',license='未核实官方软件包许可。',sources=[comm,control,rl])
 for model in s['models']:
  if model['format']=='其他仿真 / 学习模型':
   model.update(status='论文实现',detail='2022 原论文明确在 PyBullet 中建立并辨识模型，仿真环 500 Hz；尚未核实可下载文件及模型许可，未本机加载。',sources=[rl])
 s['resources']=[dict(name=x['title'],url=x['url'],note=n) for x,n in [(spec,'材料、角度范围、指节长度与传感器列表。'),(source('Butterfass 等 · Design and Experiences，2004','https://www.dlr.de/de/rm/downloads/roboter_und_systeme/hand/isora028.pdf/@@download/file'),'设计、示教与实验全文。'),(rl,'PyBullet、SAC 与实机迁移方法；不等于模型下载。'),(source('Pitz 等 · 目标姿态操作，2023','https://arxiv.org/abs/2303.04705'),'仿真与实机测试协议。'),(source('Winkelbauer 等 · 多接触抓握控制，2024','https://arxiv.org/abs/2409.12339'),'6 ms 研究控制器与实机实验。')]]
 s=support['dlr-hand-i'];s['checked_on']=DATE
 s['hardware']['integration']='官方控制箱为 120 × 110 × 220 mm、1.6 kg，独立于 1.8 kg 手体；手体尺寸与完整接线仍待核实。'
 s['resources']=[dict(name='DLR Hand I 官方机构与传感器',url=i,note='含质量、指尖力、控制箱及光学位置传感器说明。')]
 s=support['dlr-hit-hand-ii'];s['checked_on']=DATE
 s['hardware']['integration']='官方记录快换工具接口；2008 论文介绍 DSP / FPGA、PPSeCo / CAN 等路径。完整实物接线与供电规格待核实。'
 s['sdk'].update(status='已定位第三方 ROS 仓库',language='第三方 ROS 包；具体语言接口和依赖未验证。',environment='eaa3/dlr_hit_hand_ii · master，2026-10-30 检查；ROS 发行版与构建兼容性待核。',api='目录包含 dlr_description、dlr_hit_hand_ii、dlr_hit_hand_ii_hw 及 hittwo.urdf；未验证命令接口或实物控制。',compatibility='适用于五指 DLR/HIT Hand II 的第三方项目，不可替代四指 Hand II；模型零位、耦合与硬件修订需逐项比对。',license='本轮未核实模型和各子包的完整许可。',sources=[source('eaa3 第三方 ROS 仓库',repo)])
 for model in s['models']:
  if model['format']=='URDF / Xacro':
   model.update(status='第三方模型',detail='eaa3 仓库 master 的 hittwo.urdf 已定位，配有 dlr_description 目录；未本机加载，未验证惯量、限位、耦合、网格依赖与许可。',sources=[source('第三方 hittwo.urdf',repo+'/blob/master/hittwo.urdf')])
 s['resources']=[dict(name='eaa3 · ROS / URDF 目录',url=repo,note='第三方代码与模型文件入口；非官方 SDK 支持承诺。'),dict(name='Liu 等 · IROS 2008 全文',url=paper,note='Tables II–IV、机械与传感架构。')]
 write('platform-support',support)
 reports=read('report-pages')
 summaries={'dlr-hand-ii':'四指 13 DoF；官方材料、范围与传感数据已核实，补充阻抗控制、PyBullet 和 2022–2024 学习控制证据。','dlr-hand-i':'1998 四指多传感研究手；1.8 kg 手体、11 N 指尖力，控制箱与手体参数分别记录。','dlr-hit-hand-ii':'五指 15 DoF；补齐论文尺寸与关节范围，定位第三方 ROS / URDF 文件并注明兼容性与许可待核。'}
 for row in reports:
  key=Path(row['source']).stem
  if key in summaries:row.update(checked_on=DATE,summary=summaries[key],gaps=kin[key]['gaps'])
 write('report-pages',reports)
 lineage=read('product-lineages')
 for family in lineage['families']:
  if family['id']=='dlr-hit-hand-ii-review':
   family.update(reviewed_on=DATE,summary=summaries['dlr-hit-hand-ii'],open_questions=kin['dlr-hit-hand-ii']['gaps'])
   family['sources']['third-party-urdf']=source('eaa3 · 第三方 ROS / URDF',repo)
 write('product-lineages',lineage)
 # Research organizations are known facts, separate from commercial availability.
 metrics=read('research-metrics')
 institute='德国航空航天中心（DLR）机器人与机电一体化研究所'
 for key,m in metrics.items():
  if not key.startswith('dlr-'):
   continue
  joint=key.startswith('dlr-hit-')
  organization=('哈尔滨工业大学（HIT） / '+institute) if joint else institute
  country='中国 / 德国' if joint else '德国'
  if joint:
   org_url=('https://www.dlr.de/en/rm/downloads/roboter_und_systeme/hand/icra2003hitdlr.pdf/@@download/file' if key=='dlr-hit-hand-i' else 'https://www.dlr.de/de/rm/forschung/robotersysteme/hande/dlr-hit-hand-ii')
   org_title='HIT / DLR 联合研发 · 原论文作者单位' if key=='dlr-hit-hand-i' else 'DLR 官方 · HIT / DLR 联合研发说明'
   kind='paper' if key=='dlr-hit-hand-i' else 'official'
  else:
   org_url='https://elib.dlr.de/119008/' if key in ['dlr-hand-i','dlr-hand-ii','dlr-david','dlr-spacehand'] else (base.rsplit('/',1)[0]+'/clash' if key=='dlr-clash' else m['source'])
   org_title='DLR Multi-fingered Hands · 研发机构与系列历史' if 'elib.dlr.de' in org_url else 'DLR 机器人与机电一体化研究所 · 官方系统页'
   kind='report' if 'elib.dlr.de' in org_url else 'official'
  m.setdefault('facts',{}).update(company=organization,country=country)
  audit=m.setdefault('audit',dict(checked_on=DATE,explanation=m['scope'],gaps={},sources=[],facts={}))
  audit['checked_on']=DATE
  audit.setdefault('facts',{}).update(company=organization,country=country)
  if not any(x['url']==org_url for x in audit['sources']):
   audit['sources'].append(source(org_title,org_url,kind=kind))
  note=ROOT/'research/collection/hands'/f'{key}.md'
  text=note.read_text(encoding='utf-8-sig')
  marker='<!-- dlr-organization-2026-10-30 -->'
  if marker not in text:
   title,body=text.split('\n',1)
   detail=('联合研发单位为'+organization+'。HIT 为高校，DLR 为科研机构。' if joint else '研发单位为'+organization+'（Institute of Robotics and Mechatronics, German Aerospace Center），位于德国。机构类型为科研机构。')
   text=title+'\n\n'+marker+'\n\n## 研发机构\n\n**fact：** '+detail+' ['+org_title+']('+org_url+')\n'+body
   note.write_text(text,encoding='utf-8')
 write('research-metrics',metrics)
 print('Updated DLR technical records and research organizations for eight listed models.')

if __name__=='__main__':
 main()
