---
title: Choix d'un film
---

# Chosir un film

```js
// Configuration
const baseTmdbImageUrl = "https://image.tmdb.org/t/p/w92";
const baseTallyUrl = "https://tally.so/r/wa6jyb";
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
    20`,
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

${results.length > 0 ? results[0].total : 0} films trouvés:

```js
if (results.length > 0) {
  results
    .slice(0, 20)
    .forEach(({ id, title, original_title, production_year, poster_path }) => {
      const tallyUrl = `${baseTallyUrl}?id=${id}&original_title=${
        original_title || title
      }`;
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
        display(
          html`<div
            x-data="{tooltip: '${original_title}'}"
            class="card"
            style="max-width:220px; display: flex; flex-direction: column; align-items: center; justify-content: center;"
          >
            <h2>${title}</h2>
            <h3>${production_year}</h3>
            <a href="${tallyUrl}" x-tooltip="tooltip">${imageHtml}</a>
          </div>`
        );
      } else {
        display(
          html`<div
            class="card"
            style="max-width:220px; display: flex; flex-direction: column; align-items: center; justify-content: center;"
          >
            <h2>${title}</h2>
            <h3>${production_year}</h3>
            <a href="${tallyUrl}">${imageHtml}</a>
          </div>`
        );
      }
    });
} else {
  display(
    html`Désolé, ce film n'est pas répertorié dans notre base.
      <a href="${baseTallyUrl}">Aller au questionnaire</a>`
  );
}
```

</div>

<a href="./">Retour</a>

#### Crédits

broken image by Rahmat Hidayat from <a href="https://thenounproject.com/browse/icons/term/broken-image/" target="_blank" title="broken image Icons">Noun Project</a> (CC BY 3.0)
