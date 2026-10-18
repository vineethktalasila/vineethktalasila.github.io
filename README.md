# Vineeth Krishna Talasila — personal website

An academic website built with [Quarto](https://quarto.org/). Source stays in the GitHub repository `vineethktalasila/vineethktalasila.github.io`; GitHub Pages serves the rendered website, and Cloudflare supplies the domain registration and DNS for `vineethkrishnat.com`.

The preferred public address is **https://vineethkrishnat.com**. This folder is prepared for that address; editing the files does not register the domain with GitHub or change DNS.

## Preview and check locally

[Install Quarto](https://quarto.org/docs/get-started/) if needed. The deployment workflow and this revision use Quarto **1.10.18**. No Python notebooks, R installation, Node packages, or Conda environment are required to build the website.

From this folder:

```sh
quarto preview
```

Open the local address printed by Quarto. To make and validate the publishable files:

```sh
quarto render
python3 scripts/check_site.py
```

Python 3.9 or newer is needed only for the checker. `environment.yml` is an optional minimal Python environment. The build goes into `_site/`, which is ignored by Git. Never publish the repository root as the built site: it contains source, documentation, and development files.

The checker examines the five rendered pages, internal links and anchors, metadata, image descriptions, required deployment files, and common accidental personal-contact patterns. It is a useful check, not a substitute for reviewing new content before publishing.

## Editing guide

| File | Purpose |
| --- | --- |
| `index.qmd` | Introduction, recent papers, and contact section |
| `research.qmd` | Research themes with links to related papers |
| `publications.qmd` | Paper records, journal/arXiv links, and talks |
| `cv.qmd` | Public academic CV; browser print / Save as PDF button |
| `styles.css` | Colors, typography, responsive layout, and print layout |
| `assets/profile.jpeg` | Resized, re-encoded public portrait |
| `assets/site.js` | Progressive enhancement: publication search and CV printing |
| `_quarto.yml` | Navigation, metadata, domain, and build resources |
| `.github/workflows/publish.yml` | Build checks on pull requests; deploy on pushes to `main` |
| `scripts/check_site.py` | Checks the actual `_site` output |

After adding a paper, update the initial paper count in `publications.qmd`. Update the home page's recent papers separately when appropriate. All papers and contact links work without JavaScript; search and the print button appear when JavaScript is available. Browser printing is also available from the browser menu.

To change the domain later, update `_quarto.yml`, `CNAME`, and `robots.txt`, then change the GitHub Pages custom-domain setting and DNS. GitHub Actions deployments use the domain in **repository Settings → Pages**; GitHub ignores `CNAME` files for this publishing method. The included `CNAME` documents the intended domain and supports a future branch-based setup. [GitHub's explanation](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/troubleshooting-custom-domains-and-github-pages).

## Manual setup: GitHub Pages + Cloudflare domain

You do not need to transfer the domain, move the source code, or create a Cloudflare Pages project. Use GitHub Pages as the web host and Cloudflare as the DNS provider. Cloudflare website proxying is optional; the straightforward configuration below leaves these website records **DNS only**.

### 1. Review and push the files

Review the public biography, CV, and talks. Commit these changes and push them to the `main` branch of your existing repository using GitHub Desktop or your normal Git workflow. No commit, push, account-setting change, or DNS change was performed as part of preparing this folder.

The workflow builds on pushes and can also be run manually from the Actions tab. Pull requests run the build and checks without deployment. It uses GitHub's automatic `GITHUB_TOKEN`; do not create a personal access token or add Cloudflare credentials.

### 2. Enable GitHub Pages

1. Open [the repository](https://github.com/vineethktalasila/vineethktalasila.github.io).
2. Go to **Settings → Pages → Build and deployment**.
3. Set **Source** to **GitHub Actions**.
4. Open **Actions → Build and deploy website**. Let the workflow finish, or choose **Run workflow** on `main` if its initial deployment ran before Pages was enabled.
5. Confirm that the `build` and `deploy` jobs succeed. Until the custom domain is configured, the site can be served at `https://vineethktalasila.github.io`.

The workflow uploads only `_site/`. GitHub serves the generated HTML; it does not directly render `.qmd` source files. [GitHub custom workflows](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages), [Quarto publishing guidance](https://quarto.org/docs/publishing/github-pages.html).

### 3. Verify ownership of the domain in GitHub

Do this in your **personal GitHub account settings**, separate from the repository settings:

1. Go to **profile picture → Settings → Pages → Add a domain**.
2. Enter `vineethkrishnat.com`.
3. GitHub will show a TXT record name and a verification value. Copy those exact values; the value is account-specific and cannot be supplied in this repository.
4. In Cloudflare, choose `vineethkrishnat.com`, then **DNS → Records → Add record**. Select **TXT**, enter GitHub's record name and verification value, and save. If Cloudflare supplies the zone suffix automatically, enter just the record-name portion rather than duplicating the domain.
5. Return to GitHub and select **Verify** once the record is visible. Keep the TXT record after verification.

[GitHub domain verification instructions](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/verifying-your-custom-domain-for-github-pages).

### 4. Set the custom domain in the repository

In the repository's **Settings → Pages → Custom domain**, enter:

```text
vineethkrishnat.com
```

Choose **Save**. A DNS-check warning is expected until the next step is complete. Set this before directing the domain's website records to GitHub. [GitHub custom-domain guidance](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site).

### 5. Add the website DNS records in Cloudflare

Select `vineethkrishnat.com` in Cloudflare, then **DNS → Records**. Create the following records with TTL **Auto**:

| Type | Name | Content / target | Proxy status |
| --- | --- | --- | --- |
| A | `@` | `185.199.108.153` | DNS only (gray cloud) |
| A | `@` | `185.199.109.153` | DNS only (gray cloud) |
| A | `@` | `185.199.110.153` | DNS only (gray cloud) |
| A | `@` | `185.199.111.153` | DNS only (gray cloud) |
| CNAME | `www` | `vineethktalasila.github.io` | DNS only (gray cloud) |

`@` means the bare domain. The CNAME target is a hostname, with no `https://` or path. Replace conflicting website A/AAAA/CNAME records for `@` and `www`; preserve email records (MX/SPF/DKIM/DMARC), the verification TXT record, and unrelated subdomains. Do not add wildcard website records.

IPv6 is optional. If you want it, add all four GitHub Pages AAAA records for `@`, also DNS only: `2606:50c0:8000::153`, `2606:50c0:8001::153`, `2606:50c0:8002::153`, and `2606:50c0:8003::153`. Otherwise, remove conflicting old AAAA website records.

The addresses above come from [GitHub's current DNS table](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site). Cloudflare's [record editor guide](https://developers.cloudflare.com/dns/manage-dns-records/how-to/create-dns-records/) explains the fields. [DNS only](https://developers.cloudflare.com/dns/proxy-status/) sends visitors directly to GitHub Pages, which supplies HTTPS. Keep this setting for the documented configuration; Cloudflare proxy, cache, and SSL settings do not control DNS-only traffic.

### 6. Enable HTTPS and check both addresses

Return to **repository Settings → Pages**. Wait for GitHub's DNS check and certificate provisioning, then select **Enforce HTTPS**. DNS propagation can take up to 24 hours; GitHub notes that HTTPS can take up to an hour after domain configuration. [GitHub HTTPS instructions](https://docs.github.com/en/pages/getting-started-with-github-pages/securing-your-github-pages-site-with-https), [troubleshooting](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/troubleshooting-custom-domains-and-github-pages).

Confirm these behaviors in a browser:

- `https://vineethkrishnat.com` opens the home page.
- `https://www.vineethkrishnat.com` redirects to the bare domain.
- The old `github.io` address redirects to the custom domain.
- Navigation, portrait, publication links, publication search, and the CV print action work.
- An unknown URL shows the custom 404 page.

With both DNS names configured, GitHub handles the `www` redirect. [Supported domain behavior](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/about-custom-domains-and-github-pages).

If the domain fails, check that all website records are DNS only, the GitHub Pages source is GitHub Actions, the workflow succeeded, and the custom-domain value is saved in repository settings. If you have restrictive CAA records, ensure that they allow `letsencrypt.org` for GitHub's certificate. Do not change unrelated email records to troubleshoot the website.

## Content and privacy notes

This revision removes the home address, phone numbers, personal email addresses, grades, fellowship monetary amounts, and machine-specific environment paths from current public source. It uses the public university profile as the contact route. The portrait was resized and re-encoded, with EXIF and embedded metadata checked separately. No analytics, third-party font requests, contact-form service, or cookie-based tracking were added by this project.

**Existing Git history still contains the old versions.** These changes do not erase previous commits, GitHub caches, other clones, or information already published elsewhere. If the old contact details were pushed publicly, review the repository's history before sharing it widely. Removing historical copies is a separate, disruptive Git-history operation and was not performed here.

Public affiliation was checked against the [University of Michigan profile](https://lsa.umich.edu/litp/people/postdoctoral-fellows/vineeth-krishna.html). Paper titles, author lists, identifiers, and available journal references were checked against the linked arXiv/publisher records. The 2026 paper with Finn Larsen was added; the grey-galaxy and bulk-replica placeholders were replaced with verified records. The unverified “Multi-Entropy in 2d Yang-Mills” draft entry was omitted rather than given an invented identifier. The talk dates, education, teaching, awards, and appointment dates follow the supplied draft and should receive your final review.

Useful next additions, when you have the material: seminar slides or recordings, an approved professional email address, and a short description of any public research code. Add only links and projects that you want public.
