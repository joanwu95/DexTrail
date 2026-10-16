"""Publish the source-audited TARS DexHand entry (2026-10-15)."""
import importlib.util
from pathlib import Path
spec=importlib.util.spec_from_file_location('registry',Path(__file__).with_name('expand-curated-hands.py'))
r=importlib.util.module_from_spec(spec)
spec.loader.exec_module(r)
r.DATE='2026-10-15'
r.records=[]
key='tars-dexhand'
recap='https://www.prnewswire.com/news-releases/tars-brings-real-life-embodied-ai-to-icra-2026-robotics-conference-302790438.html'
debut='https://www.prnewswire.com/news-releases/from-mind-to-hand-tars-brings-a-dexterous-hand-with-brain-and-awe3-0-to-icra-2026--302788465.html'
sources=[dict(title='TARS 官方发布稿 · 2026-06-08',url=recap),dict(title='TARS 官方首秀公告 · 2026-06-02',url=debut)]
r.add(key,'TARS DexHand · 它石智航','它石智航 · TARS',2026,'官方 ICRA 2026 发布稿',
 '厂商标称 21 DOF、人手尺度；逐指主动 / 耦合分配和电机数量未核清，地图主动轴坐标留空。',
 None,None,'geared-drive',
 [('整手','标称 21 DOF；主动分配待核','未公开耦合表','仿人手掌骨与指骨拓扑'),
 ('拇指','逐轴数量待核','轴序待核','厂商强调 CMC / MCP 轴线空间交汇')],
 '刚性准直驱，自研关节集成精密减速器。官方称使用三类电机及减速器，这是器件种类，不是仅三个电机。减速比与背隙数值待核。',
 '指尖微型相机与弹性体触觉层构成视触觉路线。官方称纹理细节达 0.05 mm、采集频率 >240 Hz；不等同于定位精度、测力精度或闭环控制频率。编码器、独立力传感器及本体感知配置待核。',
 '官方展示 26 个英文字母手势、实时镜像交互，并介绍 AWE 3.0 触觉理解；未给出统一任务成功率和端到端延迟。',
 '未取得逐关节限位、轴序和零位表。',
 '重量、毫米尺寸、指尖力、负载、扭矩、速度、功耗、接口、耐久协议与售价未在已读官方资料中核实；尚未确认量产交付。',
 '工程解释：仿人拓扑便于人类动作映射；刚性减速传动仍需检查摩擦、背隙与接触安全。准直驱称呼不能代替低阻抗和力控实测，视触觉效果也依赖标定与模型。',
 spec=recap,time_source=debut,
 time_detail='2026-06-02 官方公告记录 ICRA 2026 全球首秀；采用展示年，不视为上市或量产日期。',
 facts=dict(fingers=5,country='中国',dimensions='厂商称 1:1 人手尺度；毫米尺寸表待核',materials='触觉层为弹性体；骨架材料待核',product_status='2026 公开展示；供货、量产与售价待核',application='精细接触操作与具身学习；适用性需任务验证'),
 extra_sources=[(sources[1]['title'],debut)],
 media=[dict(kind='image',url='https://mma.prnewswire.com/media/2994436/TARS_1.jpg',label='TARS 官方 ICRA 展示图')])
def main():
 candidate='research/sources/tars-2026-10-15-media.json'
 r.write(candidate,{key:dict(source=recap,assets=r.records[0]['media'])})
 r.main(r.records,candidate,'research/sources/tars-2026-10-15-published.json','<!-- tars-audit-2026-10-15 -->')
 reports=r.read('data/report-pages.json')
 next(x for x in reports if x['source'].endswith('/tars-dexhand.md'))['checked_on']=r.DATE
 r.write('data/report-pages.json',reports)
 support=r.read('data/platform-support.json')
 support[key]=dict(checked_on=r.DATE,version='ICRA 2026 公开配置',
  hardware=dict(summary=r.records[0]['summary'],drive=r.records[0]['drive'],integration='供电、安装、电气与通信接口待核。',sources=sources),
  sdk=dict(status='尚未核实',language='未核实',environment='未核实',api='PID、阻抗、力控与模型控制接口未公开核实。',compatibility='AWE 3.0 集成陈述不等于可下载 SDK；镜像演示不等于公开遥操作接口。',license='未核实',sources=sources),
  models=[dict(format=f,status='尚未核实',detail='未核实本型号下载文件；不等于不支持。',sources=[]) for f in ['CAD / 制造文件','URDF / Xacro','MuJoCo / MJCF','Isaac Sim / Lab / Gym','Gazebo','其他仿真 / 学习模型']],
  resources=[dict(name='WIYH · 相关人类操作数据项目',url='https://wiyh.tars-ai.com/',note='相关生态入口，不等于本手专用数据集、SDK 或仿真。')],
  validation='文档核查；未运行实物、控制或仿真。')
 r.write('data/platform-support.json',support)
 lineage=r.read('data/product-lineages.json')
 family=dict(id='tars-dexhand-family',organization='它石智航 · TARS',name='TARS DexHand',reviewed_on=r.DATE,member_ids=[key],status='review',mode='review',
  summary='ICRA 2026 公开配置；未建立代际关系。',scope='本轮仅收录 TARS DexHand 五指灵巧手。',
  open_questions='未取得足以建立前后代关系的公开版本文件。',
  sources={'debut':sources[1]},summary_sources=['debut'],
  milestones=[dict(id=key+'-record',hand_id=key,name='TARS DexHand',kind='公开展示',date='2026-06-02',date_relation='by',date_label='至迟 2026.06.02',date_basis='当日官方公告已记录首秀，不是供货日。',summary=r.records[0]['summary'],sources=['debut'])],
  relationships=[],comparisons=[],ecosystem=[])
 lineage['families']=[f for f in lineage['families'] if f['id']!=family['id']]+[family]
 lineage['reviewed_on']=r.DATE
 r.write('data/product-lineages.json',lineage)
 note=r.ROOT/'research/collection/hands/tars-dexhand.md'
 content=note.read_text(encoding='utf-8')
 marker='<!-- tars-resource-scope -->'
 if marker not in content:
  content+='\n'+marker+'\n\n## 机械与参数边界\n\n'+r.records[0]['drive']+' [官方硬件依据]('+recap+')\n\n## 控制与演示\n\n'+r.records[0]['capability']+' [官方演示依据]('+debut+')\n\n## 软件、论文与资源\n\n未核实本型号专用论文、CAD、URDF、MJCF、MuJoCo、Isaac Sim、ROS 包或公开 SDK。相关 [WIYH 数据项目](https://wiyh.tars-ai.com/) 不等于本手专用模型。官方公告含展示图，本轮未核实可嵌入的官方视频。\n\n## 参数差异处理\n\n采用 6 月 8 日官方稿的 0.05 mm 纹理细节与 >240 Hz 采集陈述，不混用其他报道的 0.03 mm，也不转换为运动控制指标。全部为厂商陈述，尚无本轮独立测试。\n'
  note.write_text(content,encoding='utf-8')
if __name__=='__main__':main()
