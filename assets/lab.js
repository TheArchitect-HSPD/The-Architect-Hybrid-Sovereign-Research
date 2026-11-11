/* HSPD Interactive Lab. Runs entirely in browser; no network calls. */
(() => {
  'use strict';
  const $ = id => document.getElementById(id);
  const escape = value => String(value == null ? '' : value).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const text = (id, value) => { const n = $(id); if (n) n.textContent = String(value); };
  const MODES = {majority:'Raw majority',confidence:'Confidence-weighted',arbiter:'The Arbiter policy'};
  const names = {'agent-01':'Aegaryn','agent-02':'Veylith','agent-03':'Thariven','agent-04':'Aurivex','agent-05':'Narethyl','agent-21':'The Arbiter'};
  let previous = null, truthVisible = false, draft = [];
  if (!window.HSPD || !window.HSPD_DATA) { text('lab-message','Browser engine failed to load. Check dataset.js and engine_browser.js.'); return; }
  const scenarioInput = $('lab-scenario');
  const fixtures = window.HSPD.scenarios;
  function availableScenarios() {
    scenarioInput.innerHTML = Object.entries(fixtures).map(([key,s]) => '<option value="'+escape(key)+'">'+escape(s.title)+'</option>').join('');
  }
  availableScenarios();
  function activate(tab) {
    document.querySelectorAll('[data-tab]').forEach(b => {
      const active = b.dataset.tab === tab;
      b.setAttribute('aria-selected', String(active));
      b.tabIndex = active ? 0 : -1;
    });
    for (const key of ['test','compose','trace','import']) {
      const panel = $('panel-'+key);
      panel.hidden = key !== tab;
    }
  }
  document.querySelectorAll('[data-tab]').forEach(b => b.addEventListener('click', () => activate(b.dataset.tab)));
  function numberSeed() {
    const s = Number($('lab-seed').value);
    if (!Number.isSafeInteger(s) || s < 0 || s > 10000000) throw Error('Seed must be a whole number between 0 and 10,000,000.');
    return s;
  }
  function run() {
    try {
      const scenario = scenarioInput.value, seed = numberSeed();
      if (!Object.prototype.hasOwnProperty.call(fixtures, scenario)) throw Error('Choose a scenario.');
      previous = window.HSPD.compare(scenario, seed);
      if (!Array.isArray(previous) || previous.length !== 3) throw Error('Engine returned incomplete comparisons.');
      truthVisible = false; text('lab-truth','Evaluator label hidden.');
      $('lab-export').disabled = false;
      const sample = previous[0], s = fixtures[scenario];
      $('lab-scenario-info').innerHTML = '<strong>'+escape(s.title)+'</strong><p>Claim: '+escape(s.claim)+'</p><p>Adversarial premise: '+escape(s.attack_description)+'</p>';
      $('lab-result-cards').innerHTML = previous.map(r => '<article class="lab-result"><h3>'+escape(MODES[r.mode])+'</h3><span class="lab-decision">'+escape(r.recommendation)+'</span><p>'+escape(r.explanation)+'</p><p class="lab-small">Illustrative evidence support score: '+escape(r.confidence_score === null ? 'N/A' : String(r.confidence_score))+'</p></article>').join('');
      $('lab-evidence').innerHTML = sample.evidence.map(e => '<tr><td>'+escape(e.id)+'</td><td>'+escape(e.observed_root)+'</td><td>'+ (e.supports_claim?'Yes':'No')+'</td><td>'+escape(e.confidence)+'</td><td>'+(e.intervention_generated?'Yes':'No')+'</td></tr>').join('');
      const arb = previous.find(r => r.mode === 'arbiter');
      $('lab-alerts').innerHTML = arb.alerts.map(s => '<li>'+escape(s)+'</li>').join('');
      text('lab-message','PASS: Three deterministic policy assessments completed. No live model calls.');
      renderTrace();
    } catch (err) {
      text('lab-message','ERROR: '+String(err.message || 'Invalid input'));
      previous = null; $('lab-export').disabled = true;
    }
  }
  function renderTrace() {
    const trace = previous?.find(r => r.mode === 'arbiter')?.trace || [];
    const filter = $('lab-filter').value.trim().toLowerCase();
    const filtered = trace.filter(t => (t.agent+' '+t.role+' '+t.message+' '+t.phase).toLowerCase().includes(filter));
    text('trace-count','Showing '+filtered.length+' of '+trace.length+' labelled policy and context steps. None is a separate model invocation.');
    $('lab-trace').innerHTML = filtered.map(t => '<article><strong>'+escape(String(t.seq).padStart(2,'0'))+' · '+escape(t.agent)+'</strong><br><small>'+escape(t.role)+' | '+escape(t.phase)+'</small><p>'+escape(t.message)+'</p></article>').join('') || '<p>No matching trace steps.</p>';
  }
  $('lab-run').addEventListener('click', run);
  scenarioInput.addEventListener('change', run);
  $('lab-filter').addEventListener('input', renderTrace);
  $('lab-reveal').addEventListener('click', () => {
    if (!previous) return;
    truthVisible = !truthVisible;
    const truth = previous[0].ground_truth;
    text('lab-truth', !truthVisible ? 'Evaluator label hidden.' : truth === null ? 'Ground truth intentionally unspecified.' : 'Synthetic evaluator label: claim '+(truth?'TRUE':'FALSE')+'. This is an authored test label, not evidence.');
  });
  function saveJson(obj, filename) {
    const blob = new Blob([JSON.stringify(obj, null, 2)+'\n'], {type:'application/json'});
    const url = URL.createObjectURL(blob), a = document.createElement('a');
    a.href=url; a.download=filename; document.body.appendChild(a);a.click();a.remove();
    setTimeout(()=>URL.revokeObjectURL(url),3000);
  }
  $('problem-export').addEventListener('click', () => {
    const problem = $('problem-text').value.trim();
    if (!problem) { text('problem-feedback','Enter a fictional problem before exporting.'); return; }
    const stamp = new Date().toISOString().replace(/[-:]/g,'').replace(/\\..+$/,'').replace('T','_');
    const id = 'HSPD-WEB-DRAFT-'+stamp;
    saveJson({
      scenario_id:id,
      classification:'SYNTHETIC TEST DATA ONLY',
      description:'UNVERIFIED AUTHOR-SUPPLIED SYNTHETIC RESEARCH DRAFT',
      research_question:problem,
      signals:[{id:'USER-PROBLEM-001',type:'user_supplied_scenario',source:'UNVERIFIED_USER_INPUT',description:problem}],
      research_limitations:{structured_constitutional_evidence:'NOT_PROVIDED',independent_evidence_authentication:'NOT_PROVIDED',structured_safeguards:'NOT_PROVIDED',human_review_mandatory:true,real_world_actions_permitted:false}
    }, 'HSPD_problem_'+stamp+'.json');
    text('problem-feedback','Synthetic draft exported locally. No validation, inference or network transmission occurred.');
  });
  $('problem-clear').addEventListener('click', () => { $('problem-text').value='';text('problem-feedback','Problem editor cleared.'); });
  $('lab-export').addEventListener('click', () => {
    if (!previous) return;
    const r=previous[0];
    saveJson({classification:'SYNTHETIC POLICY DEMONSTRATION',engine:'HSPD browser v0.1',independent_llm_calls:0,generated_at:new Date().toISOString(),scenario:r.scenario_id,seed:r.seed,comparisons:previous}, 'HSPD_browser_'+r.scenario_id+'.json');
  });
  $('lab-batch').addEventListener('click', () => {
    try {
      const rows=window.HSPD.batch(30);
      const titles='<tr><th>Scenario</th><th>Policy</th><th>Review</th><th>Hold</th><th>Matching known toy labels</th></tr>';
      $('lab-batch-results').innerHTML='<h3>30 shuffled-seed checks per scenario and policy</h3><p class="lab-small">Different orderings of the same data are not independent-world replications.</p><div class="lab-scroll"><table><thead>'+titles+'</thead><tbody>'+rows.map(x=>'<tr><td>'+escape(x.scenario_id)+'</td><td>'+escape(MODES[x.mode])+'</td><td>'+escape(x.review)+'</td><td>'+escape(x.hold)+'</td><td>'+escape(x.correct)+' / '+escape(x.known)+'</td></tr>').join('')+'</tbody></table></div>';
    } catch(e) { text('lab-message','Batch test failed: '+String(e.message)); }
  });
  function renderDraft() {
    $('custom-list').innerHTML = draft.map((e,i) => '<tr><td>'+escape(e.id)+'</td><td>'+escape(e.observed_root)+'</td><td>'+(e.supports_claim?'Yes':'No')+'</td><td>'+escape(e.confidence)+'</td><td><button data-remove="'+i+'" type="button" aria-label="Remove '+escape(e.id)+'">Remove</button></td></tr>').join('') || '<tr><td colspan="5">No evidence entered yet.</td></tr>';
  }
  $('custom-list').addEventListener('click', e => {
    const button = e.target.closest('button[data-remove]');
    if (!button) return;
    const index = Number(button.dataset.remove);
    if (Number.isInteger(index) && index >= 0 && index < draft.length) {draft.splice(index,1);renderDraft();}
  });
  $('custom-add').addEventListener('click', () => {
    const id=$('custom-id').value.trim(), root=$('custom-root').value.trim();
    const confidence=Number($('custom-confidence').value);
    if (!/^[A-Za-z0-9][A-Za-z0-9_.:-]{0,69}$/.test(id) || !/^[A-Za-z0-9][A-Za-z0-9_.:-]{0,69}$/.test(root)) {text('custom-feedback-text','Use an ID and claimed root of up to 70 letters, digits, underscores, dots, colons or hyphens.');return;}
    if (draft.some(x=>x.id===id)) {text('custom-feedback-text','Evidence ID already exists.');return;}
    if (!Number.isFinite(confidence)||confidence<0||confidence>1||$('custom-confidence').value==='') {text('custom-feedback-text','Confidence must be between 0 and 1.');return;}
    if(draft.length>=100) {text('custom-feedback-text','Maximum 100 synthetic evidence records.');return;}
    draft.push({id,observed_root:root,confidence,supports_claim:$('custom-support').checked,intervention_generated:$('custom-feedback').checked});
    $('custom-id').value=''; renderDraft();text('custom-feedback-text',draft.length+' synthetic records in draft. No source authentication is implied.');
  });
  $('custom-reset').addEventListener('click',()=>{draft=[];renderDraft();text('custom-feedback-text','Draft cleared.');});
  $('custom-run').addEventListener('click',()=>{
    if(!draft.length){text('custom-feedback-text','Add at least one evidence record first.');return;}
    const claim=$('custom-question').value.trim();
    if(!claim){text('custom-feedback-text','Enter a research question first.');return;}
    const key='local_custom_synthetic';
    fixtures[key]={title:'User-created synthetic evidence test',claim,ground_truth:null,severity:'unspecified',attack_description:'Unverified user-provided source labels. No independent authentication.',domain_context:{},evidence:draft.map(x=>({...x}))};
    availableScenarios();scenarioInput.value=key;activate('test');run();
    text('custom-feedback-text','Custom scenario tested locally. No LLM inference and no external transmission.');
  });
  renderDraft();
  const requiredIds=['agent-01','agent-02','agent-03','agent-04','agent-05','agent-21'];
  function put(parent,tag,value,cls) {
    const el=document.createElement(tag);
    if(cls) el.className=cls;
    el.textContent=String(value==null?'Not supplied':value);
    parent.appendChild(el); return el;
  }
  function showJson(parent,title,data) {
    put(parent,'h4',title);
    const pre=document.createElement('pre');
    const serial=JSON.stringify(data==null?'Not supplied':data,null,2);
    pre.textContent=serial.length>16000?serial.slice(0,16000)+'\n[Display truncated locally]':serial;
    parent.appendChild(pre);
  }
  function renderReport(report) {
    const container=$('lab-import-output'); container.replaceChildren();
    const meta=put(container,'div','', 'lab-report-meta');meta.textContent='';
    put(meta,'h3','Imported federation report');
    for(const [label,key] of [['Scenario','scenario_id'],['Enforced decision','enforced_decision'],['Real-world actions enabled','real_world_actions_enabled'],['Configured roles','agent_count_configured']]){
      put(meta,'p',label+': '+(Object.prototype.hasOwnProperty.call(report,key)?JSON.stringify(report[key]):'Not available'));
    }
    const receipts=new Map();
    if(Array.isArray(report.specialists)) for(const r of report.specialists){if(r&&typeof r==='object'&&typeof r.agent_id==='string') receipts.set(r.agent_id,r);}
    if(report.arbiter&&typeof report.arbiter==='object')receipts.set('agent-21',report.arbiter);
    const complete=requiredIds.filter(id=>{const r=receipts.get(id);return r&&r.mode==='llm'&&['ASSESSED','ABSTAIN'].includes(r.status);});
    put(meta,'p','Valid LLM receipts in required six roles: '+complete.length+'/6',complete.length===6?'lab-success':'lab-error');
    if(report.enforced_decision!=='REQUEST_HUMAN_REVIEW')put(meta,'p','Warning: the imported report does not document an enforced human-review decision.','lab-error');
    for(const id of requiredIds){
      const r=receipts.get(id),details=document.createElement('details');
      details.className='lab-report-card';details.open=id==='agent-21'||!!(r&&r.status==='ERROR');
      const summary=document.createElement('summary');
      summary.textContent=id+' '+(r?.agent_name||names[id]||'')+' | '+(r?.status||'NOT_PRESENT')+' | '+(r?.mode||'UNKNOWN');
      details.appendChild(summary);
      if(!r){put(details,'p','No receipt for this role.','lab-error');container.appendChild(details);continue;}
      put(details,'p','Action: '+(r.proposed_action||'Not supplied')+' | Risk: '+(r.risk??'N/A')+' | Confidence: '+(r.confidence??'N/A'));
      if(r.status==='ERROR'){put(details,'p','Error recorded. Diagnostic text is deliberately not displayed by this public viewer.','lab-error');}
      else{
        put(details,'h4','Assessment reasoning');put(details,'p',r.reasoning||'Not supplied');
        put(details,'h4','Alternative explanation');put(details,'p',r.alternative_explanation||'Not supplied');
        showJson(details,'Evidence IDs',r.evidence_ids);showJson(details,'Doctrine references',r.cited_doctrine_refs);
        showJson(details,'Doctrine review',r.doctrine_compliance);
        showJson(details,'Patch assessments',r.doctrine_patch_assessments);
        if(id==='agent-21')put(details,'p','Human approval required: '+String(r.human_approval_required));
      }
      container.appendChild(details);
    }
    put(container,'p','Local review only. No provider call or independent source authentication.','lab-import-note');
  }
  $('lab-file').addEventListener('change',async event=>{
    const file=event.target.files?.[0];
    if(!file) return;
    if(file.size>15*1024*1024){text('lab-file-msg','Report exceeds 15 MB local viewer limit.');return;}
    try{
      const value=JSON.parse(await file.text());
      if(!value||typeof value!=='object'||Array.isArray(value)||typeof value.scenario_id!=='string'||value.scenario_id.length>200)throw Error('Unsupported federation report structure.');
      if(!Array.isArray(value.specialists)||!value.arbiter||typeof value.arbiter!=='object')throw Error('Expected specialists array and Arbiter object.');
      renderReport(value);text('lab-file-msg','Report opened locally: '+file.name+'. No upload occurred.');
    }catch(error){$('lab-import-output').replaceChildren();text('lab-file-msg','Cannot display report: '+String(error.message));}
  });
  $('lab-clear-file').addEventListener('click',()=>{$('lab-file').value='';$('lab-import-output').replaceChildren();text('lab-file-msg','Imported report cleared from the viewer.');});
  run();
})();
