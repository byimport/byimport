(function () {
  'use strict';

  // Récupère l'identifiant depuis l'URL /p/:id
  const id = decodeURIComponent(location.pathname.split('/').filter(Boolean)[1] || '');
  const root = document.getElementById('root');

  // Likes déjà donnés par ce visiteur (anti double-clic, persistant localement).
  const likedKey = 'monqr_liked';
  const liked = new Set(JSON.parse(localStorage.getItem(likedKey) || '[]'));
  function rememberLike(cid) {
    liked.add(cid);
    localStorage.setItem(likedKey, JSON.stringify([...liked]));
  }

  function fmtDate(ts) {
    try {
      return new Date(ts).toLocaleDateString('fr-FR', {
        day: 'numeric', month: 'short', year: 'numeric',
      });
    } catch (_) { return ''; }
  }

  function el(tag, props = {}, ...children) {
    const node = document.createElement(tag);
    Object.assign(node, props);
    for (const c of children) {
      if (c == null) continue;
      node.appendChild(typeof c === 'string' ? document.createTextNode(c) : c);
    }
    return node;
  }

  async function load() {
    let data;
    try {
      const res = await fetch('/api/profiles/' + encodeURIComponent(id));
      if (res.status === 404) return renderNotFound();
      data = await res.json();
    } catch (e) {
      root.innerHTML = '<div class="card"><p class="muted center">Impossible de charger ce profil.</p></div>';
      return;
    }
    render(data.profile, data.comments || []);
  }

  function renderNotFound() {
    root.innerHTML =
      '<div class="card center"><h2>Profil introuvable</h2>' +
      '<p class="muted">Ce QR code ne correspond à aucune carte.</p>' +
      '<a class="btn" href="/">Créer ma carte</a></div>';
  }

  function render(profile, comments) {
    if (profile.accent) {
      document.documentElement.style.setProperty('--accent', profile.accent);
    }
    root.innerHTML = '';

    // --- En-tête + liens ---
    const head = el('div', { className: 'card' });
    const initial = (profile.name || '?').trim().charAt(0).toUpperCase();
    const avatar = profile.avatar
      ? el('img', { className: 'avatar', src: profile.avatar, alt: profile.name })
      : el('div', { className: 'avatar placeholder' }, initial);

    const headInner = el('div', { className: 'profile-head' },
      avatar,
      el('h1', {}, profile.name),
      profile.bio ? el('p', { className: 'bio' }, profile.bio) : null,
    );
    head.appendChild(headInner);

    if (profile.socials && profile.socials.length) {
      const links = el('div', { className: 'links' });
      for (const s of profile.socials) {
        const meta = window.SOCIAL_BY_TYPE[s.type] || { label: s.type, color: '#64748b', icon: '?' };
        const a = el('a', { className: 'link-btn', href: s.url, target: '_blank', rel: 'noopener noreferrer' });
        a.appendChild(el('span', {
          className: 'badge',
          style: 'background:' + meta.color,
        }, meta.icon));
        a.appendChild(el('span', {}, s.label || meta.label));
        a.appendChild(el('span', { className: 'chev' }, '›'));
        links.appendChild(a);
      }
      head.appendChild(links);
    } else {
      head.appendChild(el('p', { className: 'muted center', style: 'margin-top:16px' },
        'Aucun réseau renseigné.'));
    }
    root.appendChild(head);

    // --- Section commentaires / avis ---
    const cbox = el('div', { className: 'card' });
    cbox.appendChild(el('h2', {}, 'Avis & commentaires'));

    const author = el('input', { id: 'cAuthor', maxLength: 60, placeholder: 'Votre nom (optionnel)' });
    const text = el('textarea', { id: 'cText', maxLength: 1000, placeholder: 'Laissez un mot, un avis…' });
    const sendBtn = el('button', { className: 'btn' }, 'Publier');
    const cMsg = el('div');

    sendBtn.addEventListener('click', async () => {
      const body = { author: author.value.trim(), text: text.value.trim() };
      if (!body.text) {
        cMsg.innerHTML = '<div class="msg error">Écrivez quelque chose avant de publier.</div>';
        return;
      }
      sendBtn.disabled = true;
      try {
        const res = await fetch('/api/profiles/' + encodeURIComponent(id) + '/comments', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(body),
        });
        const d = await res.json();
        if (!res.ok) throw new Error(d.error || 'Erreur');
        text.value = '';
        cMsg.innerHTML = '<div class="msg ok">Merci pour votre message !</div>';
        listEl.prepend(renderComment(d.comment));
        empty.style.display = 'none';
      } catch (e) {
        cMsg.innerHTML = '<div class="msg error">' + (e.message || 'Erreur') + '</div>';
      } finally {
        sendBtn.disabled = false;
      }
    });

    cbox.appendChild(el('label', {}, 'Votre nom'));
    cbox.appendChild(author);
    cbox.appendChild(el('label', {}, 'Votre message'));
    cbox.appendChild(text);
    cbox.appendChild(el('div', { className: 'spacer' }));
    cbox.appendChild(sendBtn);
    cbox.appendChild(cMsg);
    cbox.appendChild(el('div', { className: 'spacer' }));

    const listEl = el('div', { id: 'commentList' });
    const empty = el('p', { className: 'muted' }, 'Soyez le premier à laisser un avis 👍');
    if (comments.length) empty.style.display = 'none';
    cbox.appendChild(empty);
    cbox.appendChild(listEl);
    for (const c of comments) listEl.appendChild(renderComment(c));

    root.appendChild(cbox);

    // Bouton créer sa propre carte
    root.appendChild(el('p', { className: 'center', style: 'margin-top:8px' },
      el('a', { className: 'btn secondary', href: '/' }, 'Créer ma propre carte MonQR')));
  }

  function renderComment(c) {
    const node = el('div', { className: 'comment' });
    node.appendChild(el('div', { className: 'top' },
      el('span', { className: 'author' }, c.author || 'Anonyme'),
      el('span', { className: 'date' }, fmtDate(c.createdAt)),
    ));
    node.appendChild(el('p', { className: 'text' }, c.text));

    const btn = el('button', { className: 'like-btn' });
    const thumb = el('span', { className: 'thumb' }, '👍');
    const count = el('span', {}, String(c.likes || 0));
    btn.appendChild(thumb);
    btn.appendChild(count);
    if (liked.has(c.id)) btn.classList.add('liked');

    btn.addEventListener('click', async () => {
      if (liked.has(c.id)) return; // un seul like par visiteur
      btn.classList.add('liked');
      rememberLike(c.id);
      try {
        const res = await fetch(
          '/api/profiles/' + encodeURIComponent(id) + '/comments/' + encodeURIComponent(c.id) + '/like',
          { method: 'POST' });
        const d = await res.json();
        if (res.ok) count.textContent = String(d.likes);
      } catch (_) { /* on garde l'état optimiste */ }
    });

    node.appendChild(btn);
    return node;
  }

  load();
})();
