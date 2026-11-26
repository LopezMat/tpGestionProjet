// Page de consultation des disponibilités (T-055, F-01, lecture seule).
// CSP : aucun style en ligne, aucune ressource externe ; données insérées par textContent.

import { ErreurApi, lireDisponibilites } from "./api.js";
import {
  LIBELLES,
  JOURS_MAX,
  aucunCreneau,
  ajouterJours,
  etatAffiche,
  instantParis,
  libelleHoraire,
  messageErreur,
} from "./creneaux.js";

const champDate = document.getElementById("date");
const zoneMessage = document.getElementById("message");
const zoneSalles = document.getElementById("salles");

let requeteEnCours = null; // pour ignorer une réponse devenue obsolète

function afficherMessage(texte, erreur) {
  zoneMessage.textContent = texte;
  zoneMessage.classList.toggle("message-erreur", erreur);
  zoneMessage.hidden = texte === "";
  // role="alert" pour les erreurs (annoncé tout de suite), "status" sinon.
  zoneMessage.setAttribute("role", erreur ? "alert" : "status");
}

function vider(element) {
  element.replaceChildren();
}

function creerCreneau(creneau, date, maintenant) {
  const etat = etatAffiche(creneau.etat, date, creneau.heure_debut, maintenant);
  const libelle = LIBELLES[etat];

  const li = document.createElement("li");
  li.classList.add("creneau", `creneau-${etat}`);

  const horaire = document.createElement("span");
  horaire.classList.add("horaire");
  horaire.textContent = libelleHoraire(creneau.heure_debut, creneau.heure_fin);

  const statut = document.createElement("span");
  statut.classList.add("statut");
  const icone = document.createElement("span");
  icone.setAttribute("aria-hidden", "true");
  icone.textContent = libelle.icone;
  const texte = document.createElement("span");
  texte.textContent = libelle.texte;
  statut.append(icone, " ", texte);

  li.append(horaire, statut);
  return li;
}

function afficher(donnees, date, maintenant) {
  vider(zoneSalles);
  if (aucunCreneau(donnees)) {
    afficherMessage("Aucun créneau ce jour-là.", false);
    return;
  }
  afficherMessage("", false);
  for (const salle of donnees.salles) {
    const section = document.createElement("section");
    section.classList.add("salle");
    const titre = document.createElement("h2");
    titre.textContent = salle.nom;
    const liste = document.createElement("ul");
    liste.classList.add("creneaux");
    for (const creneau of salle.creneaux) {
      liste.append(creerCreneau(creneau, date, maintenant));
    }
    section.append(titre, liste);
    zoneSalles.append(section);
  }
}

async function charger() {
  const date = champDate.value;
  if (requeteEnCours) requeteEnCours.abort();
  vider(zoneSalles);
  if (!/^\d{4}-\d{2}-\d{2}$/.test(date)) {
    afficherMessage("Choisissez une date.", true);
    return;
  }
  const controleur = new AbortController();
  requeteEnCours = controleur;
  zoneSalles.setAttribute("aria-busy", "true");
  afficherMessage("Chargement…", false);
  try {
    const donnees = await lireDisponibilites(date, controleur.signal);
    // L'heure est lue après la réponse : l'état « passé » est celui du moment de l'affichage.
    afficher(donnees, date, instantParis(new Date()));
  } catch (e) {
    if (e && e.name === "AbortError") return;
    vider(zoneSalles);
    afficherMessage(messageErreur(e instanceof ErreurApi ? e.statut : null), true);
  } finally {
    if (requeteEnCours === controleur) {
      requeteEnCours = null;
      zoneSalles.removeAttribute("aria-busy");
    }
  }
}

function demarrer() {
  const aujourdhui = instantParis(new Date()).date;
  champDate.min = aujourdhui;
  champDate.max = ajouterJours(aujourdhui, JOURS_MAX);
  champDate.value = aujourdhui;
  champDate.addEventListener("change", charger);
  charger();
}

demarrer();
