(() => {
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];

  /* ---------- menu mobile ---------- */
  const mb = $(".menu-btn"), mn = $("#mnav");
  if (mb && mn) {
    const set = open => {
      mb.setAttribute("aria-expanded", open);
      mb.setAttribute("aria-label", open ? "Chiudi menu" : "Apri menu");
      mn.hidden = !open;
      document.documentElement.classList.toggle("nav-open", open);
      $(".menu-btn use").setAttribute("href", open ? "#i-x" : "#i-menu");
    };
    matchMedia("(min-width:1000px)").addEventListener("change", e => { if (e.matches) set(false); });
    mb.addEventListener("click", () => set(mn.hidden));
    mn.addEventListener("click", e => { if (e.target.closest("a")) set(false); });
    document.addEventListener("keydown", e => { if (e.key === "Escape" && !mn.hidden) { set(false); mb.focus(); } });
  }

  /* ---------- camera scelta dal pulsante "Chiedi disponibilità" ---------- */
  document.addEventListener("click", e => {
    const t = e.target.closest("[data-room]");
    const sel = $("#camera");
    if (t && sel) sel.value = t.dataset.room;
  });

  /* ---------- moduli (solo visivi) ---------- */
  const rules = {
    required: v => v.trim() !== "",
    tel: v => v.replace(/\D/g, "").length >= 8,
  };
  function check(el) {
    const box = el.closest(".field");
    if (!box) return true;
    let ok = true;
    const v = el.value;
    if (el.required && !rules.required(v)) ok = false;
    else if (v && el.dataset.rule && !rules[el.dataset.rule](v)) ok = false;
    else if (el.dataset.after) { const a = $("#" + el.dataset.after); if (a && a.value && v && v <= a.value) ok = false; }
    const err = $(".err", box);
    el.setAttribute("aria-invalid", !ok);
    if (err) err.hidden = ok;
    return ok;
  }
  $$("form[data-demo]").forEach(f => {
    f.noValidate = true;
    $$("input,select,textarea", f).forEach(el => el.addEventListener("blur", () => { if (el.value || el.getAttribute("aria-invalid") === "true") check(el); }));
    f.addEventListener("submit", e => {
      e.preventDefault();
      const bad = $$("input,select,textarea", f).filter(el => !check(el));
      if (bad.length) { bad[0].focus(); return; }
      const done = $("#" + f.dataset.demo);
      f.hidden = true;
      done.hidden = false;
      done.setAttribute("tabindex", "-1");
      done.focus();
    });
  });
})();
