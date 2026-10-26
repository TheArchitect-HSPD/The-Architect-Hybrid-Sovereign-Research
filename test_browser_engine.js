/* Optional Node.js regression checks for the offline browser policy engine. */
const fs=require('fs');const vm=require('vm');const path=require('path');
const root=__dirname;const context={window:{}};vm.createContext(context);
for(const name of ['dataset.js','engine_browser.js'])vm.runInContext(fs.readFileSync(path.join(root,name),'utf8'),context);
const H=context.window.HSPD;
const expectations={
 copied_false_consensus:['REQUEST_HUMAN_REVIEW','REQUEST_HUMAN_REVIEW','HOLD_UNCERTAINTY'],
 independently_confirmed_true:['REQUEST_HUMAN_REVIEW','REQUEST_HUMAN_REVIEW','REQUEST_HUMAN_REVIEW'],
 mixed_unknown:['HOLD_UNCERTAINTY','HOLD_UNCERTAINTY','HOLD_UNCERTAINTY'],
 intervention_feedback:['REQUEST_HUMAN_REVIEW','HOLD_UNCERTAINTY','HOLD_UNCERTAINTY'],
 spoofed_source_origins:['REQUEST_HUMAN_REVIEW','REQUEST_HUMAN_REVIEW','REQUEST_HUMAN_REVIEW'],
 single_source_true:['HOLD_UNCERTAINTY','HOLD_UNCERTAINTY','HOLD_UNCERTAINTY']
};
for(const [id,values] of Object.entries(expectations)){
 const got=H.compare(id,1).map(r=>r.recommendation);
 if(JSON.stringify(got)!==JSON.stringify(values))throw Error(`Mismatch ${id}: ${got}`);
 const r=H.run(id,1,'arbiter');
 if(r.trace.length!==21)throw Error(`Trace length ${id}`);
 if(r.evidence.some(x=>'actual_root_for_scoring' in x))throw Error('Evaluator roots leaked into policy evidence');
}
console.log('PASS: 6 browser engine scenario checks, 21 role traces, evaluator-only roots filtered.');
