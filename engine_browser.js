/* HSPD v0.1 illustrative offline sandbox. No models or network access. */
(function(global){
'use strict';
const D=global.HSPD_DATA;
if(!D) throw new Error('dataset.js must be loaded first');
const MODES=['majority','confidence','arbiter'];
function seededOrder(items,seed){
  // Deterministic within browser; Python uses its own seeded order.
  let x=(Number(seed)>>>0) || 1;
  const rng=()=>{x^=(x<<13); x^=x>>>17; x^=(x<<5);return (x>>>0)/4294967296};
  const e=items.map(v=>Object.assign({},v));
  for(let i=e.length-1;i>0;i--){const j=Math.floor(rng()*(i+1));[e[i],e[j]]=[e[j],e[i]];}
  return e;
}
function base(e){const yes=e.filter(x=>x.supports_claim).length;
return {recommendation:yes>e.length-yes?'REQUEST_HUMAN_REVIEW':'HOLD_UNCERTAINTY',explanation:`Raw majority: ${yes} supporting, ${e.length-yes} opposing. No lineage check.`,alerts:['Baseline counts copied evidence as separate votes.'],confidence_score:e.length?yes/e.length:null,eligible_roots:null};}
function confidence(e){const pos=e.filter(x=>x.supports_claim).reduce((a,b)=>a+b.confidence,0);
const neg=e.filter(x=>!x.supports_claim).reduce((a,b)=>a+b.confidence,0);
const v=(pos+neg)?pos/(pos+neg):0;
return {recommendation:v>=.7?'REQUEST_HUMAN_REVIEW':'HOLD_UNCERTAINTY',explanation:`Confidence-weighted support is ${v.toFixed(2)}; threshold 0.70. Ignores lineage.`,alerts:['Confidence is a synthetic input, not calibrated probability.'],confidence_score:Math.round(v*1000)/1000,eligible_roots:null};}
function arbiter(e){let roots={};let excluded=[];
for(const x of e){if(x.intervention_generated){excluded.push(x.id);continue;}(roots[x.observed_root]||=([])).push(x);}
let votes={},conflicted=[];
for(const root of Object.keys(roots).sort()){
const vals=new Set(roots[root].map(x=>x.supports_claim));
if(vals.size>1)conflicted.push(root);else votes[root]=[...vals][0];
}
const yes=Object.values(votes).filter(Boolean).length,no=Object.values(votes).length-yes,total=yes+no,frac=total?yes/total:0;
const affirmative=yes>=2&&frac>=.67;
let alerts=[];
if(excluded.length)alerts.push(`Excluded intervention-generated evidence: ${excluded.join(', ')}`);
if(conflicted.length)alerts.push(`Conflicting observations under same root: ${conflicted.join(', ')}`);
if(Object.keys(roots).length<e.length-excluded.length)alerts.push('Shared upstream roots detected: raw agreement is not independent confirmation.');
if(no)alerts.push('Independent contradictory source(s) preserved for human review.');
if(!affirmative)alerts.push('Insufficient independent evidence: preserve unknown/other hypothesis.');
alerts.push('Observed source labels may be spoofed; lineage authenticity is not verified.');
return {recommendation:affirmative?'REQUEST_HUMAN_REVIEW':'HOLD_UNCERTAINTY',explanation:`Observed independent roots: ${yes} supporting / ${no} opposing; ${conflicted.length} internally conflicted, ${excluded.length} excluded. Candidate rule: >=2 supporting roots and >=0.67 support share.`,alerts,confidence_score:Math.round(frac*1000)/1000,eligible_roots:votes};}
function run(id='copied_false_consensus',seed=1,mode='arbiter'){
if(!(id in D.scenarios)||!MODES.includes(mode))throw Error('Unknown scenario or mode');
if(!Number.isInteger(Number(seed))||seed<0||seed>10000000)throw Error('Seed must be 0–10,000,000');
const s=D.scenarios[id],e=seededOrder(s.evidence.map(x=>{let y={...x};delete y.actual_root_for_scoring;return y;}),seed),trace=[];
const evaluator_actual_roots=Object.fromEntries(s.evidence.map(x=>[x.id,x.actual_root_for_scoring]));
const record=(agent,role,message,phase='simulated_policy')=>trace.push({seq:trace.length+1,agent,role,message,phase});
for(const a of D.agents.slice(0,8)){record(a.name,a.role,`Context only: ${s.domain_context[a.domain]||'No domain-specific event in this toy case'}. No external action or domain model.`,'context_stub');}
const count=e.filter(x=>x.supports_claim).length;
record('Solvyr','Independent analyst A',`Blind synthetic first-pass: ${count} supporting / ${e.length-count} opposing. Sources not independently verified.`);
record('Elyrion','Independent analyst B',`Independent policy pass (same input records): weighted confidence ${Number(confidence(e).confidence_score).toFixed(2)}. Not an independent model instance.`);
record('Thornev','Independent challenge',count&&count<e.length?'Preserve contradictory observations; challenge consensus and source reuse.':'No contradictory observation present; still require independent verification.');
record('Orivane','Provenance auditing',`${e.length} records identify ${new Set(e.map(x=>x.observed_root)).size} observed upstream roots. Root identifiers may be falsified.`);
record('Kaelrix','Causal and falsification review','Keep claim true / claim false / unknown open; synthetic causal mechanisms are not verified.');
record('Varrun','Defensive-cost review',`Synthetic evidence-processing cost: ${e.length} units; real computation costs not measured.`);
record('Farreth','Priority and tail-risk review',`Scenario priority label: ${s.severity}; no actual triage undertaken.`);
record('Elyndra','Civilian burden review','Human impacts remain simulated; no population consequences are enacted.');
record('Oathryn','Constitutional review','All outcomes advisory only; consequential actions require external human authority.');
record('Synthera','System orchestration',`Run mode ${mode}; seed ${seed}; data order randomized but no network messaging.`);
record('Scarveth','Audit, replay and versioning','Exact inputs, role labels and outputs included in downloadable trace.');
record('Umbrakar','Independent red-team',s.attack_description);
const d=mode==='arbiter'?arbiter(e):mode==='majority'?base(e):confidence(e);
record('The Arbiter','Evidence-integrity oversight',mode==='arbiter'?d.explanation+' Advisory only.':'Disabled in this ablation condition.',mode==='arbiter'?'active_policy':'disabled');
const pos=d.recommendation==='REQUEST_HUMAN_REVIEW';
return {schema_version:'0.1',experiment_type:'synthetic_deterministic_policy_test',not_a_live_ai_swarm:true,scenario_id:id,scenario_title:s.title,claim:s.claim,seed:Number(seed),mode,agent_registry_count:D.agents.length,implemented_independent_llm_agents:0,evidence:e,ground_truth:s.ground_truth,evaluator_actual_roots,labels_withheld_from_candidate_policy:true,labels_not_security_isolated:true,recommendation:d.recommendation,positive_classification:pos,correct_classification:s.ground_truth===null?null:pos===s.ground_truth,confidence_score:d.confidence_score,explanation:d.explanation,alerts:d.alerts,observed_root_votes:d.eligible_roots,trace,limitations:['Every role is a deterministic policy/stub; no independent LLMs.','No OS-level security boundary is implemented.','All data and ground truth are invented for the test.','All outputs are advisory, not operational permission.','Source labels can be spoofed, defeating this toy Arbiter.']};
}
function compare(id,seed){return MODES.map(m=>run(id,seed,m));}
function batch(n=30){let rows=[];for(const id of Object.keys(D.scenarios))for(const mode of MODES){let positive=0,negative=0,correct=0,totalKnown=0;for(let seed=0;seed<n;seed++){const r=run(id,seed,mode);positive+=r.positive_classification?1:0;negative+=r.positive_classification?0:1;if(r.correct_classification!==null){totalKnown++;if(r.correct_classification)correct++;}}rows.push({scenario_id:id,mode,n,review:positive,hold:negative,correct,known:totalKnown});}return rows;}
global.HSPD={run,compare,batch,MODES,agents:D.agents,scenarios:D.scenarios};
})(window);
