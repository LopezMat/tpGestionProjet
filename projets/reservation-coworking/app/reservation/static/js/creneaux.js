// Fonctions pures de la page de disponibilités (T-055) : aucun accès au DOM, au réseau
// ni à l'horloge. L'instant courant est toujours passé en paramètre, pour être testé
// avec une heure simulée. Réutilisable par T-022 et T-023.

export const FUSEAU = "Europe/Paris";
export const JOURS_MAX = 14; // fenêtre de consultation : de J à J+14 (H-10)

const FORMAT_PARIS = new Intl.DateTimeFormat("en-CA", {
  timeZone: FUSEAU,
  year: "numeric",
  month: "2-digit",
  day: "2-digit",
  hour: "2-digit",
  hourCycle: "h23",
});

/**
 * Date (AAAA-MM-JJ) et heure entière (0-23) à Paris pour un instant donné,
 * quel que soit le fuseau du navigateur.
 * @param {Date} instant
 * @returns {{date: string, heure: number}}
 */
export function instantParis(instant) {
  const p = {};
  for (const { type, value } of FORMAT_PARIS.formatToParts(instant)) {
    p[type] = value;
  }
  return { date: `${p.year}-${p.month}-${p.day}`, heure: Number(p.hour) };
}

/**
 * Ajoute des jours à une date AAAA-MM-JJ (calcul calendaire, sans fuseau).
 * @param {string} date
 * @param {number} jours
 * @returns {string}
 */
export function ajouterJours(date, jours) {
  const [a, m, j] = date.split("-").map(Number);
  const d = new Date(Date.UTC(a, m - 1, j + jours));
  return d.toISOString().slice(0, 10);
}

/**
 * État affiché d'un créneau : « passe » si la date affichée est le jour J à Paris et que
 * l'heure de début est atteinte ; sinon l'état renvoyé par l'API (« libre » ou « occupe »).
 * @param {string} etatApi "libre" | "occupe"
 * @param {string} dateAffichee AAAA-MM-JJ
 * @param {number} heureDebut
 * @param {{date: string, heure: number}} maintenantParis voir instantParis
 * @returns {"libre"|"occupe"|"passe"}
 */
export function etatAffiche(etatApi, dateAffichee, heureDebut, maintenantParis) {
  if (dateAffichee === maintenantParis.date && heureDebut <= maintenantParis.heure) {
    return "passe";
  }
  return etatApi === "occupe" ? "occupe" : "libre";
}

/** Libellés texte (et icône) de chaque état : jamais la couleur seule. */
export const LIBELLES = {
  libre: { icone: "✓", texte: "Libre" },
  occupe: { icone: "✗", texte: "Occupé" },
  passe: { icone: "–", texte: "Passé" },
};

/** @param {number} heure @returns {string} ex. « 8 h – 9 h » */
export function libelleHoraire(heureDebut, heureFin) {
  return `${heureDebut} h – ${heureFin} h`;
}

/**
 * Message affiché pour une erreur de l'API. Propre à la page : le message renvoyé par
 * l'API n'est jamais recopié (il peut parler de réservation, ou être technique).
 * @param {number|null} statut code HTTP, ou null si le réseau a échoué
 * @returns {string}
 */
export function messageErreur(statut) {
  if (statut === 422) {
    return `Cette date ne peut pas être consultée. Choisissez un jour entre aujourd'hui et dans ${JOURS_MAX} jours.`;
  }
  if (statut === 503) {
    return "Le service est momentanément indisponible. Réessayez dans quelques instants.";
  }
  if (statut === null) {
    return "Impossible de joindre le service. Vérifiez votre connexion puis réessayez.";
  }
  return "Les disponibilités ne peuvent pas être affichées pour le moment. Réessayez plus tard.";
}

/** @param {{salles: Array<{creneaux: Array}>}} donnees @returns {boolean} */
export function aucunCreneau(donnees) {
  return donnees.salles.every((s) => s.creneaux.length === 0);
}
