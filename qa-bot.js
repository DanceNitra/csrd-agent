/**
 * CSRD Comply — Q&A Bot
 * In-browser knowledge base. No external API calls.
 * Answers updated to reflect real project status (no false claims).
 */

const knowledgeBase = {
  "kto musí reportovať podľa csrd": {
    answer: "Povinnosť reportovať podľa CSRD (Corporate Sustainability Reporting Directive) majú od 2025:\n\n**Veľké firmy** (od 2025):\n• ≥ 500 zamestnancov A\n• ≥ €50M obrat ALEBO ≥ €25M aktív\n\n**Ostatné veľké firmy** (od 2026):\n• ≥ 250 zamestnancov A\n• ≥ €40M obrat ALEBO €20M aktív\n\n**Kótované MSP** (od 2028, opt-out do 2030)\n\n➡️ Po Omnibus I (apríl 2026) boli kritériá upravené — na Slovensku ostalo ~20 firiem, v ČR ~50.",
    related: ["aké esrs štandardy", "čo je csrd"]
  },
  "kto musí reportovať": {
    answer: "Povinnosť reportovať podľa CSRD (Corporate Sustainability Reporting Directive) majú od 2025:\n\n**Veľké firmy** (od 2025):\n• ≥ 500 zamestnancov A\n• ≥ €50M obrat ALEBO ≥ €25M aktív\n\n**Ostatné veľké firmy** (od 2026):\n• ≥ 250 zamestnancov A\n• ≥ €40M obrat ALEBO €20M aktív\n\n**Kótované MSP** (od 2028, opt-out do 2030)\n\n➡️ Po Omnibus I (apríl 2026) boli kritériá upravené — na Slovensku ostalo ~20 firiem, v ČR ~50.",
    related: ["aké esrs štandardy", "čo je csrd"]
  },
  "čo je csrd": {
    answer: "**CSRD** (Corporate Sustainability Reporting Directive) je európska smernica, ktorá nahrádza NFRD. Vyžaduje od firiem štruktúrované reportovanie ESG údajov podľa ESRS (European Sustainability Reporting Standards) v iXBRL formáte.\n\n**Kľúčové fakty:**\n• Platné európske právo — priama regulácia, nie dobrovoľná\n• Reportuje sa v iXBRL (inline XBRL) — strojovo čitateľný formát\n• ESMA kontroluje ESEF (European Single Electronic Format) súlad\n• Audit trail a limited assurance od audítora sú povinné",
    related: ["kto musí reportovať", "čo je ixbrl"]
  },
  "čo je ixbrl": {
    answer: "**iXBRL** (inline XBRL) je formát, v ktorom sa musia podávať CSRD reporty podľa ESMA ESEF nariadenia.\n\n**Prečo je dôležitý?**\n• Ľudsky čitateľný — vyzerá ako normálna HTML stránka\n• Strojovo čitateľný — tagované dáta v XBRL formáte\n• ESMA ho kontroluje 17 rôznymi checkmi\n• Umožňuje automatické spracovanie a analýzu reportov\n\nNáš engine generuje iXBRL automaticky — vrátane správneho tagovania, namespace, kontextov a jednotiek.",
    related: ["čo je esma esef", "aké normy spĺňate"]
  },
  "aké esrs štandardy pokrývate": {
    answer: "Pokrývame tieto ESRS štandardy:\n\n**Environmentálne (E1-E5):**\n• E1 — Klimatická zmena (Scope 1/2/3, energy, ciele)\n• E2 — Znečistenie\n• E3 — Vodné zdroje\n• E4 — Biodiverzita\n• E5 — Cirkulárna ekonomika\n\n**Sociálne (S1-S4):**\n• S1 — Vlastná pracovná sila\n• S2 — Pracovníci v hodnotovom reťazci\n• S3 — Dotknuté komunity\n• S4 — Spotrebitelia\n\n**Governance (G1):**\n• G1 — Riadenie a podnikanie\n\nVšetky element names sú overené proti oficiálnej EFRAG XSD.",
    related: ["čo je csrd", "aké normy spĺňate"]
  },
  "aké esrs štandardy": {
    answer: "Pokrývame tieto ESRS štandardy:\n\n**Environmentálne (E1-E5):**\n• E1 — Klimatická zmena (Scope 1/2/3, energy, ciele)\n• E2 — Znečistenie\n• E3 — Vodné zdroje\n• E4 — Biodiverzita\n• E5 — Cirkulárna ekonomika\n\n**Sociálne (S1-S4):**\n• S1 — Vlastná pracovná sila\n• S2 — Pracovníci v hodnotovom reťazci\n• S3 — Dotknuté komunity\n• S4 — Spotrebitelia\n\n**Governance (G1):**\n• G1 — Riadenie a podnikanie\n\nVšetky element names sú overené proti oficiálnej EFRAG XSD.",
    related: ["čo je csrd", "aké normy spĺňate"]
  },
  "aké normy spĺňate": {
    answer: "Čo CSRD Comply naozaj spĺňa a čo nie:\n\n**✅ NAOZAJ SPĹŇAME:**\n✓ EFRAG ESRS Set 1 XBRL Taxonomy — oficiálne element names (overené v esrs_cor.xsd)\n✓ Správny namespace: https://xbrl.efrag.org/taxonomy/esrs/2023-12-22\n✓ Inline XBRL 1.1 — ix:header, ix:hidden, ix:resources štruktúra\n✓ SHA-256 audit trail pre každý report\n✓ 33 element names — všetky overené proti oficiálnej EFRAG XSD\n\n**❌ NESPĹŇAME (ešte):**\n✗ Nie sme ESMA-certifikovaný validátor\n✗ Nie sme limited assurance — potrebný registrovaný audítor\n✗ Report má 25-35 faktov — reálny ESRS report 800-3,000\n✗ Chýbajú dimenzie, linkbasy, Scope 3 breakdown\n\n**Transparentnosť:** Používame oficiálnu EFRAG taxonómiu, nie custom XSD.",
    related: ["ako overíte správnosť", "čo je ixbrl"]
  },
  "ako overíte že report je správny": {
    answer: "Validačný proces:\n\n**1. Element name verifikácia**\nKaždý element name je skontrolovaný proti oficiálnej EFRAG esrs_cor.xsd (5,432 elementov). Žiadne vymyslené mená.\n\n**2. XML validácia**\nReport sa parsuje ako XML — kontroluje sa well-formedness.\n\n**3. iXBRL štruktúra**\nSprávny namespace, schemaRef, kontexty, jednotky.\n\n**4. SHA-256 audit trail**\nKryptografický hash — akákoľvek zmena = iný hash.\n\n**Poznámka:** Nie sme ESMA-certifikovaný validátor. Oficiálny ESEF filing vyžaduje nástroj ako Arelle.",
    related: ["čo je audit trail", "aké normy spĺňate"]
  },
  "ako overíte správnosť": {
    answer: "Validačný proces:\n\n**1. Element name verifikácia**\nKaždý element name je skontrolovaný proti oficiálnej EFRAG esrs_cor.xsd (5,432 elementov). Žiadne vymyslené mená.\n\n**2. XML validácia**\nReport sa parsuje ako XML — kontroluje sa well-formedness.\n\n**3. iXBRL štruktúra**\nSprávny namespace, schemaRef, kontexty, jednotky.\n\n**4. SHA-256 audit trail**\nKryptografický hash — akákoľvek zmena = iný hash.\n\n**Poznámka:** Nie sme ESMA-certifikovaný validátor. Oficiálny ESEF filing vyžaduje nástroj ako Arelle.",
    related: ["čo je audit trail", "aké normy spĺňate"]
  },
  "čo je audit trail": {
    answer: "**Audit trail** je kryptografický záznam o vzniku a integrite reportu:\n\n• **SHA-256 hash** celého reportu — akákoľvek zmena = iný hash\n• **Timestamp** — kedy bol report vygenerovaný\n• **Verzia** — ktorá verzia enginu a taxonómie bola použitá\n• **Zoznam faktov** — presne aké dáta boli vložené\n\n🔒 **Pre audítora:** Audit trail umožňuje overiť, že report nebol po vygenerovaní zmenený.",
    related: ["ako overíte správnosť", "aké normy spĺňate"]
  },
  "koľko stojí csrd report": {
    answer: "Cena závisí od rozsahu a počtu firiem:\n\n**📊 Orientačná cenová mapa:**\n• **Pilotný report** — €0 (zadarmo, ukážka na mieru)\n• **Jednorazový report** — podľa rozsahu dát\n• **Ročný reporting** — opakujúci sa, s automatizáciou\n• **Batch pre viac firiem** — skupinová zľava\n\nPre porovnanie: Big4 účtujú €50K-€200K za prvý CSRD report.\n\nKontaktujte nás pre presnú cenovú ponuku.",
    related: ["kto musí reportovať", "čo produkt dokáže"]
  },
  "cena": {
    answer: "Cena závisí od rozsahu a počtu firiem:\n\n**📊 Orientačná cenová mapa:**\n• **Pilotný report** — €0 (zadarmo, ukážka na mieru)\n• **Jednorazový report** — podľa rozsahu dát\n• **Ročný reporting** — opakujúci sa, s automatizáciou\n• **Batch pre viac firiem** — skupinová zľava\n\nPre porovnanie: Big4 účtujú €50K-€200K za prvý CSRD report.\n\nKontaktujte nás pre presnú cenovú ponuku.",
    related: ["kto musí reportovať", "čo produkt dokáže"]
  },
  "čo je esma esef": {
    answer: "**ESMA ESEF** (European Single Electronic Format) je nariadenie Európskeho orgánu pre cenné papiere a trhy (ESMA), ktoré určuje formát CSRD reportov.\n\n**Požiadavky:**\n• Formát: iXBRL (inline XBRL)\n• Taxonómia: EFRAG\n• Validácia: 17 kontrol (formát, namespace, elementy, kontexty)\n\nNáš engine generuje iXBRL s oficiálnou EFRAG taxonómiou, ale nie sme ESMA-certifikovaný validátor.",
    related: ["čo je ixbrl", "aké normy spĺňate"]
  },
  "aké sú limity produktu": {
    answer: "**Transparentné limity CSRD Comply:**\n\n1. **Hĺbka reportov:** 25-35 faktov vs. 800-3,000 v reálnom ESRS reporte\n2. **Chýbajúce dimenzie:** Scope 3 breakdown, country breakdown, target trajectories\n3. **Nie je ESMA certifikovaný:** na oficiálny filing treba ESMA nástroj\n4. **Nie je limited assurance:** potrebný registrovaný audítor\n5. **CLI nástroj:** nie je to webová aplikácia\n6. **ESRS2 narrative:** nie všetky textové koncepty sú namapované\n\nVšetky element names sú ale 100% overené proti oficiálnej EFRAG XSD. Žiadne vymyslené koncepty.",
    related: ["aké normy spĺňate", "čo produkt dokáže"]
  },
  "default": {
    answer: "Ďakujem za otázku! 🙏\n\nBohužiaľ, neviem na ňu presne odpovedať z mojej znalostnej bázy. Skúste sa opýtať inak alebo si vyberte z návrhov nižšie:\n\n• *Kto musí reportovať podľa CSRD?*\n• *Čo je iXBRL?*\n• *Aké ESRS štandardy pokrývate?*\n• *Ako overíte správnosť reportu?*\n• *Koľko stojí CSRD report?*\n\nAlebo nás kontaktujte priamo pre individuálnu konzultáciu.",
    related: []
  }
};

