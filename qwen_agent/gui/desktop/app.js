/**
 * Qwen-Agent Desktop v2 · app.js
 * SPA Router · i18n · Discovery · SSE Streaming
 */

// ═══════════════════════════════════════════
//  i18n Strings
// ═══════════════════════════════════════════
const I18N = {
  zh: {
    newChat:'新对话', chat:'对话', discover:'发现', searchConv:'搜索对话…',
    mySpace:'我的空间', welcomeTitle:'你好，我是 Qwen-Agent',
    welcomeSub:'有什么可以帮你的？', recording:'录音', ppt:'PPT',
    avMedia:'音视频', documents:'文档', modeTask:'任务助理',
    modeThink:'深度思考', modeCode:'代码', modeAnalyze:'文本分析',
    modeTranslate:'翻译', webSearch:'联网搜索', wsAuto:'自动联网搜索',
    wsOn:'开启联网搜索', wsOff:'关闭联网搜索',
    inputPlaceholder:'向 Qwen-Agent 提问…', hotNew:'热门上新',
    discoverTitle:'智能代码，轻松编程一键读写',
    discoverSub:'探索 Qwen-Agent 的强大工具和智能体',
    fcPpt:'PPT创作', fcPptDesc:'一句话生成精美PPT演示文稿',
    fcStart:'✎ 开始创作', fcRecord:'实时记录',
    fcRecordDesc:'语音转文字，智能分析对话内容',
    fcStartRecord:'🎙 开始录音', fcVideo:'音视频速读',
    fcVideoDesc:'音视频内容快速提取和总结', fcUpload:'📤 开始上传',
    catAll:'全部分类', catDraw:'绘图', catUtil:'实用',
    catFun:'娱乐', catLearn:'学习', catWork:'职场',
    searchTools:'搜索智能体', toolRead:'阅读助手',
    toolReadDesc:'文档问答、总结翻译', toolLink:'链接速读',
    toolLinkDesc:'解析网页和图客链接', toolNote:'AI笔记',
    toolNoteDesc:'个人知识管理和笔记', settingsTitle:'⚙ 设置',
    sgAppearance:'外观', darkMode:'深色模式', darkModeDesc:'切换界面主题',
    language:'语言', languageDesc:'界面显示语言', sgSystem:'系统',
    sysInfo:'系统信息', convCount:'对话数量', sgData:'数据',
    clearAll:'清除所有对话', clearAllDesc:'此操作不可撤销',
    clearBtn:'清除', version:'版本', you:'你', confirmClear:'确定要清除所有对话吗？',
    modeResearch:'深度研究', modeImage:'图像', modeMore:'更多', modeWrite:'写作',
    fileProcessing:'文档处理中…', fileProcessed:'份对话文档处理完成',
    backToChat:'回到对话', imgProcessing:'图片分析中…', imgProcessed:'图片分析完成',
    // Recording page
    recReady:'准备录音', recStart:'开始录音', recPause:'暂停', recResume:'继续',
    recRecording:'录音中…', recPaused:'已暂停', recProcessing:'正在转写…',
    recFinished:'录音完成', recCancel:'取消', recDone:'完成', recTranscript:'转写结果',
    recCopy:'📋 复制文本', recAnalyze:'🤖 AI 分析',
    // PPT page
    pptTopic:'主题描述', pptTopicPh:'描述你想要的PPT主题，例如：AI在教育领域的应用趋势分析',
    pptStyle:'风格选择', pptPages:'页数设置', pptPageUnit:'页',
    pptGenerate:'生成 PPT', pptGenerating:'正在生成大纲…', pptResult:'生成结果',
    pptCopyOutline:'📋 复制大纲', pptRefine:'✨ 优化细化',
    tplBiz:'商务', tplTech:'科技', tplEdu:'教育', tplCre:'创意', tplMin:'极简',
    // Audio/Video page
    avUploadTitle:'上传音视频文件', avUploadSub:'支持 MP3, MP4, WAV, M4A, WebM 等格式',
    avSelectFile:'选择文件', avStep1:'上传文件', avStep2:'音频提取',
    avStep3:'语音识别', avStep4:'内容分析',
    avSummary:'内容摘要', avTranscript:'完整文稿', avTimeline:'时间线',
    avCopy:'📋 复制', avAsk:'💬 向AI提问',
    // Document page
    docUploadTitle:'上传文档', docUploadSub:'支持 PDF, DOCX, TXT, Markdown 等格式',
    docSelectFile:'选择文件', docQaTitle:'文档问答', docQaPh:'对文档内容提问…',
    // Tool cards — Drawing
    tdAiDraw:'🎨 AI绘画', tdAiDrawD:'描述画面，AI为你生成精美图片',
    tdStory:'🌺 古风小绘本', tdStoryD:'创作古风绘本故事与插图',
    tdLogo:'🎯 Logo设计', tdLogoD:'一句话生成品牌 Logo',
    tdAvatar:'👤 头像生成', tdAvatarD:'生成个性化头像和头照',
    // Tool cards — Utility
    tdFmt:'🔄 格式转换', tdFmtD:'万能文件格式转换助手',
    tdRewrite:'✍️ 文本改写', tdRewriteD:'智能改写，保留原意优化表达',
    tdTranslate:'🌐 翻译助手', tdTranslateD:'多语言互译，专业精准',
    tdCode:'💻 代码助手', tdCodeD:'编写、调试、解释代码',
    // Tool cards — Fun
    tdTitle:'💥 爆炸标题党', tdTitleD:'生成吸引眼球的爬文标题',
    tdStoryWrite:'📚 故事创作', tdStoryWriteD:'创作小说、童话、剧本故事',
    tdRole:'🎭 角色扮演', tdRoleD:'AI扮演任意角色对话',
    tdPuzzle:'🧩 脑筋急转弯', tdPuzzleD:'趣味谜语和智力挑战',
    // Tool cards — Learning
    tdKnowledge:'💡 知识问答', tdKnowledgeD:'任何问题，即问即答',
    tdPaper:'🎓 论文助手', tdPaperD:'学术写作、摘要、综述生成',
    tdEnglish:'📖 英语老师', tdEnglishD:'英语学习、练习、纠错',
    tdMath:'📊 数学辅导', tdMathD:'解题步骤详解，从小学到大学',
    // Tool cards — Work
    tdPolish:'✨ 文本润色', tdPolishD:'专业文档润色，提升表达质量',
    tdReport:'📋 周报生成', tdReportD:'一键生成工作周报/月报',
    tdEmail:'✉️ 邮件写作', tdEmailD:'商务邮件、回复模板生成',
    tdInterview:'💼 面试模拟', tdInterviewD:'AI模拟面试官，练习问答',
  },
  en: {
    newChat:'New Chat', chat:'Chat', discover:'Discover', searchConv:'Search chats…',
    mySpace:'My Space', welcomeTitle:'Hello, I\'m Qwen-Agent',
    welcomeSub:'How can I help you?', recording:'Record', ppt:'PPT',
    avMedia:'A/V Media', documents:'Docs', modeTask:'Task Assistant',
    modeThink:'Deep Think', modeCode:'Code', modeAnalyze:'Text Analysis',
    modeTranslate:'Translate', webSearch:'Web Search', wsAuto:'Auto web search',
    wsOn:'Enable web search', wsOff:'Disable web search',
    inputPlaceholder:'Ask Qwen-Agent…', hotNew:'Trending',
    discoverTitle:'Smart Coding, One-Click Read & Write',
    discoverSub:'Explore Qwen-Agent\'s powerful tools and agents',
    fcPpt:'PPT Creator', fcPptDesc:'Generate beautiful PPTs in one sentence',
    fcStart:'✎ Start Creating', fcRecord:'Live Recording',
    fcRecordDesc:'Speech-to-text with intelligent analysis',
    fcStartRecord:'🎙 Start Recording', fcVideo:'A/V Quick Read',
    fcVideoDesc:'Fast extraction & summary from media', fcUpload:'📤 Upload',
    catAll:'All', catDraw:'Drawing', catUtil:'Utility',
    catFun:'Fun', catLearn:'Learning', catWork:'Work',
    searchTools:'Search agents', toolRead:'Reading Assistant',
    toolReadDesc:'Document Q&A, summarize & translate', toolLink:'Link Reader',
    toolLinkDesc:'Parse web and image links', toolNote:'AI Notes',
    toolNoteDesc:'Personal knowledge management', settingsTitle:'⚙ Settings',
    sgAppearance:'Appearance', darkMode:'Dark Mode', darkModeDesc:'Toggle UI theme',
    language:'Language', languageDesc:'Interface language', sgSystem:'System',
    sysInfo:'System Info', convCount:'Conversations', sgData:'Data',
    clearAll:'Clear All Chats', clearAllDesc:'This cannot be undone',
    clearBtn:'Clear', version:'Version', you:'You', confirmClear:'Clear all conversations?',
    modeResearch:'Deep Research', modeImage:'Image', modeMore:'More', modeWrite:'Writing',
    fileProcessing:'Processing document…', fileProcessed:' document(s) processed',
    backToChat:'Back to chat', imgProcessing:'Analyzing image…', imgProcessed:'Image analysis complete',
    recReady:'Ready', recStart:'Start Recording', recPause:'Pause', recResume:'Resume',
    recRecording:'Recording…', recPaused:'Paused', recProcessing:'Transcribing…',
    recFinished:'Done', recCancel:'Cancel', recDone:'Done', recTranscript:'Transcript',
    recCopy:'📋 Copy Text', recAnalyze:'🤖 AI Analyze',
    pptTopic:'Topic Description', pptTopicPh:'Describe your PPT topic, e.g.: AI trends in education',
    pptStyle:'Style', pptPages:'Page Count', pptPageUnit:'pages',
    pptGenerate:'Generate PPT', pptGenerating:'Generating outline…', pptResult:'Result',
    pptCopyOutline:'📋 Copy Outline', pptRefine:'✨ Refine',
    tplBiz:'Business', tplTech:'Tech', tplEdu:'Education', tplCre:'Creative', tplMin:'Minimal',
    avUploadTitle:'Upload Audio/Video', avUploadSub:'Supports MP3, MP4, WAV, M4A, WebM, etc.',
    avSelectFile:'Select File', avStep1:'Upload', avStep2:'Extract Audio',
    avStep3:'Speech Recognition', avStep4:'Content Analysis',
    avSummary:'Summary', avTranscript:'Full Transcript', avTimeline:'Timeline',
    avCopy:'📋 Copy', avAsk:'💬 Ask AI',
    docUploadTitle:'Upload Document', docUploadSub:'Supports PDF, DOCX, TXT, Markdown, etc.',
    docSelectFile:'Select File', docQaTitle:'Document Q&A', docQaPh:'Ask about the document…',
    tdAiDraw:'🎨 AI Drawing', tdAiDrawD:'Describe a scene, AI generates art',
    tdStory:'🌺 Storybook', tdStoryD:'Create illustrated storybooks',
    tdLogo:'🎯 Logo Design', tdLogoD:'Generate brand logos in one sentence',
    tdAvatar:'👤 Avatar Gen', tdAvatarD:'Generate personalized avatars',
    tdFmt:'🔄 Format Convert', tdFmtD:'Universal file format converter',
    tdRewrite:'✍️ Text Rewrite', tdRewriteD:'Rewrite text while keeping meaning',
    tdTranslate:'🌐 Translator', tdTranslateD:'Multi-language professional translation',
    tdCode:'💻 Code Helper', tdCodeD:'Write, debug, explain code',
    tdTitle:'💥 Title Gen', tdTitleD:'Generate viral clickbait titles',
    tdStoryWrite:'📚 Story Writer', tdStoryWriteD:'Create novels, fairy tales, scripts',
    tdRole:'🎭 Roleplay', tdRoleD:'AI plays any character you want',
    tdPuzzle:'🧩 Brain Teasers', tdPuzzleD:'Fun riddles and challenges',
    tdKnowledge:'💡 Knowledge QA', tdKnowledgeD:'Any question, instant answer',
    tdPaper:'🎓 Paper Helper', tdPaperD:'Academic writing & summarization',
    tdEnglish:'📖 English Tutor', tdEnglishD:'English practice & correction',
    tdMath:'📊 Math Tutor', tdMathD:'Step-by-step math solutions',
    tdPolish:'✨ Text Polish', tdPolishD:'Professional document polishing',
    tdReport:'📋 Report Gen', tdReportD:'Generate weekly/monthly reports',
    tdEmail:'✉️ Email Writer', tdEmailD:'Business email templates',
    tdInterview:'💼 Interview Prep', tdInterviewD:'AI mock interview practice',
  }
};

