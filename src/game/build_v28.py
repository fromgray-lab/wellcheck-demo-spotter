# v28(v38): 구글 시트 저장소 연결 (SHEETS.url 있으면 최우선)  (build.py가 exec, build_v27 뒤)
src = rep(src, "\n/* 초기화 */", parts('v28.js') + "\n/* 초기화 */")
# 쓰기: teamAdd 맨 앞에서 시트 시도
src = rep(src, "async function teamAdd(col, doc, fromOutbox){ const db=await getDB();", "async function teamAdd(col, doc, fromOutbox){ if(SHEETS.url){ try{ await shPost(col, doc); if(!fromOutbox) setTimeout(flushOutbox, 400); return 'sheets'; }catch(e){} } const db=await getDB();")
src = rep(src, "async function teamWritable(){ if(TEAMW!==null) return TEAMW;", "async function teamWritable(){ if(SHEETS.url) return true; if(TEAMW!==null) return TEAMW;")
src = rep(src, "function saveStatus(where){ if(where==='supabase'||where==='db')", "function saveStatus(where){ if(where==='supabase'||where==='db'||where==='sheets')")
# 읽기
src = rep(src, "async function loadRuns(){\n", "async function loadRuns(){\n  if(SHEETS.url){ try{ return { rows:mergeRows(await shGet('runs'), localRuns()), src:'팀 공유 기록 (구글 시트)' }; }catch(e){} }\n")
src = rep(src, "async function loadFeedback(){ ", "async function loadFeedback(){ if(SHEETS.url){ try{ return mergeRows(await shGet('feedback'), localList('dsg_fb')); }catch(e){} } ")
src = rep(src, "async function loadEvals(){ ", "async function loadEvals(){ if(SHEETS.url){ try{ return mergeRows(await shGet('evals'), localList('dsg_evals')); }catch(e){} } ")
src = rep(src, "async function loadNotes(){ ", "async function loadNotes(){ if(SHEETS.url){ try{ const o={}; (await shGet('notes')).forEach(n=>{ if(n&&n.id) o[n.id]=n; }); return o; }catch(e){} } ")
src = rep(src, "BOARD.notes[id]=body; const db=await getDB();", "BOARD.notes[id]=body; if(SHEETS.url){ try{ await shPost('notes', { id, ...body }); return; }catch(e){} } const db=await getDB();")
src = rep(src, "async function loadOverrides(){ ", "async function loadOverrides(){ if(SHEETS.url){ try{ return (await shGet('overrides')).reverse(); }catch(e){} } ")
src = rep(src, "async function saveOverride(o){ const id=o.id||('ov'+Date.now().toString(36)+Math.random().toString(36).slice(2,6)); o.id=id; try{ const l=localList('dsg_overrides').filter(x=>x.id!==id); l.unshift(o); localStorage.setItem('dsg_overrides', JSON.stringify(l.slice(0,500))); }catch(e){}",
               "async function saveOverride(o){ const id=o.id||('ov'+Date.now().toString(36)+Math.random().toString(36).slice(2,6)); o.id=id; try{ const l=localList('dsg_overrides').filter(x=>x.id!==id); l.unshift(o); localStorage.setItem('dsg_overrides', JSON.stringify(l.slice(0,500))); }catch(e){} if(SHEETS.url){ try{ await shPost('overrides', o); return 'sheets'; }catch(e){} }")
