<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/banner-dark.svg">
  <img alt="Yumeng Ye, AI engineer in Paris. LLMs, agents, retrieval, evaluation and fine-tuning." src="assets/banner-light.svg" width="100%">
</picture>

<div align="center">

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/yumeng-ye-5bb6a1246/)
[![Hugging Face](https://img.shields.io/badge/Hugging_Face-FFD21E?style=for-the-badge&logo=huggingface&logoColor=black)](https://huggingface.co/blog/noebrndl/european-vision-language-model-optimization-for-nu)

</div>

---

## Open source

### [genspark-ai/genoffice](https://github.com/genspark-ai/genoffice) &nbsp; ![stars](https://img.shields.io/github/stars/genspark-ai/genoffice?style=flat&color=555)

An open-source AI office suite: Word, Excel, PowerPoint and PDF editors with a built-in agent.
**15 pull requests merged**, 5 more in review.

- **Excel engine on WebAssembly**: made the spreadsheet engine run without threads so it builds for the browser ([#1979](https://github.com/genspark-ai/genoffice/pull/1979), [#1990](https://github.com/genspark-ai/genoffice/pull/1990))
- **PowerPoint**: charts carry their workbook so *Edit Data* works ([#2090](https://github.com/genspark-ai/genoffice/pull/2090)), real 3D models in slides ([#2091](https://github.com/genspark-ai/genoffice/pull/2091)), slide shows narrated slide by slide ([#2056](https://github.com/genspark-ai/genoffice/pull/2056))
- **PDF and Sheets**: undo and redo of page edits, password unlocking, Flash Fill, formulas that survive a sort, exports that wait for results

<details>
<summary><b>All 15 merged pull requests</b></summary>
<br>

- [#2630](https://github.com/genspark-ai/genoffice/pull/2630) fix(sheets): Flash Fill reads every column of the list, not the six nearest
- [#2526](https://github.com/genspark-ai/genoffice/pull/2526) fix(pdf): Undo and Redo of Replace pages, Page size, Crop and Insert PDF
- [#2525](https://github.com/genspark-ai/genoffice/pull/2525) fix(pdf): try the owner password first, so a one-password protection unlocks as the owner
- [#2524](https://github.com/genspark-ai/genoffice/pull/2524) fix(sheets): a sort right after opening shifts its formulas
- [#2501](https://github.com/genspark-ai/genoffice/pull/2501) fix(pdf): keep lines a wrap cannot explain out of one text block
- [#2500](https://github.com/genspark-ai/genoffice/pull/2500) fix(sheets): CSV export, PDF export and Print wait for the formula results
- [#2499](https://github.com/genspark-ai/genoffice/pull/2499) fix(docs): insert the gallery page number as a PAGE field
- [#2103](https://github.com/genspark-ai/genoffice/pull/2103) fix(pptx-engine): a reparsed slide keeps its unsaved edits marked
- [#2102](https://github.com/genspark-ai/genoffice/pull/2102) fix(pptx-engine): restore what #2090 added and #2091's merge dropped
- [#2091](https://github.com/genspark-ai/genoffice/pull/2091) feat(slides): real 3D models — stored as PowerPoint stores them, turned in the editor
- [#2090](https://github.com/genspark-ai/genoffice/pull/2090) feat(pptx-engine): a chart carries its workbook, so PowerPoint's Edit Data works
- [#2056](https://github.com/genspark-ai/genoffice/pull/2056) feat(slides): Slide Show > Record narrates the show, slide by slide
- [#1997](https://github.com/genspark-ai/genoffice/pull/1997) fix(sheets): load the cell-font aliases a workbook uses, not all at startup
- [#1990](https://github.com/genspark-ai/genoffice/pull/1990) fix(xlsx-engine): open and save workbooks on WASI, where canonicalize is unsupported
- [#1979](https://github.com/genspark-ai/genoffice/pull/1979) feat(xlsx-engine): run without threads, so the engine builds for WebAssembly

[See them on GitHub →](https://github.com/genspark-ai/genoffice/pulls?q=is%3Apr+author%3AMidsummerYU+is%3Amerged)

</details>

---

## Research & projects

<table>
<tr>
<td width="50%" valign="top">

### Vision-language model for nuclear regulation
Fine-tuned a small vision-language model to find the right page in regulatory documents, read as images. First author, published on Hugging Face.

`SmolVLM` `Fine-tuning` `Document retrieval`<br>
**[Article](https://huggingface.co/blog/noebrndl/european-vision-language-model-optimization-for-nu) · [Model](https://huggingface.co/racineai/Flantier-Nuclear-Reglementation-1) · [Dataset](https://huggingface.co/datasets/racineai/VDR_Nuclear)**

</td>
<td width="50%" valign="top">

### [Huawei Signal Processing Competition](https://github.com/MidsummerYU/Polimi_Signal_Processing_HUAWAI_Competition)
Denoising real audio recordings corrupted by different kinds of noise, with adaptive filtering and spectral analysis. Politecnico di Milano × Huawei, 2024.

`MATLAB` `Signal processing` `Adaptive filters`

</td>
</tr>
</table>

**More:** [RAG_on_arXiv_ML](https://github.com/Leo-D-M-Appourchaux/RAG_on_arXiv_ML) (question answering over arXiv machine-learning papers, group project at Politecnico di Milano)

---

## Tech stack

| | |
|---|---|
| **Languages** | ![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white) ![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?style=flat&logo=typescript&logoColor=white) ![SQL](https://img.shields.io/badge/SQL-4479A1?style=flat&logo=postgresql&logoColor=white) |
| **AI agents** | ![Pydantic AI](https://img.shields.io/badge/Pydantic_AI-E92063?style=flat&logo=pydantic&logoColor=white) ![LangGraph](https://img.shields.io/badge/LangGraph-1C3C3C?style=flat&logo=langchain&logoColor=white) ![MCP](https://img.shields.io/badge/MCP-000?style=flat&logo=anthropic&logoColor=white) ![Claude Code](https://img.shields.io/badge/Claude_Code-D97757?style=flat&logo=anthropic&logoColor=white) |
| **ML** | ![PyTorch](https://img.shields.io/badge/PyTorch-EE4C2C?style=flat&logo=pytorch&logoColor=white) ![Hugging Face](https://img.shields.io/badge/Transformers-FFD21E?style=flat&logo=huggingface&logoColor=black) ![LoRA](https://img.shields.io/badge/LoRA_·_SFT_·_DPO-555?style=flat) |
| **Backend & data** | ![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat&logo=fastapi&logoColor=white) ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=flat&logo=postgresql&logoColor=white) ![Redis](https://img.shields.io/badge/Redis-DC382D?style=flat&logo=redis&logoColor=white) |
| **Frontend** | ![React](https://img.shields.io/badge/React-20232A?style=flat&logo=react&logoColor=61DAFB) ![Next.js](https://img.shields.io/badge/Next.js-000?style=flat&logo=nextdotjs&logoColor=white) ![Playwright](https://img.shields.io/badge/Playwright-2EAD33?style=flat&logo=playwright&logoColor=white) |
| **Cloud & infra** | ![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat&logo=docker&logoColor=white) ![Kubernetes](https://img.shields.io/badge/Kubernetes-326CE5?style=flat&logo=kubernetes&logoColor=white) ![GCP](https://img.shields.io/badge/GCP-4285F4?style=flat&logo=googlecloud&logoColor=white) ![AWS](https://img.shields.io/badge/AWS-232F3E?style=flat&logo=amazonwebservices&logoColor=white) ![Azure](https://img.shields.io/badge/Azure-0078D4?style=flat&logo=microsoftazure&logoColor=white) |