// ═══════════════════════════════════════════
//  State
// ═══════════════════════════════════════════
const state = {
  lang: 'zh', currentPage: 'chat', currentMode: 'chat',
  currentModel: 'claude-sonnet-4-5', currentModelName: 'Claude Sonnet 4.5',
  currentConvId: null, streaming: false, streamBuffer: '', abortCtrl: null,
  conversations: [], webSearch: 'auto', attachments: [], models: [],
  previousPage: 'chat',
};

const $ = (s) => document.querySelector(s);
const $$ = (s) => document.querySelectorAll(s);
let dom = {};

// ═══════════════════════════════════════════
//  API
// ═══════════════════════════════════════════
async function apiGet(p) { try { return await (await fetch(p)).json(); } catch(e) { return null; } }
async function apiPost(p, b={}) { try { return await (await fetch(p,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(b)})).json(); } catch(e) { return null; } }

// ═══════════════════════════════════════════
//  i18n Engine
// ═══════════════════════════════════════════
function t(key) { return (I18N[state.lang] || I18N.zh)[key] || key; }

function applyI18n() {
  $$('[data-i18n]').forEach(el => { el.textContent = t(el.dataset.i18n); });
  $$('[data-i18n-placeholder]').forEach(el => { el.placeholder = t(el.dataset.i18nPlaceholder); });
  document.documentElement.lang = state.lang === 'zh' ? 'zh-CN' : 'en';
  renderToolGrid();
}

function setLang(lang) {
  state.lang = lang;
  localStorage.setItem('qa-lang', lang);
  // Update all lang selectors
  $$('.lang-select button').forEach(b => b.classList.toggle('active', b.dataset.lang === lang));
  applyI18n();
}

// ═══════════════════════════════════════════
//  Router
// ═══════════════════════════════════════════
function navigateTo(page) {
  if (state.currentPage !== page) state.previousPage = state.currentPage;
  state.currentPage = page;
  // Show the correct page
  $$('.page').forEach(p => p.classList.toggle('active', p.id === 'page-' + page));
  // Update sidebar nav
  $$('.sidebar-nav button').forEach(b => b.classList.toggle('active', b.dataset.page === page));
  // Update global bottom nav
  $$('.gnav-item').forEach(b => b.classList.toggle('active', b.dataset.nav === page));
  // Show/hide input area (only on chat page)
  const inputArea = $('#input-area');
  if (inputArea) inputArea.style.display = (page === 'chat') ? '' : 'none';
  // Focus input on chat
  if (page === 'chat' && dom.input) dom.input.focus();
}

// ═══════════════════════════════════════════
//  Splash
// ═══════════════════════════════════════════
function initSplash() {
  setTimeout(() => {
    dom.splash.classList.add('hidden');
    dom.app.classList.add('visible');
    setTimeout(() => { if (dom.splash) dom.splash.remove(); }, 600);
  }, 2200);
}

// ═══════════════════════════════════════════
//  Theme
// ═══════════════════════════════════════════
function initTheme() {
  if (localStorage.getItem('qa-theme') === 'dark') document.body.classList.add('dark');
  syncToggle();
}
function toggleTheme() {
  document.body.classList.toggle('dark');
  localStorage.setItem('qa-theme', document.body.classList.contains('dark') ? 'dark' : 'light');
  syncToggle();
}
function syncToggle() {
  if (dom.toggleDark) dom.toggleDark.classList.toggle('on', document.body.classList.contains('dark'));
}

// ═══════════════════════════════════════════
//  Sidebar
// ═══════════════════════════════════════════
function toggleSidebar() {
  if (window.innerWidth <= 900) {
    dom.app.classList.toggle('sidebar-expanded');
  } else {
    dom.app.classList.toggle('sidebar-collapsed');
  }
}

async function loadConversations() {
  const convs = await apiGet('/api/conversations');
  if (!convs) return;
  state.conversations = convs;
  renderConvList(convs);
  if (dom.convCount) dom.convCount.textContent = convs.length;
}

function renderConvList(convs) {
  const q = (dom.convSearch ? dom.convSearch.value : '').trim().toLowerCase();
  const list = q ? convs.filter(c => c.title.toLowerCase().includes(q)) : convs;
  dom.convList.innerHTML = list.map(c => `
    <div class="conv-item ${c.id === state.currentConvId ? 'active' : ''}" data-id="${c.id}">
      <span class="conv-icon">💬</span>
      <span class="conv-title">${esc(c.title)}</span>
      <button class="conv-delete" title="Delete">✕</button>
    </div>`).join('');
  dom.convList.querySelectorAll('.conv-item').forEach(el => {
    el.addEventListener('click', (e) => {
      if (e.target.classList.contains('conv-delete')) { e.stopPropagation(); deleteConv(el.dataset.id); }
      else { navigateTo('chat'); switchConv(el.dataset.id); }
    });
  });
}

async function switchConv(id) {
  if (state.streaming) return;
  state.currentConvId = id;
  const msgs = await apiPost('/api/conversations/switch', { id });
  if (msgs) renderMessages(msgs);
  highlightActive();
}

async function deleteConv(id) {
  await apiPost('/api/conversations/delete', { id });
  if (state.currentConvId === id) { state.currentConvId = null; showWelcome(); }
  loadConversations();
}

function highlightActive() {
  dom.convList.querySelectorAll('.conv-item').forEach(el => {
    el.classList.toggle('active', el.dataset.id === state.currentConvId);
  });
}