// ─── Helper: find matched answer ───
function findAnswer(input) {
  const normalized = input.toLowerCase().trim();
  const ascii = normalized.normalize("NFD").replace(/[\u0300-\u036f]/g, "");

  for (const [key, value] of Object.entries(knowledgeBase)) {
    if (key === "default") continue;
    if (ascii === key || ascii.includes(key) || key.includes(ascii)) {
      return value;
    }
  }

  const keywords = {
    "kto": ["kto musí reportovať"],
    "povinne": ["kto musí reportovať"],
    "csrd": ["čo je csrd"],
    "ixbrl": ["čo je ixbrl"],
    "esef": ["čo je esma esef"],
    "esma": ["čo je esma esef"],
    "esrs": ["aké esrs štandardy"],
    "norm": ["aké normy spĺňate"],
    "valid": ["ako overíte správnosť"],
    "overi": ["ako overíte správnosť"],
    "audit": ["čo je audit trail"],
    "sha": ["čo je audit trail"],
    "cena": ["koľko stojí csrd report"],
    "stoj": ["koľko stojí csrd report"],
    "produkt": ["aké sú limity produktu"],
    "limit": ["aké sú limity produktu"],
    "standard": ["aké esrs štandardy"],
  };

  for (const [kw, targets] of Object.entries(keywords)) {
    if (ascii.includes(kw)) {
      for (const t of targets) {
        if (knowledgeBase[t]) return knowledgeBase[t];
      }
    }
  }

  return knowledgeBase.default;
}

