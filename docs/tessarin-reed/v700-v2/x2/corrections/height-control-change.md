# Explicit height application

The original browser attempt changed the numeric field while the prism status stayed at height 1.5. B12 records the field value only and is not render validation. B13 failed its clamp comparison. The original HTML remains byte-exact. The correction adds an Apply height button and Enter action that call the existing normalization and render procedure. The targeted checks compare both numeric field and visible status, with prism coordinates checked for valid and clamped heights.

The empty-string fill helper did not clear the field. Keyboard selection and Backspace established an empty visible field, after which Apply used height 1.5. This is a retained interaction failure and targeted input recovery, with no further HTML edit.

```diff
--- original.html
+++ current.html
@@ -11,7 +11,7 @@
 <label for="rotation">Rotation <output id="rotation-value" for="rotation">−28°</output></label><input id="rotation" type="range" min="-180" max="180" value="-28" step="1">
 <label for="tilt">Tilt <output id="tilt-value" for="tilt">32°</output></label><input id="tilt" type="range" min="10" max="75" value="32" step="1">
 <label for="height">Display height (0.25 to 4)</label><input id="height" type="number" min="0.25" max="4" step="0.25" value="1.5" inputmode="decimal">
-<div class="buttons"><button class="secondary" id="left" type="button">Rotate left</button><button class="secondary" id="right" type="button">Rotate right</button><button id="reset" type="button">Reset view</button></div>
+<div class="buttons"><button id="apply-height" type="button">Apply height</button><button class="secondary" id="left" type="button">Rotate left</button><button class="secondary" id="right" type="button">Rotate right</button><button id="reset" type="button">Reset view</button></div>
 <p id="status" role="status" aria-live="polite"></p></section></div>
 <section class="panel" aria-labelledby="selected-heading"><h2 id="selected-heading">Selected coordinates</h2><p id="selected-summary"></p><p class="coords" id="coordinates"></p><p class="coords" id="prism-coordinates"></p><p id="polynomial"></p></section>
 <section class="notice" aria-label="Evidence limits"><p><strong>Finite synthetic geometry.</strong> These prisms are coordinate displays, and their height does not describe a material or a physical field. The arithmetic and browser checks are same-owner evidence. External observation, independent reproduction and evaluation with assistive technology remain separate work.</p><p>Mind, Body and Heart may be used as structural analogies. This display grants no scientific, cultural, legal or deployment authority. Māori concepts remain under Māori authority. The phase remains <strong>NOT_READY_FOR_STAGE_20</strong>.</p></section>
@@ -63,7 +63,10 @@
 controls.model.addEventListener('change',()=>{state.id=controls.model.value;render();});
 controls.rotation.addEventListener('input',()=>{state.rotation=clamp(Number(controls.rotation.value),-180,180);render();});
 controls.tilt.addEventListener('input',()=>{state.tilt=clamp(Number(controls.tilt.value),10,75);render();});
-controls.height.addEventListener('change',()=>{const raw=Number(controls.height.value);state.height=clamp(Number.isFinite(raw)&&controls.height.value!==''?raw:1.5,.25,4);render();});
+function applyHeight(){const raw=Number(controls.height.value);state.height=clamp(Number.isFinite(raw)&&controls.height.value!==''?raw:1.5,.25,4);render();}
+controls.height.addEventListener('change',applyHeight);
+byId('apply-height').addEventListener('click',applyHeight);
+controls.height.addEventListener('keydown',e=>{if(e.key==='Enter'){e.preventDefault();applyHeight();}});
 byId('left').addEventListener('click',()=>{state.rotation=clamp(state.rotation-15,-180,180);render();});
 byId('right').addEventListener('click',()=>{state.rotation=clamp(state.rotation+15,-180,180);render();});
 byId('reset').addEventListener('click',reset);
```

Bounded same-owner synthetic mathematical and software evidence only. No empirical GMUT, production THOS or Freed ID, independent reproduction, identity continuity, consciousness, personhood, qualification, agency, professional, legal, cultural, affected-party or Maori authority, complete privacy or accessibility, exhaustive security, deployment, Theory-of-Everything, canon or Stage 20 claim. Maori concepts remain under Maori authority.