async function newChat() {
  if (state.streaming) return;
  const r = await apiPost('/api/conversations/new');
  if (!r) return;
  state.currentConvId = r.id;
  navigateTo('chat');
  showWelcome();
  loadConversations();
  dom.input.focus();
}

// ═══════════════════════════════════════════
//  Messages
// ═══════════════════════════════════════════
function showWelcome() { dom.welcome.classList.remove('hidden'); dom.messages.classList.add('hidden'); dom.messages.innerHTML = ''; }
function showMessages() { dom.welcome.classList.add('hidden'); dom.messages.classList.remove('hidden'); }

function renderMessages(msgs) {
  if (!msgs || !msgs.length) { showWelcome(); return; }
  showMessages();
  dom.messages.innerHTML = msgs.map(m => msgHtml(m.role, m.content)).join('');
  scrollBottom();
}

function msgHtml(role, content) {
  const isUser = role === 'user';
  const avatar = isUser ? 'U' : '<img src="Qwen3.png" alt="Q">';
  const label = isUser ? t('you') : 'Qwen-Agent';
  return `<div class="msg ${role}">
    <div class="msg-avatar">${avatar}</div>
    <div class="msg-body"><div class="msg-role">${label}</div>
    <div class="msg-content">${isUser ? esc(content) : fmtMd(content)}</div></div></div>`;
}

function appendUserMsg(text) { showMessages(); dom.messages.insertAdjacentHTML('beforeend', msgHtml('user', text)); scrollBottom(); }
function appendBotPlaceholder() {
  showMessages();
  dom.messages.insertAdjacentHTML('beforeend',
    `<div class="msg assistant msg-streaming" id="stream-msg">
      <div class="msg-avatar"><img src="Qwen3.png" alt="Q"></div>
      <div class="msg-body"><div class="msg-role">Qwen-Agent</div>
      <div class="msg-content"><span class="cursor-blink"></span></div></div></div>`);
  scrollBottom();
}
function updateStream(text) { const el=$('#stream-msg .msg-content'); if(el) el.innerHTML=fmtMd(text)+'<span class="cursor-blink"></span>'; scrollBottom(); }
function finalizeStream(text) { const el=$('#stream-msg'); if(!el) return; el.removeAttribute('id'); el.classList.remove('msg-streaming'); const c=el.querySelector('.msg-content'); if(c) c.innerHTML=fmtMd(text); }
function scrollBottom() { requestAnimationFrame(()=>{dom.chatArea.scrollTop=dom.chatArea.scrollHeight;}); }

// ═══════════════════════════════════════════
//  Send + SSE
// ═══════════════════════════════════════════
async function sendMessage() {
  let text = dom.input.value.trim();
  // Append file attachments content
  if (state.attachments.length > 0) {
    const parts = state.attachments.filter(a => a.content).map(a => {
      if (a.type === 'image') return `[附件图片: ${a.name}]`;
      return `\n--- 文件: ${a.name} ---\n\`\`\`\n${a.content}\n\`\`\``;
    });
    if (parts.length) text = (text || `请分析以下${state.attachments.length}个文件`) + '\n' + parts.join('\n');
    state.attachments = [];
    renderAttachList();
  }
  if (!text || state.streaming) return;
  dom.input.value = ''; autoResize();
  state.streaming = true; state.streamBuffer = ''; dom.btnSend.disabled = true;
  navigateTo('chat');
  appendUserMsg(text); appendBotPlaceholder();

  state.abortCtrl = new AbortController();
  try {
    const resp = await fetch('/api/chat', {
      method:'POST', headers:{'Content-Type':'application/json'},
      body: JSON.stringify({text, mode:state.currentMode, model:state.currentModel, web_search:state.webSearch}),
      signal: state.abortCtrl.signal,
    });
    const reader = resp.body.getReader();
    const decoder = new TextDecoder();
    let buf = '';
    while (true) {
      const {done, value} = await reader.read();
      if (done) break;
      buf += decoder.decode(value, {stream:true});
      const lines = buf.split('\n'); buf = lines.pop();
      let evt = '';
      for (const line of lines) {
        if (line.startsWith('event: ')) evt = line.slice(7).trim();
        else if (line.startsWith('data: ')) { handleSSE(evt, line.slice(6)); evt = ''; }
      }
    }
  } catch(e) { if(e.name!=='AbortError') { state.streamBuffer+='\n\n⚠️ '+e.message; updateStream(state.streamBuffer); } }
  finalizeStream(state.streamBuffer);
  state.streaming=false; state.abortCtrl=null; dom.btnSend.disabled=false;
  loadConversations();
}

function handleSSE(evt, data) {
  if (evt==='token') { try { state.streamBuffer+=JSON.parse(data); updateStream(state.streamBuffer); } catch(e){} }
  else if (evt==='error') { try { state.streamBuffer+='\n\n⚠️ '+JSON.parse(data); updateStream(state.streamBuffer); } catch(e){} }
  else if (evt==='title') { try { const i=JSON.parse(data); const el=document.querySelector(`.conv-item[data-id="${i.id}"] .conv-title`); if(el) el.textContent=i.title; } catch(e){} }
}
function cancelStream() { if(state.abortCtrl) state.abortCtrl.abort(); }

// ═══════════════════════════════════════════
//  Models
// ═══════════════════════════════════════════
async function loadModels() {
  const models = await apiGet('/api/models'); if(!models) return;
  state.models = models;
  dom.modelDropdown.innerHTML = models.map(m => `
    <div class="model-option ${m.id===state.currentModel?'active':''}" data-id="${m.id}">
      <span>${esc(m.name)}</span><span class="provider">${esc(m.provider)}</span>
    </div>`).join('');
  dom.modelDropdown.querySelectorAll('.model-option').forEach(el => {
    el.addEventListener('click', (e) => { e.stopPropagation(); selectModel(el.dataset.id, el.querySelector('span').textContent); });
  });
  // Sync sub-page model selectors
  updateSubpageModels();
}
async function selectModel(id, name) {
  state.currentModel=id; state.currentModelName=name;
  dom.modelName.textContent=name; dom.modelDropdown.classList.remove('show');
  await apiPost('/api/model',{model:id});
  dom.modelDropdown.querySelectorAll('.model-option').forEach(el => el.classList.toggle('active',el.dataset.id===id));
  // Sync sub-page model selectors
  updateSubpageModels();
}

// ═══════════════════════════════════════════
//  Chips + Web Search
// ═══════════════════════════════════════════
function initChips() {
  $$('.mode-chips .chip').forEach(c => c.addEventListener('click', () => {
    $$('.chip').forEach(x=>x.classList.remove('active')); c.classList.add('active');
    state.currentMode = c.dataset.mode;
  }));
}

function initWebSearch() {
  const btn = $('#btn-web-search'), dd = $('#web-search-dropdown');
  btn.addEventListener('click', (e) => { e.stopPropagation(); dd.classList.toggle('show'); });
  dd.querySelectorAll('.ws-option').forEach(opt => {
    opt.addEventListener('click', (e) => {
      e.stopPropagation();
      state.webSearch = opt.dataset.ws;
      dd.querySelectorAll('.ws-option').forEach(o => { o.classList.toggle('active', o===opt); o.querySelector('.ws-check').textContent = o===opt?'✓':''; });
      dd.classList.remove('show');
    });
  });
  document.addEventListener('click', () => dd.classList.remove('show'));
}

// ═══════════════════════════════════════════
//  Global Bottom Nav
// ═══════════════════════════════════════════
function initGlobalNav() {
  $$('.gnav-item').forEach(btn => {
    btn.addEventListener('click', () => {
      navigateTo(btn.dataset.nav);
    });
  });
}

// ═══════════════════════════════════════════
//  Sub-page Model Selectors
// ═══════════════════════════════════════════
function initSubpageModels() {
  $$('[data-model-select]').forEach(wrap => {
    const nameEl = wrap.querySelector('.smodel-name');
    const dd = wrap.querySelector('.smodel-dropdown');
    if (!nameEl || !dd) return;

    // Toggle dropdown
    wrap.addEventListener('click', (e) => {
      e.stopPropagation();
      // Close all other dropdowns first
      $$('.smodel-dropdown.show').forEach(d => { if (d !== dd) d.classList.remove('show'); });
      dd.classList.toggle('show');
    });
  });
  // Close all on outside click
  document.addEventListener('click', () => {
    $$('.smodel-dropdown.show').forEach(d => d.classList.remove('show'));
  });
}

