---
title: Choix d'un film
---

# Chosir un film

```js
const tallyUrl = "https://tally.so/r/wa6jyb";
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
    .forEach(({ id, title, original_title, production_year }) => {
      const url = `${tallyUrl}?id=${id}&original_title=${original_title}`;
      if (original_title.length > 0) {
        display(
          html`<div
            x-data="{tooltip: '${production_year} | ${original_title}'}"
          >
            <a href="${url}" x-tooltip="tooltip">${title}</a>
          </div>`
        );
      } else {
        display(
          html`<div x-data="{tooltip: '${production_year}'}">
            <a href="${url}" x-tooltip="tooltip">${title}</a>
          </div>`
        );
      }
    });
} else {
  display(
    html`Désolé, ce film n'est pas répertorié dans notre base.
      <a href="${tallyUrl}">Aller au questionnaire</a>`
  );
}
```

</div>

<a href="./">Retour</a>