// ─── UI Logic ───
const qaMessages = document.getElementById("qaMessages");
const qaInput = document.getElementById("qaInput");
const qaSend = document.getElementById("qaSend");
const qaSugs = document.getElementById("qaSuggestions");

function addMessage(text, isUser = false) {
  const div = document.createElement("div");
  div.className = `qa-msg ${isUser ? "qa-user" : "qa-bot"}`;
  div.innerHTML = `
    <div class="qa-avatar">${isUser ? "◆" : "◇"}</div>
    <div class="qa-bubble">${text.replace(/\n/g, '<br>')}</div>
  `;
  qaMessages.appendChild(div);
  qaMessages.scrollTop = qaMessages.scrollHeight;
}

function handleQuestion(q) {
  if (!q.trim()) return;
  addMessage(q, true);
  const result = findAnswer(q);
  setTimeout(() => {
    addMessage(result.answer);
    if (result.related && result.related.length > 0) {
      updateSuggestions(result.related);
    }
  }, 300);
  qaInput.value = "";
}

function updateSuggestions(terms) {
  qaSugs.innerHTML = terms
    .map(t => {
      const q = Object.keys(knowledgeBase).find(k => k.includes(t));
      if (q && knowledgeBase[q]) {
        return `<button class="qa-chip" data-q="${q}">${capitalize(t)}</button>`;
      }
      return "";
    })
    .join("");
}

function capitalize(s) { return s.charAt(0).toUpperCase() + s.slice(1); }

qaSend.addEventListener("click", () => handleQuestion(qaInput.value));
qaInput.addEventListener("keydown", (e) => {
  if (e.key === "Enter") handleQuestion(qaInput.value);
});
qaSugs.addEventListener("click", (e) => {
  const chip = e.target.closest(".qa-chip");
  if (chip) {
    const q = chip.dataset.q;
    if (knowledgeBase[q]) {
      addMessage(chip.textContent, true);
      setTimeout(() => {
        addMessage(knowledgeBase[q].answer);
        if (knowledgeBase[q].related && knowledgeBase[q].related.length > 0) {
          updateSuggestions(knowledgeBase[q].related);
        }
      }, 300);
    }
  }
});