function updateSubpageModels() {
  // Sync all sub-page model selectors with current state
  $$('[data-model-select]').forEach(wrap => {
    const nameEl = wrap.querySelector('.smodel-name');
    const dd = wrap.querySelector('.smodel-dropdown');
    if (!nameEl || !dd) return;
    const mObj = state.models.find(m => m.id === state.currentModel);
    nameEl.textContent = mObj ? mObj.name : (state.currentModelName || state.currentModel || 'Model');
    // Rebuild dropdown
    dd.innerHTML = state.models.map(m =>
      `<div class="smd-item${m.id === state.currentModel ? ' active' : ''}" data-mid="${m.id}">${m.name}</div>`
    ).join('');
    // Bind click
    dd.querySelectorAll('.smd-item').forEach(item => {
      item.addEventListener('click', async (e) => {
        e.stopPropagation();
        const mid = item.dataset.mid;
        state.currentModel = mid;
        await apiPost('/api/model', { model: mid });
        dom.modelName.textContent = state.models.find(m => m.id === mid)?.name || mid;
        updateSubpageModels();
        dd.classList.remove('show');
      });
    });
  });
}

// ═══════════════════════════════════════════
//  Toast Notification
// ═══════════════════════════════════════════
function showToast(html, duration = 4000) {
  const el = $('#toast');
  el.innerHTML = html;
  el.classList.add('show');
  setTimeout(() => el.classList.remove('show'), duration);
}

// ═══════════════════════════════════════════
//  More Chips Dropdown
// ═══════════════════════════════════════════
function initMoreChips() {
  const btn = $('#btn-more-chips');
  const dd = $('#more-chips-dropdown');
  if (!btn || !dd) return;
  btn.addEventListener('click', (e) => { e.stopPropagation(); dd.classList.toggle('show'); });
  dd.querySelectorAll('.chip').forEach(c => {
    c.addEventListener('click', (e) => {
      e.stopPropagation();
      $$('.chip').forEach(x => x.classList.remove('active'));
      c.classList.add('active');
      state.currentMode = c.dataset.mode;
      dd.classList.remove('show');
    });
  });
  document.addEventListener('click', () => dd.classList.remove('show'));
}

// ═══════════════════════════════════════════
//  Discovery Page
// ═══════════════════════════════════════════
// ── Tool definitions (category + prompt for each) ──
function getToolDefs() {
  return [
    // Drawing (draw)
    {id:'aiDraw',  cat:'draw', name:t('tdAiDraw'),  desc:t('tdAiDrawD'),  stat:'3.8万+', prompt:'请根据以下描述生成一幅画面：'},
    {id:'story',   cat:'draw', name:t('tdStory'),   desc:t('tdStoryD'),   stat:'1.2万+', prompt:'请帮我创作一个古风绘本故事，包含每页的文字和画面描述：'},
    {id:'logo',    cat:'draw', name:t('tdLogo'),    desc:t('tdLogoD'),    stat:'8600+',  prompt:'请为以下品牌设计一个Logo，并用文字描述设计方案：'},
    {id:'avatar',  cat:'draw', name:t('tdAvatar'),  desc:t('tdAvatarD'),  stat:'5200+',  prompt:'请帮我设计一个个性化头像，风格描述如下：'},
    // Utility (util)
    {id:'fmt',       cat:'util', name:t('tdFmt'),       desc:t('tdFmtD'),       stat:'1.2万+', prompt:'请帮我进行以下格式转换：'},
    {id:'rewrite',   cat:'util', name:t('tdRewrite'),   desc:t('tdRewriteD'),   stat:'2.6万+', prompt:'请改写以下文本，保持原意但优化表达：\n\n'},
    {id:'translate', cat:'util', name:t('tdTranslate'), desc:t('tdTranslateD'), stat:'5.1万+', prompt:'请将以下内容翻译（自动识别语言并翻译为另一种语言）：\n\n'},
    {id:'code',      cat:'util', name:t('tdCode'),      desc:t('tdCodeD'),      stat:'9.3万+', prompt:'请帮我编写以下代码（请说明语言和需求）：'},
    // Fun (fun)
    {id:'title',      cat:'fun', name:t('tdTitle'),      desc:t('tdTitleD'),      stat:'4100+',  prompt:'请为以下主题生成5个吸引眼球的爆款标题：\n\n主题：'},
    {id:'storyWrite', cat:'fun', name:t('tdStoryWrite'), desc:t('tdStoryWriteD'), stat:'3.5万+', prompt:'请为我创作一个故事，类型和主题如下：'},
    {id:'role',       cat:'fun', name:t('tdRole'),       desc:t('tdRoleD'),       stat:'8.7万+', prompt:'请你扮演以下角色与我对话（请描述角色设定）：'},
    {id:'puzzle',     cat:'fun', name:t('tdPuzzle'),     desc:t('tdPuzzleD'),     stat:'2.2万+', prompt:'请给我出一道有趣的脑筋急转弯或智力题！'},
    // Learning (learn)
    {id:'knowledge', cat:'learn', name:t('tdKnowledge'), desc:t('tdKnowledgeD'), stat:'12.8万+', prompt:'请详细解答以下问题：'},
    {id:'paper',     cat:'learn', name:t('tdPaper'),     desc:t('tdPaperD'),     stat:'6.4万+',  prompt:'请帮我撰写以下学术内容（论文摘要/综述/大纲）：'},
    {id:'english',   cat:'learn', name:t('tdEnglish'),   desc:t('tdEnglishD'),   stat:'4.7万+',  prompt:'请作为英语老师，帮我练习以下内容（可以纠错、翻译、解释语法）：\n\n'},
    {id:'math',      cat:'learn', name:t('tdMath'),      desc:t('tdMathD'),      stat:'3.9万+',  prompt:'请详细解答以下数学题，给出完整解题步骤：\n\n'},
    // Work (work)
    {id:'polish',    cat:'work', name:t('tdPolish'),    desc:t('tdPolishD'),    stat:'7.2万+', prompt:'请润色以下文本，使其更加专业、流畅：\n\n'},
    {id:'report',    cat:'work', name:t('tdReport'),    desc:t('tdReportD'),    stat:'5.6万+', prompt:'请根据以下要点帮我生成一份工作周报：\n\n本周完成：\n下周计划：\n需要协调：'},
    {id:'email',     cat:'work', name:t('tdEmail'),     desc:t('tdEmailD'),     stat:'4.3万+', prompt:'请帮我写一封商务邮件，内容要求如下：'},
    {id:'interview', cat:'work', name:t('tdInterview'), desc:t('tdInterviewD'), stat:'3.1万+', prompt:'请你作为面试官，模拟面试以下职位，开始提问：\n\n应聘职位：'},
  ];
}

let _currentToolCat = 'all';
let _toolSearchQuery = '';

// ── Global: category filter (called from inline onclick) ──
function filterToolCat(btn, cat) {
  $$('.cat-tab').forEach(tab => tab.classList.remove('active'));
  btn.classList.add('active');
  _currentToolCat = cat;
  renderToolGrid();
}

// ── Global: open a dedicated tool sub-page (chat-style) ──
let _currentTool = null;
let _toolStreaming = false;
let _toolFirstMsg = true;

function _toolSetupPage(tool) {
  _currentTool = tool;
  _toolFirstMsg = true;
  const parts = tool.name.split(' ');
  const label = parts.slice(1).join(' ') || tool.name;

  const elTitle = $('#tool-page-title');
  const elDesc = $('#tool-page-desc');
  const elMsgs = $('#tool-chat-messages');
  const elInput = $('#tool-page-input');

  if (elTitle) elTitle.textContent = label;
  if (elDesc) elDesc.textContent = tool.desc;
  if (elMsgs) elMsgs.innerHTML = '';
  if (elInput) { elInput.value = ''; elInput.placeholder = tool.prompt || '在这里和我对话'; }

  navigateTo('tool');
  if (elInput) elInput.focus();
}

function openTool(toolId) {
  const tools = getToolDefs();
  const tool = tools.find(t => t.id === toolId);
  if (!tool) return;
  _toolSetupPage(tool);
}

function useToolPrompt(prompt) {
  _toolSetupPage({ id: '_adhoc', cat: 'util', name: '🤖 AI助手', desc: '智能对话助手', stat: '', prompt: prompt });
}

// ── Append a chat message to the tool chat area ──
function _toolAppendUser(text) {
  const el = $('#tool-chat-messages');
  if (!el) return;
  const div = document.createElement('div');
  div.className = 'tcm-user';
  div.textContent = text;
  el.appendChild(div);
  el.scrollTop = el.scrollHeight;
}

function _toolAppendAI() {
  const el = $('#tool-chat-messages');
  if (!el) return null;
  const wrap = document.createElement('div');
  wrap.className = 'tcm-ai';
  wrap.innerHTML = `<div class="tcm-ai-avatar"><img src="Qwen3.png" alt="Q"></div><div class="tcm-ai-body"></div>`;
  el.appendChild(wrap);
  el.scrollTop = el.scrollHeight;
  return wrap.querySelector('.tcm-ai-body');
}

function _toolAppendAIActions(bodyEl) {
  const el = $('#tool-chat-messages');
  if (!el || !bodyEl) return;
  const acts = document.createElement('div');
  acts.className = 'tcm-ai-actions';
  acts.innerHTML = `<button title="复制" onclick="navigator.clipboard.writeText(this.parentElement.previousElementSibling.querySelector('.tcm-ai-body').innerText).then(()=>{this.textContent='✅';setTimeout(()=>this.textContent='📋',1200)})">📋</button>`;
  // Insert after the tcm-ai wrapper
  bodyEl.closest('.tcm-ai').after(acts);
  el.scrollTop = el.scrollHeight;
}

