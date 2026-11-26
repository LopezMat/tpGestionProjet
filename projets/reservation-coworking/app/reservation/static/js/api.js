// Appels à l'API selon le contrat d'architecture.md et app/docs/openapi.json.
// Lecture seule, sans connexion (DEC-011). Réutilisable par T-022 et T-023.

/** Erreur d'appel : `statut` vaut null si le réseau a échoué. */
export class ErreurApi extends Error {
  constructor(statut) {
    super("Erreur de l'API"); // jamais le message du serveur
    this.statut = statut;
  }
}

/**
 * GET /api/disponibilites?date=AAAA-MM-JJ
 * @param {string} date
 * @param {AbortSignal} [signal]
 */
export async function lireDisponibilites(date, signal) {
  let reponse;
  try {
    reponse = await fetch(`/api/disponibilites?date=${encodeURIComponent(date)}`, {
      headers: { Accept: "application/json" },
      signal,
    });
  } catch (e) {
    if (e && e.name === "AbortError") throw e;
    throw new ErreurApi(null);
  }
  if (!reponse.ok) throw new ErreurApi(reponse.status);
  try {
    return await reponse.json();
  } catch {
    throw new ErreurApi(0);
  }
}
