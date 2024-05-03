---
title: Choix d'une série télévisée
toc: false
---

# Choisir une série télévisée

```js
const baseTmdbImageUrl = "https://image.tmdb.org/t/p/w92";
const baseTallyUrl = "https://tally.so/r/nP6KOB";
```

```js
import { debounce } from "./utils/debounce.js";
```

Entrez le nom d'une série télévisée:

```js
const query = view(debounce(Inputs.text(), 250));
```

```js
import { SQLiteDatabaseClient } from "npm:@observablehq/sqlite";
const db = FileAttachment("data/series.sqlite").sqlite();
```

```js
const results = db.query(
  `
  SELECT
    *,
    (SELECT COUNT(*) FROM series) total
  FROM
    series
  WHERE
    series.name LIKE ? COLLATE NOCASE OR
    series.original_name LIKE ? COLLATE NOCASE
  ORDER BY
    series.name ASC
  LIMIT 200`,
  [`%${query}%`, `%${query}%`]
);
```

```js
const brokenImageAttachment = FileAttachment(
  "images/noun-broken-image-3237447.svg"
).image({ style: "width:46x; height:46px" });
```

```js
const brokenImageElement = html`${brokenImageAttachment}`;
```

```js
import { html } from "npm:htl";
import Alpine from "npm:alpinejs";
import Tooltip from "npm:@ryangjchandler/alpine-tooltip";

Alpine.plugin(Tooltip);

window.Alpine = Alpine;
window.Alpine.start();
```

```js
const content =
  results.length > 0
    ? results.map(({ id, name, original_name, poster_path }) => {
        const tallyUrl = `${baseTallyUrl}?id_tmdb=${id}&name=${encodeURIComponent(
          name
        )}&original_name=${encodeURIComponent(original_name || name)}`;
        const imageUrl = `${baseTmdbImageUrl}${poster_path}`;
        const imageHtml = html`<div
          style="height:138px; background-color:white; display:flex; align-items:center; justify-content: center;"
        >
          <object data="${imageUrl}">
            <img
              src="${brokenImageElement.currentSrc}"
              style="width:46x; height:46px"
            />
          </object>
        </div>`;
        if (original_name.length > 0) {
          return html`<div
            x-data="{tooltip: '${original_name.replace(/'/g, "\\'")}'}"
            class="card"
            style="max-width:220px; display: flex; flex-direction: column; align-items: center; justify-content: center;"
          >
            <h2
              style="white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 100%;"
            >
              ${name}
            </h2>
            <a href="${tallyUrl}" x-tooltip="tooltip" style="width:92px"
              >${imageHtml}</a
            >
          </div>`;
        } else {
          return html`<div
            x-data="{tooltip: '${name.replace(/'/g, "\\'")}'}"
            class="card"
            style="max-width:220px; display: flex; flex-direction: column; align-items: center; justify-content: center;"
          >
            <h2
              style="white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 100%;"
            >
              ${name}
            </h2>
            <a href="${tallyUrl}" x-tooltip="tooltip" style="width:92px"
              >${imageHtml}</a
            >
          </div>`;
        }
      })
    : "";
```

${display(html`<div class="grid grid-cols-4">${content}</div>`)}

Je n'ai pas trouvé la série recherchée, ${html`<a href="${baseTallyUrl}">Aller au questionnaire</a>`}

<a href="./">Retour</a>

#### Crédits

broken image by Rahmat Hidayat from <a href="https://thenounproject.com/browse/icons/term/broken-image/" target="_blank" title="broken image Icons">Noun Project</a> (CC BY 3.0)
