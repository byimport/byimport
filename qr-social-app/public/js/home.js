(function () {
  'use strict';

  // --- Construit la grille de saisie des réseaux -----------------------------
  const grid = document.getElementById('socialGrid');
  for (const s of window.SOCIALS) {
    const row = document.createElement('div');
    row.className = 'social-row';
    row.innerHTML = `
      <span class="net">
        <span class="badge" style="background:${s.color}">${s.icon}</span>${s.label}
      </span>
      <input data-type="${s.type}" placeholder="${s.hint}" maxlength="300" />`;
    grid.appendChild(row);
  }

  function collectSocials() {
    const socials = [];
    grid.querySelectorAll('input[data-type]').forEach((input) => {
      const value = input.value.trim();
      if (value) socials.push({ type: input.dataset.type, value });
    });
    return socials;
  }

  function showMsg(el, text, kind) {
    el.innerHTML = `<div class="msg ${kind}">${text}</div>`;
  }

  // --- Création --------------------------------------------------------------
  const createBtn = document.getElementById('createBtn');
  const formMsg = document.getElementById('formMsg');

  createBtn.addEventListener('click', async () => {
    const name = document.getElementById('name').value.trim();
    if (!name) return showMsg(formMsg, 'Indiquez au moins un nom.', 'error');

    const payload = {
      name,
      bio: document.getElementById('bio').value.trim(),
      avatar: document.getElementById('avatar').value.trim(),
      accent: document.getElementById('accent').value,
      socials: collectSocials(),
    };

    createBtn.disabled = true;
    createBtn.textContent = 'Création…';
    try {
      const res = await fetch('/api/profiles', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.error || 'Erreur');
      showResult(data.profile);
      loadList();
    } catch (e) {
      showMsg(formMsg, e.message || 'Une erreur est survenue.', 'error');
    } finally {
      createBtn.disabled = false;
      createBtn.textContent = 'Générer mon QR code';
    }
  });

  // --- Affichage du QR + lien ------------------------------------------------
  let lastUrl = '';

  function showResult(profile) {
    const url = location.origin + '/p/' + profile.id;
    lastUrl = url;
    document.getElementById('resultCard').style.display = 'block';
    document.getElementById('qrName').textContent = profile.name;
    document.getElementById('profileUrl').value = url;
    document.getElementById('openBtn').href = url;

    const box = document.getElementById('qrcode');
    box.innerHTML = '';
    if (typeof QRCode === 'function') {
      new QRCode(box, {
        text: url,
        width: 240,
        height: 240,
        colorDark: '#0f172a',
        colorLight: '#ffffff',
        correctLevel: QRCode.CorrectLevel.M,
      });
    } else {
      // Repli si la librairie QR n'a pas pu être chargée (hors ligne).
      box.innerHTML =
        '<p class="muted" style="max-width:240px">Aperçu QR indisponible hors ligne. ' +
        'Votre lien fonctionne quand même :</p>';
    }
    document.getElementById('resultCard').scrollIntoView({ behavior: 'smooth' });
  }

  document.getElementById('copyBtn').addEventListener('click', () => {
    const input = document.getElementById('profileUrl');
    input.select();
    navigator.clipboard?.writeText(input.value);
    const btn = document.getElementById('copyBtn');
    btn.textContent = 'Copié ✓';
    setTimeout(() => (btn.textContent = 'Copier'), 1500);
  });

  document.getElementById('printBtn').addEventListener('click', () => window.print());

  document.getElementById('dlBtn').addEventListener('click', () => {
    const canvas = document.querySelector('#qrcode canvas');
    if (!canvas) return alert('QR indisponible au téléchargement.');
    const a = document.createElement('a');
    a.href = canvas.toDataURL('image/png');
    a.download = 'monqr.png';
    a.click();
  });

  // --- Liste des profils -----------------------------------------------------
  async function loadList() {
    const container = document.getElementById('profileList');
    try {
      const res = await fetch('/api/profiles');
      const data = await res.json();
      if (!data.profiles.length) {
        container.innerHTML = '<p class="muted">Aucune carte pour le moment. Soyez le premier !</p>';
        return;
      }
      container.innerHTML = '';
      for (const p of data.profiles) {
        const a = document.createElement('a');
        a.className = 'list-item';
        a.href = '/p/' + p.id;
        const initial = (p.name || '?').trim().charAt(0).toUpperCase();
        const mini = p.avatar
          ? `<img class="mini" src="${encodeURI(p.avatar)}" alt="" />`
          : `<span class="mini">${initial}</span>`;
        a.innerHTML = mini;
        const txt = document.createElement('div');
        const strong = document.createElement('strong');
        strong.textContent = p.name;
        const small = document.createElement('div');
        small.className = 'muted';
        small.style.fontSize = '13px';
        small.textContent = p.bio || '';
        txt.appendChild(strong);
        txt.appendChild(small);
        a.appendChild(txt);
        container.appendChild(a);
      }
    } catch (e) {
      container.innerHTML = '<p class="muted">Impossible de charger la liste.</p>';
    }
  }

  loadList();
})();
