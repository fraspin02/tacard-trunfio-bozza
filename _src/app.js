(() => {
  const P = /*PRODUCTS*/;
  const KEY = "tg-cart";
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const eur = n => n.toLocaleString("it-IT", { style: "currency", currency: "EUR" });
  const esc = s => s.replace(/[&<>"]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));

  /* ---------- menu mobile ---------- */
  const mb = $(".menu-btn"), mn = $("#mnav");
  if (mb && mn) {
    const set = open => {
      mb.setAttribute("aria-expanded", open);
      mb.setAttribute("aria-label", open ? "Chiudi menu" : "Apri menu");
      mn.hidden = !open;
      $(".menu-btn use").setAttribute("href", open ? "#i-x" : "#i-menu");
    };
    mb.addEventListener("click", () => set(mn.hidden));
    mn.addEventListener("click", e => { if (e.target.closest("a")) set(false); });
    document.addEventListener("keydown", e => { if (e.key === "Escape" && !mn.hidden) { set(false); mb.focus(); } });
  }

  /* ---------- carrello ---------- */
  let cart = {};
  try { cart = JSON.parse(localStorage.getItem(KEY)) || {}; } catch (e) {}
  const save = () => { try { localStorage.setItem(KEY, JSON.stringify(cart)); } catch (e) {} render(); };
  const count = () => Object.values(cart).reduce((a, b) => a + b, 0);
  const subtotal = () => Object.entries(cart).reduce((a, [k, q]) => a + (P[k] ? P[k].price * q : 0), 0);
  const add = (k, q = 1) => { if (!P[k]) return; cart[k] = Math.min(99, (cart[k] || 0) + q); save(); };
  const setQ = (k, q) => { if (q <= 0) delete cart[k]; else cart[k] = Math.min(99, q); save(); };
  const thumb = p => p.img ? `<img src="${p.img}" alt="" width="64" height="64" loading="lazy">` : `<div class="noimg" aria-hidden="true"></div>`;

  const drawer = $("#cart"), list = $("#cart-list"), live = $("#cart-live");
  let lastFocus = null;

  function render() {
    const n = count();
    $$(".badge").forEach(b => { b.textContent = n; b.hidden = n === 0; });
    $$(".cart-btn").forEach(b => b.setAttribute("aria-label", n ? `Carrello, ${n} ${n === 1 ? "prodotto" : "prodotti"}` : "Carrello, vuoto"));
    if (list) {
      const keys = Object.keys(cart).filter(k => P[k]);
      list.innerHTML = keys.map(k => {
        const p = P[k];
        return `<li class="line">${thumb(p)}<div><b>${esc(p.name)}</b><small>${esc(p.size)} · ${eur(p.price)}</small><br>
        <span class="qty"><button type="button" data-dec="${k}" aria-label="Diminuisci quantità di ${esc(p.name)}">−</button><input type="number" min="1" max="99" value="${cart[k]}" data-q="${k}" aria-label="Quantità di ${esc(p.name)}" inputmode="numeric"><button type="button" data-inc="${k}" aria-label="Aumenta quantità di ${esc(p.name)}">+</button></span></div>
        <div><b>${eur(p.price * cart[k])}</b><button type="button" class="rm" data-rm="${k}" aria-label="Rimuovi ${esc(p.name)}">Rimuovi</button></div></li>`;
      }).join("");
      $("#cart-empty").hidden = keys.length > 0;
      $("#cart-ft").hidden = keys.length === 0;
      $("#cart-sub").textContent = eur(subtotal());
    }
    renderCheckout();
  }

  function openCart() {
    if (!drawer) return;
    lastFocus = document.activeElement;
    drawer.hidden = false;
    document.body.style.overflow = "hidden";
    $(".drawer__close", drawer).focus();
  }
  function closeCart() {
    if (!drawer || drawer.hidden) return;
    drawer.hidden = true;
    document.body.style.overflow = "";
    if (lastFocus) lastFocus.focus();
  }

  document.addEventListener("click", e => {
    const t = e.target.closest("button,a");
    if (!t) return;
    if (t.matches(".cart-btn")) { e.preventDefault(); openCart(); }
    else if (t.matches("[data-close-cart]")) closeCart();
    else if (t.dataset.add) {
      const qi = $("#pd-qty");
      const q = qi && t.closest(".pd") ? Math.max(1, parseInt(qi.value, 10) || 1) : 1;
      add(t.dataset.add, q);
      if (live) live.textContent = `${P[t.dataset.add].name} aggiunto al carrello.`;
      const old = t.innerHTML;
      t.dataset.added = "";
      t.innerHTML = `<svg class="i" aria-hidden="true"><use href="#i-check"/></svg> Aggiunto`;
      setTimeout(() => { t.innerHTML = old; delete t.dataset.added; }, 1500);
    }
    else if (t.dataset.inc) setQ(t.dataset.inc, (cart[t.dataset.inc] || 0) + 1);
    else if (t.dataset.dec) setQ(t.dataset.dec, (cart[t.dataset.dec] || 0) - 1);
    else if (t.dataset.rm) { const n = P[t.dataset.rm].name; setQ(t.dataset.rm, 0); if (live) live.textContent = `${n} rimosso dal carrello.`; $(".drawer__close")?.focus(); }
    else if (t.dataset.step) {
      const i = $("#pd-qty"); if (i) i.value = Math.min(99, Math.max(1, (parseInt(i.value, 10) || 1) + +t.dataset.step));
    }
  });
  document.addEventListener("change", e => {
    const k = e.target.dataset && e.target.dataset.q;
    if (k) setQ(k, parseInt(e.target.value, 10) || 0);
  });
  document.addEventListener("keydown", e => {
    if (!drawer || drawer.hidden) return;
    if (e.key === "Escape") closeCart();
    if (e.key === "Tab") {
      const f = $$("button,a[href],input", drawer).filter(x => !x.closest("[hidden]"));
      const first = f[0], last = f[f.length - 1];
      if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
      else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
    }
  });

  /* ---------- checkout ---------- */
  function shipCost() {
    const r = $('input[name="consegna"]:checked');
    return r && r.value === "ritiro" ? 0 : 7;
  }
  function renderCheckout() {
    const box = $("#co-sum");
    if (!box) return;
    const keys = Object.keys(cart).filter(k => P[k]);
    const ship = keys.length ? shipCost() : 0;
    $("#co-items").innerHTML = keys.length
      ? keys.map(k => `<li><span>${cart[k]} × ${esc(P[k].name)} <small>(${esc(P[k].size)})</small></span><span>${eur(P[k].price * cart[k])}</span></li>`).join("")
      : `<li><span>Il carrello è vuoto. <a href="bottega.html">Vai alla bottega</a></span></li>`;
    $("#co-sub").textContent = eur(subtotal());
    $("#co-ship").textContent = ship ? eur(ship) : "Gratis";
    $("#co-tot").textContent = eur(subtotal() + ship);
    const btn = $("#co-submit"); if (btn) btn.disabled = !keys.length;
  }
  document.addEventListener("change", e => { if (e.target.name === "consegna") { renderCheckout(); const a = $("#addr"); if (a) { a.hidden = e.target.value === "ritiro"; $$(".err", a).forEach(x => x.hidden = true); $$("input", a).forEach(x => x.removeAttribute("aria-invalid")); } } });

  /* ---------- moduli (solo visivi) ---------- */
  const rules = {
    required: v => v.trim() !== "",
    email: v => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v.trim()),
    tel: v => v.replace(/\D/g, "").length >= 8,
    cap: v => /^\d{5}$/.test(v.trim()),
  };
  function check(el) {
    const box = el.closest(".field");
    if (!box || box.closest("[hidden]")) return true;
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
      const els = $$("input,select,textarea", f);
      const bad = els.filter(el => !check(el));
      if (bad.length) { bad[0].focus(); return; }
      const done = $("#" + f.dataset.demo);
      f.hidden = true;
      if (f.id === "co-form") { cart = {}; save(); }
      done.hidden = false;
      done.setAttribute("tabindex", "-1");
      done.focus();
    });
  });

  render();
})();
