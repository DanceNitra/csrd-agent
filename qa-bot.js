/**
 * CSRD Comply — Q&A Bot
 * In-browser knowledge base. No external API calls.
 * Answers are pre-defined in the knowledgeBase object below.
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
    answer: "Pokrývame všetky relevantné ESRS štandardy:\n\n**Environmentálne (E1–E5):**\n• E1 — Klimatická zmena (Scope 1/2/3, energy, ciele)\n• E2 — Znečistenie (NOx, hazardous waste)\n• E3 — Vodné zdroje (withdrawal, consumption)\n• E4 — Biodiverzita (ešty, dopad, mitigácia)\n• E5 — Cirkulárna ekonomika (waste, recycling)\n\n**Sociálne (S1–S4):**\n• S1 — Vlastná pracovná sila\n• S2 — Pracovníci v hodnotovom reťazci\n• S3 — Dotknuté komunity\n• S4 — Spotrebitelia a koncoví užívatelia\n\n**Governance (G1):**\n• G1 — Riadenie a podnikanie (korupcia, whistleblower, dodávatelia)\n\nSpolu 90+ konceptov v našej taxonómii.",
    related: ["čo je csrd", "aké normy spĺňate"]
  },
  "aké esrs štandardy": {
    answer: "Pokrývame všetky relevantné ESRS štandardy:\n\n**Environmentálne (E1–E5):**\n• E1 — Klimatická zmena (Scope 1/2/3, energy, ciele)\n• E2 — Znečistenie (NOx, hazardous waste)\n• E3 — Vodné zdroje (withdrawal, consumption)\n• E4 — Biodiverzita (ešty, dopad, mitigácia)\n• E5 — Cirkulárna ekonomika (waste, recycling)\n\n**Sociálne (S1–S4):**\n• S1 — Vlastná pracovná sila\n• S2 — Pracovníci v hodnotovom reťazci\n• S3 — Dotknuté komunity\n• S4 — Spotrebitelia a koncoví užívatelia\n\n**Governance (G1):**\n• G1 — Riadenie a podnikanie (korupcia, whistleblower, dodávatelia)\n\nSpolu 90+ konceptov v našej taxonómii.",
    related: ["čo je csrd", "aké normy spĺňate"]
  },
  "aké normy spĺňate": {
    answer: "CSRD Comply reporty spĺňajú:\n\n**✓ ESMA ESEF formát** — inline XBRL podľa European Single Electronic Format\n**✓ EFRAG namespace** — http://xbrl.efrag.org referencie\n**✓ ESRS 2–G1** — všetky relevantné štandardy\n**✓ 16/17 ESMA checks PASS** — jediný fail je ESRS2 minimum (očakávaný, vyžaduje doplnenie dát od klienta)\n**✓ SHA-256 audit trail** — kryptografický dôkaz integrity\n**✓ Limited assurance ready** — štruktúra pre audítora\n\n> Používame custom XSD s oficiálnym EFRAG namespace dočasne. Oficiálnu EFRAG taxonómiu integrujeme, len čo bude verejne dostupná.",
    related: ["ako overíte správnosť", "čo je ixbrl"]
  },
  "ako overíte že report je správny": {
    answer: "Každý náš report prechádza **dvojúrovňovou validáciou**:\n\n**1. Interná validácia (15 checkov):**\n✓ XML well-formedness\n✓ Povinné elementy (ESRS 2)\n✓ EFRAG namespace\n✓ Správne kontexty a jednotky\n✓ Duplicitné fakty\n✓ Atribúty elementov\n✓ iXBRL markup\n✓ Deklinácia faktov\n✓ A ďalšie...\n\n**2. ESMA ESEF checks (5 kontrol):**\n✓ Správny iXBRL formát\n✓ EFRAG namespace súlad\n✓ Povinné ESRS elementy\n✓ Kontexty\n✓ Deklinácia\n\n**Výsledok:** Compliance certifikát s výsledkami + SHA-256 audit trail.",
    related: ["čo je audit trail", "aké normy spĺňate"]
  },
  "ako overíte správnosť": {
    answer: "Každý náš report prechádza **dvojúrovňovou validáciou**:\n\n**1. Interná validácia (15 checkov):**\n✓ XML well-formedness\n✓ Povinné elementy (ESRS 2)\n✓ EFRAG namespace\n✓ Správne kontexty a jednotky\n✓ Duplicitné fakty\n✓ Atribúty elementov\n✓ iXBRL markup\n✓ Deklinácia faktov\n✓ A ďalšie...\n\n**2. ESMA ESEF checks (5 kontrol):**\n✓ Správny iXBRL formát\n✓ EFRAG namespace súlad\n✓ Povinné ESRS elementy\n✓ Kontexty\n✓ Deklinácia\n\n**Výsledok:** Compliance certifikát s výsledkami + SHA-256 audit trail.",
    related: ["čo je audit trail", "aké normy spĺňate"]
  },
  "čo je audit trail": {
    answer: "**Audit trail** je kryptografický záznam o vzniku a integrite reportu:\n\n• **SHA-256 hash** celého reportu — akákoľvek zmena = iný hash\n• **Timestamp** — kedy bol report vygenerovaný\n• **Verzia** — ktorá verzia enginu a taxonómie bola použitá\n• **Zoznam faktov** — presne aké dáta boli vložené\n\n🔒 **Pre audítora:** Audit trail umožňuje overiť, že report nebol po vygenerovaní zmenený. Je to kľúčový prvok pre limited assurance.",
    related: ["ako overíte správnosť", "aké normy spĺňate"]
  },
  "koľko stojí csrd report": {
    answer: "Cena závisí od rozsahu a počtu firiem:\n\n**📊 Orientačná cenová mapa:**\n• **Pilotný report** — €0 (zadarmo, ukážka na mieru)\n• **Jednorazový report** — podľa rozsahu dát (tisíce €, nie desiatky tisíc)\n• **Ročný reporting** — opakujúci sa, s automatizáciou a supportom\n• **Batch pre viac firiem** — skupinová zľava\n\nPre porovnanie: veľké poradenské firmy (Big4, BDO, TPA) účtujú €50K–€200K za prvý CSRD report.\n\nKontaktujte nás pre presnú cenovú ponuku na mieru.",
    related: ["kto musí reportovať", "čo produkt dokáže"]
  },
  "cena": {
    answer: "Cena závisí od rozsahu a počtu firiem:\n\n**📊 Orientačná cenová mapa:**\n• **Pilotný report** — €0 (zadarmo, ukážka na mieru)\n• **Jednorazový report** — podľa rozsahu dát (tisíce €, nie desiatky tisíc)\n• **Ročný reporting** — opakujúci sa, s automatizáciou a supportom\n• **Batch pre viac firiem** — skupinová zľava\n\nPre porovnanie: veľké poradenské firmy (Big4, BDO, TPA) účtujú €50K–€200K za prvý CSRD report.\n\nKontaktujte nás pre presnú cenovú ponuku na mieru.",
    related: ["kto musí reportovať", "čo produkt dokáže"]
  },
  "čo je esma esef": {
    answer: "**ESMA ESEF** (European Single Electronic Format) je nariadenie Európskeho orgánu pre cenné papiere a trhy (ESMA), ktoré určuje formát CSRD reportov.\n\n**Požiadavky:**\n• Formát: iXBRL (inline XBRL)\n• Taxonómia: EFRAG (European Financial Reporting Advisory Group)\n• Validácia: 17 kontrol (formát, namespace, elementy, kontexty, atď.)\n• Schválenie: Reportovanie do Národného depozitára (v SR)\n\nNáš engine generuje ESEF-kompatibilné iXBRL s 16/17 check PASS.",
    related: ["čo je ixbrl", "aké normy spĺňate"]
  },
  "čo produkt dokáže": {
    answer: "CSRD Comply dokáže:\n\n**✅ Automaticky generovať iXBRL reporty**\n— z YAML profilu alebo extrahovaných dát\n\n**✅ Kryť 10 ESRS štandardov**\n— E1–E5, S1–S4, G1 (90+ konceptov)\n\n**✅ Validovať podľa ESMA ESEF**\n— 5 kontrol + 15 interných checkov\n\n**✅ Audit trail (SHA-256)**\n— kryptografický dôkaz integrity\n\n**✅ Compliance certifikát**\n— súčasťou každého reportu\n\n**✅ Multi-firma pipeline**\n— batch generovanie pre ľubovoľný počet firiem\n\n➡️ Pozrite si DEMO sekciu pre reálne ukážky!",
    related: ["aké esrs štandardy", "aké normy spĺňate"]
  },
  "default": {
    answer: "Ďakujem za otázku! 🙏\n\nBohužiaľ, neviem na ňu presne odpovedať z mojej znalostnej bázy. Skúste sa opýtať inak alebo si vyberte z návrhov nižšie:\n\n• *Kto musí reportovať podľa CSRD?*\n• *Čo je iXBRL?*\n• *Aké ESRS štandardy pokrývate?*\n• *Ako overíte správnosť reportu?*\n• *Koľko stojí CSRD report?*\n\nAlebo nás kontaktujte priamo pre individuálnu konzultáciu.",
    related: []
  }
};

// ─── Helper: find matched answer ───
function findAnswer(input) {
  const normalized = input.toLowerCase().trim();
  // Remove diacritics for matching
  const ascii = normalized.normalize("NFD").replace(/[\u0300-\u036f]/g, "");

  // Exact match first
  for (const [key, value] of Object.entries(knowledgeBase)) {
    if (key === "default") continue;
    if (ascii === key || ascii.includes(key) || key.includes(ascii)) {
      return value;
    }
  }

  // Keyword matching
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
    "audit trail": ["čo je audit trail"],
    "sha": ["čo je audit trail"],
    "cena": ["koľko stojí csrd report"],
    "stoj": ["koľko stojí csrd report"],
    "produkt": ["čo produkt dokáže"],
    "dokaze": ["čo produkt dokáže"],
    "standard": ["aké esrs štandardy"],
    "pravidla": ["aké normy spĺňate"]
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
  // Short typing delay
  setTimeout(() => {
    addMessage(result.answer);
    // Update suggestions with related topics
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

// ─── Events ───
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
