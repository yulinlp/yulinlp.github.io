# Link audit — 2026-09-29

Audited 60 distinct external URLs and 14 internal navigation link occurrences from the live homepage. Checked destinations and paper titles where readable, in addition to HTTP status.

- Fixed Homepage anchor: nonexistent `about-me` → `about`.
- Replaced Yanyan Zhao’s old HTTP homepage (502 in this audit) with her current official HIT faculty profile.
- SaRFT and CSO: replaced direct PDFs with verified ACL Anthology abstract pages for the same papers.
- OpenReview uses browser verification; its Safety Patching paper ID was corroborated by the indexed PDF. Added the verified arXiv version as an alternate link, preserving the original venue link.
- Springer shows a client challenge to direct requests; the DOI and matching paper title were independently readable through web retrieval.
- HIT/SCIR homepages had TLS errors in the direct checker but were readable through web retrieval. Their URLs remain unchanged.
- All checked code repositories, CUE-Mem demo/dataset, and both project news links returned HTTP 200 and matched their labels.
- Google Scholar returned HTTP 429 on the profile request. Stopped without retrying; individual citation destinations were not freshly verified in this audit. These IDs were populated by the successful Scholar synchronization earlier in this session.

This is a URL/content audit, not a browser interaction test; CAPTCHA, visitor network differences, and future link changes can affect access.
