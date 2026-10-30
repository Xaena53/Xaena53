<div align="center">

<img src="assets/hero.svg" alt="Xaena53 — Full-Stack Developer: backends, computer vision and AI tooling" width="100%"/>

<img src="assets/status.svg" alt="currently building Warden of the Fields" width="100%"/>

</div>

<br/>

<div align="center">
<img src="assets/pipeline-asfalya.svg" alt="Asfalya — vehicle-mounted road damage detection for municipalities" width="100%"/>
</div>

Computer vision for municipal road maintenance. Phone cameras ride on city buses; a YOLO11 detector trained on 35,984 images finds potholes, cracks and sunken manholes; GPS interpolation and OSM map-matching pin each one to a street, and duplicate sightings across passes collapse into a single tracked repair. Faces and plates are blurred **before** detection, and the pipeline refuses to process an unmasked frame at all, so the privacy rule cannot be forgotten. Node/Express + PostGIS behind a MapLibre panel, with weekly PDF reports for the public works desk. Presented as my internship project at BAUM, Anadolu University.

<br/>

<div align="center">
<img src="assets/plate-asfalya.jpg" alt="Asfalya screens — damage map of Eskişehir and two detection frames" width="100%"/>
</div>

<br/>

<div align="center">
<img src="assets/pipeline-aegis.svg" alt="Aegis — network-verified approvals for AI agents that spend money" width="100%"/>
</div>

[Aegis](https://github.com/Xaena53/aegis) hands Google Ads and Meta to a language model and keeps the budget in human hands. Approval happens on the server: when the client supports MCP elicitation the server asks the person directly and ignores the agent's own `confirm` flag. Before that question is even shown, the mobile network is asked through GSMA Open Gateway / CAMARA whether the approver's SIM was swapped recently, and a failed or silent network check refuses the action. Campaigns are created paused, the account owner sets a ceiling the model cannot raise, and scraped site copy is treated as untrusted input. Started as AdsPilot; open source under AGPL-3.0.

<br/>

<div align="center">
<img src="assets/pipeline-animerank.svg" alt="AnimeRank media pipeline architecture" width="100%"/>
</div>

A video platform for anime that I designed and built from the interface to the servers. Sources arrive over P2P, pass a season guard and a quality score, and are re-encoded to H.264 that every browser can play; selected series get a 4K pass through an Adore upscaling model running on TensorRT. Around it: MyAnimeList and AniList two-way sync per profile, multiple profiles per account, a community layer with daily quests and levels, a subtitle checker that measures timing against speech in the audio, and deployments that swap between two instances without dropping a request.

<br/>

<div align="center">
<img src="assets/pipeline-kurenai.svg" alt="Kurenai subtitle translation pipeline" width="100%"/>
</div>

Batch translation for anime subtitles. Karaoke, song and on-screen effect lines are filtered out before anything is sent, which also cut the cost of a typical episode several times over. A line-shift gate rejects any episode whose translated lines drifted out of step with the source, and nothing reaches viewers until it has passed the quality gates. A budget cap governs the translate step.

<br/>

<div align="center">
<img src="assets/plate-kurenai.jpg" alt="Kurenai screens — kurenai.shop and a station sign redrawn in Turkish" width="100%"/>
</div>

<br/>

<div align="center">
<img src="assets/pipeline-repchat.svg" alt="RepChat live-support architecture" width="100%"/>
</div>

A live-support runtime running in production: embeddable widget, WebSocket gateway, category-routed queues, and an AI greeter that resolves the easy tickets before a human ever sees them.

<br/>

<div align="center">
<img src="assets/plate-repchat.jpg" alt="RepChat screens — operator inbox and the phone widget" width="100%"/>
</div>

<br/>

<div align="center">
<img src="assets/pipeline-security.svg" alt="Production hardening — defense in depth" width="100%"/>
</div>

<br/>

<div align="center">
<img src="assets/work.svg" alt="More work — EKT Akademi, Warden of the Fields, Demir Cephe, Hapivanak, Çakmak Pen, MHRS data module" width="100%"/>
</div>

<br/>

<div align="center">
<img src="assets/plate-warden.jpg" alt="Warden of the Fields — Unreal Engine 5.8 captures of the village" width="100%"/>
</div>

<br/>

<div align="center">
<img src="assets/plate-clients.jpg" alt="Client sites in production — EKT Akademi and Çakmak Pen" width="100%"/>
</div>

<br/>

<div align="center">
<img src="assets/skilltree.svg" alt="Capability tree — 33 technologies grouped by role, each branch naming the projects that use it" width="100%"/>
</div>

Grouped by the job each tool does, and every branch names the projects it is used in. The list was read off the dependency manifests in those repositories, so it records what ships.

<br/>

<div align="center">
<img src="assets/code.svg" alt="Live build — the Aegis approval gate typing itself out" width="100%"/>
</div>

<br/>

<div align="center">
<img src="assets/focus.svg" alt="Engineering core competencies" width="100%"/>
</div>

<br/>

<div align="center">
<img src="assets/metrics.svg" alt="Verified metrics — 2,720 passing tests across six projects and the road-damage model training curve" width="100%"/>
</div>

Every number on this page is measured: test counts come from the suites that gate each push, and the training curve is the actual run that produced the road-damage model, including the class it is still weak at. A passing test only proves a line ran, so the Aegis suite is held to a stricter standard: each guard is broken on purpose to confirm a test notices.

<br/>

<div align="center">
<img src="assets/opensource.svg" alt="Upstream contributions and shipped systems" width="100%"/>
</div>

<br/>

<div align="center">

<sub><a href="https://xaena53.github.io/portfolio/">portfolio</a> · <a href="https://www.linkedin.com/in/bedirhan-%C3%A7etin/">linkedin</a> · <a href="mailto:bedometom@gmail.com">bedometom@gmail.com</a></sub>

<br/>

<sub><code>DWG SET XR-001 — XR-025 · REV 2026.10</code></sub>

</div>
