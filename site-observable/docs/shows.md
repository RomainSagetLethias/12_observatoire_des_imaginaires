---
title: Choix d'une série télévisée
---

# Choisir une série télévisée

```js
const baseTmdbImageUrl = "https://image.tmdb.org/t/p/w92";
const baseTallyUrl = "https://tally.so/r/w48jMo";
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
  `SELECT *, (SELECT COUNT(*) FROM shows) total FROM shows WHERE shows.name LIKE ? COLLATE NOCASE ORDER BY shows.name ASC LIMIT 20`,
  [`%${query}%`]
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

${results.length > 0 ? results[0].total : 0} séries trouvées:

```js
if (results.length > 0) {
  results.slice(0, 20).forEach(({ id, name, original_name, poster_path }) => {
    const tallyUrl = `${baseTallyUrl}?id=${id}&original_name=${
      original_name || name
    }`;
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
      display(html`<div
        x-data="{tooltip: '${original_name}'}"
        class="card"
        style="max-width:220px; display: flex; flex-direction: column; align-items: center; justify-content: center;"
      >
        <h2>${name}</h2>
        <a href="${tallyUrl}" x-tooltip="tooltip" style="width:92px"
          >${imageHtml}</a
        >
      </div>`);
    } else {
      display(
        html`<div
          class="card"
          style="max-width:220px; display: flex; flex-direction: column; align-items: center; justify-content: center;"
        >
          <h2>${name}</h2>
          <a href="${tallyUrl}" style="width:92px">${imageHtml}</a>
        </div>`
      );
    }
  });
} else {
  display(
    html`Désolé, cette série n'est pas répertoriée dans notre base.
      <a href="${baseTallyUrl}">Aller au questionnaire</a>`
  );
}
```

</div>

<a href="./">Retour</a>

#### Crédits

broken image by Rahmat Hidayat from <a href="https://thenounproject.com/browse/icons/term/broken-image/" target="_blank" title="broken image Icons">Noun Project</a> (CC BY 3.0)
