var e=(o,t,n)=>new Promise((u,r)=>{var s=a=>{try{l(n.next(a))}catch(g){r(g)}},p=a=>{try{l(n.throw(a))}catch(g){r(g)}},l=a=>a.done?u(a.value):Promise.resolve(a.value).then(s,p);l((n=n.apply(o,t)).next())});import{p as c}from"./index.65159add.js";const S=()=>c({url:"/getProjectSummaryForBarplot/"}),h=()=>c({url:"/getRunSummaryForBarplot/"}),j=(o,t)=>e(void 0,null,function*(){var u;const n=yield c({url:"/getTumorTypeToID/"});o.value=n.map(r=>(r[0]=r.short_name,r[1]=r.phenotype_name,r[2]=r.mesh_id,r[3]=r.project_count,r[4]=r.run_count,r[5]=r.marker_count,r)),(u=o==null?void 0:o.value)==null||u.sort((r,s)=>s[1]-r[1]),t()}),k=()=>c({url:"/getTumorRank/"});export{j as a,S as b,h as c,k as g};