# TRB — The Red Button

A tiny universe behind one red button. Press it. See what happens.

A single-page WebGL game (three.js) that installs like an app on Android and iPhone and works offline.

## Publish it on GitHub Pages

1. Create an **empty public repository named `trb`** on GitHub (no README, no licence, nothing).
2. From this folder:

   ```bash
   git init
   git add .
   git commit -m "TRB: first release"
   git branch -M main
   git remote add origin https://github.com/nztdev/trb.git
   git push -u origin main
   ```

3. On GitHub: **Settings → Pages → Build and deployment → Source: Deploy from a branch → Branch: `main` / `(root)` → Save.**
4. After a minute it is live at **https://nztdev.github.io/trb/**

(If your GitHub username is not `nztdev`, replace it in the commands and in the URL.)

## Install it as an app

- **Android (Chrome):** open the URL → menu **⋮ → Install app** (or tap the install banner).
- **iPhone / iPad (Safari):** open the URL → **Share → Add to Home Screen**. It must be Safari; other iOS browsers can't install web apps.
- **Desktop (Chrome / Edge):** click the install icon in the address bar.

Open it once while online. After that it loads from the phone itself and works offline.

Good to know:
- On iPhone, the installed app keeps its **own save data**, separate from Safari. Progress in Safari does not carry over.
- Location is asked once, in-game, and stays on the device.
- The first tap on the black screen starts the sound (phones block audio until you touch the screen).

## Shipping an update

1. Change `index.html` (or anything else).
2. In `sw.js`, bump the version: `const V = 'trb-v2';`
3. Commit and push. Phones pick the new version up the next time the app is opened online (sometimes on the second launch).

## Structure

```
trb/
├── index.html               the whole game
├── manifest.webmanifest     app name, colours, icons  (what makes it installable)
├── sw.js                    service worker            (what makes it work offline)
├── .nojekyll                tells GitHub Pages to serve files as they are
├── icons/                   app icons (any, maskable, iOS, favicon, SVG)
├── splash/                  iOS launch screens (portrait iPhones)
├── vendor/                  three.js r128 (+ licence)
├── fonts/                   Bricolage Grotesque woff2 (+ licence)
└── tools/make_icons.py      regenerates icons and launch screens
```

## Testing the install setup

In Chrome on a computer: open the live URL → DevTools (F12) → **Application** tab →
**Manifest** (check the icons load, no warnings) and **Service Workers** (should say *activated*).
Lighthouse → *Progressive Web App* gives a full report.

## Debug panel

The small **debug** button (bottom right) shows frames per second, graphics card and game state, and has shortcuts:
*reset world, jump: sky, sky: night, jump: space, depart now, to planets, toggle low quality, clear location*.
