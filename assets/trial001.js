/* TRIAL001 published snapshot and private local receipt audit. No provider calls. */
(() => {
  "use strict";
  const $ = id => document.getElementById(id);
  const set = (id, msg) => { $(id).textContent = String(msg); };
  const required = ["agent-01","agent-02","agent-03","agent-04","agent-05","agent-21"];
  const caseName = n => "HSPD-TRIAL001-" + String(n).padStart(2,"0");
  let audited = [];

  function node(tag, text, parent, className) {
    const el=document.createElement(tag);
    if(className) el.className=className;
    el.textContent=String(text);
    if(parent) parent.appendChild(el);
    return el;
  }
  function metric(holder, title, value, explanation) {
    const card=node("article","",holder,"lab-result");
    node("h3",title,card);
    node("div",value,card,"lab-metric");
    node("p",explanation,card,"lab-small");
  }
  async function published() {
    try {
      const response=await fetch("trial001_status.json",{cache:"no-store"});
      if(!response.ok) throw Error("HTTP "+response.status);
      const data=await response.json();
      if(data.experiment_id!=="HSPD-TRIAL001" || data.scenario_total!==30) throw Error("Unexpected status schema");
      set("trial-status-note","Evidence source: "+data.report_provenance+". Published "+data.published_date+".");
      const metrics=$("trial-metrics");metrics.replaceChildren();
      metric(metrics,"Reported completed",data.scenarios_executed_reported+" / "+data.scenario_total,"Cases that generated a reported live six-role result.");
      metric(metrics,"Reported six-role accepted",data.scenarios_with_six_valid_llm_receipts_reported+" / "+data.scenario_total,"This is a receipt completion rate, not inference correctness.");
      metric(metrics,"Incomplete or failed",String(data.scenarios_with_incomplete_model_receipts_reported||0),"An incomplete receipt is kept as a failure, not counted as a completed case.");
      metric(metrics,"Unreported cases",data.scenarios_unexecuted_or_unreported+" / "+data.scenario_total,"No result is claimed for an unreported case.");
      const table=$("trial-case-table");table.replaceChildren();
      const done=new Set(data.successful_six_role_case_ids||[]);
      const incomplete=new Map((data.incomplete_cases||[]).map(x=>[x.scenario_id,x]));
      for(let i=1;i<=30;i++){
        const id=caseName(i);
        const tr=document.createElement("tr");
        node("td",id,tr);
        node("td",done.has(id)?"Reported 6/6 valid live receipts":incomplete.has(id)?("Incomplete: "+incomplete.get(id).valid_model_receipts_reported+"/6"):"No result reported",tr);
        node("td",done.has(id)?"Operator console summary, full JSON not reviewed":incomplete.has(id)?("Operator reported missing "+(incomplete.get(id).missing_agent_ids||[]).join(", ")+"; cause unverified"):"No receipt in published evidence",tr);
        table.appendChild(tr);
      }
    } catch(error) {set("trial-status-note","Could not load published progress: "+error.message);}
  }
  function audit(obj,filename) {
    if(!obj||typeof obj!=="object"||Array.isArray(obj)) throw Error("Not a JSON report object");
    const id=obj.scenario_id;
    if(typeof id!=="string"||!/^HSPD-TRIAL001-(0[1-9]|[12][0-9]|30)$/.test(id))throw Error("Unexpected scenario_id");
    if(!Array.isArray(obj.specialists)||obj.specialists.length!==5)throw Error("Expected five specialist receipts");
    const receipts=new Map();
    for(const r of obj.specialists) {
      if(!r||typeof r!=="object"||typeof r.agent_id!=="string"||receipts.has(r.agent_id))throw Error("Invalid or duplicate specialist ID");
      receipts.set(r.agent_id,r);
    }
    if(!obj.arbiter||typeof obj.arbiter!=="object"||receipts.has("agent-21"))throw Error("No Arbiter");
    receipts.set(obj.arbiter.agent_id,obj.arbiter);
    const valid=required.filter(a=>{
      const r=receipts.get(a);
      return r && r.mode==="llm" && ["ASSESSED","ABSTAIN"].includes(r.status);
    });
    const review=obj.enforced_decision==="REQUEST_HUMAN_REVIEW";
    const actionsDisabled=obj.real_world_actions_enabled===false;
    const missing=required.filter(a=>!valid.includes(a));
    return {scenario_id:id,file_name:filename,valid_llm_receipts:valid.length,missing_agent_ids:missing,
      human_review_enforced:review,real_world_actions_disabled:actionsDisabled,
      structural_receipt_pass:valid.length===6&&receipts.size===6&&review&&actionsDisabled,
      independently_verified:false,doctrine_efficacy_validated:false};
  }
  $("trial-files").addEventListener("change",async e=>{
    const files=Array.from(e.target.files||[]);
    audited=[];$("trial-audit-results").replaceChildren();
    $("trial-download").disabled=true;
    if(!files.length) return;
    if(files.length>30){set("trial-file-message","Select at most 30 reports.");return;}
    const seen=new Set(), failures=[];
    for(const f of files) {
      if(f.size>15*1024*1024){failures.push(f.name+": file exceeds 15 MB");continue;}
      try{
        const result=audit(JSON.parse(await f.text()),f.name);
        if(seen.has(result.scenario_id))throw Error("Duplicate scenario ID");
        seen.add(result.scenario_id);
        audited.push(result);
      }catch(error){failures.push(f.name+": "+error.message);}
    }
    const pass=audited.filter(r=>r.structural_receipt_pass).length;
    set("trial-file-message","Inspected "+audited.length+" valid report structures, "+pass+" passed strict six-role receipt checks. "+failures.length+" file errors. All processing is local.");
    const wrapper=$("trial-audit-results");wrapper.replaceChildren();
    const t=document.createElement("table");
    const head=document.createElement("thead"),hr=document.createElement("tr");
    for(const label of ["Case","Valid receipts","Safety","Verdict"])node("th",label,hr);
    head.appendChild(hr);t.appendChild(head);
    const body=document.createElement("tbody");
    for(const r of audited){
      const tr=document.createElement("tr");
      node("td",r.scenario_id,tr);
      node("td",r.valid_llm_receipts+" / 6",tr);
      node("td",r.human_review_enforced&&r.real_world_actions_disabled?"Review enforced, actions disabled":"SAFETY CHECK FAILED",tr);
      node("td",r.structural_receipt_pass?"Structural pass":"Incomplete or unsafe",tr);
      body.appendChild(tr);
    }
    t.appendChild(body);wrapper.appendChild(t);
    for(const fail of failures)node("p","Error: "+fail,wrapper,"lab-error");
    $("trial-download").disabled=!audited.length;
  });
  $("trial-download").addEventListener("click",()=>{
    if(!audited.length)return;
    const data={experiment_id:"HSPD-TRIAL001",source:"Local browser inspection of user-selected files",audited_at:new Date().toISOString(),
      results:audited,important_limitation:"Receipt and reported-safety checks only; no source authenticity or doctrine efficacy assessment"};
    const url=URL.createObjectURL(new Blob([JSON.stringify(data,null,2)+"\n"],{type:"application/json"}));
    const a=document.createElement("a");a.href=url;a.download="HSPD_TRIAL001_local_receipt_audit.json";a.click();
    setTimeout(()=>URL.revokeObjectURL(url),2500);
  });
  published();
})();
