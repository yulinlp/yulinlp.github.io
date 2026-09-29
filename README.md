# Yulin Hu — Academic Homepage

Personal academic website: https://yulinlp.github.io/

Built with the MIT-licensed [AcadHomepage](https://github.com/RayeRen/acad-homepage.github.io) template, following [Qiguang Chen’s homepage](https://lightchen233.github.io/).

## Maintain the website

- `_pages/about.md`: biography, news, projects, education, experience, and honors.
- `_data/publications.json`: publications grouped by research topic. Use [Yulin Hu’s Google Scholar profile](https://scholar.google.com/citations?user=ZhV-ua0AAAAJ) as the source of truth for titles, authors, and publication venues. Each record includes its Scholar source URL. Last checked: 2026-09-29; 19 records across six topics. Per-paper topic tags, citation snapshots, and source-backed presentation distinctions are maintained in the same data file. See `docs/publication-evidence.md` for evidence.
- `_config.yml`: name, institutional email, social links, and website metadata.
- `_data/navigation.yml`: navigation links; each anchor must match an ID in the homepage.
- `assets/css/profile.css`: small visual refinements on top of the original theme.

At the owner’s explicit request, CUE-Mem was added from its verified arXiv record (https://arxiv.org/abs/2609.32574), marked as a preprint submitted to AAAI 2027, not accepted. Selected Projects contains only QiaoBan and HIT AI Counselor. Education and honors were checked against the owner’s supplied application materials. The current Huawei Consumer BG research internship was confirmed by the owner; the internship runs from June 2026 to the present.

## Preview

Use Ruby 3.3 and Bundler:

```sh
bundle install
bundle exec jekyll serve
```

Open http://127.0.0.1:4000/.

## Publish

GitHub Pages uses GitHub Actions. A push to `main` builds and deploys the website. The same workflow refreshes Google Scholar daily at 01:23 UTC (09:23 Beijing time), and can also be run manually from Actions. Scheduled runs may be delayed by GitHub; inactive public repositories may have schedules disabled after 60 days.

Citation totals and per-paper counts are refreshed from Google Scholar. Newly indexed papers are added under Recent Publications with full author names fetched from their Scholar detail pages. Existing editorial metadata (topics, author roles, conference labels, awards, links) is preserved; curate new entries in `_data/publications.json` when needed. If Scholar blocks a request or returns incomplete data, the workflow keeps the previous data and reports a failed refresh. No API key is required. CUE-Mem remains present even before Scholar indexes it.

`google_scholar_crawler/test_sync.py` covers metadata preservation, deduplication, and invalid responses. `images/avatar.jpeg` is the owner-provided homepage avatar.

Keep private application materials and full CV source files outside this public repository.
