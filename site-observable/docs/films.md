---
title: Choix d'un film
---

# Chosir un film

```js
// Configuration
const baseTmdbImageUrl = "https://image.tmdb.org/t/p/w92";
const baseTallyUrl = "https://tally.so/r/w2e0PD";
```

Entrez le nom d'un film:

```js
const query = view(Inputs.text());
```

```js
import { SQLiteDatabaseClient } from "npm:@observablehq/sqlite";
const db = FileAttachment("data/films.sqlite").sqlite();
```

```js
const results = db.query(
  `
  SELECT
    *,
    (SELECT COUNT(*) FROM films) total
  FROM
    films
  WHERE
    films.title LIKE ? COLLATE NOCASE
    OR films.original_title LIKE ? COLLATE NOCASE
  ORDER BY
    films.title
  LIMIT
    200`,
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
    ? results.map(
        ({ id, title, original_title, production_year, poster_path }) => {
          const tallyUrl = `${baseTallyUrl}?id_tmdb=${id}&title=${encodeURIComponent(
            title
          )}&original_title=${encodeURIComponent(original_title || title)}`;
          const imageUrl = `${baseTmdbImageUrl}${poster_path}`;
          const imageHtml = html`<div
            style="width: 92px; height:138px; background-color:white; display:flex; align-items:center; justify-content: center;"
          >
            <object data="${imageUrl}">
              <img
                src="${brokenImageElement.currentSrc}"
                style="width:46x; height:46px"
              />
            </object>
          </div>`;
          if (original_title.length > 0) {
            return html`<div
              x-data="{tooltip: '${original_title}'}"
              class="card"
              style="white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 100%;"
            >
              <h2
                style="white-space: nowrap; overflow: hidden; text-overflow: ellipsis;"
              >
                ${title}
              </h2>
              <h3>${production_year}</h3>
              <a href="${tallyUrl}" x-tooltip="tooltip">${imageHtml}</a>
            </div>`;
          } else {
            return html`<div
              class="card"
              style="max-width:220px; display: flex; flex-direction: column; align-items: center; justify-content: center;"
            >
              <h2
                style="white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 100%;"
              >
                ${title}
              </h2>
              <h3>${production_year}</h3>
              <a href="${tallyUrl}">${imageHtml}</a>
            </div>`;
          }
        }
      )
    : "";
```

${display(html`<div class="grid grid-cols-4">${content}</div>`)}

Je n'ai pas trouvé le film recherché, ${html`<a href="${baseTallyUrl}">Aller au questionnaire</a>`}

<a href="./">Retour</a>

#### Crédits

broken image by Rahmat Hidayat from <a href="https://thenounproject.com/browse/icons/term/broken-image/" target="_blank" title="broken image Icons">Noun Project</a> (CC BY 3.0)