// ── Tool page: send user input to API and stream result ──
async function toolSend() {
  if (_toolStreaming || !_currentTool) return;
  const elInput = $('#tool-page-input');
  const btnSend = $('#tool-page-send');
  if (!elInput) return;

  const userText = elInput.value.trim();
  if (!userText && !_toolFirstMsg) return;

  // On first message, prepend tool system prompt
  const displayText = userText || _currentTool.prompt;
  const fullPrompt = _toolFirstMsg
    ? (_currentTool.prompt + (userText ? '\n' + userText : ''))
    : userText;
  _toolFirstMsg = false;

  // Show user bubble
  _toolAppendUser(displayText);
  elInput.value = '';

  // Create AI bubble
  const aiBody = _toolAppendAI();
  if (!aiBody) return;
  aiBody.innerHTML = '<span class="tcm-typing">正在思考…</span>';

  _toolStreaming = true;
  if (btnSend) btnSend.disabled = true;

  try {
    const result = await readSSETokens('/api/chat', {
      text: fullPrompt,
      model: state.currentModel,
      ephemeral: true,
    }, (partial) => {
      aiBody.innerHTML = fmtMd(partial);
      const el = $('#tool-chat-messages');
      if (el) el.scrollTop = el.scrollHeight;
    });
    aiBody.innerHTML = fmtMd(result || '(无响应)');
    _toolAppendAIActions(aiBody);
  } catch (e) {
    aiBody.innerHTML = `<span style="color:#ef4444">请求失败: ${esc(e.message)}</span>`;
  } finally {
    _toolStreaming = false;
    if (btnSend) btnSend.disabled = false;
    const el = $('#tool-chat-messages');
    if (el) el.scrollTop = el.scrollHeight;
  }
}

// ── Init tool page event bindings ──
function initToolPage() {
  const btnSend = $('#tool-page-send');
  const elInput = $('#tool-page-input');

  if (btnSend) btnSend.addEventListener('click', toolSend);
  // Enter to send (single-line input, just Enter)
  if (elInput) {
    elInput.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); toolSend(); }
    });
  }
}

function renderToolGrid() {
  const tools = getToolDefs();
  const grid = $('#tool-grid');
  if (!grid) return;

  // Filter by category
  let filtered = _currentToolCat === 'all' ? tools : tools.filter(t => t.cat === _currentToolCat);
  // Filter by search
  if (_toolSearchQuery) {
    const q = _toolSearchQuery.toLowerCase();
    filtered = filtered.filter(t => t.name.toLowerCase().includes(q) || t.desc.toLowerCase().includes(q));
  }

  if (filtered.length === 0) {
    grid.innerHTML = '<div style="padding:24px;color:var(--c-text-3);text-align:center;">暂无相关工具</div>';
    return;
  }

  grid.innerHTML = filtered.map(t => {
    const parts = t.name.split(' ');
    const icon = parts[0] || '🤖';
    const label = parts.slice(1).join(' ') || t.name;
    return `<div class="tool-card" data-tool-id="${t.id}"><div class="tc-avatar">${icon}</div>
    <div class="tc-info"><div class="tc-name">${esc(label)}</div><div class="tc-desc">${esc(t.desc)}</div>
    <div class="tc-stats">♡ ${t.stat}</div></div></div>`;
  }).join('');
}

function initDiscoverNav() {
  // Event delegation for tool card clicks → open dedicated tool page
  const grid = $('#tool-grid');
  if (grid) {
    grid.addEventListener('click', (e) => {
      const card = e.target.closest('.tool-card');
      if (!card) return;
      const tid = card.dataset.toolId;
      if (tid) openTool(tid);
    });
  }

  // Tool search input
  const searchInput = $('.discover-search input');
  if (searchInput) {
    searchInput.addEventListener('input', () => {
      _toolSearchQuery = searchInput.value.trim();
      renderToolGrid();
    });
  }
}

// ═══════════════════════════════════════════
//  Input
// ═══════════════════════════════════════════
function initInput() {
  dom.input.addEventListener('keydown', (e) => { if(e.key==='Enter'&&!e.shiftKey){e.preventDefault();sendMessage();} });
  dom.input.addEventListener('input', autoResize);
  dom.btnSend.addEventListener('click', sendMessage);
}
function autoResize() { dom.input.style.height='auto'; dom.input.style.height=Math.min(dom.input.scrollHeight,150)+'px'; }

// ═══════════════════════════════════════════
//  File Upload (with attachment cards + progress)
// ═══════════════════════════════════════════
function fmtSize(bytes) {
  if (bytes < 1024) return bytes + ' B';
  if (bytes < 1024*1024) return (bytes/1024).toFixed(1) + ' KB';
  return (bytes/(1024*1024)).toFixed(1) + ' MB';
}

function fileIcon(name) {
  const ext = name.split('.').pop().toLowerCase();
  const icons = {pdf:'📕',docx:'📘',doc:'📘',pptx:'📙',ppt:'📙',xlsx:'📊',xls:'📊',py:'🐍',js:'📜',ts:'📜',json:'📋',csv:'📊',html:'🌐',css:'🎨',md:'📝',txt:'📄',xml:'📰',yaml:'⚙',yml:'⚙',sql:'🗃',java:'☕',c:'⚡',cpp:'⚡',go:'🔵',rs:'🦀',rb:'💎',php:'🐘',sh:'💻',log:'📋'};
  return icons[ext] || '📄';
}

function triggerFileUpload(acceptFilter) {
  const fi = document.createElement('input'); fi.type = 'file'; fi.multiple = true;
  fi.accept = acceptFilter || '.txt,.md,.py,.js,.json,.csv,.html,.css,.xml,.yaml,.yml,.log,.java,.c,.cpp,.ts,.tsx,.sql,.sh,.go,.rs,.rb,.php,.pdf,.doc,.docx,.xls,.xlsx,.ppt,.pptx,.png,.jpg,.jpeg,.gif,.bmp,.webp';
  fi.onchange = (e) => {
    Array.from(e.target.files).forEach(f => {
      if (f.type.startsWith('image/')) addImageAttachment(f);
      else addFileAttachment(f);
    });
  };
  fi.click();
}

function triggerImageUpload() {
  const fi = document.createElement('input'); fi.type = 'file';
  fi.accept = 'image/*';
  fi.onchange = (e) => { const f = e.target.files[0]; if (f) addImageAttachment(f); };
  fi.click();
}

async function uploadFileToServer(file) {
  const formData = new FormData();
  formData.append('file', file);
  try {
    const resp = await fetch('/api/upload', { method: 'POST', body: formData });
    return await resp.json();
  } catch (e) {
    return { text: `[上传失败: ${e.message}]`, type: 'error', meta: { name: file.name, size: file.size } };
  }
}

function addFileAttachment(file) {
  const id = 'att-' + Date.now() + '-' + Math.random().toString(36).slice(2,6);
  const att = { id, name: file.name, size: file.size, type: 'file', content: null, file };
  state.attachments.push(att);
  renderAttachList();

  const card = document.getElementById(id);
  if (card) card.classList.add('processing');
  let progress = 0;
  const bar = card ? card.querySelector('.ac-progress-bar') : null;
  // Animate progress while uploading
  const iv = setInterval(() => {
    progress = Math.min(progress + Math.random() * 8 + 3, 90);
    if (bar) bar.style.width = progress + '%';
  }, 200);

  uploadFileToServer(file).then(result => {
    clearInterval(iv);
    if (bar) bar.style.width = '100%';
    att.content = result.text || '[空文件]';
    att.parsedType = result.type;
    att.meta = result.meta;
    setTimeout(() => {
      if (card) { card.classList.remove('processing'); card.classList.add('done'); }
      const label = result.meta?.pages ? `${result.meta.pages}页` :
                    result.meta?.paragraphs ? `${result.meta.paragraphs}段` :
                    result.meta?.slides ? `${result.meta.slides}张` : '';
      showToast(`<span class="toast-icon">✅</span> 1${t('fileProcessed')}${label ? ' ('+label+')' : ''} <span class="toast-link" onclick="navigateTo('chat')">${t('backToChat')}</span>`);
    }, 300);
  });
}

function addImageAttachment(file) {
  const id = 'att-' + Date.now() + '-' + Math.random().toString(36).slice(2,6);
  const att = { id, name: file.name, size: file.size, type: 'image', content: null, dataUrl: null, file };
  state.attachments.push(att);

  // Read as data URL for local preview
  const previewReader = new FileReader();
  previewReader.onload = (ev) => { att.dataUrl = ev.target.result; renderAttachList(); };
  previewReader.readAsDataURL(file);
  renderAttachList();

  // Upload to server for proper parsing
  const card = document.getElementById(id);
  if (card) card.classList.add('processing');
  let progress = 0;
  const bar = card ? card.querySelector('.ac-progress-bar') : null;
  const iv = setInterval(() => {
    progress = Math.min(progress + Math.random() * 10 + 5, 90);
    if (bar) bar.style.width = progress + '%';
  }, 150);

  uploadFileToServer(file).then(result => {
    clearInterval(iv);
    if (bar) bar.style.width = '100%';
    att.content = result.text || `[图片: ${file.name}]`;
    att.meta = result.meta;
    setTimeout(() => {
      const c = document.getElementById(id);
      if (c) { c.classList.remove('processing'); c.classList.add('done'); }
      showToast(`<span class="toast-icon">✅</span> ${t('imgProcessed')}`);
    }, 300);
  });
}

