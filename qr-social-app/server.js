'use strict';

/**
 * MonQR — petit serveur HTTP sans dépendance (Node.js standard library).
 *
 * Fonctions :
 *   - création de profils "carte de visite" regroupant tous les réseaux sociaux ;
 *   - chaque profil a une URL publique encodée dans un QR code imprimable ;
 *   - les visiteurs laissent des commentaires/avis et peuvent les liker (pouce bleu).
 *
 * Stockage : deux fichiers JSON dans ./data (aucune base de données requise).
 */

const http = require('http');
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

const PORT = process.env.PORT || 3000;
const ROOT = __dirname;
const PUBLIC_DIR = path.join(ROOT, 'public');
const DATA_DIR = process.env.MONQR_DATA_DIR || path.join(ROOT, 'data');
const PROFILES_FILE = path.join(DATA_DIR, 'profiles.json');
const COMMENTS_FILE = path.join(DATA_DIR, 'comments.json');

// --- Petite couche de stockage JSON ------------------------------------------

function ensureStore() {
  if (!fs.existsSync(DATA_DIR)) fs.mkdirSync(DATA_DIR, { recursive: true });
  if (!fs.existsSync(PROFILES_FILE)) fs.writeFileSync(PROFILES_FILE, '[]');
  if (!fs.existsSync(COMMENTS_FILE)) fs.writeFileSync(COMMENTS_FILE, '{}');
}

function readJSON(file, fallback) {
  try {
    return JSON.parse(fs.readFileSync(file, 'utf8'));
  } catch (_) {
    return fallback;
  }
}

function writeJSON(file, data) {
  // Écriture atomique : on écrit dans un fichier temporaire puis on renomme.
  const tmp = file + '.tmp';
  fs.writeFileSync(tmp, JSON.stringify(data, null, 2));
  fs.renameSync(tmp, file);
}

// --- Helpers -----------------------------------------------------------------

const ALLOWED_SOCIALS = new Set([
  'instagram', 'facebook', 'tiktok', 'x', 'youtube', 'linkedin',
  'snapchat', 'whatsapp', 'telegram', 'twitch', 'pinterest',
  'website', 'email', 'phone',
]);

function makeId() {
  return crypto.randomBytes(5).toString('hex'); // 10 caractères
}

function slugify(str) {
  return String(str || '')
    .toLowerCase()
    .normalize('NFD').replace(/[̀-ͯ]/g, '') // enlève les accents
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '')
    .slice(0, 40);
}

function clean(str, max) {
  return String(str == null ? '' : str).trim().slice(0, max);
}

function isHttpUrl(value) {
  try {
    const u = new URL(value);
    return u.protocol === 'http:' || u.protocol === 'https:';
  } catch (_) {
    return false;
  }
}

function send(res, status, body, headers = {}) {
  res.writeHead(status, { 'Content-Type': 'application/json; charset=utf-8', ...headers });
  res.end(typeof body === 'string' ? body : JSON.stringify(body));
}

function readBody(req) {
  return new Promise((resolve, reject) => {
    let data = '';
    let tooBig = false;
    req.on('data', (chunk) => {
      data += chunk;
      if (data.length > 1e6) { // garde-fou : 1 Mo max
        tooBig = true;
        req.destroy();
      }
    });
    req.on('end', () => {
      if (tooBig) return reject(new Error('payload too large'));
      if (!data) return resolve({});
      try { resolve(JSON.parse(data)); } catch (e) { reject(e); }
    });
    req.on('error', reject);
  });
}

// --- Normalisation d'un profil entrant ---------------------------------------

function normalizeSocials(input) {
  if (!Array.isArray(input)) return [];
  const out = [];
  for (const item of input.slice(0, 30)) {
    if (!item || typeof item !== 'object') continue;
    const type = clean(item.type, 20).toLowerCase();
    let value = clean(item.value, 300);
    if (!ALLOWED_SOCIALS.has(type) || !value) continue;

    // On reconstruit une URL/valeur exploitable selon le type.
    let url = value;
    if (type === 'email') {
      url = value.startsWith('mailto:') ? value : 'mailto:' + value;
    } else if (type === 'phone') {
      url = value.startsWith('tel:') ? value : 'tel:' + value.replace(/[^\d+]/g, '');
    } else if (type === 'whatsapp') {
      const digits = value.replace(/[^\d]/g, '');
      url = digits ? 'https://wa.me/' + digits : value;
    } else if (!/^https?:\/\//i.test(value)) {
      // L'utilisateur a saisi un pseudo : on devine l'URL du réseau.
      const handle = value.replace(/^@/, '');
      const bases = {
        instagram: 'https://instagram.com/',
        facebook: 'https://facebook.com/',
        tiktok: 'https://tiktok.com/@',
        x: 'https://x.com/',
        youtube: 'https://youtube.com/@',
        linkedin: 'https://linkedin.com/in/',
        snapchat: 'https://snapchat.com/add/',
        telegram: 'https://t.me/',
        twitch: 'https://twitch.tv/',
        pinterest: 'https://pinterest.com/',
        website: 'https://',
      };
      url = (bases[type] || 'https://') + handle;
    }
    out.push({ type, label: clean(item.label, 40), value, url });
  }
  return out;
}

// --- API ---------------------------------------------------------------------

function listProfilesPublic() {
  const profiles = readJSON(PROFILES_FILE, []);
  return profiles
    .slice()
    .sort((a, b) => (b.createdAt || 0) - (a.createdAt || 0))
    .slice(0, 50)
    .map((p) => ({ id: p.id, name: p.name, bio: p.bio, avatar: p.avatar }));
}

function getProfile(id) {
  const profiles = readJSON(PROFILES_FILE, []);
  return profiles.find((p) => p.id === id) || null;
}

