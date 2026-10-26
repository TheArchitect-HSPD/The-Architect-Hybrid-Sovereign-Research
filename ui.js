(function(){
'use strict';
const $=id=>document.getElementById(id);
const esc=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const titles={majority:'Baseline / majority',confidence:'Confidence-only monitor',arbiter:'The Arbiter / candidate policy'};
const scenarios=HSPD.scenarios;
$('scenario').innerHTML=Object.entries(scenarios).map(([id,s])=>`<option value="${esc(id)}">${esc(s.title)}</option>`).join('');
const query=new URLSearchParams(location.search);if(query.has('scenario')&&scenarios[query.get('scenario')])$('scenario').value=query.get('scenario');
let last=[],reveal=false;
function go(){let id=$('scenario').value,seed=Number($('seed').value);if(!Number.isInteger(seed)||seed<0||seed>10000000){alert('Please enter a whole seed between 0 and 10,000,000.');return;}
last=HSPD.compare(id,seed);reveal=false;$('truth').textContent='Not revealed';$('reveal').textContent='Reveal evaluator truth';
const s=scenarios[id];$('scenario-info').innerHTML=`<strong>${esc(s.title)}</strong><span><b>Claim:</b> ${esc(s.claim)} &nbsp; <b>Adversarial test:</b> ${esc(s.attack_description)}</span>`;
$('results').innerHTML=last.map(r=>`<article class="result-card ${r.mode==='arbiter'?'featured':''}"><div class="rhead">${esc(titles[r.mode])}</div><div class="rbody"><span class="decision ${r.positive_classification?'review':'hold'}">${r.positive_classification?'REQUEST HUMAN REVIEW':'HOLD / UNCERTAIN'}</span><p>${esc(r.explanation)}</p><div class="scorebar"><b style="width:${Math.round(100*(r.confidence_score||0))}%"></b></div><p class="caption">Synthetic supporting fraction: ${r.confidence_score===null?'N/A':Math.round(100*r.confidence_score)+'%'}; monitor scores are not calibrated probabilities.</p></div></article>`).join('');
const rows=last[0].evidence;
$('evidence-rows').innerHTML=rows.map(e=>`<tr><td>${esc(e.id)}</td><td><code>${esc(e.observed_root)}</code></td><td class="${e.supports_claim?'pos':'neg'}">${e.supports_claim?'SUPPORT':'OPPOSE'}</td><td>${esc((100*e.confidence).toFixed(0))}%</td><td>${e.intervention_generated?'<span class="pos">INTERVENTION-GENERATED</span>':'Direct / inherited report'}</td></tr>`).join('');
const arb=last[2];$('alerts').innerHTML=arb.alerts.map(a=>`<li>${esc(a)}</li>`).join('');
$('roots').innerHTML=Object.entries(arb.observed_root_votes||{}).map(([k,v])=>`<div class="root-item"><span>${esc(k)}</span><strong class="${v?'pos':'neg'}">${v?'SUPPORT':'OPPOSE'}</strong></div>`).join('')||'<p>Insufficient admissible root evidence.</p>';
$('trace-body').innerHTML=arb.trace.map(t=>`<div class="trace-event"><strong>${esc(String(t.seq).padStart(2,'0'))} · ${esc(t.agent)} <small>(${esc(t.phase)})</small></strong><p>${esc(t.message)}</p></div>`).join('');
}
$('compare').onclick=go;
$('scenario').addEventListener('change',go);
$('seed').addEventListener('change',go);
$('reveal').onclick=()=>{reveal=!reveal;
if(!reveal){$('truth').textContent='Not revealed';$('reveal').textContent='Reveal evaluator truth';return;}
let truth=last[0].ground_truth;
let ground=truth===null?'UNKNOWN / NOT SPECIFIED':truth?'CLAIM TRUE':'CLAIM FALSE';
let failures=last.filter(r=>r.correct_classification===false).map(r=>titles[r.mode]);
$('truth').textContent=`${ground}. ${truth===null?'No correct/incorrect classification exists for this case.':failures.length?'Misclassified: '+failures.join(', '):'All three classifiers match this toy label.'}`;
$('reveal').textContent='Hide evaluator truth';
};
$('download').onclick=()=>{
const payload={exported_by:'HSPD Sandbox v0.1 offline browser demonstrator',warning:'Toy policy simulation. Not independent AI-agent testing.',cases:last};
const blob=new Blob([JSON.stringify(payload,null,2)],{type:'application/json'});
const link=document.createElement('a');link.href=URL.createObjectURL(blob);link.download=`HSPD_${last[0].scenario_id}_seed${last[0].seed}.json`;link.click();setTimeout(()=>URL.revokeObjectURL(link.href),1500);
};
function renderAgents(){const q=$('agent-filter').value.toLowerCase().trim();const items=HSPD.agents.filter(a=>(a.name+' '+a.role+' '+a.group).toLowerCase().includes(q));
$('agent-count').textContent=`${items.length} / 21 roles`;
$('agent-grid').innerHTML=items.map(a=>`<article class="agent ${a.id===21?'arbiter':''}"><span class="agent-no">ROLE ${String(a.id).padStart(2,'0')} · ${esc(a.group.toUpperCase())}</span><h3>${esc(a.name)}</h3><p>${esc(a.role)}</p><span class="impl">${a.id===21?'CANDIDATE POLICY':a.id<=8?'SIMULATED CONTEXT STUB':'SIMULATED POLICY STUB'} · ${a.name_status==='author_named'?'AUTHOR-NAMED':'PROPOSED NAME'}</span></article>`).join('');}
$('agent-filter').addEventListener('input',renderAgents);
$('batch-run').onclick=()=>{const rows=HSPD.batch(30);let html='<table><thead><tr><th>Case</th><th>Rule</th><th>Review</th><th>Hold</th><th>Correct* / Known</th></tr></thead><tbody>';
for(const r of rows)html+=`<tr><td>${esc(r.scenario_id)}</td><td>${esc(titles[r.mode])}</td><td>${r.review}</td><td>${r.hold}</td><td>${r.correct} / ${r.known}</td></tr>`;
$('batch-results').innerHTML=html+'</tbody></table><p class="fine">* Counts only toy classification agreement with known synthetic ground truth, not real-world reliability. The thirty seeds reorder evidence; they are not thirty independent experimental worlds.</p>';
};
renderAgents();go();
})();
