---
permalink: /
title: "Yulin Hu · 胡雨林"
excerpt: "Yulin Hu, master's student at Harbin Institute of Technology. Research on long-term agent memory, personalization, and safe language models."
author_profile: true
redirect_from:
  - /about/
  - /about.html
---
<h1 id="about">Yulin Hu <span class="chinese-name" lang="zh-CN">胡雨林</span></h1>

Hello! I am a master's student in Computer Science and Technology at [Harbin Institute of Technology](https://www.hit.edu.cn/), in the **Sentiment Computing (SC) group** of [SCIR](https://ir.hit.edu.cn/) (Research Center for Social Computing and Interactive Robotics). I am advised by [Prof. Yanyan Zhao](http://ir.hit.edu.cn/~yanyan/) and co-advised by [Prof. Weixiang Zhao](https://circle-hit.github.io/). I am currently a research intern at **Huawei Consumer Business Group (终端 BG)**.

My research focuses on **long-term memory for multimodal agents**: how agents store, maintain, retrieve, and use information across sustained interactions. I also work on **personalized and empathetic dialogue**, **safety alignment**, and **reasoning in large language models**.

I am interested in building agents that understand users over time and use memory when it is relevant and helpful. Feel free to reach out at [ylhu@ir.hit.edu.cn](mailto:ylhu@ir.hit.edu.cn).

<h2 id="news">🔥 News</h2>

- **Sept. 2026** · [CUE-Mem](https://arxiv.org/abs/2609.32574), our benchmark for long-term user memory from implicit multimodal cues, is now available on arXiv. Submitted to **AAAI 2027**.

- **2026** · [OP-Bench](https://arxiv.org/abs/2601.13722), our work on over-personalization in memory-augmented conversational agents, is accepted to **EMNLP 2026**.
- **2026** · Our work on proactive memory retrieval, tool-enhanced emotional support, and personalized-agent safety appears at **ACL 2026 / Findings**.
- **2025** · I started my master's studies at Harbin Institute of Technology.

<div class="publications-heading" id="publications">
<h2>📝 Publications</h2>
<div class="citation-stat" aria-label="{{ site.data.scholar_metrics.total_citations }} total citations"><strong>{{ site.data.scholar_metrics.total_citations }}</strong><span>Citations</span></div>
</div>

<nav class="topic-index" aria-label="Publication topics">
{% for group in site.data.publications %}<a href="#{{ group.id }}">{{ group.icon }} {{ group.name }}</a>{% endfor %}
</nav>

{% for group in site.data.publications %}
<section class="publication-topic" aria-labelledby="{{ group.id }}">
<h3 id="{{ group.id }}">{{ group.icon }} {{ group.name }}</h3>
<ul class="publication-list">
{% for paper in group.papers %}
<li class="publication-entry">
{% if paper.distinction != empty %}<span aria-hidden="true">🏆</span> {% elsif paper.featured_citations %}<span aria-hidden="true">🔥</span> {% endif %}<span class="{{ paper.venue_type }}-tag">{{ paper.venue | escape }}</span>
{% if paper.distinction != empty %}<a class="paper-distinction" href="{{ paper.distinction_source | escape }}">({{ paper.distinction | escape }})</a>{% endif %}
{% if paper.submission_status %}<span class="submission-status">({{ paper.submission_status | escape }})</span>{% endif %}
<a class="paper-title" href="{{ paper.paper_url | escape }}">{{ paper.title | escape }}</a>,
<span class="paper-authors">{% assign author_names = paper.authors | split: ', ' %}{% assign before_yulin = true %}{% for author_name in author_names %}{% if author_name == 'Yulin Hu' %}<strong>{{ author_name | escape }}{% if paper.co_first_author %}<sup title="Co-first author">*</sup>{% endif %}</strong>{% assign before_yulin = false %}{% else %}{{ author_name | escape }}{% if paper.co_first_author and before_yulin %}<sup title="Co-first author">*</sup>{% endif %}{% endif %}{% unless forloop.last %}, {% endunless %}{% endfor %}.</span>
{% if paper.co_first_author %}<span class="student-first-tag">Co-first Author</span> {% elsif paper.first_author %}<span class="student-first-tag">First Author</span> {% elsif paper.student_first_author %}<span class="student-first-tag">Student First Author</span> {% endif %}
{% for tag in paper.tags %}<span class="topic-tag tag-{{ tag.style }}">{{ tag.label }}</span> {% endfor %}
{% for link in paper.links %}{% unless link.label == 'Paper' %}<a class="paper-resource" href="{{ link.url | escape }}">[{{ link.label }}]</a> {% endunless %}{% endfor %}
{% if paper.citations and paper.citations > 0 %}<a class="citation-count{% if paper.featured_citations %} citation-highlight{% endif %}" href="{{ paper.scholar_url | escape }}" title="Google Scholar citations, checked {{ paper.citation_checked }}">{% if paper.featured_citations %}🔥 {% endif %}Citations: {{ paper.citations }}</a>{% endif %}
</li>
{% endfor %}
</ul>
</section>
{% endfor %}

<h2 id="projects">🛠️ Selected Projects</h2>

- **[QiaoBan (巧板)](https://github.com/HIT-SCIR-SC/QiaoBan)** — Core developer of a personalized, empathetic conversational model for children and adolescents. [Official news: QiaoBan-P1 release](https://ir.hit.edu.cn/2025/0626/c19589a372759/page.htm) (June 2025).
- **HIT AI Counselor (工小星)** — Core project lead and developer of a campus assistant combining university knowledge retrieval and empathetic dialogue. [Project news: official launch](https://ir.hit.edu.cn/2025/0806/c19589a376151/page.htm) (August 2025).

<h2 id="education">🎓 Education</h2>

- **Sept. 2025 – Present** · Master's student in Computer Science and Technology, **Harbin Institute of Technology**. Advisor: Prof. Yanyan Zhao.
- **Sept. 2021 – June 2025** · Bachelor’s degree in Computer Science and Technology, School of Future Technology, **Harbin Institute of Technology**.

<h2 id="experience">💻 Research Experience</h2>

- **Huawei Consumer Business Group (终端 BG)** · Research Intern · **June 2026 – Present**.
- **Du Xiaoman Financial Technology** · Research Intern · **Dec. 2024 – Mar. 2025**. Research on empathetic and role-based conversational language models.

<h2 id="honors">🎖️ Honors & Awards</h2>

- **Special-class Graduate Academic Scholarship**, Harbin Institute of Technology, 2025 & 2026.
- **Outstanding Undergraduate Thesis**, Harbin Institute of Technology, 2025.
- **Wentian Scholarship**, Harbin Institute of Technology, annually from **2021 to 2025**.
- **Innovation and Entrepreneurship Scholarship**, Harbin Institute of Technology, annually from **2021 to 2025**.

<footer class="site-credit">Last updated: September 2026 · Built with <a href="https://github.com/RayeRen/acad-homepage.github.io">AcadHomepage</a>, following <a href="https://lightchen233.github.io/">Qiguang Chen's homepage</a>.</footer>
