/* Keep the academic content available when JavaScript is disabled. */
const skipLink = document.querySelector('.skip-link');
if (skipLink) document.body.prepend(skipLink);
const mainContent = document.querySelector('main.content');
if (mainContent) mainContent.setAttribute('tabindex', '-1');

document.querySelectorAll('[data-print]').forEach((button) => {
  button.hidden = false;
  button.addEventListener('click', () => window.print());
});

const publicationSearch = document.querySelector('[data-publication-search]');
if (publicationSearch) {
  const controls = document.querySelector('[data-publication-controls]');
  const entries = [...document.querySelectorAll('.publication-entry')];
  const status = document.querySelector('[data-publication-status]');
  const empty = document.querySelector('[data-publication-empty]');
  controls.hidden = false;
  publicationSearch.addEventListener('input', () => {
    const terms = publicationSearch.value.trim().toLocaleLowerCase().split(/\s+/).filter(Boolean);
    let visible = 0;
    entries.forEach((entry) => {
      const matches = terms.every((term) => entry.textContent.toLocaleLowerCase().includes(term));
      entry.hidden = !matches;
      if (matches) visible += 1;
    });
    status.textContent = `${visible} of ${entries.length} papers`;
    empty.hidden = visible !== 0;
  });
}
