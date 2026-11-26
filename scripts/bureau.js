/* bureau.js : rendu Canvas 2D de la page « Le bureau » de la console (DEC-016). Responsable : D.
 *
 * Copié tel quel dans console/assets/ par scripts/console.py. Les données viennent du bloc
 * <script type="application/json" id="donnees-bureau"> écrit par scripts/bureau.py : aucune ressource
 * externe, fonctionne en file:// et hors ligne. Tout est dessiné par le code (pixel art 16 bits) : aucun
 * sprite, aucune police ni image externe. Seule exception, le mode Direct (DEC-018) : quand la page est
 * servie par scripts/bureau_direct.py sur 127.0.0.1, il ouvre le flux SSE relatif « direct/flux » (même
 * origine) ; en file://, il reste désactivé.
 *
 * Sécurité : les textes venus des fichiers ne passent que par textContent et fillText ; jamais d'insertion
 * de HTML. Les liens sont revalidés (chemin relatif .html de la console) avant d'être utilisés.
 * Accessibilité : prefers-reduced-motion respecté (aucun déplacement animé, aucun clignotement) ; les
 * listes texte de la page sont l'alternative au dessin et suivent le replay.
 */
(function () {
  "use strict";

  var source = document.getElementById("donnees-bureau");
  var canvas = document.getElementById("b-canvas");
  if (!source || !canvas || !canvas.getContext) { return; }
  var D;
  try { D = JSON.parse(source.textContent); } catch (err) { return; }

  function $(id) { return document.getElementById(id); }
  var cadre = $("b-cadre"), fiche = $("b-fiche"), annonce = $("b-annonce");
  var ctx = canvas.getContext("2d");

  // ------------------------------------------------------------------ utilitaires
  var RE_LIEN = /^[A-Za-z0-9][A-Za-z0-9\/_.%-]*\.html(#[A-Za-z0-9_-]+)?$/;
  function lienSur(h) { return typeof h === "string" && RE_LIEN.test(h) && h.indexOf("..") === -1 ? h : null; }
  function tronquer(t, n) {
    t = String(t || "").replace(/\s+/g, " ").trim();
    return t.length <= n ? t : t.slice(0, n - 1).replace(/\s+$/, "") + "…";
  }
  function el(tag, classe, texte) {
    var n = document.createElement(tag);
    if (classe) { n.className = classe; }
    if (texte !== undefined && texte !== null) { n.textContent = String(texte); }
    return n;
  }
  function vider(n) { while (n.firstChild) { n.removeChild(n.firstChild); } }
  function assombrir(hex, f) {
    var m = /^#([0-9a-f]{6})$/i.exec(hex || "");
    if (!m) { return "#333333"; }
    var v = parseInt(m[1], 16), r = (v >> 16) & 255, g = (v >> 8) & 255, b = v & 255;
    function c(x) { x = Math.max(0, Math.min(255, Math.round(x * (1 - f)))); return ("0" + x.toString(16)).slice(-2); }
    return "#" + c(r) + c(g) + c(b);
  }
  function eclaircir(hex, f) {
    var m = /^#([0-9a-f]{6})$/i.exec(hex || "");
    if (!m) { return "#cccccc"; }
    var v = parseInt(m[1], 16), r = (v >> 16) & 255, g = (v >> 8) & 255, b = v & 255;
    function c(x) { x = Math.round(x + (255 - x) * f); return ("0" + x.toString(16)).slice(-2); }
    return "#" + c(r) + c(g) + c(b);
  }

  var mq = window.matchMedia ? window.matchMedia("(prefers-reduced-motion: reduce)") : null;
  var reduit = !!(mq && mq.matches);

  // ------------------------------------------------------------------ plan
  var P = D.plan, T = P.tuile, LW = P.largeur * T, LH = P.hauteur * T;
  var pieces = {}, postes = {}, persos = {}, ordre = [];
  P.pieces.forEach(function (p) { pieces[p.id] = p; });
  P.postes.forEach(function (p) { postes[p.id] = p; });
  D.personnages.forEach(function (d) {
    var po = postes[d.poste] || { x: 24, y: 14, piece: "couloir", bureau: false };
    persos[d.id] = { d: d, poste: po, x: po.x, y: po.y, chemin: [], v: 7, dir: "haut", etat: "cafe",
                     bulle: null, marque: false, cafe: null, maison: true };
    ordre.push(d.id);
  });
  function projetParSlug(slug) {
    for (var i = 0; i < D.projets.length; i++) { if (D.projets[i].slug === slug) { return D.projets[i]; } }
    return D.projets[0];
  }
  function pieceEn(x, y) {
    for (var i = 0; i < P.pieces.length; i++) {
      var p = P.pieces[i];
      if (x >= p.x && x < p.x + p.l && y >= p.y && y < p.y + p.h) { return p; }
    }
    return null;
  }

  // ------------------------------------------------------------------ déplacements
  function chemin(a, b) {
    var pa = pieceEn(a.x + 0.5, a.y + 0.5), pb = pieceEn(b.x + 0.5, b.y + 0.5), R = P.rang_couloir, pts = [];
    if (pa && pb && pa.id === pb.id) { return [{ x: b.x, y: a.y }, { x: b.x, y: b.y }]; }
    if (pa && pa.porte) { pts.push({ x: pa.porte.x, y: a.y }); pts.push({ x: pa.porte.x, y: R }); }
    else { pts.push({ x: a.x, y: R }); }
    if (pb && pb.porte) { pts.push({ x: pb.porte.x, y: R }); pts.push({ x: pb.porte.x, y: b.y }); }
    else { pts.push({ x: b.x, y: R }); }
    pts.push({ x: b.x, y: b.y });
    return pts;
  }
  function aller(p, dest, duree) {
    if (!dest) { return; }
    if (reduit || duree === 0) {
      p.x = dest.x; p.y = dest.y; p.chemin = []; p.dir = dest.dir || p.dir; redessiner = true;
      return;
    }
    if (Math.abs(p.x - dest.x) < 0.01 && Math.abs(p.y - dest.y) < 0.01 && !p.chemin.length) {
      p.dir = dest.dir || p.dir; return;
    }
    p.chemin = chemin({ x: p.x, y: p.y }, dest);
    p.chemin[p.chemin.length - 1].dir = dest.dir;
    var lg = 0, px = p.x, py = p.y;
    p.chemin.forEach(function (q) { lg += Math.abs(q.x - px) + Math.abs(q.y - py); px = q.x; py = q.y; });
    p.v = Math.max(7, duree ? lg / duree : 7);
  }
  function avancer(p, dt) {
    var reste = p.v * dt;
    while (p.chemin.length && reste > 0) {
      var q = p.chemin[0], dx = q.x - p.x, dy = q.y - p.y, d = Math.abs(dx) + Math.abs(dy);
      if (Math.abs(dx) > 0.001) { p.dir = dx > 0 ? "droite" : "gauche"; }
      else if (Math.abs(dy) > 0.001) { p.dir = dy > 0 ? "bas" : "haut"; }
      if (d <= reste) {
        p.x = q.x; p.y = q.y; reste -= d; p.chemin.shift();
        if (!p.chemin.length && q.dir) { p.dir = q.dir; }
      } else {
        var k = reste / d; p.x += dx * k; p.y += dy * k; reste = 0;
      }
    }
  }
  function placeCafe(p) {
    if (p.cafe === null) {
      var prises = {};
      ordre.forEach(function (id) { if (persos[id].cafe !== null) { prises[persos[id].cafe] = true; } });
      for (var i = 0; i < P.cafe.length; i++) { if (!prises[i]) { p.cafe = i; break; } }
      if (p.cafe === null) { p.cafe = 0; }
    }
    var c = P.cafe[p.cafe];
    return { x: c.x, y: c.y, dir: "bas" };
  }
  function aLAccueil(d) {
    return d.nature === "coordinateur" || d.nature === "humain" || d.nature === "visiteur";
  }
  function domicile(p) {
    // Le coordinateur, les membres humains de l'équipe projet et les visiteurs restent à l'accueil ;
    // les autres vont au café.
    if (aLAccueil(p.d)) {
      p.cafe = null; return { x: p.poste.x, y: p.poste.y, dir: p.d.nature === "coordinateur" ? "haut" : "bas" };
    }
    return placeCafe(p);
  }
  function auPoste(p) {
    p.cafe = null;
    return { x: p.poste.x, y: p.poste.y, dir: p.poste.bureau ? "haut" : "bas" };
  }
  var DECALAGES = [[1.15, 0], [-1.15, 0], [1.15, 0.9], [-1.15, 0.9], [0, 1.3], [0.6, 1.6]];
  function aCote(cibleId, k) {
    var c = persos[cibleId], o = DECALAGES[k % DECALAGES.length];
    return { x: c.poste.x + o[0], y: c.poste.y + o[1], dir: o[0] > 0 ? "gauche" : (o[0] < 0 ? "droite" : "haut") };
  }

  // ------------------------------------------------------------------ pixel art : personnages
  var TEINTS = ["#f6d5b8", "#e3b088", "#b97d53", "#7b4b2e"];
  var CHEVEUX = ["#2b1d14", "#5a3a1e", "#a0522d", "#d6a84a", "#8d8d8d", "#1d2340"];
  var ICONES = {
    "loupe": [".kkk..", "kbwbk.", "kwbbk.", "kbbbk.", ".kkkn.", "....nn"],
    "coche": ["......", ".....g", "....gg", "g..gg.", "gggg..", ".gg..."],
    "bouclier": ["kkkkkk", "krrwrk", "krwwrk", "krrwrk", ".krrk.", "..kk.."],
    "fusee": ["...w..", "..wbw.", "..wbw.", ".rwwwr", ".r.o.r", "...y.."],
    "portable": [".kkkk.", ".kbbk.", ".kbbk.", ".kkkk.", "ssssss", "......"],
    "palette": [".nnnn.", "nrnybn", "nnnnnn", "ngnpnn", ".nnn..", "......"],
    "plans": ["......", "bbbbbw", "bwbwbw", "bbbbbw", "......", "......"],
    "bloc-notes": [".kkkk.", ".wwww.", ".wkkw.", ".wwww.", ".wkkw.", ".wwww."],
    "presse-papiers": ["..kk..", "nwwwwn", "nwkkwn", "nwwwwn", "nwkkwn", "nnnnnn"],
    "longue-vue": [".....s", "....ss", "...nn.", "..nn..", ".nn...", "k....."],
    "courbe": ["wwwwww", "wwwwgw", "wwwgww", "wgwgww", "wwgwww", "kkkkkk"],
    "tampon": ["..nn..", "..nn..", ".nnnn.", "rrrrrr", "......", "......"],
    "tasse": ["......", "wwww..", "wwwwww", "wwww.w", "wwwww.", ".ww..."],
    "talkie": [".k....", ".k....", "kkkk..", "krrk..", "kssk..", "kkkk.."]
  };
  var COULEURS_ICONES = { k: "#1f2430", w: "#f8fafc", b: "#60a5fa", g: "#16a34a", r: "#dc2626", y: "#facc15",
                          o: "#f97316", p: "#a855f7", n: "#8b5a2b", s: "#cbd5e1" };
  // Icônes d'activité du mode Direct (7 × 7), dessinées au-dessus du personnage.
  var ICONES_ACT = {
    lit: ["kkkkkkk", "kbbkbbk", "kbbkbbk", "kbbkbbk", "kbbkbbk", "kkkkkkk", "...k..."],
    tape: ["......k", ".....ky", "....kyk", "...kyk.", "..kyk..", ".kok...", "kk....."],
    terminal: ["kkkkkkk", "kkkkkkk", "kgkkkkk", "kkgkkkk", "kgkkkkk", "kkkkggk", "kkkkkkk"],
    web: ["..bbb..", ".bgbbb.", "bggbbgb", "bbgbggb", "bbbbggb", ".bbbgb.", "..bbb.."]
  };
  var cacheSprites = {};

  function pix(c, x, y, w, h, coul) { c.fillStyle = coul; c.fillRect(x, y, w, h); }

  function dessinerSprite(c, d, dir, image, pose) {
    var peau = TEINTS[d.teint % TEINTS.length], chev = CHEVEUX[d.cheveux % CHEVEUX.length];
    var haut = d.couleur || "#64748b", hautS = assombrir(haut, 0.35), hautC = eclaircir(haut, 0.25);
    var bas = d.nature === "salarie" ? "#3f3f46" : "#334155", contour = "#1b1b24";
    var marche = pose === "marche", tape = pose === "tape";
    var g = marche && image % 2 === 1 ? 1 : 0, dr = marche && image % 2 === 0 && image > 0 ? 1 : 0;
    if (marche && image === 3) { g = 0; dr = 1; }
    if (marche && image === 1) { g = 1; dr = 0; }
    var lat = dir === "gauche" || dir === "droite";
    // ombre
    c.fillStyle = "rgba(0,0,0,0.28)"; c.fillRect(3, 22, 10, 2); c.fillRect(4, 21, 8, 1);
    // jambes et chaussures
    if (lat) {
      pix(c, 6, 17, 4, 4 - g, contour); pix(c, 7, 17, 2, 3 - g, bas);
      pix(c, 6 + (dir === "droite" ? 1 : -1) * (g ? 1 : 0), 21 - g, 4, 1, contour);
    } else {
      pix(c, 4, 17, 4, 5 - g, contour); pix(c, 5, 17, 2, 4 - g, bas);
      pix(c, 8, 17, 4, 5 - dr, contour); pix(c, 9, 17, 2, 4 - dr, bas);
    }
    // corps
    var bx = lat ? 5 : 4, bw = lat ? 6 : 8;
    pix(c, bx - 1, 10, bw + 2, 8, contour);
    pix(c, bx, 10, bw, 7, haut);
    pix(c, bx, 10, bw, 1, hautC);
    pix(c, bx, 16, bw, 1, hautS);
    if (d.nature === "salarie") { pix(c, bx + 1, 11, 2, 2, "#fef3c7"); }          // badge
    if (d.nature === "coordinateur") { pix(c, 7, 11, 2, 5, "#e2e8f0"); }          // chemise et cravate
    // bras
    if (lat) {
      var bxBras = dir === "droite" ? 7 : 7, osc = marche ? (image % 2 ? 1 : -1) : 0;
      pix(c, bxBras - 1, 11, 3, 5, contour); pix(c, bxBras, 11, 1, 4, hautS);
      pix(c, bxBras + osc * 0, 15, 1, 1, peau);
    } else if (tape) {
      var leve = image % 2;
      pix(c, 2, 10, 2, 5, contour); pix(c, 12, 10, 2, 5, contour);
      pix(c, 3, 10 - leve, 1, 4, hautS); pix(c, 12, 10 - (1 - leve), 1, 4, hautS);
      pix(c, 3, 9 - leve, 1, 1, peau); pix(c, 12, 9 - (1 - leve), 1, 1, peau);
    } else {
      var a1 = marche ? (image === 1 ? -1 : (image === 3 ? 1 : 0)) : 0;
      pix(c, 2, 11 + a1, 2, 6, contour); pix(c, 12, 11 - a1, 2, 6, contour);
      pix(c, 3, 11 + a1, 1, 4, hautS); pix(c, 12, 11 - a1, 1, 4, hautS);
      pix(c, 3, 15 + a1, 1, 1, peau); pix(c, 12, 15 - a1, 1, 1, peau);
    }
    // tête
    var hx = lat ? (dir === "droite" ? 5 : 3) : 4;
    pix(c, hx - 1, 1, 10, 10, contour);
    pix(c, hx, 2, 8, 8, peau);
    pix(c, hx, 9, 8, 1, assombrir(peau, 0.15));
    // cheveux
    if (dir === "haut") {
      pix(c, hx, 1, 8, 8, chev); pix(c, hx + 1, 2, 6, 1, eclaircir(chev, 0.25));
    } else {
      pix(c, hx, 1, 8, 3, chev); pix(c, hx + 1, 1, 5, 1, eclaircir(chev, 0.25));
      if (d.coiffure === 1) { pix(c, hx, 4, 1, 4, chev); pix(c, hx + 7, 4, 1, 4, chev); }
      if (d.coiffure === 2) { pix(c, hx, 4, 1, 2, chev); pix(c, hx + 7, 4, 1, 2, chev); pix(c, hx + 2, 4, 3, 1, chev); }
      if (lat) { pix(c, dir === "droite" ? hx : hx + 6, 4, 2, 3, chev); }
    }
    // visage
    if (dir === "bas") {
      pix(c, hx + 2, 5, 1, 2, "#1b1b24"); pix(c, hx + 5, 5, 1, 2, "#1b1b24");
      pix(c, hx + 3, 8, 2, 1, assombrir(peau, 0.3));
    } else if (lat) {
      pix(c, dir === "droite" ? hx + 6 : hx + 1, 5, 1, 2, "#1b1b24");
    }
    // accessoires de tête
    if (d.accessoire === "casque") {
      pix(c, hx - 1, 2, 10, 1, "#1f2430"); pix(c, hx - 1, 3, 1, 4, "#1f2430"); pix(c, hx + 8, 3, 1, 4, "#1f2430");
      if (dir === "bas") { pix(c, hx + 6, 7, 2, 1, "#1f2430"); }
    }
    if (d.accessoire === "gyrophare") { pix(c, hx + 2, 0, 4, 2, "#dc2626"); pix(c, hx + 3, 0, 1, 1, "#fecaca"); }
    // objet tenu
    var ic = ICONES[d.accessoire];
    if (ic && dir !== "haut") {
      var ox = dir === "gauche" ? 0 : 10, oy = 12;
      for (var y = 0; y < ic.length; y++) {
        for (var x = 0; x < ic[y].length; x++) {
          var ch = ic[y].charAt(x);
          if (ch !== ".") { pix(c, ox + x, oy + y, 1, 1, COULEURS_ICONES[ch] || "#000"); }
        }
      }
    }
  }
  function sprite(d, dir, image, pose) {
    var cle = d.id + "|" + dir + "|" + image + "|" + pose;
    var s = cacheSprites[cle];
    if (!s) {
      s = document.createElement("canvas"); s.width = 16; s.height = 24;
      var c = s.getContext("2d");
      if (dir === "gauche") { c.translate(16, 0); c.scale(-1, 1); dessinerSprite(c, d, "droite", image, pose); }
      else { dessinerSprite(c, d, dir, image, pose); }
      cacheSprites[cle] = s;
    }
    return s;
  }

  // ------------------------------------------------------------------ pixel art : décor
  var SOLS = { reunion: ["#bdb6d3", "#b3abca"], chef: ["#caa47c", "#c09a72"], supervision: ["#a3b2c2", "#99a9b9"],
               serveur: ["#9ea5b0", "#959ca8"], couloir: ["#d8d4cb", "#d0ccc2"], openspace: ["#dcbc92", "#d3b388"],
               salaries: ["#aac6a2", "#a0bd98"], cafe: ["#ebdfca", "#dccbb0"] };
  var decor = document.createElement("canvas"); decor.width = LW; decor.height = LH;
  var scene = document.createElement("canvas"); scene.width = LW; scene.height = LH;
  var dc = decor.getContext("2d"), sc = scene.getContext("2d");

  function plante(c, x, y) {
    pix(c, x + 4, y + 9, 8, 6, "#9a5b34"); pix(c, x + 4, y + 9, 8, 1, "#b8743f");
    pix(c, x + 3, y + 2, 10, 7, "#2f855a"); pix(c, x + 5, y, 6, 4, "#38a169"); pix(c, x + 6, y + 3, 2, 2, "#68d391");
  }
  function ecran(c, x, y, couleur) {
    pix(c, x, y, 12, 9, "#1f2430"); pix(c, x + 1, y + 1, 10, 6, couleur || "#3b82f6"); pix(c, x + 5, y + 9, 2, 2, "#1f2430");
  }
  function bureau(c, po) {
    var x = Math.round((po.x - 0.5) * T), y = Math.round((po.y - 1) * T + 3);
    pix(c, x, y + 11, 32, 3, "rgba(0,0,0,0.18)");
    pix(c, x, y, 32, 12, "#6b4423"); pix(c, x + 1, y, 30, 10, "#9c6b3c"); pix(c, x + 1, y, 30, 2, "#b98450");
    ecran(c, x + 10, y - 6, "#2563eb");
    pix(c, x + 24, y + 4, 5, 3, "#e2e8f0");               // papiers
    // chaise
    pix(c, x + 11, y + 15, 10, 4, "#374151"); pix(c, x + 12, y + 15, 8, 2, "#4b5563");
  }
  function dessinerDecor() {
    var c = dc;
    pix(c, 0, 0, LW, LH, "#1f2430");
    P.pieces.forEach(function (p) {
      var s = SOLS[p.type] || SOLS.couloir;
      for (var ty = p.y; ty < p.y + p.h; ty++) {
        for (var tx = p.x; tx < p.x + p.l; tx++) {
          pix(c, tx * T, ty * T, T, T, s[(tx + ty) % 2]);
          if (p.type === "openspace" || p.type === "chef") { pix(c, tx * T, ty * T + 7, T, 1, "rgba(0,0,0,0.06)"); }
          if (p.type === "serveur") { pix(c, tx * T, ty * T, T, 1, "rgba(0,0,0,0.1)"); pix(c, tx * T, ty * T, 1, T, "rgba(0,0,0,0.1)"); }
        }
      }
    });
    P.pieces.forEach(function (p) {
      if (p.type === "couloir") { return; }
      var x0 = p.x * T, y0 = p.y * T, w = p.l * T, h = p.h * T;
      // mur du haut (face visible), avec la porte pour les pièces du bas
      pix(c, x0, y0, w, T, "#5b6478"); pix(c, x0, y0, w, 3, "#7d879c"); pix(c, x0, y0 + T - 2, w, 2, "#3f4656");
      pix(c, x0, y0 + 3, w, 2, p.couleur);
      // murs latéraux
      pix(c, x0, y0, 3, h, "#3f4656"); pix(c, x0 + w - 3, y0, 3, h, "#3f4656");
      if (p.porte) {
        var px0 = p.porte.x * T;
        if (p.y < P.rang_couloir) {
          pix(c, x0, y0 + h - 4, w, 4, "#3f4656");
          pix(c, px0, y0 + h - 4, 2 * T, 4, (SOLS[p.type] || SOLS.couloir)[0]);
        } else {
          pix(c, px0, y0, 2 * T, T, (SOLS.couloir)[0]);
          pix(c, px0, y0, 2, T, "#3f4656"); pix(c, px0 + 2 * T - 2, y0, 2, T, "#3f4656");
        }
      } else if (p.y < P.rang_couloir) {
        pix(c, x0, y0 + h - 4, w, 4, "#3f4656");
      }
      mobilier(c, p);
    });
    // accueil du couloir
    var cl = pieces.couloir;
    if (cl) {
      pix(c, 21 * T, 12 * T + 4, 6 * T, 3 * T - 8, "#b45309"); pix(c, 21 * T + 3, 12 * T + 7, 6 * T - 6, 3 * T - 14, "#d97706");
      plante(c, 1 * T, 11 * T + 2); plante(c, 46 * T, 11 * T + 2);
    }
    P.postes.forEach(function (po) { if (po.bureau) { bureau(c, po); } });
  }
  function mobilier(c, p) {
    var x0 = p.x * T, y0 = p.y * T, w = p.l * T;
    if (p.type === "reunion") {
      pix(c, x0 + 2 * T, y0 + 4, 4 * T, 9, "#f8fafc");               // tableau blanc
      pix(c, x0 + 2 * T + 4, y0 + 6, 20, 1, "#2563eb"); pix(c, x0 + 2 * T + 4, y0 + 9, 30, 1, "#dc2626");
      pix(c, x0 + 3 * T, y0 + 2 * T, 6 * T, 2 * T, "#5b3a1e"); pix(c, x0 + 3 * T + 2, y0 + 2 * T + 2, 6 * T - 4, 2 * T - 5, "#8b5a2b");
      pix(c, x0 + 5 * T, y0 + 2 * T + 9, 12, 8, "#f1f5f9");          // documents sur la table
      plante(c, x0 + (p.l - 2) * T, y0 + T);
    } else if (p.type === "chef") {
      pix(c, x0 + 2 * T, y0 + 3, 6 * T, 11, "#f8fafc");              // Gantt mural
      var barres = [["#22c55e", 4, 20], ["#3b82f6", 18, 26], ["#8b5cf6", 34, 22], ["#f59e0b", 50, 30]];
      barres.forEach(function (b, i) { pix(c, x0 + 2 * T + b[1], y0 + 5 + i * 2, b[2], 1, b[0]); });
      pix(c, x0 + (p.l - 3) * T, y0 + T, 2 * T, T + 6, "#64748b"); pix(c, x0 + (p.l - 3) * T + 2, y0 + T + 4, 2 * T - 4, 2, "#94a3b8");
      plante(c, x0 + T, y0 + T);
    } else if (p.type === "supervision") {
      for (var i = 0; i < 4; i++) { ecran(c, x0 + T + i * 2.5 * T, y0 + 3, "#0f172a"); }
      pix(c, x0 + T, y0 + T + 2, (p.l - 2) * T, 8, "#475569");
    } else if (p.type === "serveur") {
      for (var r = 0; r < 4; r++) {
        var rx = x0 + T + r * 2.5 * T;
        pix(c, rx, y0 + 2, 28, 2 * T - 2, "#111827"); pix(c, rx + 2, y0 + 4, 24, 2 * T - 6, "#1f2937");
        for (var k = 0; k < 4; k++) { pix(c, rx + 3, y0 + 7 + k * 6, 22, 1, "#374151"); }
      }
      pix(c, x0 + (p.l - 2) * T, y0 + 3, 12, 11, "#f8fafc");          // affiche « fusée »
      pix(c, x0 + (p.l - 2) * T + 5, y0 + 4, 2, 7, "#dc2626"); pix(c, x0 + (p.l - 2) * T + 4, y0 + 10, 4, 2, "#f59e0b");
    } else if (p.type === "openspace") {
      pix(c, x0 + 2 * T, y0 + 3, 5 * T, 10, "#f8fafc");
      pix(c, x0 + 2 * T + 4, y0 + 6, 40, 1, "#0d9488"); pix(c, x0 + 2 * T + 4, y0 + 9, 26, 1, "#334155");
      plante(c, x0 + (p.l - 2) * T, y0 + T); plante(c, x0 + T, y0 + (p.h - 2) * T);
      pix(c, x0 + 9 * T, y0 + T, 10, 18, "#bfdbfe"); pix(c, x0 + 9 * T + 2, y0 + T + 2, 6, 6, "#e0f2fe");  // fontaine
    } else if (p.type === "salaries") {
      for (var b = 0; b < 3; b++) {
        pix(c, x0 + (2 + b * 2) * T, y0 + 2, 2 * T - 2, T + 4, "#7c4a21");
        pix(c, x0 + (2 + b * 2) * T + 2, y0 + 5, 2 * T - 6, 4, ["#dc2626", "#2563eb", "#16a34a"][b]);
        pix(c, x0 + (2 + b * 2) * T + 2, y0 + 12, 2 * T - 6, 4, ["#f59e0b", "#7c3aed", "#0d9488"][b]);
      }
      plante(c, x0 + (p.l - 2) * T, y0 + T);
    } else if (p.type === "cafe") {
      pix(c, x0 + T, y0 + T, 5 * T, T + 4, "#78350f"); pix(c, x0 + T, y0 + T, 5 * T, 3, "#a16207");
      pix(c, x0 + T + 6, y0 + 2, 14, 18, "#1f2937"); pix(c, x0 + T + 9, y0 + 6, 8, 4, "#ef4444");   // machine à café
      pix(c, x0 + T + 26, y0 + T + 2, 5, 5, "#f8fafc"); pix(c, x0 + T + 34, y0 + T + 2, 5, 5, "#f8fafc");
      pix(c, x0 + 7 * T, y0 + T, 4 * T, 2 * T - 4, "#9f1239"); pix(c, x0 + 7 * T + 3, y0 + T + 3, 4 * T - 6, T, "#be123c");
      plante(c, x0 + (p.l - 2) * T, y0 + (p.h - 2) * T);
    }
  }
  dessinerDecor();

  function animerDecor(c, t) {
    if (reduit) { return; }
    P.pieces.forEach(function (p) {
      var x0 = p.x * T, y0 = p.y * T;
      if (p.type === "serveur") {
        for (var r = 0; r < 4; r++) {
          for (var k = 0; k < 4; k++) {
            var on = Math.sin(t / 180 + r * 1.7 + k * 2.3) > 0;
            pix(c, x0 + T + r * 2.5 * T + 20, y0 + 8 + k * 6, 2, 2, on ? "#22c55e" : "#14532d");
            if ((r + k) % 3 === 0) { pix(c, x0 + T + r * 2.5 * T + 16, y0 + 8 + k * 6, 2, 2, Math.sin(t / 97 + k) > 0.6 ? "#f59e0b" : "#78350f"); }
          }
        }
      } else if (p.type === "supervision") {
        for (var i = 0; i < 4; i++) {
          var sx = x0 + T + i * 2.5 * T + 1, sy = y0 + 4;
          for (var j = 0; j < 10; j++) {
            var hh = 1 + Math.round(2.5 + 2.5 * Math.sin(t / 400 + j * 0.9 + i * 2));
            pix(c, sx + j, sy + 6 - hh, 1, 1, i === 2 ? "#f59e0b" : "#22c55e");
          }
        }
      } else if (p.type === "cafe") {
        var v = Math.floor(t / 300) % 3;
        pix(c, x0 + T + 12, y0 + 1 - v, 1, 2, "rgba(255,255,255,0.7)"); pix(c, x0 + T + 14, y0 + 2 - ((v + 1) % 3), 1, 2, "rgba(255,255,255,0.6)");
      }
    });
  }

  // ------------------------------------------------------------------ dessin principal
  var k = 1, dpr = 1, redessiner = true, survol = null, selection = null, banniere = null;

  function dimensionner() {
    dpr = window.devicePixelRatio || 1;
    var plein = document.fullscreenElement === cadre;
    var cw = plein ? window.innerWidth : Math.max(200, cadre.clientWidth - 12);
    var kk = cw / LW;
    if (plein) { kk = Math.min(kk, window.innerHeight / LH); }
    k = kk * dpr;
    canvas.width = Math.round(LW * k); canvas.height = Math.round(LH * k);
    if (plein) { canvas.style.width = Math.round(LW * kk) + "px"; canvas.style.height = Math.round(LH * kk) + "px"; }
    else { canvas.style.width = ""; canvas.style.height = ""; }
    redessiner = true;
  }

  function police(px, gras) { return (gras ? "700 " : "600 ") + Math.round(px) + "px ui-monospace, Consolas, 'Courier New', monospace"; }
  function taille() { return Math.max(10 * dpr, 4.6 * k); }

  function chevauche(r, liste) {
    for (var i = 0; i < liste.length; i++) {
      var o = liste[i];
      if (r.x < o.x + o.w && o.x < r.x + r.w && r.y < o.y + o.h && o.y < r.y + r.h) { return true; }
    }
    return false;
  }
  function bulleRect(c, x, y, texte, fond, bord, couleur, pris) {
    var fs = taille() * 0.92;
    c.font = police(fs);
    var w = c.measureText(texte).width + fs, h = fs * 1.6, bx = Math.round(x - w / 2), by = Math.round(y - h - fs * 0.5);
    bx = Math.max(2, Math.min(canvas.width - w - 2, bx));
    var r = { x: bx - 2, y: by - 2, w: w + 4, h: h + 4 }, pointe = by + h + 2;
    for (var essai = 0; essai < 6 && chevauche(r, pris); essai++) { r.y -= h + 6; }
    r.y = Math.max(2, r.y); by = r.y + 2; pris.push(r);
    c.fillStyle = bord; c.fillRect(bx - 2, by - 2, w + 4, h + 4);
    c.fillStyle = fond; c.fillRect(bx, by, w, h);
    c.fillStyle = bord; c.fillRect(Math.round(x - 1), by + h + 2, 2, Math.max(2, pointe - (by + h + 2)) + fs * 0.35);
    c.fillStyle = couleur; c.textBaseline = "middle"; c.textAlign = "left";
    c.fillText(texte, bx + fs / 2, by + h / 2 + 1);
  }
  var STYLES_BULLE = {
    bloque: ["#fee2e2", "#dc2626", "#7f1d1d"], decision: ["#fef3c7", "#b45309", "#78350f"],
    statut: ["#ede9fe", "#6d28d9", "#3b0764"], revue: ["#ede9fe", "#6d28d9", "#3b0764"],
    attente: ["#fef3c7", "#d97706", "#78350f"], attend: ["#fffbeb", "#a16207", "#713f12"],
    creation: ["#ecfeff", "#0e7490", "#164e63"], defaut: ["#ffffff", "#1f2430", "#1f2430"]
  };

  function dessiner(t) {
    sc.drawImage(decor, 0, 0);
    animerDecor(sc, t);
    var tries = ordre.slice().sort(function (a, b) { return persos[a].y - persos[b].y; });
    tries.forEach(function (id) {
      var p = persos[id], pose = "debout", image = 0;
      if (p.chemin.length && !reduit) { pose = "marche"; image = Math.floor(t / 120) % 4; }
      else if (p.etat === "tape" && p.dir === "haut" && p.poste.bureau && Math.abs(p.x - p.poste.x) < 0.05 &&
               Math.abs(p.y - p.poste.y) < 0.05) { pose = "tape"; image = reduit ? 0 : Math.floor(t / 160) % 2; }
      var dir = p.chemin.length ? p.dir : (p.dir || "bas");
      var s = sprite(p.d, dir, image, pose);
      var sx = Math.round((p.x + 0.5) * T - 8), sy = Math.round((p.y + 1) * T - 24);
      if (pose === "tape" && !reduit && image) {
        pix(sc, Math.round((p.poste.x - 0.5) * T) + 11, Math.round((p.poste.y - 1) * T + 3) - 5, 10, 6,
            Math.floor(t / 90) % 2 ? "#60a5fa" : "#3b82f6");
      }
      sc.drawImage(s, sx, sy);
    });
    ctx.imageSmoothingEnabled = false;
    ctx.drawImage(scene, 0, 0, canvas.width, canvas.height);
    calques(t);
  }

  function calques(t) {
    var c = ctx, fs = taille();
    // titres des pièces
    c.textBaseline = "top"; c.textAlign = "left";
    P.pieces.forEach(function (p) {
      if (p.type === "couloir") { return; }
      c.font = police(fs * 0.9, true);
      var tx = (p.x * T + 6) * k / 1, ty = (p.y * T + (p.y < P.rang_couloir ? T - 1 : 4)) * k;
      if (p.y >= P.rang_couloir) { ty = (p.y * T + T + 1) * k; }
      var w = c.measureText(p.titre).width + fs * 0.6;
      c.fillStyle = "rgba(15,23,42,0.72)"; c.fillRect(tx, ty, w, fs * 1.35);
      c.fillStyle = "#f8fafc"; c.fillText(p.titre, tx + fs * 0.3, ty + fs * 0.2);
    });
    c.font = police(fs * 0.85, true);
    var acc = "Accueil · coordinateur", ax = 24 * T * k - c.measureText(acc).width / 2, ay = (11 * T + 3) * k;
    c.fillStyle = "rgba(15,23,42,0.6)"; c.fillRect(ax - 4, ay, c.measureText(acc).width + 8, fs * 1.25);
    c.fillStyle = "#fff7ed"; c.fillText(acc, ax, ay + fs * 0.15);
    // étiquettes (décalées vers le bas si elles se chevauchent)
    c.font = police(fs * 0.82);
    var etiquettes = [];
    ordre.slice().sort(function (a, b) { return persos[a].y - persos[b].y || persos[a].x - persos[b].x; })
      .forEach(function (id) {
        var p = persos[id], nom = p.d.nom, w = c.measureText(nom).width;
        var cx = (p.x + 0.5) * T * k, r = { x: cx - w / 2 - 3, y: ((p.y + 1) * T + 1) * k, w: w + 6, h: fs * 1.05 };
        for (var essai = 0; essai < 4 && chevauche(r, etiquettes); essai++) { r.y += r.h + 1; }
        etiquettes.push(r);
        c.fillStyle = id === selection ? "rgba(37,99,235,0.92)" : "rgba(15,23,42,0.68)";
        c.fillRect(r.x, r.y, r.w, r.h);
        c.fillStyle = "#ffffff"; c.textBaseline = "top"; c.fillText(nom, r.x + 3, r.y + fs * 0.08);
      });
    // sélection et survol
    [selection, survol].forEach(function (id, i) {
      if (!id || !persos[id]) { return; }
      var p = persos[id];
      c.strokeStyle = i === 0 ? "#2563eb" : "#f8fafc"; c.lineWidth = Math.max(2, k * 0.6);
      c.strokeRect(((p.x + 0.5) * T - 10) * k, ((p.y + 1) * T - 26) * k, 20 * k, 27 * k);
    });
    // bulles et « ! »
    var cligno = reduit ? true : Math.floor(t / 450) % 2 === 0, bulles = etiquettes.slice();
    ordre.forEach(function (id) {
      var p = persos[id], cx = (p.x + 0.5) * T * k, haut = ((p.y + 1) * T - 25) * k;
      if (p.marque) {
        var m = fs * 1.6;
        if (cligno) {
          c.fillStyle = "#1f2430"; c.fillRect(cx - m / 2 - 2, haut - m * 1.25 - 2, m + 4, m + 4);
          c.fillStyle = "#facc15"; c.fillRect(cx - m / 2, haut - m * 1.25, m, m);
          c.fillStyle = "#1f2430"; c.font = police(m * 0.9, true); c.textAlign = "center"; c.textBaseline = "middle";
          c.fillText("!", cx, haut - m * 0.75 + 1); c.textAlign = "left";
        }
        haut -= m * 1.4;
      }
      if (p.bulle && p.bulle.texte) {
        var st = STYLES_BULLE[p.bulle.type] || STYLES_BULLE.defaut;
        bulleRect(c, cx, haut, p.bulle.texte, st[0], st[1], st[2], bulles);
      }
      // icône d'activité du mode Direct, à droite de la tête
      if (etat.mode === "direct" && p.act && ICONES_ACT[p.act.cat]) {
        var ic = ICONES_ACT[p.act.cat], u = Math.max(2, Math.round(k * 1.5)), w = ic.length * u;
        var ix = Math.round(cx + 7 * k), iy = Math.round(((p.y + 1) * T - 22) * k) - w;
        c.fillStyle = "#1f2430"; c.fillRect(ix - u - 1, iy - u - 1, w + 2 * u + 2, w + 2 * u + 2);
        c.fillStyle = "#f8fafc"; c.fillRect(ix - u, iy - u, w + 2 * u, w + 2 * u);
        for (var yy = 0; yy < ic.length; yy++) {
          for (var xx = 0; xx < ic[yy].length; xx++) {
            var chi = ic[yy].charAt(xx);
            if (chi !== ".") { c.fillStyle = COULEURS_ICONES[chi] || "#000"; c.fillRect(ix + xx * u, iy + yy * u, u, u); }
          }
        }
      }
    });
    // bannière de décision
    if (banniere && (reduit || t < banniere.fin)) {
      c.font = police(fs * 1.25, true);
      var bw = c.measureText(banniere.texte).width + fs * 2, bh = fs * 2.4, bx = (canvas.width - bw) / 2, by = fs;
      c.fillStyle = "#78350f"; c.fillRect(bx - 3, by - 3, bw + 6, bh + 6);
      c.fillStyle = "#fde68a"; c.fillRect(bx, by, bw, bh);
      c.fillStyle = "#f59e0b"; c.fillRect(bx, by + bh - 4, bw, 4);
      c.fillStyle = "#78350f"; c.textAlign = "center"; c.textBaseline = "middle";
      c.fillText(banniere.texte, canvas.width / 2, by + bh / 2); c.textAlign = "left";
    } else if (banniere && !reduit && t >= banniere.fin) { banniere = null; }
  }

  // ------------------------------------------------------------------ état de la page
  var etat = { projet: null, mode: "instantane" };
  var selProjet = $("b-projet");

  function projetCourant() { return projetParSlug(etat.projet); }

  function libelleEtat(e) { return (D.etats && D.etats[e]) || e; }

  function texteCourt(i) {
    var ids = i.tickets.filter(function (x) { return x.role === i.etat; }).map(function (x) { return x.id; });
    var base = tronquer(ids.join(" "), 22);
    return { tape: base, revue: base + " · revue", bloque: base + " · bloqué", attend: base + " · attend",
             attente: base + " · à décider" }[i.etat] || base;
  }

  function appliquerInstantane(immediat) {
    var pr = projetCourant(), parId = {}, aCoteDe = {};
    (pr.instantane || []).forEach(function (i) { parId[i.perso] = i; });
    ordre.forEach(function (id) { persos[id].cafe = null; });
    ordre.forEach(function (id) {
      var p = persos[id], i = parId[id];
      p.etat = i ? i.etat : "cafe"; p.marque = !!(i && i.etat === "attente");
      p.bulle = i && i.etat !== "cafe" ? { texte: texteCourt(i), type: i.etat === "tape" ? "defaut" : i.etat } : null;
      var dest;
      if (!i || i.etat === "cafe") { dest = domicile(p); }
      else if (i.etat === "revue" && i.cible && persos[i.cible]) {
        aCoteDe[i.cible] = (aCoteDe[i.cible] || 0) + 1; p.cafe = null; dest = aCote(i.cible, aCoteDe[i.cible] - 1);
      } else { dest = auPoste(p); }
      aller(p, dest, immediat ? 0 : undefined);
    });
    banniere = null;
    resume();
    redessiner = true;
  }

  function resume() {
    var n = { tape: 0, revue: 0, attente: 0, bloque: 0, cafe: 0 };
    if (etat.mode === "instantane") {
      (projetCourant().instantane || []).forEach(function (i) { if (n[i.etat] !== undefined) { n[i.etat]++; } });
      canvas.setAttribute("aria-label", "Vue de dessus du bureau, " + projetCourant().libelle + " : " + n.tape +
        " au travail, " + n.revue + " en revue, " + n.attente + " décision(s) humaine(s) attendue(s), " + n.bloque +
        " bloqué(s). Détail dans la liste « Personnages et état ».");
    } else if (etat.mode === "direct") {
      var actifs = ordre.filter(function (id) { return persos[id].d.nature === "agent" && DR.instances[id]; })
        .map(function (id) { return persos[id].d.nom; });
      canvas.setAttribute("aria-label", "Bureau en direct : " + sessionsActives() + " session(s) de coordinateur, " +
        (actifs.length ? "agents au travail : " + actifs.join(", ") : "aucun agent au travail") +
        ". Détail dans la liste « Derniers événements (direct) ».");
    } else {
      canvas.setAttribute("aria-label", "Replay du bureau, " + projetCourant().libelle +
        ". Détail dans la liste « Événements du replay ».");
    }
  }

  // ------------------------------------------------------------------ fiche
  function ligneFiche(dl, terme, valeur) {
    if (valeur === null || valeur === undefined || valeur === "") { return; }
    dl.appendChild(el("dt", null, terme));
    var dd = el("dd");
    if (typeof valeur === "string") { dd.textContent = valeur; } else { dd.appendChild(valeur); }
    dl.appendChild(dd);
  }
  function afficherFiche(id) {
    var p = persos[id];
    if (!p || !fiche) { return; }
    var d = p.d;
    vider(fiche);
    var h = el("h3"), pastille = el("span", "b-pastille");
    pastille.style.background = d.couleur;
    h.appendChild(pastille); h.appendChild(document.createTextNode(d.nom));
    fiche.appendChild(h);
    var nature = { agent: "Agent IA", salarie: "Salarié", coordinateur: "Coordinateur",
      humain: "Membre de l'équipe projet", visiteur: "Visiteur" }[d.nature] || d.nature;
    fiche.appendChild(el("p", "meta", nature + (d.systeme && d.systeme !== "salarie" && d.systeme !== "visiteur" &&
      d.systeme !== "humain" && d.systeme !== "coordinateur" ? " · " + (d.systeme === "realisation" ? "pôle réalisation" : d.systeme === "autres" ? "hors catalogue" : d.systeme) : "")));
    fiche.appendChild(el("p", null, d.role));
    var dl = el("dl");
    ligneFiche(dl, "Modèle", d.modele);
    ligneFiche(dl, d.nature === "salarie" ? "Compétences" : "Outils", (d.outils || []).join(", "));
    var i = null;
    (projetCourant().instantane || []).forEach(function (x) { if (x.perso === id) { i = x; } });
    if (etat.mode === "instantane") {
      ligneFiche(dl, "État (" + projetCourant().libelle + ")", libelleEtat(i ? i.etat :
        (aLAccueil(d) ? "accueil" : "cafe")));
    } else if (etat.mode === "direct") {
      ligneFiche(dl, "En direct", texteActivite(p));
    } else if (p.bulle && p.bulle.texte) {
      ligneFiche(dl, "Dernière action du replay", p.bulle.long || p.bulle.texte);
    }
    if (i && i.tickets.length) {
      var ul = el("ul");
      i.tickets.forEach(function (tk) {
        var li = el("li"), href = lienSur(tk.page);
        if (href) { var a = el("a", null, tk.id); a.href = href; li.appendChild(a); }
        else { li.appendChild(document.createTextNode(tk.id)); }
        li.appendChild(document.createTextNode(" " + tk.statut + " · " + tronquer(tk.titre, 70)));
        ul.appendChild(li);
      });
      ligneFiche(dl, "Tickets en cours", ul);
    } else {
      ligneFiche(dl, "Tickets en cours", "aucun");
    }
    fiche.appendChild(dl);
    if (d.description) {
      var det = el("details"); det.appendChild(el("summary", null, "Description complète"));
      det.appendChild(el("p", "meta", d.description)); fiche.appendChild(det);
    }
    var href = lienSur(d.page);
    if (href) {
      var pl = el("p", "plus"), a = el("a", null, d.nature === "salarie" ? "Fiche dans l'équipe →" :
        d.nature === "agent" ? "Page de l'agent →" : "Voir la page →");
      a.href = href; pl.appendChild(a); fiche.appendChild(pl);
    }
  }

  // ------------------------------------------------------------------ replay
  var R = { liste: [], i: -1, lecture: false, vitesse: 1, prochain: 0, actif: {} };
  var liEvenements = {}, olEvenements = $("b-evenements"), courantLi = null;
  if (olEvenements) {
    Array.prototype.forEach.call(olEvenements.querySelectorAll("li[data-n]"), function (li) {
      liEvenements[li.getAttribute("data-n")] = li;
    });
  }
  function jalonsSeulement() { var c = $("b-jalons"); return !c || c.checked; }
  function construireListe() {
    var slug = etat.projet, jal = jalonsSeulement();
    R.liste = D.evenements.filter(function (ev) {
      return (slug === "_esn" || ev.projet === slug) && (!jal || ev.jalon);
    });
    filtrerListes();
    var cur = $("b-curseur");
    if (cur) { cur.max = String(Math.max(0, R.liste.length - 1)); }
  }
  function filtrerListes() {
    var slug = etat.projet, jal = jalonsSeulement();
    Object.keys(liEvenements).forEach(function (n) {
      var li = liEvenements[n], ok = (slug === "_esn" || li.getAttribute("data-projet") === slug) &&
        (!jal || li.getAttribute("data-jalon") === "1");
      li.classList.toggle("b-masque", !ok);
    });
    Array.prototype.forEach.call(document.querySelectorAll(".b-etats"), function (b) {
      b.classList.toggle("b-masque", b.getAttribute("data-projet") !== slug);
    });
  }
  function periode() {
    var n = R.liste.length || 1, base = Math.min(2.0, Math.max(0.35, 90 / n));
    if (reduit) { base = Math.max(base, 1.2); }
    return base / R.vitesse;
  }
  function reinitialiserReplay() {
    R.actif = {}; banniere = null;
    ordre.forEach(function (id) { var p = persos[id]; p.cafe = null; p.bulle = null; p.marque = false; p.etat = "cafe"; });
    ordre.forEach(function (id) { var p = persos[id], d = domicile(p); p.x = d.x; p.y = d.y; p.dir = d.dir; p.chemin = []; });
  }
  function nomDe(id) { return persos[id] ? persos[id].d.nom : id; }
  function appliquerEvenement(ev, idx, anime) {
    var p = persos[ev.perso];
    if (!p) { return; }
    var duree = anime ? periode() * 0.7 : 0, dest;
    R.actif[ev.perso] = idx;
    if (ev.type === "decision") {
      var places = P.reunion || [], c = places.length ? places[idx % places.length] : p.poste;
      p.cafe = null; dest = { x: c.x, y: c.y, dir: "haut" };
      p.etat = "decision";
      if (anime || idx === R.i) {
        banniere = { texte: "✔ " + (ev.dec || "") + " · décidé par " + nomDe(ev.perso) + (ev.valide ? " · VALIDÉ" : ""),
                     fin: performance.now() + 2200 };
      }
    } else if (ev.statut === "EN_REVUE" && p.d.systeme === "realisation" && persos["agent:relecteur-code"]) {
      p.cafe = null; dest = aCote("agent:relecteur-code", 0); p.etat = "revue";
    } else {
      dest = auPoste(p);
      p.etat = ev.statut === "BLOQUE" ? "bloque" : (ev.statut === "ATTENTE_HUMAIN" ? "attend" : "tape");
    }
    aller(p, dest, duree);
    var texte = (ev.ticket ? ev.ticket + " · " : "") + ev.texte;
    if (ev.type === "decision") { texte = ev.texte; }
    var type = ev.type === "statut" ? (ev.statut === "BLOQUE" ? "bloque" : "statut") : ev.type;
    p.bulle = { texte: tronquer(texte, 40), long: texte, type: type === "travail" ? "defaut" : type, n: idx };
    // Les personnages inactifs depuis 8 événements retournent au café (ou à l'accueil).
    Object.keys(R.actif).forEach(function (id) {
      if (idx - R.actif[id] > 8) {
        var q = persos[id]; q.bulle = null; q.etat = "cafe"; delete R.actif[id]; aller(q, domicile(q), duree);
      } else if (persos[id].bulle && idx - persos[id].bulle.n > 3) { persos[id].bulle = null; }
    });
  }
  function allerA(i, anime) {
    if (!R.liste.length) { majHorloge(); return; }
    i = Math.max(0, Math.min(R.liste.length - 1, i));
    var reprise = i !== R.i + 1 || R.i < 0;
    if (reprise) {
      reinitialiserReplay();
      for (var j = 0; j < i; j++) { appliquerEvenement(R.liste[j], j, false); }
    }
    R.i = i;
    appliquerEvenement(R.liste[i], i, anime && !reduit);
    majHorloge();
    majListe();
    redessiner = true;
  }
  function majHorloge() {
    var h = $("b-horloge"), cur = $("b-curseur"), ev = R.liste[R.i];
    if (cur) { cur.value = String(Math.max(0, R.i)); }
    if (h) {
      h.textContent = ev ? (ev.date + " " + (ev.sans_heure ? "--:--" : (ev.estimee ? "~" : "") + ev.heure) + " · " +
        (R.i + 1) + " / " + R.liste.length) : "aucun événement pour ce choix";
    }
    var b = $("b-lecture");
    if (b) { b.textContent = R.lecture ? "❚❚ Pause" : "▶ Lecture"; b.setAttribute("aria-label", R.lecture ? "Pause" : "Lecture"); }
  }
  function majListe() {
    if (courantLi) { courantLi.removeAttribute("aria-current"); }
    var ev = R.liste[R.i];
    courantLi = ev ? liEvenements[String(ev.n)] : null;
    if (courantLi && olEvenements) {
      courantLi.setAttribute("aria-current", "true");
      olEvenements.scrollTop = Math.max(0, courantLi.offsetTop - olEvenements.clientHeight / 2);
    }
  }
  function annoncer(texte) { if (annonce) { annonce.textContent = texte; } }
  function annoncerEvenement() {
    var ev = R.liste[R.i];
    if (ev) { annoncer(ev.date + " " + ev.heure + ", " + nomDe(ev.perso) + " : " + (ev.ticket ? ev.ticket + ", " : "") + ev.texte); }
  }
  function lecture(on) {
    R.lecture = on && R.liste.length > 0;
    if (R.lecture && R.i >= R.liste.length - 1) { allerA(0, false); }
    R.prochain = performance.now() + periode() * 1000;
    majHorloge();
    annoncer(R.lecture ? "Lecture du replay : " + R.liste.length + " événements." :
      "Pause à l'événement " + (R.i + 1) + " sur " + R.liste.length + ".");
  }

  // ------------------------------------------------------------------ mode Direct (DEC-018)
  // Disponible seulement quand la page est servie par scripts/bureau_direct.py (127.0.0.1) : en file://,
  // le bouton reste désactivé. Flux SSE relatif (même origine) ; les textes ne passent que par textContent.
  var DIRECT_DISPO = location.protocol === "http:" &&
    (location.hostname === "127.0.0.1" || location.hostname === "localhost") && typeof window.EventSource === "function";
  var TYPES_DIRECT = { session_debut: 1, demande: 1, outil_debut: 1, outil_fin: 1, autorisation: 1, attente: 1,
                       agent_debut: 1, agent_fin: 1, fin_tour: 1, session_fin: 1 };
  var RE_ACTEUR = /^[a-z0-9][a-z0-9-]{0,39}$/, RE_COURT = /^[A-Za-z0-9_:.+-]{0,40}$/;
  var LIB_CATEGORIE = { lit: "lit", tape: "écrit", terminal: "terminal", delegue: "lance un agent", web: "cherche sur le web",
                        autre: "outil" };
  var LIB_ATTENTE = { permission_prompt: "attend une autorisation", idle_prompt: "attend une réponse",
                      elicitation_dialog: "attend une saisie" };
  var FENETRE_SESSION = 15 * 60 * 1000, RECENT = 10000, MIN_ACT = 1200, MAX_ACT = 120000;
  var DR = { source: null, pret: false, sessions: {}, instances: {}, vus: {}, nVus: 0, annonce: 0, controle: 0 };
  var olDirect = $("b-direct-liste");

  function evValide(ev) {
    return ev && typeof ev === "object" && TYPES_DIRECT[ev.evenement] === 1 && typeof ev.ts === "string" &&
      typeof ev.session === "string" && RE_COURT.test(ev.session) && typeof ev.acteur === "string" &&
      RE_ACTEUR.test(ev.acteur) && RE_COURT.test(String(ev.outil || "")) && RE_COURT.test(String(ev.categorie || "")) &&
      RE_COURT.test(String(ev.detail || "")) && RE_COURT.test(String(ev.instance || ""));
  }
  function persoDirect(acteur) {
    if (acteur === "coordinateur") { return "coordinateur"; }
    return persos["agent:" + acteur] ? "agent:" + acteur : null;
  }
  function bulleDirect(p, texte, type, ms, anime) {
    if (!anime) { return; }
    p.bulle = { texte: texte, type: type, expire: performance.now() + ms, long: texte };
  }
  function texteDirect(ev) {
    switch (ev.evenement) {
      case "demande": return "nouvelle demande";
      case "outil_debut": return (LIB_CATEGORIE[ev.categorie] || "outil") + " (" + ev.outil + ")";
      case "outil_fin": return "échec de " + ev.outil;
      case "autorisation": return "attend une autorisation (" + ev.outil + ")";
      case "attente": return LIB_ATTENTE[ev.detail] || "attend";
      case "agent_debut": return "agent lancé";
      case "agent_fin": return "agent terminé";
      case "fin_tour": return "fin du tour";
      case "session_debut": return "session ouverte" + (ev.detail ? " (" + ev.detail + ")" : "");
      case "session_fin": return "session fermée";
    }
    return ev.evenement;
  }
  function ajouterListeDirect(ev, id) {
    if (!olDirect || (ev.evenement === "outil_fin" && ev.detail !== "echec")) { return; }
    var li = el("li", "ev ev-" + ev.evenement), heure = /T(\d{2}:\d{2}:\d{2})/.exec(ev.ts);
    li.appendChild(el("time", null, heure ? heure[1] : "--:--:--"));
    li.appendChild(document.createTextNode(" "));
    li.appendChild(el("strong", null, id ? nomDe(id) : ev.acteur + " (hors catalogue)"));
    li.appendChild(document.createTextNode(" " + texteDirect(ev)));
    olDirect.insertBefore(li, olDirect.firstChild);
    while (olDirect.childNodes.length > 30) { olDirect.removeChild(olDirect.lastChild); }
  }
  function annoncerDirect(ev, id, anime) {
    var marquant = { demande: 1, agent_debut: 1, autorisation: 1, attente: 1, fin_tour: 1 };
    var t = performance.now();
    if (!anime || !marquant[ev.evenement] || t - DR.annonce < 3000) { return; }
    DR.annonce = t;
    annoncer("Direct : " + (id ? nomDe(id) : ev.acteur) + ", " + texteDirect(ev) + ".");
  }
  function activite(p, cat, tsMs, recent) {
    var maintenant = performance.now();
    if (!recent || !ICONES_ACT[cat]) { return; }
    p.act = { cat: cat, ts: tsMs, depuis: maintenant, fin: tsMs <= (p.dernierFin || 0) };
    if (p.d.nature === "agent") { p.etat = cat === "tape" ? "tape" : "poste"; }
  }
  function sessionsActives() {
    var n = 0, t = Date.now();
    Object.keys(DR.sessions).forEach(function (s) {
      var x = DR.sessions[s];
      if (!x.fin && t - x.dernier < FENETRE_SESSION) { n++; }
    });
    return n;
  }
  function controlerSessions() {
    var n = sessionsActives(), al = $("b-direct-alerte"), sp = $("b-direct-sessions");
    if (al) { al.hidden = n < 2; }
    if (sp) { sp.textContent = n + " session(s) de coordinateur active(s) · 15 dernières minutes"; }
    if (etat.mode === "direct") { resume(); }
  }
  function rentrer(p, anime) {
    p.act = null; p.marque = false; p.bulle = null; p.etat = "cafe";
    aller(p, domicile(p), anime ? undefined : 0);
  }
  function appliquerDirect(ev, anime) {
    var tsMs = Date.parse(ev.ts) || Date.now(), recent = Date.now() - tsMs < RECENT;
    var s = DR.sessions[ev.session] || (DR.sessions[ev.session] = { dernier: 0, fin: false });
    s.dernier = Math.max(s.dernier, tsMs);
    if (ev.evenement === "session_fin") { s.fin = true; } else { s.fin = false; }
    var id = persoDirect(ev.acteur), p = id ? persos[id] : null, coord = persos.coordinateur;
    var duree = anime ? undefined : 0;
    switch (ev.evenement) {
      case "demande":
        if (p) { p.marque = false; bulleDirect(p, "nouvelle demande", "creation", 4000, anime || recent); }
        break;
      case "outil_debut":
        if (p) {
          p.marque = false;
          if (p.d.nature === "agent" && !DR.instances[id]) { DR.instances[id] = {}; aller(p, auPoste(p), duree); }
          activite(p, ev.categorie, tsMs, anime || recent);
          if (ev.categorie === "delegue") { bulleDirect(p, "lance un agent", "creation", 3000, anime || recent); }
        }
        break;
      case "outil_fin":
        if (p) {
          p.marque = false;
          p.dernierFin = Math.max(p.dernierFin || 0, tsMs);
          if (p.act && tsMs >= p.act.ts) { p.act.fin = true; }
          if (ev.detail === "echec") { bulleDirect(p, "échec", "bloque", 1500, anime || recent); }
        }
        break;
      case "autorisation":
      case "attente":
        if (p) { p.marque = true; bulleDirect(p, texteDirect(ev), "attente", 6000, anime || recent); }
        break;
      case "agent_debut":
        if (p) {
          var inst = DR.instances[id] || (DR.instances[id] = {});
          inst[ev.instance || "?"] = true;
          p.etat = "poste"; p.marque = false;
          aller(p, auPoste(p), duree);
          bulleDirect(p, "au travail", "creation", 2500, anime || recent);
        }
        if (coord) { bulleDirect(coord, "lance " + ev.acteur, "creation", 3000, anime || recent); }
        break;
      case "agent_fin":
        if (p) {
          var ins = DR.instances[id] || {};
          delete ins[ev.instance || "?"];
          if (!Object.keys(ins).length) { delete DR.instances[id]; rentrer(p, anime); }
        }
        break;
      case "fin_tour":
        if (p) { p.act = null; p.marque = false; aller(p, domicile(p), duree); bulleDirect(p, "tour terminé", "defaut", 2500, anime || recent); }
        break;
      case "session_debut":
        if (p) { bulleDirect(p, "session ouverte", "defaut", 2500, anime || recent); }
        break;
      case "session_fin":
        if (!sessionsActives()) {
          DR.instances = {};
          ordre.forEach(function (pid) { rentrer(persos[pid], anime); });
        }
        break;
    }
    ajouterListeDirect(ev, id);
    annoncerDirect(ev, id, anime);
    redessiner = true;
  }
  function majConnexion(connecte, texte) {
    var b = $("b-direct-etat");
    if (!b) { return; }
    b.textContent = connecte ? "● connecté" : "○ " + (texte || "déconnecté");
    b.classList.toggle("b-connecte", !!connecte);
  }
  function connecterDirect() {
    if (DR.source || !DIRECT_DISPO || etat.mode !== "direct") { return; }
    DR.pret = false;
    majConnexion(false, "connexion…");
    var es = new EventSource("direct/flux");
    DR.source = es;
    es.onopen = function () { majConnexion(true); };
    es.addEventListener("pret", function () { DR.pret = true; controlerSessions(); redessiner = true; });
    es.addEventListener("evenement", function (m) {
      if (m.lastEventId) {
        if (DR.vus[m.lastEventId]) { return; }
        if (DR.nVus > 5000) { DR.vus = {}; DR.nVus = 0; }
        DR.vus[m.lastEventId] = true; DR.nVus++;
      }
      var ev;
      try { ev = JSON.parse(m.data); } catch (err) { return; }
      if (evValide(ev)) { appliquerDirect(ev, DR.pret); }
    });
    es.onerror = function () {
      DR.pret = false;
      if (es.readyState === 2) {           // fermé : nouvelle tentative dans 5 s
        majConnexion(false, "déconnecté, nouvelle tentative…");
        es.close(); DR.source = null;
        window.setTimeout(connecterDirect, 5000);
      } else {
        majConnexion(false, "déconnecté, reconnexion…");
      }
    };
  }
  function fermerDirect() {
    if (DR.source) { DR.source.close(); DR.source = null; }
    ordre.forEach(function (id) { persos[id].act = null; });
  }
  function entrerDirect() {
    reinitialiserReplay();
    DR.sessions = {}; DR.instances = {}; DR.vus = {}; DR.nVus = 0;
    ordre.forEach(function (id) { persos[id].act = null; persos[id].dernierFin = 0; });
    if (olDirect) { vider(olDirect); }
    controlerSessions();
    connecterDirect();
  }
  function entretenirDirect() {
    var t = performance.now(), change = false;
    ordre.forEach(function (id) {
      var p = persos[id];
      if (p.bulle && p.bulle.expire && t >= p.bulle.expire) { p.bulle = null; change = true; }
      if (p.act && ((p.act.fin && t - p.act.depuis >= MIN_ACT) || t - p.act.depuis >= MAX_ACT)) {
        p.act = null; change = true;
        if (p.d.nature === "agent" && p.etat === "tape") { p.etat = "poste"; }
      }
    });
    if (t - DR.controle > 1000) { DR.controle = t; controlerSessions(); }
    if (change) { redessiner = true; }
  }
  function texteActivite(p) {
    if (p.marque) { return "attend une autorisation ou une réponse"; }
    if (p.act) { return LIB_CATEGORIE[p.act.cat] || "au travail"; }
    if (p.d.nature === "agent" && DR.instances[p.d.id]) { return "à son poste"; }
    return aLAccueil(p.d) ? "à l'accueil" : "au café";
  }

  // ------------------------------------------------------------------ modes et commandes
  function lireHash() {
    var res = {};
    (location.hash || "").replace(/^#/, "").split("&").forEach(function (kv) {
      var i = kv.indexOf("=");
      if (i > 0) { try { res[kv.slice(0, i)] = decodeURIComponent(kv.slice(i + 1)); } catch (err) { /* ignoré */ } }
    });
    return res;
  }
  function ecrireHash() {
    try { history.replaceState(null, "", "#projet=" + encodeURIComponent(etat.projet) + "&mode=" + etat.mode); }
    catch (err) { /* file:// selon le navigateur */ }
  }
  function changerMode(mode, immediat) {
    if (mode === "direct" && !DIRECT_DISPO) { mode = "instantane"; }
    var avant = etat.mode;
    etat.mode = mode;
    var bi = $("b-mode-instantane"), br = $("b-mode-replay"), bd = $("b-mode-direct"), zone = $("b-replay");
    if (bi) { bi.setAttribute("aria-pressed", String(mode === "instantane")); }
    if (br) { br.setAttribute("aria-pressed", String(mode === "replay")); }
    if (bd) { bd.setAttribute("aria-pressed", String(mode === "direct")); }
    if (zone) { zone.hidden = mode !== "replay"; }
    if ($("b-direct")) { $("b-direct").hidden = mode !== "direct"; }
    if ($("b-direct-evenements")) { $("b-direct-evenements").hidden = mode !== "direct"; }
    if (selProjet) { selProjet.disabled = mode === "direct"; }
    R.lecture = false;
    if (avant === "direct" && mode !== "direct") { fermerDirect(); }
    if (mode === "instantane") {
      appliquerInstantane(immediat);
      if (courantLi) { courantLi.removeAttribute("aria-current"); courantLi = null; }
    } else if (mode === "direct") {
      if (courantLi) { courantLi.removeAttribute("aria-current"); courantLi = null; }
      if (avant !== "direct" || !DR.source) { entrerDirect(); }
    } else {
      construireListe(); R.i = -1; allerA(0, false); annoncerEvenement();
    }
    resume();
    if (selection) { afficherFiche(selection); }
    ecrireHash();
  }
  function changerProjet(slug) {
    etat.projet = projetParSlug(slug).slug;
    if (selProjet) { selProjet.value = etat.projet; }
    construireListe();
    changerMode(etat.mode);
  }

  if (selProjet) { selProjet.addEventListener("change", function () { changerProjet(selProjet.value); }); }
  if ($("b-mode-instantane")) { $("b-mode-instantane").addEventListener("click", function () { changerMode("instantane"); }); }
  if ($("b-mode-replay")) { $("b-mode-replay").addEventListener("click", function () { changerMode("replay"); }); }
  if ($("b-mode-direct")) {
    var aide = $("b-direct-aide");
    if (DIRECT_DISPO) {
      $("b-mode-direct").disabled = false;
      $("b-mode-direct").addEventListener("click", function () { changerMode("direct"); });
      if (aide) { aide.textContent = "Mode Direct disponible : la page est servie par le serveur local."; aide.classList.add("b-dispo"); }
    } else if (aide) {
      aide.insertBefore(document.createTextNode("Mode Direct désactivé ici (page ouverte sans le serveur local). "),
        aide.firstChild);
    }
  }
  if ($("b-lecture")) { $("b-lecture").addEventListener("click", function () { lecture(!R.lecture); }); }
  if ($("b-prec")) { $("b-prec").addEventListener("click", function () { R.lecture = false; allerA(R.i - 1, false); annoncerEvenement(); }); }
  if ($("b-suiv")) { $("b-suiv").addEventListener("click", function () { R.lecture = false; allerA(R.i + 1, true); annoncerEvenement(); }); }
  if ($("b-vitesse")) {
    $("b-vitesse").addEventListener("change", function () { R.vitesse = parseFloat($("b-vitesse").value) || 1; });
  }
  if ($("b-curseur")) {
    $("b-curseur").addEventListener("input", function () { R.lecture = false; allerA(parseInt($("b-curseur").value, 10) || 0, false); });
    $("b-curseur").addEventListener("change", annoncerEvenement);
  }
  if ($("b-jalons")) {
    $("b-jalons").addEventListener("change", function () {
      var n = R.liste[R.i] ? R.liste[R.i].n : -1;
      construireListe();
      var idx = 0;
      R.liste.forEach(function (ev, j) { if (ev.n <= n) { idx = j; } });
      if (etat.mode === "replay") { R.i = -1; allerA(idx, false); }
    });
  }
  if ($("b-plein") && cadre.requestFullscreen) {
    $("b-plein").addEventListener("click", function () {
      if (document.fullscreenElement) { document.exitFullscreen(); } else { cadre.requestFullscreen().catch(function () {}); }
    });
    document.addEventListener("fullscreenchange", dimensionner);
  } else if ($("b-plein")) { $("b-plein").hidden = true; }
  Array.prototype.forEach.call(document.querySelectorAll(".b-perso"), function (b) {
    b.addEventListener("click", function () {
      selection = b.getAttribute("data-perso"); afficherFiche(selection); redessiner = true;
      if (fiche && fiche.scrollIntoView) { fiche.scrollIntoView({ block: "nearest", behavior: reduit ? "auto" : "smooth" }); }
    });
  });

  function persoSous(ev) {
    var r = canvas.getBoundingClientRect();
    var x = (ev.clientX - r.left) / r.width * LW, y = (ev.clientY - r.top) / r.height * LH, trouve = null;
    ordre.forEach(function (id) {
      var p = persos[id], cx = (p.x + 0.5) * T, pied = (p.y + 1) * T;
      if (x >= cx - 8 && x <= cx + 8 && y >= pied - 24 && y <= pied) { trouve = id; }
    });
    return trouve;
  }
  canvas.addEventListener("mousemove", function (ev) {
    var id = persoSous(ev);
    if (id !== survol) {
      survol = id; canvas.style.cursor = id ? "pointer" : "default"; redessiner = true;
      if (id) { afficherFiche(id); } else if (selection) { afficherFiche(selection); }
    }
  });
  canvas.addEventListener("mouseleave", function () { survol = null; redessiner = true; if (selection) { afficherFiche(selection); } });
  canvas.addEventListener("click", function (ev) {
    var id = persoSous(ev);
    selection = id || null; redessiner = true;
    if (id) { afficherFiche(id); }
  });

  if (mq) {
    var surChangement = function () { reduit = mq.matches; redessiner = true; };
    if (mq.addEventListener) { mq.addEventListener("change", surChangement); } else if (mq.addListener) { mq.addListener(surChangement); }
  }
  if (window.ResizeObserver) { new ResizeObserver(dimensionner).observe(cadre); }
  else { window.addEventListener("resize", dimensionner); }

  // ------------------------------------------------------------------ boucle
  var avant = performance.now();
  function boucle(t) {
    var dt = Math.min(0.1, (t - avant) / 1000), bouge = false;
    avant = t;
    ordre.forEach(function (id) { if (persos[id].chemin.length) { avancer(persos[id], dt); bouge = true; } });
    if (etat.mode === "replay" && R.lecture && t >= R.prochain) {
      if (R.i >= R.liste.length - 1) { lecture(false); }
      else { allerA(R.i + 1, true); R.prochain = t + periode() * 1000; }
    }
    if (etat.mode === "direct") { entretenirDirect(); }
    if (!reduit || bouge || redessiner || (banniere && t < banniere.fin)) {
      dessiner(t);
      redessiner = false;
    }
    window.requestAnimationFrame(boucle);
  }

  // ------------------------------------------------------------------ démarrage
  var h = lireHash();
  etat.projet = projetParSlug(h.projet || (selProjet ? selProjet.value : D.projets[0].slug)).slug;
  if (selProjet) { selProjet.value = etat.projet; }
  if (h.jalons === "0" && $("b-jalons")) { $("b-jalons").checked = false; }
  dimensionner();
  construireListe();
  ordre.forEach(function (id) { var p = persos[id], d = domicile(p); p.x = d.x; p.y = d.y; p.dir = d.dir; });
  changerMode(h.mode === "replay" ? "replay" : (h.mode === "direct" ? "direct" : "instantane"), true);
  if (h.mode === "replay" && h.ev) { allerA(parseInt(h.ev, 10) || 0, false); }
  if (h.perso && persos[h.perso]) { selection = h.perso; afficherFiche(h.perso); }
  window.requestAnimationFrame(boucle);
}());