function removeAttachment(id) {
  state.attachments = state.attachments.filter(a => a.id !== id);
  renderAttachList();
}

function renderAttachList() {
  const el = $('#attach-list');
  if (!el) return;
  el.innerHTML = state.attachments.map(a => {
    const isImg = a.type === 'image' && a.dataUrl;
    const iconHtml = isImg
      ? `<div class="ac-icon img-preview"><img src="${a.dataUrl}" alt=""></div>`
      : `<div class="ac-icon">${fileIcon(a.name)}</div>`;
    return `<div class="attach-card" id="${a.id}">
      ${iconHtml}
      <div class="ac-info"><div class="ac-name">${esc(a.name)}</div><div class="ac-size">${fmtSize(a.size)}</div></div>
      <div class="ac-close" onclick="removeAttachment('${a.id}')">✕</div>
      <div class="ac-progress"><div class="ac-progress-bar"></div></div>
    </div>`;
  }).join('');
}

function initUpload() {
  dom.btnAttach.addEventListener('click', triggerFileUpload);
  const imgBtn = $('#btn-img-upload');
  if (imgBtn) imgBtn.addEventListener('click', triggerImageUpload);
  const micBtn = $('#btn-mic');
  if (micBtn) micBtn.addEventListener('click', () => navigateTo('record'));
  const fsBtn = $('#btn-fullscreen');
  if (fsBtn) fsBtn.addEventListener('click', () => {
    if (document.fullscreenElement) document.exitFullscreen();
    else document.documentElement.requestFullscreen().catch(()=>{});
  });
}

// ═══════════════════════════════════════════
//  Settings
// ═══════════════════════════════════════════
function initSettings() {
  $('#btn-open-settings').addEventListener('click', () => navigateTo('settings'));
  $('#btn-settings-top').addEventListener('click', () => navigateTo('settings'));
  dom.toggleDark.addEventListener('click', toggleTheme);
  $('#btn-clear-all').addEventListener('click', async () => {
    if (!confirm(t('confirmClear'))) return;
    for (const c of state.conversations) await apiPost('/api/conversations/delete',{id:c.id});
    state.currentConvId=null; showWelcome(); loadConversations(); navigateTo('chat');
  });
}

async function loadSysInfo() {
  const info = await apiGet('/api/system-info');
  if (!info) return;
  const p=[];
  if(info.os) p.push(info.os); if(info.cpu) p.push('CPU: '+info.cpu);
  if(info.ram) p.push('RAM: '+info.ram); if(info.gpu) p.push('GPU: '+info.gpu);
  dom.sysInfo.textContent = p.join(' · ') || '—';
}

// ═══════════════════════════════════════════
//  Shared SSE Token Reader (used by sub-pages)
// ═══════════════════════════════════════════
async function readSSETokens(url, body, onProgress) {
  const resp = await fetch(url, {
    method: 'POST', headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });
  if (!resp.ok) throw new Error(`HTTP ${resp.status}: ${resp.statusText}`);
  const reader = resp.body.getReader();
  const decoder = new TextDecoder();
  let buf = '', result = '', curEvt = '';
  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    buf += decoder.decode(value, { stream: true });
    const lines = buf.split('\n'); buf = lines.pop();
    for (const line of lines) {
      if (line.startsWith('event: ')) { curEvt = line.slice(7).trim(); }
      else if (line.startsWith('data: ')) {
        if (curEvt === 'token') {
          try { result += JSON.parse(line.slice(6)); } catch (e) {}
          if (onProgress) onProgress(result);
        }
        curEvt = '';
      }
    }
  }
  return result;
}

