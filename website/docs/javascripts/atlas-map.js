/* Local SVG explorer. No CDN, downloaded media or inferred product relations. */
(() => {
  "use strict";
  const NS = "http://www.w3.org/2000/svg";
  const colors = ["#176c73", "#4166a1", "#7760a0", "#9b6744", "#278568", "#a6536e", "#637536", "#507d8c"];
  const evidence = {official: "官方支持", paper: "文献实现", experiment: "本人验证"};
  const make = (tag, cls, content) => {
    const el = document.createElement(tag);
    if (cls) el.className = cls;
    if (content != null) el.textContent = content;
    return el;
  };
  function init(root) {
    if (root.dataset.ready) return;
    root.dataset.ready = "true";
    const data = JSON.parse(root.dataset.atlasMap);
    // Script location anchors all navigation to the site's base, including subdirectory hosting.
    const script = [...document.scripts].find(s => s.src.includes("/javascripts/atlas-map.js"));
    const base = new URL("../", script.src);
    const url = path => new URL(path, base).href;
    let mode = data.hand ? "product" : "system";
    let hand = data.hands.find(h => h.id === data.hand) || data.hands[0];
    let filter = "all", selected = null;
    const terms = new Map();
    data.dimensions.forEach((d, i) => d.terms.forEach(t => terms.set(t.id, {...t, dimension: d, color: colors[i % colors.length]})));
    const sources = new Map(data.sources.map(s => [s.id, s]));
    root.replaceChildren();
    const toolbar = make("div", "atlas-map-toolbar");
    const modes = make("div", "atlas-map-modes");
    const systemButton = make("button", "", "系统结构");
    const productButton = make("button", "", "产品关联");
    [systemButton, productButton].forEach(b => { b.type = "button"; modes.append(b); });
    if (!data.hand) toolbar.append(modes);
    const handLabel = make("label", "atlas-map-control", "灵巧手 ");
    const handSelect = make("select");
    handSelect.setAttribute("aria-label", "选择灵巧手");
    data.hands.forEach(h => {
      const option = make("option", "", h.name + (h.status === "planned" ? " · 待核验" : ""));
      option.value = h.id; handSelect.append(option);
    });
    handSelect.value = hand.id;
    handLabel.append(handSelect);
    if (!data.hand) toolbar.append(handLabel);
    const filterLabel = make("label", "atlas-map-control", "技术维度 ");
    const filterSelect = make("select");
    filterSelect.setAttribute("aria-label", "筛选技术维度");
    [["all", "全部维度"], ...data.dimensions.map(d => [d.id, d.name])].forEach(([id, name]) => {
      const option = make("option", "", name); option.value = id; filterSelect.append(option);
    });
    filterLabel.append(filterSelect); toolbar.append(filterLabel);
    root.append(toolbar);
    const summary = make("p", "atlas-map-summary");
    root.append(summary);
    const stage = make("div", "atlas-map-stage");
    const svg = document.createElementNS(NS, "svg");
    svg.setAttribute("role", "group");
    svg.setAttribute("aria-label", "交互知识地图，按 Tab 选择节点，Enter 查看详情");
    stage.append(svg); root.append(stage);
    const legend = make("div", "atlas-map-legend");
    root.append(legend);
    const detail = make("section", "atlas-map-detail");
    detail.setAttribute("aria-live", "polite");
    root.append(detail);
    function link(label, path, external = false) {
      const a = make("a", "", label);
      a.href = external ? path : url(path);
      if (external) { a.target = "_blank"; a.rel = "noopener noreferrer"; }
      return a;
    }
    function show(node) {
      selected = node.id;
      svg.querySelectorAll("[data-node]").forEach(g => g.setAttribute("aria-pressed", String(g.dataset.node === selected)));
      detail.replaceChildren(make("span", "atlas-map-eyebrow", node.subtitle || "知识入口"), make("h3", "", node.label));
      if (node.dimension) {
        detail.append(make("p", "", "分类词条：" + node.dimension.terms.map(t => t.name).join(" · ")));
        detail.append(make("p", "", "这是资料组织分类，不代表任何产品具备这些能力。"));
        detail.append(link("进入分类 →", "technologies/#" + node.id));
      } else if (node.relations) {
        node.relations.forEach(r => {
          const block = make("div", "atlas-map-evidence");
          block.append(make("strong", "", evidence[r.evidence_type]), make("p", "", r.scope));
          r.sources.forEach(id => {
            const s = sources.get(id);
            block.append(link(s.title, s.url, true), make("small", "", "版本：" + s.version + " · 核验：" + s.verified_on));
          });
          detail.append(block);
        });
        detail.append(link("查看技术分类 →", "technologies/#" + node.id));
      } else if (node.id === "research") {
        detail.append(make("p", "", data.projects.map(p => p.name + "（" + ({planned:"计划中","in-progress":"进行中",completed:"已完成"}[p.status]) + "）").join("；")));
        detail.append(link("进入研究与实验 →", "research/"));
      } else if (mode === "product") {
        detail.append(make("p", "", hand.status === "planned" ? "尚无已核验技术关联。没有连线不代表产品不支持这些能力。" : "点击外围节点查看具体能力、适用条件和原始来源。"));
        if (hand.status !== "planned") detail.append(link("查看产品参数与分析 →", "hands/generated/" + hand.id + "/"));
      } else {
        detail.append(make("p", "", "从中心进入机械、感知、控制、仿真与研究案例。细灰线仅表示分类归属；切换产品关联查看有证据支持的连接。"));
      }
    }
    function render() {
      svg.replaceChildren(); selected = null;
      handLabel.hidden = mode !== "product"; filterLabel.hidden = mode !== "product";
      systemButton.setAttribute("aria-pressed", String(mode === "system"));
      productButton.setAttribute("aria-pressed", String(mode === "product"));
      let nodes;
      if (mode === "system") {
        nodes = data.dimensions.map((d, i) => ({id:d.id, label:d.name, subtitle:d.terms.length + " 个分类词条", dimension:d, color:colors[i % colors.length]}));
        nodes.push({id:"research", label:"研究与实验", subtitle:"方法 · 结果 · 复现", color:colors[7]});
      } else {
        const grouped = new Map();
        (hand.technologies || []).forEach(r => {
          const t = terms.get(r.id);
          if (filter !== "all" && t.dimension.id !== filter) return;
          if (!grouped.has(r.id)) grouped.set(r.id, {id:r.id, label:t.name, subtitle:t.dimension.name, color:t.color, relations:[]});
          grouped.get(r.id).relations.push(r);
        });
        nodes = [...grouped.values()];
      }
      const w = Math.max(320, stage.clientWidth);
      const wide = w >= 700;
      const rows = Math.ceil(nodes.length / 2);
      const h = wide ? Math.max(470, rows * 76 + 130) : Math.max(230, rows * 94 + 160);
      svg.setAttribute("viewBox", "0 0 " + w + " " + h);
      svg.style.height = h + "px";
      const center = {id:"center", label: mode === "system" ? "灵巧操作" : "Shadow Hand",
        subtitle: mode === "system" ? "DEXTEROUS MANIPULATION" : hand.name, x:w/2, y:wide?h/2:52, color:"#243f4b"};
      if (mode === "product" && hand.id !== "shadow-hand") center.label = hand.name.split("（")[0];
      const nodeW = wide ? 168 : Math.min(162, (w-34)/2);
      const positions = nodes.map((n, i) => {
        if (wide) {
          const side = i < Math.ceil(nodes.length/2) ? -1 : 1;
          const list = side === -1 ? nodes.slice(0, Math.ceil(nodes.length/2)) : nodes.slice(Math.ceil(nodes.length/2));
          const idx = side === -1 ? i : i-Math.ceil(nodes.length/2);
          return {...n, x:side === -1 ? 100 : w-100, y:h/2 + (idx-(list.length-1)/2)*86};
        }
        return {...n, x:i%2===0 ? w/4 : 3*w/4, y:160+Math.floor(i/2)*94};
      });
      const s = (tag, attrs, content) => {
        const el = document.createElementNS(NS, tag);
        Object.entries(attrs || {}).forEach(([k,v]) => el.setAttribute(k,v));
        if (content != null) el.textContent = content;
        return el;
      };
      positions.forEach(n => {
        const types = mode === "system" ? ["structure"] : [...new Set(n.relations.map(r => r.evidence_type))];
        types.forEach((type, i) => {
          const startX = wide ? center.x + (n.x<center.x ? -90:90) : center.x;
          const startY = wide ? center.y : 88;
          const endX = wide ? n.x + (n.x<center.x ? nodeW/2:-nodeW/2) : n.x;
          const endY = wide ? n.y : n.y-31;
          const path = s("path", {d:"M "+startX+" "+(startY+i*5)+" C "+startX+" "+endY+", "+endX+" "+startY+", "+endX+" "+endY,
            class:"atlas-map-edge " + type});
          svg.append(path);
        });
      });
      function draw(n, central) {
        const g = s("g", {transform:"translate("+n.x+" "+n.y+")", role:"button", tabindex:"0", "aria-label":n.label+"，查看详情", "aria-pressed":"false", "data-node":n.id, class:"atlas-map-node"});
        const width = central ? (wide ? 188 : Math.min(w-28,310)) : nodeW;
        g.append(s("rect", {x:-width/2,y:-33,width,height:66,rx:central?20:12,fill:central?"#243f4b":"#fff",stroke:n.color}));
        if (!central) g.append(s("circle",{cx:-width/2+13,cy:-12,r:3.5,fill:n.color}));
        const font = n.label.length > 15 ? 11 : 14;
        g.append(s("text", {y:-5,"text-anchor":"middle",fill:central?"white":"#233f4b","font-size":font,"font-weight":"650"}, n.label));
        const subtitle = central && mode === "product" ? "点击节点查看证据" : n.subtitle;
        g.append(s("text",{y:17,"text-anchor":"middle",fill:central?"#d1e2e5":"#627480","font-size":10},subtitle));
        g.addEventListener("click", () => show(n));
        g.addEventListener("keydown", e => { if(e.key==="Enter" || e.key===" ") {e.preventDefault();show(n);} });
        svg.append(g);
      }
      positions.forEach(n => draw(n, false)); draw(center, true);
      summary.textContent = mode === "system" ? "系统结构 · 点击任意节点进入知识分支" :
        hand.name + " · " + nodes.length + " 个技术节点 / " + nodes.reduce((sum,n)=>sum+n.relations.length,0) + " 条证据关联";
      legend.replaceChildren();
      (mode==="system" ? [["structure","分类归属（非能力）"]] : [["official","官方支持"],["paper","文献实现"],["experiment","本人验证"]]).forEach(([cls,label]) => {
        const item = make("span", "", label);
        item.prepend(make("i", cls)); legend.append(item);
      });
      if (!nodes.length) {
        const empty = s("text",{x:w/2,y:150,"text-anchor":"middle",fill:"#627480","font-size":13}, "暂无符合条件的已核验关联");
        svg.append(empty);
      }
      show(center);
    }
    systemButton.onclick = () => {mode="system";render();};
    productButton.onclick = () => {mode="product";render();};
    handSelect.onchange = () => {hand=data.hands.find(h=>h.id===handSelect.value);render();};
    filterSelect.onchange = () => {filter=filterSelect.value;render();};
    let lastWidth = 0;
    new ResizeObserver(entries => {
      const width = Math.round(entries[0].contentRect.width);
      if (width !== lastWidth) {lastWidth=width;render();}
    }).observe(stage);
    render();
  }
  const boot = () => document.querySelectorAll("[data-atlas-map]").forEach(init);
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded",boot); else boot();
})();
