# First Voice

## Local-first narrative reframing with Gemma

First Voice is a **local-first narrative reframing prototype** built with **Gemma 4 through Ollama**.

It helps experienced professionals, career changers, and non-technical users turn real work experience into language they can understand, reuse, and continue developing with AI.

The project was built for **The Gemma 4 Good Hackathon**.

---

## One-line Summary

First Voice helps people build the right context before asking AI to write for them.

Instead of starting with a blank prompt box, users answer a short guided workflow about what actually happens in their work. Gemma 4 then reframes that experience into a clearer professional narrative, while the entire workflow stays on the user's local machine.

---

## Why This Exists

Many people do not lack experience.

They have years of observation, judgment, coordination, service, problem-solving, and operational knowledge.

But when they open an AI tool, they often do not know:

- what they want to say
- how to describe what they actually do
- how to ask AI for help
- how to judge whether the output still feels true to them

They open ChatGPT.  
They see a blank box.  
They close it.

This is not only a writing problem.

It is a context problem.

First Voice was built for the moment before AI collaboration begins.

---

## The Problem: Expression Anxiety

This project focuses on **Expression Anxiety**.

Many experienced people do not struggle because they have nothing to say.

They struggle because their real work is often invisible.

They may be the person others call when things are unclear, stuck, messy, or difficult to explain. They may help teams understand what is really happening, organize fragmented information, or turn confusion into something people can act on.

But because this work does not always fit neatly into a job title, it can be hard to describe.

People may ask themselves:

> "Does this count as a real skill?"  
> "Does this sound too ordinary?"  
> "Does this sound too AI-generated?"  
> "Will anyone care about this?"  
> "Do my past experiences still matter in the AI era?"

First Voice helps users slow down, identify the actual pattern behind their work, and translate that pattern into language they can understand and reuse.

---

## Hackathon Track Fit

First Voice is especially aligned with two parts of the Gemma 4 Good Hackathon:

- **Ollama Award**: the prototype demonstrates Gemma 4 running locally through Ollama.
- **Digital Equity and Inclusion**: the interface lowers the barrier for people who are not already fluent in prompting, AI tools, or professional self-presentation.

The project does not assume that users already know how to write a good prompt. It helps them build the context first.

---

## What First Voice Is Not

First Voice is not:

- a prompt library
- a resume generator
- a job recommendation tool
- a LinkedIn post generator
- a personal branding tool
- a therapy chatbot

It can produce resume, interview, portfolio, social, and AI collaboration language, but only after the user first builds a grounded work context.

It does not try to replace the user's voice.

It helps the user become easier for AI to understand.

---

## What First Voice Does

In the prototype, the user goes through a guided local workflow:

1. The user enters a real work-related confusion or experience.
2. The system identifies the work behavior pattern behind the input.
3. The system asks curated follow-up questions.
4. The user answers based on their own lived experience.
5. Gemma 4 reframes the experience into a core narrative result.
6. The system gives lightweight reasoning cues, such as the detected work pattern and classification rationale.
7. The user chooses a practical use case: resume, interview, portfolio, social post, AI collaboration, or shortcut table.
8. The system generates only the selected use-case version instead of overwhelming the user with every possible output at once.

Most AI tools try to generate better answers faster.

First Voice intentionally slows down the interaction. It creates a small reflective space before the model reframes the user's experience.

> The user should not be replaced by AI.  
> The user should become easier for AI to understand.

---

## How It Works

### Step 1 — Original Input

The user begins with an unclear thought, professional concern, or work experience they do not yet know how to describe.

The input does not need to be polished. It can be uncertain, emotional, incomplete, or messy.

That is the point.

---

### Step 2 — Work Pattern Classification

First Voice identifies the likely work behavior pattern behind the user's input.

The current prototype includes five work pattern categories:

- coordination
- technical sensemaking
- organization
- mentoring
- stabilization

If the model call fails, the prototype includes a fallback keyword classifier to keep the demo usable.

---

### Step 3 — Curated Reflection

Instead of asking Gemma to freely generate any question, First Voice uses curated follow-up questions tied to the detected work pattern.

This design choice helps prevent the system from drifting into:

- therapy-like questions
- vague motivational coaching
- generic self-help language
- overly philosophical prompts
- career advice given too early in the process

The purpose is not to analyze the user as a person.

The purpose is to help the user describe what actually happened, what they noticed, and how they acted.

---

### Step 4 — Core Narrative Reframing

Gemma 4 reframes the user's answer into a structured core result.

The core result focuses on four sections:

1. what the user was doing beyond "miscellaneous work"
2. the work behavior pattern behind the experience
3. the hidden capabilities accumulated through that pattern
4. why this kind of capability is often underestimated