// ═══════════════════════════════════════════
//  Markdown
// ═══════════════════════════════════════════
function fmtMd(text) {
  if(!text) return '';
  let h=esc(text);
  h=h.replace(/```(\w*)\n([\s\S]*?)```/g,(_,l,c)=>`<pre><code>${c}</code></pre>`);
  h=h.replace(/`([^`]+)`/g,'<code>$1</code>');
  h=h.replace(/\*\*(.+?)\*\*/g,'<strong>$1</strong>');
  h=h.replace(/\*(.+?)\*/g,'<em>$1</em>');
  h=h.replace(/^### (.+)$/gm,'<h4>$1</h4>');
  h=h.replace(/^## (.+)$/gm,'<h3>$1</h3>');
  h=h.replace(/^# (.+)$/gm,'<h2>$1</h2>');
  h=h.replace(/\n\n/g,'</p><p>'); h=h.replace(/\n/g,'<br>');
  h='<p>'+h+'</p>';
  h=h.replace(/<p>\s*<\/p>/g,'');
  h=h.replace(/<p>(<(?:h[2-4]|pre)>)/g,'$1');
  h=h.replace(/(<\/(?:h[2-4]|pre)>)<\/p>/g,'$1');
  return h;
}
function esc(s) { const d=document.createElement('span'); d.textContent=s; return d.innerHTML; }

// ═══════════════════════════════════════════
//  SUB-PAGE: Recording
// ═══════════════════════════════════════════
let recState = { recording: false, mediaRec: null, chunks: [], timer: null, seconds: 0, stream: null };

function initRecordPage() {
  const toggle = $('#rec-toggle'), cancel = $('#rec-cancel'), done = $('#rec-done');
  if (!toggle) return;

  toggle.addEventListener('click', async () => {
    if (!recState.recording) {
      try {
        recState.stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        recState.mediaRec = new MediaRecorder(recState.stream);
        recState.chunks = [];
        recState.mediaRec.ondataavailable = (e) => { if (e.data.size > 0) recState.chunks.push(e.data); };
        recState.mediaRec.start();
        recState.recording = true;
        recState.seconds = 0;
        toggle.textContent = t('recPause') || '暂停';
        toggle.classList.add('recording');
        cancel.disabled = false; done.disabled = false;
        $('#record-visual').classList.add('recording');
        $('#record-status').textContent = t('recRecording') || '录音中…';
        recState.timer = setInterval(() => {
          recState.seconds++;
          const m = String(Math.floor(recState.seconds / 60)).padStart(2, '0');
          const s = String(recState.seconds % 60).padStart(2, '0');
          $('#record-timer').textContent = `${m}:${s}`;
        }, 1000);
      } catch (e) {
        showToast(`<span class="toast-icon">⚠️</span> ${e.message}`);
      }
    } else {
      // Pause/resume
      if (recState.mediaRec.state === 'recording') {
        recState.mediaRec.pause();
        clearInterval(recState.timer);
        toggle.textContent = t('recResume') || '继续';
        $('#record-status').textContent = t('recPaused') || '已暂停';
      } else {
        recState.mediaRec.resume();
        recState.timer = setInterval(() => {
          recState.seconds++;
          const m = String(Math.floor(recState.seconds / 60)).padStart(2, '0');
          const s = String(recState.seconds % 60).padStart(2, '0');
          $('#record-timer').textContent = `${m}:${s}`;
        }, 1000);
        toggle.textContent = t('recPause') || '暂停';
        $('#record-status').textContent = t('recRecording') || '录音中…';
      }
    }
  });

  cancel.addEventListener('click', () => {
    stopRecording(false);
  });

  done.addEventListener('click', () => {
    stopRecording(true);
  });

  const copyBtn = $('#rec-copy');
  if (copyBtn) copyBtn.addEventListener('click', () => {
    const txt = $('#record-transcript').textContent;
    navigator.clipboard.writeText(txt);
    showToast('<span class="toast-icon">✅</span> 已复制');
  });

  const analyzeBtn = $('#rec-analyze');
  if (analyzeBtn) analyzeBtn.addEventListener('click', () => {
    const txt = $('#record-transcript').textContent;
    if (!txt) return;
    navigateTo('chat');
    dom.input.value = `请分析以下录音转写内容：\n\n${txt}`;
    autoResize();
    sendMessage();
  });
}

function stopRecording(save) {
  clearInterval(recState.timer);
  if (recState.mediaRec && recState.mediaRec.state !== 'inactive') {
    recState.mediaRec.stop();
  }
  if (recState.stream) {
    recState.stream.getTracks().forEach(t => t.stop());
  }
  recState.recording = false;
  $('#rec-toggle').textContent = t('recStart') || '开始录音';
  $('#rec-toggle').classList.remove('recording');
  $('#rec-cancel').disabled = true;
  $('#rec-done').disabled = true;
  $('#record-visual').classList.remove('recording');

  if (save && recState.chunks.length > 0) {
    $('#record-status').textContent = t('recProcessing') || '正在转写…';
    // Simulate transcription (real implementation would use speech-to-text API)
    setTimeout(() => {
      const duration = recState.seconds;
      const m = Math.floor(duration / 60), s = duration % 60;
      const transcript = `[录音时长: ${m}分${s}秒]\n\n录音内容已捕获。由于当前环境未配置语音识别服务，请将录音文件发送至支持语音转文字的服务进行转写。\n\n您也可以点击"AI 分析"按钮，将录音信息发送给AI进行进一步处理。`;
      $('#record-transcript').textContent = transcript;
      $('#record-result').classList.remove('hidden');
      $('#record-status').textContent = t('recFinished') || '录音完成';
    }, 1500);
  } else {
    $('#record-timer').textContent = '00:00';
    $('#record-status').textContent = t('recReady') || '准备录音';
  }
}

// ═══════════════════════════════════════════
//  SUB-PAGE: PPT
// ═══════════════════════════════════════════
let pptPageCount = 10;
let pptTemplate = 'business';

function initPptPage() {
  // Template selection
  $$('.ppt-tpl').forEach(tpl => {
    tpl.addEventListener('click', () => {
      $$('.ppt-tpl').forEach(t => t.classList.remove('active'));
      tpl.classList.add('active');
      pptTemplate = tpl.dataset.tpl;
    });
  });

  // Page count
  const minus = $('#ppt-minus'), plus = $('#ppt-plus'), countEl = $('#ppt-page-count');
  if (minus) minus.addEventListener('click', () => {
    pptPageCount = Math.max(3, pptPageCount - 1);
    countEl.textContent = pptPageCount;
  });
  if (plus) plus.addEventListener('click', () => {
    pptPageCount = Math.min(30, pptPageCount + 1);
    countEl.textContent = pptPageCount;
  });

  // Generate
  const genBtn = $('#ppt-generate');
  if (genBtn) genBtn.addEventListener('click', generatePpt);

  // Copy outline
  const copyBtn = $('#ppt-copy-outline');
  if (copyBtn) copyBtn.addEventListener('click', () => {
    navigator.clipboard.writeText($('#ppt-outline').textContent);
    showToast('<span class="toast-icon">✅</span> 大纲已复制');
  });

  // Refine
  const refineBtn = $('#ppt-refine');
  if (refineBtn) refineBtn.addEventListener('click', () => {
    const outline = $('#ppt-outline').textContent;
    navigateTo('chat');
    dom.input.value = `请对以下PPT大纲进行优化细化，添加更多细节和要点：\n\n${outline}`;
    autoResize();
    sendMessage();
  });
}

async function generatePpt() {
  const topic = $('#ppt-topic').value.trim();
  if (!topic) { showToast('<span class="toast-icon">⚠️</span> 请输入PPT主题'); return; }

  const progress = $('#ppt-progress'), preview = $('#ppt-preview');
  const fill = $('#ppt-progress-fill'), pText = $('#ppt-progress-text');
  progress.classList.remove('hidden');
  preview.classList.add('hidden');
  fill.style.width = '0%';

  let p = 0;
  const iv = setInterval(() => { p = Math.min(p + Math.random() * 5 + 2, 90); fill.style.width = p + '%'; }, 300);

  const prompt = `请为以下主题生成一个${pptPageCount}页PPT的详细大纲，风格为${pptTemplate}：\n\n主题：${topic}\n\n要求：\n1. 每页包含标题和3-5个要点\n2. 内容专业、结构清晰\n3. 包含开场、正文、总结\n4. 适合演示汇报使用`;

  try {
    const result = await readSSETokens('/api/chat', { text: prompt, mode: 'write', model: state.currentModel }, (partial) => {
      pText.textContent = `正在生成… ${partial.length} 字`;
    });
    clearInterval(iv);
    fill.style.width = '100%';
    setTimeout(() => {
      progress.classList.add('hidden');
      preview.classList.remove('hidden');
      $('#ppt-outline').textContent = result;
    }, 500);
  } catch (e) {
    clearInterval(iv);
    showToast(`<span class="toast-icon">⚠️</span> ${e.message}`);
    progress.classList.add('hidden');
  }
}

// ═══════════════════════════════════════════
//  SUB-PAGE: Audio/Video
// ═══════════════════════════════════════════
let avData = { summary: '', transcript: '', timeline: '' };

function initAvPage() {
  const uploadBtn = $('#av-upload-btn');
  const zone = $('#av-upload-zone');
  if (uploadBtn) uploadBtn.addEventListener('click', (e) => { e.stopPropagation(); triggerAvUpload(); });
  if (zone) zone.addEventListener('click', triggerAvUpload);

  // Tabs
  $$('.av-tab').forEach(tab => {
    tab.addEventListener('click', () => {
      $$('.av-tab').forEach(t => t.classList.remove('active'));
      tab.classList.add('active');
      const key = tab.dataset.avt;
      $('#av-tab-content').textContent = avData[key] || '';
    });
  });

  const copyBtn = $('#av-copy');
  if (copyBtn) copyBtn.addEventListener('click', () => {
    const activeTab = document.querySelector('.av-tab.active');
    const key = activeTab ? activeTab.dataset.avt : 'summary';
    navigator.clipboard.writeText(avData[key] || '');
    showToast('<span class="toast-icon">✅</span> 已复制');
  });

  const askBtn = $('#av-ask');
  if (askBtn) askBtn.addEventListener('click', () => {
    navigateTo('chat');
    dom.input.value = `请对以下音视频内容进行深度分析：\n\n${avData.summary}`;
    autoResize();
    dom.input.focus();
  });

  const reupBtn = $('#av-reupload');
  if (reupBtn) reupBtn.addEventListener('click', () => {
    $('#av-result').classList.add('hidden');
    $('#av-processing').classList.add('hidden');
    $('#av-upload-zone').classList.remove('hidden');
  });
}

function triggerAvUpload() {
  const fi = document.createElement('input'); fi.type = 'file';
  fi.accept = 'audio/*,video/*,.mp3,.mp4,.wav,.m4a,.webm,.ogg,.avi,.mov,.flac';
  fi.onchange = (e) => { const f = e.target.files[0]; if (f) processAvFile(f); };
  fi.click();
}

async function processAvFile(file) {
  const zone = $('#av-upload-zone'), proc = $('#av-processing'), result = $('#av-result');
  zone.classList.add('hidden');
  proc.classList.remove('hidden');
  result.classList.add('hidden');

  $('#av-file-info').innerHTML = `<span>🎬</span> <strong>${esc(file.name)}</strong> <span style="color:var(--c-text-3)">(${fmtSize(file.size)})</span>`;
  const fill = $('#av-progress-fill'), pText = $('#av-progress-text');

  // Reset all steps
  const steps = ['av-step-1', 'av-step-2', 'av-step-3', 'av-step-4'];
  steps.forEach(s => { const el = $(`#${s}`); if (el) { el.classList.remove('active', 'done'); } });
  let stepIdx = 0;

  const advanceStep = () => {
    if (stepIdx > 0) $(`#${steps[stepIdx - 1]}`).classList.replace('active', 'done');
    if (stepIdx < steps.length) $(`#${steps[stepIdx]}`).classList.add('active');
    stepIdx++;
  };

  advanceStep();
  fill.style.width = '25%'; pText.textContent = '25%';

  await new Promise(r => setTimeout(r, 800));
  advanceStep(); fill.style.width = '50%'; pText.textContent = '50%';

  await new Promise(r => setTimeout(r, 800));
  advanceStep(); fill.style.width = '75%'; pText.textContent = '75%';

  const prompt = `用户上传了一个${file.type.startsWith('video') ? '视频' : '音频'}文件，文件名为"${file.name}"，大小${fmtSize(file.size)}。请生成：\n1. 一段简要的内容摘要（假设这是一段会议/讲座内容）\n2. 可能的完整文稿概要\n3. 关键时间节点时间线\n\n请分别用【摘要】【文稿】【时间线】标签分隔。`;

  try {
    const fullText = await readSSETokens('/api/chat', { text: prompt, mode: 'analyze', model: state.currentModel });

    advanceStep(); fill.style.width = '100%'; pText.textContent = '100%';

    avData.summary = fullText;
    avData.transcript = fullText;
    avData.timeline = fullText;
    const sumMatch = fullText.match(/【摘要】([\s\S]*?)(?=【|$)/);
    const transMatch = fullText.match(/【文稿】([\s\S]*?)(?=【|$)/);
    const timeMatch = fullText.match(/【时间线】([\s\S]*?)(?=【|$)/);
    if (sumMatch) avData.summary = sumMatch[1].trim();
    if (transMatch) avData.transcript = transMatch[1].trim();
    if (timeMatch) avData.timeline = timeMatch[1].trim();

    setTimeout(() => {
      proc.classList.add('hidden');
      result.classList.remove('hidden');
      $('#av-tab-content').textContent = avData.summary;
    }, 500);
  } catch (e) {
    showToast(`<span class="toast-icon">⚠️</span> ${e.message}`);
  }
}

