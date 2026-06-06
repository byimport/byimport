// Catalogue des réseaux pris en charge : libellé, couleur de marque,
// initiale affichée dans le badge, et indice de saisie.
window.SOCIALS = [
  { type: 'instagram', label: 'Instagram', color: '#E1306C', icon: 'IG', hint: '@pseudo ou lien' },
  { type: 'facebook',  label: 'Facebook',  color: '#1877F2', icon: 'f',  hint: 'pseudo ou lien' },
  { type: 'tiktok',    label: 'TikTok',    color: '#010101', icon: 'TT', hint: '@pseudo ou lien' },
  { type: 'x',         label: 'X / Twitter', color: '#000000', icon: 'X', hint: '@pseudo ou lien' },
  { type: 'youtube',   label: 'YouTube',   color: '#FF0000', icon: 'YT', hint: 'chaîne ou lien' },
  { type: 'linkedin',  label: 'LinkedIn',  color: '#0A66C2', icon: 'in', hint: 'pseudo ou lien' },
  { type: 'snapchat',  label: 'Snapchat',  color: '#FFFC00', icon: '👻', hint: 'pseudo' },
  { type: 'whatsapp',  label: 'WhatsApp',  color: '#25D366', icon: 'WA', hint: 'n° avec indicatif' },
  { type: 'telegram',  label: 'Telegram',  color: '#229ED9', icon: 'TG', hint: '@pseudo' },
  { type: 'twitch',    label: 'Twitch',    color: '#9146FF', icon: 'tv', hint: 'pseudo' },
  { type: 'pinterest', label: 'Pinterest', color: '#E60023', icon: 'P',  hint: 'pseudo ou lien' },
  { type: 'website',   label: 'Site web',  color: '#0EA5E9', icon: '🌐', hint: 'https://...' },
  { type: 'email',     label: 'E-mail',    color: '#6366F1', icon: '@',  hint: 'adresse e-mail' },
  { type: 'phone',     label: 'Téléphone', color: '#10B981', icon: '☎',  hint: 'n° de téléphone' },
];

window.SOCIAL_BY_TYPE = Object.fromEntries(window.SOCIALS.map((s) => [s.type, s]));