function createProfile(payload) {
  const name = clean(payload.name, 60);
  if (!name) return { error: 'Le nom est obligatoire.' };

  const profiles = readJSON(PROFILES_FILE, []);

  // Identifiant lisible et unique basé sur le nom.
  let base = slugify(name) || 'profil';
  let id = base;
  let n = 1;
  while (profiles.some((p) => p.id === id)) {
    id = base + '-' + (++n);
  }

  let avatar = clean(payload.avatar, 500);
  if (avatar && !isHttpUrl(avatar)) avatar = '';

  const profile = {
    id,
    name,
    bio: clean(payload.bio, 280),
    avatar,
    accent: clean(payload.accent, 7) || '#2563eb',
    socials: normalizeSocials(payload.socials),
    editToken: makeId(), // permet de prouver la propriété plus tard
    createdAt: Date.now(),
  };

  profiles.push(profile);
  writeJSON(PROFILES_FILE, profiles);
  return { profile };
}

function addComment(profileId, payload) {
  const profile = getProfile(profileId);
  if (!profile) return { error: 'Profil introuvable.' };

  const author = clean(payload.author, 60) || 'Anonyme';
  const text = clean(payload.text, 1000);
  if (!text) return { error: 'Le commentaire est vide.' };

  const comments = readJSON(COMMENTS_FILE, {});
  if (!comments[profileId]) comments[profileId] = [];
  const comment = {
    id: makeId(),
    author,
    text,
    likes: 0,
    createdAt: Date.now(),
  };
  comments[profileId].unshift(comment);
  writeJSON(COMMENTS_FILE, comments);
  return { comment };
}

function listComments(profileId) {
  const comments = readJSON(COMMENTS_FILE, {});
  return comments[profileId] || [];
}

function likeComment(profileId, commentId) {
  const comments = readJSON(COMMENTS_FILE, {});
  const list = comments[profileId] || [];
  const comment = list.find((c) => c.id === commentId);
  if (!comment) return { error: 'Commentaire introuvable.' };
  comment.likes = (comment.likes || 0) + 1;
  writeJSON(COMMENTS_FILE, comments);
  return { likes: comment.likes };
}

// --- Serveur de fichiers statiques -------------------------------------------

const MIME = {
  '.html': 'text/html; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.js': 'text/javascript; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.svg': 'image/svg+xml',
  '.png': 'image/png',
  '.ico': 'image/x-icon',
};

function serveStatic(res, filePath) {
  // Empêche la traversée de répertoire.
  const resolved = path.normalize(filePath);
  if (!resolved.startsWith(PUBLIC_DIR)) return send(res, 403, { error: 'forbidden' });
  fs.readFile(resolved, (err, data) => {
    if (err) return send(res, 404, { error: 'not found' });
    const ext = path.extname(resolved).toLowerCase();
    res.writeHead(200, { 'Content-Type': MIME[ext] || 'application/octet-stream' });
    res.end(data);
  });
}

// --- Routage -----------------------------------------------------------------

const server = http.createServer(async (req, res) => {
  const url = new URL(req.url, `http://${req.headers.host}`);
  const parts = url.pathname.split('/').filter(Boolean);

  try {
    // ----- API -----
    if (parts[0] === 'api') {
      // GET /api/profiles
      if (req.method === 'GET' && parts[1] === 'profiles' && parts.length === 2) {
        return send(res, 200, { profiles: listProfilesPublic() });
      }
      // POST /api/profiles
      if (req.method === 'POST' && parts[1] === 'profiles' && parts.length === 2) {
        const body = await readBody(req);
        const result = createProfile(body);
        return send(res, result.error ? 400 : 201, result);
      }
      // GET /api/profiles/:id
      if (req.method === 'GET' && parts[1] === 'profiles' && parts.length === 3) {
        const profile = getProfile(parts[2]);
        if (!profile) return send(res, 404, { error: 'Profil introuvable.' });
        const { editToken, ...publicProfile } = profile;
        return send(res, 200, { profile: publicProfile, comments: listComments(parts[2]) });
      }
      // GET /api/profiles/:id/comments
      if (req.method === 'GET' && parts[1] === 'profiles' && parts[3] === 'comments' && parts.length === 4) {
        return send(res, 200, { comments: listComments(parts[2]) });
      }
      // POST /api/profiles/:id/comments
      if (req.method === 'POST' && parts[1] === 'profiles' && parts[3] === 'comments' && parts.length === 4) {
        const body = await readBody(req);
        const result = addComment(parts[2], body);
        return send(res, result.error ? 400 : 201, result);
      }
      // POST /api/profiles/:id/comments/:cid/like
      if (req.method === 'POST' && parts[1] === 'profiles' && parts[3] === 'comments' && parts[5] === 'like') {
        const result = likeComment(parts[2], parts[4]);
        return send(res, result.error ? 404 : 200, result);
      }
      return send(res, 404, { error: 'route inconnue' });
    }

    // ----- Pages -----
    if (req.method === 'GET') {
      // Page profil public : /p/:id
      if (parts[0] === 'p' && parts[1]) {
        return serveStatic(res, path.join(PUBLIC_DIR, 'profile.html'));
      }
      // Racine
      if (parts.length === 0) {
        return serveStatic(res, path.join(PUBLIC_DIR, 'index.html'));
      }
      // Fichiers statiques (css/js/...)
      return serveStatic(res, path.join(PUBLIC_DIR, ...parts));
    }

    send(res, 405, { error: 'méthode non autorisée' });
  } catch (err) {
    send(res, 400, { error: 'Requête invalide.' });
  }
});

ensureStore();
server.listen(PORT, () => {
  console.log(`MonQR démarré sur http://localhost:${PORT}`);
});

module.exports = { server };