// ═══════════════════════════════════════════
//  SUB-PAGE: Document
// ═══════════════════════════════════════════
let docContent = '';
let docName = '';

function initDocPage() {
  const uploadBtn = $('#doc-upload-btn');
  const zone = $('#doc-upload-zone');
  if (uploadBtn) uploadBtn.addEventListener('click', (e) => { e.stopPropagation(); triggerDocUpload(); });
  if (zone) zone.addEventListener('click', triggerDocUpload);

  const sendBtn = $('#doc-qa-send');
  const qaInput = $('#doc-qa-input');
  if (sendBtn) sendBtn.addEventListener('click', docQaSend);
  if (qaInput) qaInput.addEventListener('keydown', (e) => { if (e.key === 'Enter') docQaSend(); });

  const reupBtn = $('#doc-reupload');
  if (reupBtn) reupBtn.addEventListener('click', () => {
    $('#doc-result').classList.add('hidden');
    $('#doc-processing').classList.add('hidden');
    $('#doc-upload-zone').classList.remove('hidden');
    docContent = ''; docName = '';
  });
}

function triggerDocUpload() {
  const fi = document.createElement('input'); fi.type = 'file';
  fi.accept = '.pdf,.docx,.doc,.txt,.md,.csv,.pptx,.xlsx,.html';
  fi.onchange = (e) => { const f = e.target.files[0]; if (f) processDocFile(f); };
  fi.click();
}

async function processDocFile(file) {
  const zone = $('#doc-upload-zone'), proc = $('#doc-processing'), result = $('#doc-result');
  zone.classList.add('hidden');
  proc.classList.remove('hidden');
  result.classList.add('hidden');
  docName = file.name;

  $('#doc-file-card').innerHTML = `<span>${fileIcon(file.name)}</span> <strong>${esc(file.name)}</strong> <span style="color:var(--c-text-3)">(${fmtSize(file.size)})</span>`;
  const fill = $('#doc-progress-fill'), pText = $('#doc-progress-text');
  fill.style.width = '30%'; pText.textContent = '上传中…';

  const uploadResult = await uploadFileToServer(file);
  fill.style.width = '70%'; pText.textContent = '解析中…';

  await new Promise(r => setTimeout(r, 500));
  fill.style.width = '100%'; pText.textContent = '完成';

  docContent = uploadResult.text || '[无法解析]';
  const meta = uploadResult.meta || {};

  setTimeout(() => {
    proc.classList.add('hidden');
    result.classList.remove('hidden');

    // Meta tags
    const tags = [];
    tags.push(`<span class="dm-tag">${esc(file.name)}</span>`);
    if (meta.pages) tags.push(`<span class="dm-tag">${meta.pages} 页</span>`);
    if (meta.paragraphs) tags.push(`<span class="dm-tag">${meta.paragraphs} 段</span>`);
    if (meta.slides) tags.push(`<span class="dm-tag">${meta.slides} 张幻灯片</span>`);
    tags.push(`<span class="dm-tag">${fmtSize(meta.size || file.size)}</span>`);
    tags.push(`<span class="dm-tag">${uploadResult.type || 'text'}</span>`);
    $('#doc-meta').innerHTML = tags.join('');

    // Content preview (first 2000 chars)
    const preview = docContent.length > 2000 ? docContent.substring(0, 2000) + '\n…' : docContent;
    $('#doc-content-preview').textContent = preview;

    // Clear QA
    $('#doc-qa-msgs').innerHTML = '';

    showToast(`<span class="toast-icon">✅</span> 文档解析完成 (${meta.pages ? meta.pages + '页' : fmtSize(file.size)})`);
  }, 500);
}

async function docQaSend() {
  const input = $('#doc-qa-input');
  const question = input.value.trim();
  if (!question || !docContent) return;
  input.value = '';

  const msgsEl = $('#doc-qa-msgs');
  msgsEl.insertAdjacentHTML('beforeend', msgHtml('user', question));

  const prompt = `基于以下文档内容回答问题。\n\n文档名：${docName}\n文档内容：\n${docContent.substring(0, 8000)}\n\n问题：${question}`;

  msgsEl.insertAdjacentHTML('beforeend',
    `<div class="msg assistant" id="doc-stream-msg"><div class="msg-avatar"><img src="Qwen3.png" alt="Q"></div><div class="msg-body"><div class="msg-role">Qwen-Agent</div><div class="msg-content"><span class="cursor-blink"></span></div></div></div>`);
  msgsEl.scrollTop = msgsEl.scrollHeight;

  try {
    const result = await readSSETokens('/api/chat', { text: prompt, mode: 'analyze', model: state.currentModel }, (partial) => {
      const el = $('#doc-stream-msg .msg-content');
      if (el) el.innerHTML = fmtMd(partial) + '<span class="cursor-blink"></span>';
      msgsEl.scrollTop = msgsEl.scrollHeight;
    });
    const el = $('#doc-stream-msg');
    if (el) { el.removeAttribute('id'); const c = el.querySelector('.msg-content'); if (c) c.innerHTML = fmtMd(result); }
  } catch (e) {
    showToast(`<span class="toast-icon">⚠️</span> ${e.message}`);
  }
}

// ═══════════════════════════════════════════
//  Search + Dropdowns + Shortcuts
// ═══════════════════════════════════════════
function initSearch() { if(dom.convSearch) dom.convSearch.addEventListener('input',()=>renderConvList(state.conversations)); }

function initDropdowns() {
  document.addEventListener('click',(e)=>{
    if(!dom.modelSelect.contains(e.target)) dom.modelDropdown.classList.remove('show');
  });
  dom.modelSelect.addEventListener('click',(e)=>{ e.stopPropagation(); dom.modelDropdown.classList.toggle('show'); });
}

function initKeys() {
  document.addEventListener('keydown',(e)=>{
    if(e.ctrlKey&&e.key==='n'){e.preventDefault();newChat();}
    if(e.ctrlKey&&e.key==='b'){e.preventDefault();toggleSidebar();}
    if(e.ctrlKey&&e.key==='d'){e.preventDefault();toggleTheme();}
    if(e.key==='Escape'){if(state.streaming){cancelStream();}else{$$('.show').forEach(d=>d.classList.remove('show'));}}
    if(e.ctrlKey&&e.key==='l'){e.preventDefault();dom.input.focus();}
  });
}

// ═══════════════════════════════════════════
//  Boot
// ═══════════════════════════════════════════
document.addEventListener('DOMContentLoaded', async () => {
  dom = {
    splash:$('#splash'), app:$('#app'), welcome:$('#welcome'), messages:$('#messages'),
    chatArea:$('#chat-area'), input:$('#input'), btnSend:$('#btn-send'),
    btnAttach:$('#btn-attach'), convList:$('#conv-list'), convSearch:$('#conv-search'),
    modelName:$('#model-name'), modelSelect:$('#model-select'), modelDropdown:$('#model-dropdown'),
    toggleDark:$('#toggle-dark'), sysInfo:$('#sys-info'), convCount:$('#conv-count'),
  };

  // Restore language
  state.lang = localStorage.getItem('qa-lang') || 'zh';

  const inits = [
    ['Theme', initTheme], ['Splash', initSplash], ['Input', initInput],
    ['Chips', initChips], ['WebSearch', initWebSearch], ['Settings', initSettings],
    ['Search', initSearch], ['Dropdowns', initDropdowns], ['Keys', initKeys],
    ['Upload', initUpload], ['GlobalNav', initGlobalNav], ['DiscoverNav', initDiscoverNav],
    ['MoreChips', initMoreChips], ['SubpageModels', initSubpageModels],
    ['RecordPage', initRecordPage], ['PptPage', initPptPage],
    ['AvPage', initAvPage], ['DocPage', initDocPage], ['ToolPage', initToolPage],
  ];
  for (const [name, fn] of inits) {
    try { fn(); } catch (e) { console.error(`[INIT] ${name} failed:`, e); }
  }

  // Sidebar nav tabs
  $$('.sidebar-nav button').forEach(b => b.addEventListener('click', () => navigateTo(b.dataset.page)));

  // Top bar buttons
  try {
    $('#btn-new-chat').addEventListener('click', newChat);
    $('#btn-sidebar').addEventListener('click', toggleSidebar);
    $('#btn-theme').addEventListener('click', toggleTheme);
  } catch (e) { console.error('[INIT] Topbar buttons:', e); }

  // Language selectors (both topbar and settings)
  $$('.lang-select button').forEach(b => b.addEventListener('click', () => setLang(b.dataset.lang)));

  // Apply i18n
  applyI18n();
  console.log('[BOOT] All init complete. Tool cards:', $$('.tool-card').length, 'Cat tabs:', $$('.cat-tab').length);

  // Load data
  await loadModels();
  await loadConversations();
  await loadSysInfo();
  const curId = await apiGet('/api/current-conv-id');
  if (curId) { state.currentConvId = curId; await switchConv(curId); }
});
