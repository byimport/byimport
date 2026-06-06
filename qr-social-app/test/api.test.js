'use strict';

/**
 * Test d'intégration léger, sans dépendance : démarre le serveur sur un port
 * de test, dans un dossier de données temporaire, et vérifie le parcours
 * complet (création → lecture → commentaire → like).
 */

const http = require('http');
const fs = require('fs');
const os = require('os');
const path = require('path');
const assert = require('assert');

const PORT = 4599;
process.env.PORT = String(PORT);
process.env.MONQR_DATA_DIR = fs.mkdtempSync(path.join(os.tmpdir(), 'monqr-test-'));

const { server } = require('../server.js');

function request(method, urlPath, body) {
  return new Promise((resolve, reject) => {
    const data = body ? JSON.stringify(body) : null;
    const req = http.request(
      { host: 'localhost', port: PORT, path: urlPath, method,
        headers: data ? { 'Content-Type': 'application/json', 'Content-Length': Buffer.byteLength(data) } : {} },
      (res) => {
        let buf = '';
        res.on('data', (c) => (buf += c));
        res.on('end', () => {
          let json = null;
          try { json = JSON.parse(buf); } catch (_) {}
          resolve({ status: res.statusCode, body: json, raw: buf });
        });
      });
    req.on('error', reject);
    if (data) req.write(data);
    req.end();
  });
}

let passed = 0;
function check(label, cond) {
  assert.ok(cond, '✗ ' + label);
  passed++;
  console.log('✓ ' + label);
}

async function run() {
  // Le serveur écoute déjà (listen appelé au require). Petite attente.
  await new Promise((r) => setTimeout(r, 150));

  // 1. Création de profil
  let res = await request('POST', '/api/profiles', {
    name: 'Studio Léa',
    bio: 'Photographe à Genève',
    socials: [
      { type: 'instagram', value: '@studio.lea' },
      { type: 'whatsapp', value: '+41 79 123 45 67' },
      { type: 'website', value: 'monsite.ch' },
      { type: 'inconnu', value: 'doit être ignoré' },
    ],
  });
  check('création -> 201', res.status === 201);
  check('profil a un id', res.body.profile && typeof res.body.profile.id === 'string');
  check('réseau inconnu filtré', res.body.profile.socials.length === 3);
  const ig = res.body.profile.socials.find((s) => s.type === 'instagram');
  check('pseudo IG -> URL', ig.url === 'https://instagram.com/studio.lea');
  const wa = res.body.profile.socials.find((s) => s.type === 'whatsapp');
  check('whatsapp -> wa.me', wa.url === 'https://wa.me/41791234567');
  const web = res.body.profile.socials.find((s) => s.type === 'website');
  check('site sans http -> https', web.url === 'https://monsite.ch');
  const id = res.body.profile.id;

  // 2. Création sans nom -> 400
  res = await request('POST', '/api/profiles', { name: '' });
  check('sans nom -> 400', res.status === 400);

  // 3. Lecture du profil
  res = await request('GET', '/api/profiles/' + id);
  check('lecture -> 200', res.status === 200);
  check('editToken non exposé', res.body.profile.editToken === undefined);
  check('commentaires vides au départ', Array.isArray(res.body.comments) && res.body.comments.length === 0);

  // 4. Profil inexistant -> 404
  res = await request('GET', '/api/profiles/nexiste-pas');
  check('profil inconnu -> 404', res.status === 404);

  // 5. Ajout d'un commentaire
  res = await request('POST', '/api/profiles/' + id + '/comments', {
    author: 'Marc', text: 'Superbe travail !',
  });
  check('commentaire -> 201', res.status === 201);
  const cid = res.body.comment.id;
  check('commentaire likes=0', res.body.comment.likes === 0);

  // 6. Commentaire vide -> 400
  res = await request('POST', '/api/profiles/' + id + '/comments', { text: '   ' });
  check('commentaire vide -> 400', res.status === 400);

  // 7. Like
  res = await request('POST', '/api/profiles/' + id + '/comments/' + cid + '/like');
  check('like -> 200', res.status === 200);
  check('like incrémente à 1', res.body.likes === 1);
  res = await request('POST', '/api/profiles/' + id + '/comments/' + cid + '/like');
  check('like incrémente à 2', res.body.likes === 2);

  // 8. Like d'un commentaire inexistant -> 404
  res = await request('POST', '/api/profiles/' + id + '/comments/xxx/like');
  check('like commentaire inconnu -> 404', res.status === 404);

  // 9. La liste publique contient le profil
  res = await request('GET', '/api/profiles');
  check('liste contient le profil', res.body.profiles.some((p) => p.id === id));

  // 10. Page statique servie
  res = await request('GET', '/');
  check("page d'accueil servie", res.status === 200 && /MonQR/.test(res.raw));
  res = await request('GET', '/p/' + id);
  check('page profil servie', res.status === 200 && /profile.js/.test(res.raw));

  console.log(`\n${passed} vérifications réussies ✅`);
  server.close();
  // Nettoyage du dossier temporaire.
  fs.rmSync(process.env.MONQR_DATA_DIR, { recursive: true, force: true });
}

run().catch((err) => {
  console.error(err);
  server.close();
  process.exit(1);
});
