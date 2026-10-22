# v23: 음성 중 BGM 덕킹 · 성적표 오답 라벨(응대 포함)  (build.py가 exec, build_v22 뒤)
src = rep(src, "speechSynthesis.cancel(); speechSynthesis.speak(u); TTS.last=u; return u; }catch(e){ return null; } }",
          "const bga=(typeof BGM_CUSTOM!=='undefined')&&BGM_CUSTOM.audio; if(bga&&!bga.paused){ bga.volume=0.12; const back=()=>{ try{ bga.volume=0.45; }catch(e){} }; u.addEventListener('end', back); u.addEventListener('error', back); } /* 음성 읽는 동안 BGM 줄이기 */ speechSynthesis.cancel(); speechSynthesis.speak(u); TTS.last=u; return u; }catch(e){ return null; } }")
src = rep(src, "function listenStop(){ LISTEN.on=false; LISTEN.tok=null;", "function listenStop(){ LISTEN.on=false; LISTEN.tok=null; try{ if(BGM_CUSTOM.audio) BGM_CUSTOM.audio.volume=0.45; }catch(e){}")
# 성적표: 오답에 응대 오답 포함 표시
src = rep(src, "$('sScore').textContent=total; $('sWrong').textContent=S.wrong;", "$('sScore').textContent=total; $('sWrong').textContent=S.wrong; try{ const qs=qSummary(); const lab=$('sWrong').previousElementSibling; if(lab) lab.textContent = qs.total && (qs.total-qs.ok)>0 ? `오답 (응대 ${qs.total-qs.ok} 포함)` : '오답'; }catch(e){}")
