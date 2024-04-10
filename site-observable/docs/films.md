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
  `SELECT * FROM films WHERE films.title LIKE ? COLLATE NOCASE ORDER BY films.title`,
  [`${query}%`]
);
```

```js
import { html } from "npm:htl";
import Alpine from "npm:alpinejs";
import Tooltip from "npm:@ryangjchandler/alpine-tooltip";

Alpine.plugin(Tooltip);

window.Alpine = Alpine;
window.Alpine.start();
```

${results.length} films trouvés:

```js
if (results.length > 0) {
  results
    .slice(0, 20)
    .forEach(({ id, title, original_title, production_year, poster_path }) => {
      const tallyUrl = `${baseTallyUrl}?id=${id}&original_title=${original_title}`;
      const imageUrl = `${baseTmdbImageUrl}${poster_path}`;
      if (original_title.length > 0) {
        display(
          html`<div
            x-data="{tooltip: '${production_year} | ${original_title}'}"
            class="card"
            style="max-width:220px; display: flex; flex-direction: column; align-items: center; justify-content: center;"
          >
            <h2>${title}</h2>
            <a href="${tallyUrl}" x-tooltip="tooltip"
              ><img src="${imageUrl}"
            /></a>
          </div>`
        );
      } else {
        display(
          html`<div
            x-data="{tooltip: '${production_year}'}"
            class="card"
            style="max-width:220px; display: flex; flex-direction: column; align-items: center; justify-content: center;"
          >
            <h2>${title}</h2>
            <a href="${tallyUrl}" x-tooltip="tooltip"
              ><img src="${imageUrl}"
            /></a>
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