The system does not simply make the writing sound more impressive.

It helps reveal the structure behind the user's everyday work.

---

### Step 5 — Practical Translation Layer

After the core result, the user chooses one use case.

Current options include:

- resume
- interview
- portfolio
- social post
- AI collaboration method
- shortcut command table

This layered design keeps the emotional peak of the core result separate from practical output generation.

This progressive disclosure design minimizes cognitive load, allowing the emotional peak of self-recognition to settle before moving into practical execution.

The goal is not only reflection.

The goal is to help users carry the reframed language into real-world use.

---

## Example Transformation

### Before

"I always thought I was just good at cleaning up messes. When things became confusing, people would come to me and ask what was happening."

### Reflection

"I realized the issue is often not that nobody is working. The real problem is that people do not know where things are actually stuck."

### After

"I used to think I was only cleaning up messy situations. But I was doing something more specific: helping people understand where the real blockage was. When information was scattered or the process had broken down, I would identify the actual source of confusion and reorganize the situation so people could move forward again."

---

## Why Gemma + Ollama

First Voice uses **Gemma 4 E4B via Ollama** in a local-first prototype.

The exact model tag used in code is:

```text
gemma4:e4b
```

This matters because the project is not only about generating text.

It is about creating a safer environment where users can work with sensitive personal and professional material without immediately sending it to a cloud service.

The prototype demonstrates how Gemma can support a more careful AI interaction pattern:

- not just answering
- not just generating
- not just summarizing
- but helping users build context before AI collaboration begins

This makes Gemma useful not only as a language model, but as part of a reflective interaction system.

---

## Why Local-first Matters

First Voice runs entirely on the user's machine.

No personal story needs to be uploaded to a cloud API.

This matters because users may write about:

- self-doubt
- career uncertainty
- workplace relationships
- professional shame
- sensitive lived experience
- transitions between industries
- fear of being misunderstood by AI or by other people

For this project, local-first is not only a technical feature.

It is a design ethic.

When people are trying to understand their own experience, privacy affects honesty.

A local-first workflow gives users more psychological safety to write messy, unfinished, and truthful input.

---

## Technical Stack

- **Model**: Gemma 4 E4B via Ollama
- **Model tag used in code**: `gemma4:e4b`
- **Framework**: Gradio
- **Language**: Python 3.11+
- **Runtime**: Local machine
- **Ollama API**: called through `requests`
- **Interface**: Localhost demo
- **Default local URL**: `http://127.0.0.1:7861`
- **Deployment**: 100% local prototype
- **Cloud dependency**: None required for the demo workflow

---

## Local Reproduction Guide

This project is designed to run locally using Python, Gradio, Ollama, and Gemma.

The local Ollama runtime is not fully reproducible inside Kaggle Notebook, so the primary reproduction path is a local machine setup.

The following steps are provided so reviewers can reproduce the demo locally.

---

### 1. Install Python

Install Python 3.11 or later.

Confirm installation:

```bash
python --version
```

or:

```bash
python3 --version
```

---

### 2. Install Ollama

Install Ollama from the official Ollama website:

[https://ollama.com/](https://ollama.com/)

After installation, confirm that Ollama is available:

```bash
ollama --version
```

Make sure the Ollama service is running before launching the Gradio app.

---

### 3. Pull the Gemma model

Pull the Gemma model used by this project:

```bash
ollama pull gemma4:e4b
```

Confirm the model tag is available:

```bash
ollama list
```

The model name in the code must match the model tag available in the local Ollama environment.

The prototype currently uses:

```python
OLLAMA_MODEL = "gemma4:e4b"
```

---

### 4. Clone or download this repository

```bash
git clone <YOUR_REPOSITORY_URL>
cd first-voice
```

If you download the repository as a ZIP file, unzip it and open the project folder in your terminal.

---

### 5. Create a virtual environment

macOS / Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Windows Command Prompt:

```cmd
python -m venv .venv
.venv\Scripts\activate
```

---

### 6. Install dependencies

```bash
pip install -r requirements.txt
```

If `requirements.txt` is not available, install the minimum dependencies manually:

```bash
pip install gradio requests
```

---

### 7. Run the app

```bash
python app.py
```

---

### 8. Open the local demo

Open the following URL in your browser:

```text
http://127.0.0.1:7861
```

The app should launch as a local Gradio interface.

User input is processed through the local Ollama runtime and is not sent to a cloud API.

---

## Expected Repository Structure

Recommended final submission structure:

```text
first-voice/
├── app.py
├── README.md
├── requirements.txt
├── LICENSE
├── media/
│   ├── thumbnail.png
│   └── screenshots/
└── docs/
    └── concept_note.md
```

Recommended minimum files:

```text
app.py
README.md
requirements.txt
LICENSE
```

---

## Requirements File

A minimal `requirements.txt` should include:

```text
gradio
requests
```

If additional Python packages are used in the final version of the script, they should also be added to `requirements.txt`.

---

## Troubleshooting

### Ollama is not running

If the app cannot connect to Ollama, make sure Ollama is installed and running.

Check:

```bash
ollama --version
```

You can also test whether the model responds:

```bash
ollama run gemma4:e4b
```

---

### Model tag not found

If you see an error related to the model name, confirm the installed model list:

```bash
ollama list
```

Then update the model name in the Python app to match the model tag shown in your local Ollama environment.

---

### Port already in use

The app uses port `7861`.

If the port is already in use, either close the other process or change the Gradio launch port in the Python app.

---

### The model response is slow

Local model speed depends on hardware.

If the response is slow, wait for the first generation to complete. Performance may vary depending on GPU, RAM, and Ollama configuration.

---

## Safety and Trust

First Voice is not a therapy chatbot.

It is not a personal branding tool.

It is not a LinkedIn post generator.

It is not a resume generator.

It is a local-first reflective interaction prototype that helps people recognize the hidden value in their everyday work and translate it into language they can use.

The prototype includes lightweight reasoning cues, such as the detected work pattern and classification rationale, so users can see how the system moved from their original words toward the final reframing.

This helps reduce the risk of the AI becoming a black box that defines the user too quickly.

The user remains the final editor of meaning.

---

## Design Principles

### 1. The system does not comfort the user. It reorganizes meaning.

First Voice avoids toxic positivity, exaggerated encouragement, and generic motivational language.

It does not tell the user that everything is wonderful.

It helps the user see the structure behind what they already did.

---

### 2. AI does not rush to define people.

First Voice does not force an identity, job title, or career path onto the user.

It creates a short reflective space first.

The user's experience comes before the AI's conclusion.

---

### 3. Output should not sound overly AI-generated.

First Voice avoids language that feels too polished, corporate, exaggerated, or artificial.

The goal is not to make the user sound impressive.

The goal is to help the user sound more true.

---

### 4. Reframing should remain explainable.

Because the system is working with personal experience, every reframing should be understandable.

The user should be able to see the path from their original words to the final interpretation.

The user remains the final editor of meaning.

---

## Impact

First Voice supports digital inclusion by helping people who may not already be fluent in AI interaction.

Many AI tools assume that users can write clear prompts, define their goals, and evaluate the output.

But many people need help before that stage.

They need to build the context first.

First Voice helps users move from:

> "I do not know how to explain what I do."

to:

> "I can see the pattern behind my experience, and now I have language for it."

This can help career changers, mid-career workers, and non-technical users participate more confidently in AI-assisted work.

The impact is not only faster writing.

The impact is helping people stay present in the process of expressing themselves.

---

## Submission Notes

This prototype is intended to be submitted as a local-first Gemma 4 + Ollama demo.

Reviewers can reproduce the app locally by installing Ollama, pulling `gemma4:e4b`, installing the Python dependencies, and running the Gradio app.

The public web page or Kaggle writeup can show screenshots and a video demo, but the core AI workflow is designed to run locally.

This preserves the project's privacy and design goals.

---

## Limitations

This is a prototype for the Kaggle Gemma 4 Good Hackathon.

Current limitations include:

- the reflective flow is still manually curated
- output quality depends on the user's input
- some responses still require human editing
- the system has not yet been tested with a large user group
- the local Ollama runtime is not fully reproducible inside Kaggle Notebook
- the current prototype focuses on narrative reframing rather than full career planning

These limitations are intentional for this stage.

The goal is to test the interaction pattern, not to build a complete career platform.

---

## Future Work

Future improvements may include:

- user testing with experienced professionals and career changers
- a larger curated question bank
- multilingual support
- better onboarding for low-confidence users
- before / after comparison view
- exportable narrative cards
- clearer user editing controls
- refined explainability UI
- optional templates for portfolio, interview, or self-introduction use cases

---

## License

This project is licensed under the **Creative Commons Attribution 4.0 International License (CC BY 4.0)**.

You are free to share and adapt the project, including for commercial purposes, as long as appropriate credit is given.

Author: Cynthia Tseng  
Project: First Voice  
Kaggle: [@littlebeastai](https://www.kaggle.com/littlebeastai)

See the `LICENSE` file for details.

---

## Author

**Cynthia Tseng**  
Kaggle: [@littlebeastai](https://www.kaggle.com/littlebeastai)  
Department of Interaction Design, National Taipei University of Technology  
Taiwan