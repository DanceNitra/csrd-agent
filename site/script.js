/**
 * CSRD Comply — Interactive Script
 * Hamburger menu, demo tabs, email reveal.
 */

// ─── Hamburger Menu ───
const hamburger = document.getElementById("hamburger");
const mainNav = document.getElementById("mainNav");

if (hamburger && mainNav) {
  hamburger.addEventListener("click", () => {
    mainNav.classList.toggle("open");
  });
  // Close on nav link click
  mainNav.querySelectorAll(".nav-link").forEach(link => {
    link.addEventListener("click", () => {
      mainNav.classList.remove("open");
    });
  });
}

// ─── Demo Tabs ───
const demoFiles = {
  zse: "demo/zse-2024-ixbrl.html",
  cez: "demo/cez-2025-ixbrl.html"
};

document.querySelectorAll(".demo-tab").forEach(tab => {
  tab.addEventListener("click", () => {
    document.querySelectorAll(".demo-tab").forEach(t => t.classList.remove("active"));
    tab.classList.add("active");

    const demoId = tab.dataset.demo;
    const frameContainer = document.getElementById("demoFrame");
    const listContainer = document.getElementById("demoList");

    if (demoId === "list") {
      frameContainer.style.display = "none";
      listContainer.style.display = "block";
    } else {
      frameContainer.style.display = "block";
      listContainer.style.display = "none";
      const iframe = frameContainer.querySelector("iframe");
      if (demoFiles[demoId]) {
        iframe.src = demoFiles[demoId];
      }
    }
  });
});

// ─── Email Reveal ───
function toggleEmail() {
  const el = document.getElementById("emailDisplay");
  if (el) {
    // Simple obfuscation: build from parts
    const user = "rastislav";
    const domain = "drahos";
    const tld = "sk";
    el.textContent = user + "." + domain + "@" + domain + "." + tld;
    el.style.border = "none";
    el.style.cursor = "default";
    el.onclick = null;
  }
}

// Make it globally accessible for inline onclick
window.toggleEmail = toggleEmail;
