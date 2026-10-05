/* Official streams only. No product-image guesses or autoplay on page load. */
(() => {
  const root = document.querySelector('[data-sudo-videos]');
  if (!root) return;
  const video = root.querySelector('video');
  const play = root.querySelector('.sudo-play');
  const status = root.querySelector('.sudo-video-status');
  const choices = [...root.querySelectorAll('[data-stream]')];
  let current = choices[0], hls = null, library = null, generation = 0;
  function loadLibrary() {
    if (!library) library = new Promise((resolve, reject) => {
      const script = document.createElement('script');
      script.src = new URL(root.dataset.player, document.baseURI);
      script.onload = resolve; script.onerror = reject; document.head.append(script);
    });
    return library;
  }
  function failure() {
    status.textContent = '视频暂时无法加载，可点击“官网出处”观看或重新播放。';
    play.hidden = false; play.disabled = false; play.textContent = '重新播放';
  }
  async function start() {
    const token = ++generation;
    play.disabled = true; status.textContent = '正在连接官网视频…';
    hls?.destroy(); hls = null; video.pause(); video.removeAttribute('src'); video.load();
    try {
      if (video.canPlayType('application/vnd.apple.mpegurl')) {
        video.src = current.dataset.stream;
      } else {
        await loadLibrary();
        if (token !== generation) return;
        if (!window.Hls?.isSupported()) throw new Error('HLS unavailable');
        hls = new Hls({maxBufferLength: 20, maxMaxBufferLength: 40});
        hls.on(Hls.Events.ERROR, (_event, data) => {
          if (data.fatal && token === generation) { hls?.destroy(); hls = null; failure(); }
        });
        hls.loadSource(current.dataset.stream); hls.attachMedia(video);
      }
      play.hidden = true; play.disabled = false;
      video.play().catch(() => {
        if (token !== generation) return;
        status.textContent = '视频已连接；请使用播放器的播放按钮。';
      });
    } catch { if (token === generation) { library = null; failure(); } }
  }
  play.addEventListener('click', start);
  for (const button of choices) button.addEventListener('click', () => {
    current = button;
    choices.forEach(b => b.setAttribute('aria-pressed', String(b === button)));
    root.querySelector('.sudo-video-title').textContent = button.textContent;
    root.querySelector('.sudo-video-description').textContent = button.dataset.description;
    start();
  });
  video.addEventListener('playing', () => { status.textContent = '正在播放 · 苏度官网原视频'; });
  video.addEventListener('error', () => { if (video.currentSrc) failure(); });
  window.addEventListener('pagehide', () => { generation++; hls?.destroy(); });
})();
