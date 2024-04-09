---
title: Choix d'une série télévisée
---

# Choisir une série télévisée

```js
const tallyUrl = "https://tally.so/r/w48jMo";
```

Entrez le nom d'une série télévisée:

```js
const query = view(Inputs.text());
```

```js
import { SQLiteDatabaseClient } from "npm:@observablehq/sqlite";
const db = FileAttachment("data/shows.sqlite").sqlite();
```

```js
const results = db.query(
  `SELECT * FROM shows WHERE shows.name LIKE ? COLLATE NOCASE`,
  [`${query}%`]
);
```

```js
import { html } from "npm:htl";
```

${results.length} séries trouvées:

```js
if (results.length > 0) {
  results
    .slice(0, 20)
    .forEach(({ id, name, original_name, production_countries }) => {
      const url = `${tallyUrl}?id=${id}&original_name=${original_name}`;
      if (original_name.length > 0) {
        display(html`<a href="${url}">${name} | ${original_name}</a><br />`);
      } else {
        display(html`<a href="${url}">${name}</a><br />`);
      }
    });
} else {
  display(
    html`Désolé, cette série n'est pas répertoriée dans notre base.
      <a href="${tallyUrl}">Aller au questionnaire</a>`
  );
}
```

</div>

<a href="./">Retour</a>
