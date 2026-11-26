// T-055 : tests de la logique pure de la page (node --test, aucune dépendance).
// Lancer : node --test tests/front/   (depuis app/). Rien de ce dossier n'entre dans l'image.

import assert from "node:assert/strict";
import { test } from "node:test";

import {
  aucunCreneau,
  ajouterJours,
  etatAffiche,
  instantParis,
  libelleHoraire,
  messageErreur,
} from "../../reservation/static/js/creneaux.js";

// Instants simulés (UTC). Novembre : Paris = UTC+1 ; juillet : Paris = UTC+2.
const A_13H30_PARIS = new Date("2026-11-26T12:30:00Z");

test("instantParis : 13 h 30 à Paris en hiver", () => {
  assert.deepEqual(instantParis(A_13H30_PARIS), { date: "2026-11-26", heure: 13 });
});

test("instantParis : heure d'été (UTC+2)", () => {
  assert.deepEqual(instantParis(new Date("2026-07-10T11:30:00Z")), { date: "2026-07-10", heure: 13 });
});

test("instantParis : minuit passé à Paris alors qu'il est encore la veille en UTC", () => {
  assert.deepEqual(instantParis(new Date("2026-11-25T23:30:00Z")), { date: "2026-11-26", heure: 0 });
});

test("instantParis ne dépend pas du fuseau du navigateur (TZ du processus)", () => {
  const avant = process.env.TZ;
  try {
    for (const tz of ["Pacific/Auckland", "America/Los_Angeles", "UTC"]) {
      process.env.TZ = tz;
      assert.deepEqual(instantParis(A_13H30_PARIS), { date: "2026-11-26", heure: 13 }, tz);
    }
  } finally {
    if (avant === undefined) delete process.env.TZ;
    else process.env.TZ = avant;
  }
});

const MAINTENANT = { date: "2026-11-26", heure: 13 };

test("à 13 h 30, les créneaux de 8 h à 13 h sont « passé » quel que soit l'état de l'API", () => {
  for (let h = 8; h <= 13; h++) {
    assert.equal(etatAffiche("libre", "2026-11-26", h, MAINTENANT), "passe", `libre ${h}`);
    assert.equal(etatAffiche("occupe", "2026-11-26", h, MAINTENANT), "passe", `occupe ${h}`);
  }
});

test("à 13 h 30, 14 h-15 h garde l'état de l'API (libre ou occupé)", () => {
  assert.equal(etatAffiche("libre", "2026-11-26", 14, MAINTENANT), "libre");
  assert.equal(etatAffiche("occupe", "2026-11-26", 14, MAINTENANT), "occupe");
  assert.equal(etatAffiche("libre", "2026-11-26", 19, MAINTENANT), "libre");
});

test("à l'heure pile du début (14 h 00), le créneau 14 h-15 h est « passé »", () => {
  assert.equal(etatAffiche("libre", "2026-11-26", 14, { date: "2026-11-26", heure: 14 }), "passe");
});

test("une autre date n'est pas concernée, même tard dans la journée", () => {
  const tard = { date: "2026-11-26", heure: 19 };
  assert.equal(etatAffiche("libre", "2026-11-27", 8, tard), "libre");
  assert.equal(etatAffiche("occupe", "2026-12-10", 8, tard), "occupe");
});

test("avant l'ouverture (7 h) aucun créneau du jour n'est « passé »", () => {
  assert.equal(etatAffiche("libre", "2026-11-26", 8, { date: "2026-11-26", heure: 7 }), "libre");
});

test("l'heure de Paris décide, pas celle de l'UTC : 23 h 30 UTC la veille = jour J 0 h à Paris", () => {
  const maintenant = instantParis(new Date("2026-11-25T23:30:00Z"));
  assert.equal(etatAffiche("libre", "2026-11-26", 8, maintenant), "libre"); // 0 h : rien de commencé
  assert.equal(etatAffiche("libre", "2026-11-25", 8, maintenant), "libre"); // la veille n'est pas concernée
});

test("ajouterJours : franchit fin de mois et d'année", () => {
  assert.equal(ajouterJours("2026-11-26", 14), "2026-12-10");
  assert.equal(ajouterJours("2026-12-25", 14), "2027-01-08");
  assert.equal(ajouterJours("2028-02-20", 14), "2028-03-05"); // année bissextile
});

test("libelleHoraire", () => {
  assert.equal(libelleHoraire(8, 9), "8 h – 9 h");
  assert.equal(libelleHoraire(19, 20), "19 h – 20 h");
});

test("aucunCreneau : week-end (listes vides) ou jour ouvré", () => {
  assert.equal(aucunCreneau({ salles: [{ creneaux: [] }, { creneaux: [] }] }), true);
  assert.equal(aucunCreneau({ salles: [{ creneaux: [] }, { creneaux: [{}] }] }), false);
});

test("messageErreur : messages propres à la page, sans détail technique ni mot « réserver »", () => {
  for (const statut of [422, 503, null, 500, 404, 0]) {
    const m = messageErreur(statut);
    assert.ok(m.length > 20, String(statut));
    assert.doesNotMatch(m, /réserv|HTTP|50\d|40\d|json|exception|traceback/i, String(statut));
  }
  assert.notEqual(messageErreur(422), messageErreur(503));
});
