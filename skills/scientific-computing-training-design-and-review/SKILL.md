---
name: scientific-computing-training-design-and-review
description: Design, review, restructure, or reality-check concept-led scientific-computing training for PhD students and researchers in academia, industry, or SMEs across diverse scientific domains. Use for instructor-led, self-paced, or hybrid courses when treating presentation slides as guides for live teaching rather than standalone material, prioritizing durable principles over volatile library APIs, rejecting imitation or transcription exercises, defining measurable learning objectives, aligning content and exercises, estimating realistic scope and timing, managing cognitive load and prerequisites, balancing theory with practice, grouping optional hands-on sessions, requiring complete exercise solutions, checking opening logistics, or producing a structured evidence-based course review.
---

# Scientific Computing Training Design and Review

## Purpose

Design or evaluate scientific-computing training for educational quality, realistic delivery, participant experience, and practical usefulness. Apply the principles independently of the technical subject, including scientific programming, data analysis, software engineering, machine learning, numerical methods, reproducibility, visualization, version control, parallel or GPU programming, and workflow management.

Review technical correctness when evidence permits, but do not substitute a technical-content review for a training-design review.

## Establish the evidence and task

1. Identify whether the task is to design, review, restructure, or adapt a course.
2. Inspect the available syllabus, schedule, slides, speaker notes, instructor guide, recordings or transcripts, examples, exercises, solutions, repository, setup instructions, and participant documentation. Do not infer absence from a single artifact when other course materials or live explanation may contain the item.
3. Establish the intended delivery mode: instructor-led, self-paced, or hybrid.
4. Record the stated audience, duration, prerequisites, learning objectives, and constraints.
5. Label missing information and assumptions. Distinguish an observed defect from an item that could not be verified.
6. If critical evidence is missing, continue with a provisional assessment where possible and state what would change the conclusion.

## Design philosophy

Optimize learning rather than the amount of material presented. Aim for participants to leave with:

- understanding of the general principles and core concepts;
- realistic expectations about capabilities and limitations;
- transferable reasoning they can apply to unfamiliar tools and problems;
- enough tool-specific fluency to put the principles into practice;
- sufficient references and next steps for further study.

Prefer a focused course that teaches fewer topics well. Reduce scope before increasing pace.

## Teach durable concepts, not transient APIs

Treat conceptual understanding and transfer as the main learning goal. Scientific software, libraries, and APIs change rapidly; the principles that let participants evaluate and use them usually remain valuable longer.

- Teach what problem a technique solves, why it works, when to use it, its assumptions, its trade-offs, and how to recognize failure.
- Use a particular library or API as a concrete vehicle for a general idea, not as the idea itself.
- Keep tool-specific syntax to the minimum needed to make the concept executable.
- Explicitly separate durable concepts from current implementation details.
- Teach participants how to locate and assess current API documentation rather than expecting long-term recall of signatures or options.
- Where practical, compare two implementations or ask what would remain true if the library changed.
- Move exhaustive API tours, option catalogs, and version-sensitive details to references unless direct API fluency is itself a justified objective.

Do not overcorrect by removing all concrete implementation. Principles without a worked application can remain abstract; use current tools to make reasoning visible, then test whether participants can transfer it beyond the demonstrated case.

## Treat slides as guides for live teaching

Treat instructor-led slides as presentation scaffolding, not as standalone course material or a transcript of the session. Their purpose is to guide the sequence, support spoken explanation, focus attention, show essential visuals or code, and prompt discussion. Expect the instructor to add motivation, nuance, examples, transitions, caveats, and responses to participant questions that do not appear verbatim on the slides.

- Do not require slides to contain every explanation or to make sense without the instructor.
- Do not mark a concise slide as incomplete merely because the spoken elaboration is absent from the deck.
- Do not recommend dense prose, duplicated narration, or textbook-style slides as the default remedy.
- Evaluate slide legibility, visual purpose, sequencing, cue value, and support for the live narrative.
- Check that indispensable facts participants must retain—such as commands, links, definitions, constraints, and next steps—remain accessible in slides, the repository, a reference sheet, or companion material.
- When reviewing slides without observing the session or seeing speaker notes, state that the teaching narrative and full content coverage cannot be verified. Judge only what the deck can legitimately evidence.

If delivery by multiple instructors, long-term maintenance, or handover matters, preserve essential narrative in speaker notes or an instructor guide. This is an instructor-facing continuity aid, not a reason to burden participant-facing slides with prose.

Do not repurpose the slide deck alone for self-paced learning. Create separate notes, recordings, tutorials, or other companion material that supplies the missing narration while allowing the slides to remain effective presentation aids.

## Respect participants' time

Treat participant time as a first-class design constraint. Participants invest valuable research or professional time; every slide, explanation, demonstration, example, exercise, and discussion must justify the time it occupies.

For every substantial item, ask:

- Does it directly support one or more stated learning objectives?
- Will participants be able to use or build on it after the course?
- Is this the most efficient example or activity for teaching the concept?
- Could it be shortened, omitted, or moved to further reading without weakening the course?

Do not retain material merely because it is interesting, displays instructor expertise, might be useful someday, or has traditionally been included. Briefly acknowledge valuable peripheral or advanced topics and provide references rather than teaching them in the core course unless they support a learning objective.

Apply this principle to logistics too: make setup reliable and explicit, but keep live administrative overhead concise.

## Design for the audience

Assume participants may include PhD students, postdoctoral researchers, academic staff, industry researchers, and SME employees. Their domains may range from engineering and computer science to life sciences, social sciences, and the humanities.

- Treat them as capable adult learners who can follow abstractions, read documentation, retype, and copy or adapt code without spending course time proving those basic mechanics.
- Avoid assuming extensive programming or mathematical experience unless explicitly required.
- State all prerequisites and distinguish **required** from **helpful but optional** knowledge.
- Justify prerequisites and keep them minimal.
- Explain domain-specific terminology when first introduced.
- Avoid examples that require substantial domain knowledge unrelated to the objective.
- Provide multiple points of access where a heterogeneous audience would otherwise be excluded.

Do not claim that one example is universally relatable. Prefer a simple scientific context whose incidental domain content is easy to explain.

Do not confuse intellectual ability with prior exposure. A highly capable researcher can reason deeply while still being new to a programming language, mathematical technique, command-line environment, or scientific domain. Remove low-value transcription while continuing to explain genuine prerequisites and unfamiliar concepts.

## Start with mandatory logistics

Begin every course with a short logistics section before technical content. Include, as applicable:

- course objectives and intended audience;
- required and optional prerequisites;
- schedule, breaks, and the boundary between lecture and optional hands-on work;
- slide, notation, and code conventions;
- software, accounts, data, and installation requirements;
- the training repository location and navigation;
- where exercises and complete solutions are located;
- how to ask questions or get help during and after training;
- accessibility or participation arrangements;
- expected outputs and any assessment method.

For self-paced delivery, make these items persistent and easy to find rather than relying on an instructor announcement.

## Align objectives, content, activities, and evidence

Write learning objectives that are explicit, observable, achievable in the available time, and appropriate for the audience. Prefer verbs such as *write*, *apply*, *compare*, *diagnose*, *interpret*, or *choose* over vague verbs such as *know* or *understand*.

Build an alignment map for each objective:

| Learning objective | Prerequisite | Teaching content or demonstration | Practice or exercise | Evidence of achievement | Estimated time |
|---|---|---|---|---|---|

Flag:

- content that supports no objective;
- objectives with no instruction or practice;
- exercises that do not reinforce an objective;
- objectives whose expected performance exceeds the instruction, practice, or available time;
- assessments that measure something other than the stated objective.

## Check progression, dependencies, and cognitive load

Use a progression such as motivation, core concept, minimal example, practical use, limitations, and then optional advanced material. Introduce every concept before it is required.

Check for:

- unexplained terminology or notation;
- hidden dependencies on syntax, tools, mathematics, or domain knowledge;
- long code listings with several simultaneous ideas;
- large jumps in difficulty;
- too many new concepts in one section;
- context switching between unrelated tools or abstractions;
- advanced mechanisms introduced before their motivation.

Recommend segmentation, worked examples, retrieval or recap, and removal of incidental complexity. Do not mistake simplifying the teaching example for misrepresenting the real task: state important limitations and show a path from the minimal example to realistic use.

## Make scope and timing realistic

Construct or reconstruct a time budget that includes:

- opening logistics;
- explanations and transitions;
- demonstrations, including typing and execution time;
- questions and discussion;
- hands-on work and solution discussion;
- breaks;
- setup and troubleshooting contingency;
- closing synthesis and next steps.

Compare the itemized total with the advertised duration. Treat timings without contingency as optimistic, especially for heterogeneous audiences or live coding. Do not hide infeasibility by assuming faster delivery.

When exact timing evidence is unavailable, give a range and identify its assumptions. Classify the schedule as:

- **Realistic**: fits with reasonable contingency;
- **At risk**: fits only if questions, setup, or exercises run unusually smoothly;
- **Unrealistic**: the planned material cannot reasonably fit without removing learning value.

When timing is at risk or unrealistic, prioritize objectives and propose what to cut, defer, or make optional.

## Balance theory and practice

Choose the balance from the learning objectives rather than applying a fixed ratio.

- For conceptual objectives, provide motivation, intuition, diagrams, comparison, and limitations, then include practice that requires reasoning or choice.
- For practical objectives, provide concise explanations, demonstrations, realistic examples, and substantial guided and independent practice.
- Avoid both theory without application and cookbook instructions without transferable understanding.
- Use examples drawn from research computing while removing irrelevant complexity.

## Require thinking, not imitation

Do not present “monkey see, monkey do” activities as exercises. Retyping or copying a demonstrated command, code fragment, or sequence can support setup or a live demonstration, but it is not meaningful practice by itself for this audience.

Design exercises that require participants to do one or more of the following:

- choose an appropriate approach and justify the choice;
- predict behavior or results before executing;
- adapt a principle to a changed or unfamiliar case;
- diagnose a defect, misleading result, or failed assumption;
- compare alternatives and explain trade-offs;
- interpret output in scientific terms;
- design, complete, or critique a solution under stated constraints;
- identify what information must be obtained from current documentation.

Prefer small but consequential decisions over large amounts of typing. Provide starter code, data, boilerplate, and exact setup commands when those mechanics are not the learning objective. A code-along may precede an exercise, but the exercise must add an independent reasoning or transfer step.

Judge success by the participant's explanation, choice, diagnosis, or adaptation, not merely by reproducing the instructor's output. Include an unfamiliar variation when appropriate to test transfer rather than memory.

## Design hands-on sessions deliberately

Group hands-on exercises into one or more clearly announced, contiguous sessions whenever feasible. Put the conceptual lecture first so participants who prefer not to work through exercises live may leave without missing later core teaching. Do not scatter mandatory mini-exercises throughout the lecture unless there is a specific learning reason; if short interactions are necessary, distinguish them from the optional hands-on block.

For every exercise, provide:

- the learning objective it reinforces;
- required prior knowledge and setup;
- clear starting materials and instructions;
- an expected duration or timebox;
- expected outputs or success criteria;
- a decision, prediction, diagnosis, interpretation, or transfer task beyond transcription;
- useful hints or staged support;
- a complete, runnable reference solution;
- an explanation of the solution, including important choices and limitations;
- comments where they clarify reasoning rather than narrate obvious code.

Ensure that people completing exercises later receive the same educational value as live participants. Exercises should normally reinforce introduced material, not depend on entirely new concepts. If an exercise intentionally extends the course, label and scaffold it as optional advanced work.

Evaluate exercise feasibility by trying the instructions and solution in the documented environment when practical. Account for reading, debugging, and discussion time, not just expert solution time.

If copying or retyping dominates the activity, reclassify it as setup or demonstration and replace the exercise with a reasoning task. Do not inflate exercise time with mechanics that starter materials can eliminate.

## Adapt to delivery mode

For instructor-led delivery:

- create space for questions and discussion;
- use demonstrations where live explanation adds value;
- use slides to cue and support the live narrative rather than scripting it or attempting to encode it in full;
- assess the combination of slides and instructor elaboration, not slide text alone;
- give instructors timing cues, likely misconceptions, and fallback options;
- protect breaks and the boundary before the optional exercise block.

For self-paced delivery:

- supply sufficient written or recorded guidance in companion material rather than expecting the slide deck to stand alone;
- provide explicit navigation, instructions, expected outcomes, and progress cues;
- include complete solutions and explanations;
- include troubleshooting and recovery paths;
- provide references and a clear completion point.

For hybrid use, keep the presentation deck optimized for live teaching and provide a distinct self-paced path. Do not assume instructor narration will repair incomplete self-paced material. Mark instructor notes separately from participant-facing explanations.

## Review each exercise

For every exercise, assess:

1. objective and alignment;
2. placement and prerequisite readiness;
3. clarity and completeness of instructions;
4. realistic duration for the intended audience;
5. availability and correctness of starting materials;
6. completeness, executability, and explanatory value of the solution;
7. consistency with the taught APIs, tools, notation, and environment;
8. useful feedback or success criteria;
9. suitability for live and deferred completion;
10. evidence that the participant must reason, decide, interpret, diagnose, or transfer rather than imitate;
11. emphasis on durable concepts rather than recall of a current API;
12. incidental complexity, accessibility, and likely failure modes.

Do not equate the presence of a solution file with a complete solution. Inspect it when available.

## Produce a structured course review

Lead with the conclusion. Scale detail to the evidence and course size. Use this structure:

1. **Executive summary** — overall judgment, intended audience and duration, the most important strengths, and the highest-priority risks.
2. **Evidence and assumptions** — artifacts inspected, whether the live narrative was observable, delivery mode, missing information, and provisional assumptions.
3. **Strengths** — concrete features worth preserving and why they help learning.
4. **Learning-objective alignment and conceptual durability** — objective-to-content-to-practice mapping, gaps, transfer beyond the demonstrated API, and excessive version-sensitive detail.
5. **Scope and timing realism** — itemized or reconstructed budget, contingency, realism classification, and pressure points.
6. **Learning progression and cognitive load** — dependencies, sequencing, terminology, code complexity, and difficulty jumps.
7. **Theory/practice balance** — suitability for the objectives and audience.
8. **Exercise design and solutions** — placement, grouping, optional exit point, feasibility, solution quality, and whether activities demand reasoning rather than imitation.
9. **Audience, prerequisites, and accessibility** — suitability across stated backgrounds and hidden assumptions.
10. **Slides and instructor narrative** — whether slides effectively guide the live session, what spoken content could be assessed, and whether persistent reference material covers details participants must retain.
11. **Delivery-mode readiness** — instructor-led and/or self-paced gaps, without expecting one deck to serve both modes alone.
12. **Opening logistics** — repository, setup, conventions, schedule, support, and solution access.
13. **Participant-time audit** — unsupported material, avoidable overhead, and content to cut or defer.
14. **Prioritized recommendations** — changes ordered by impact and effort, each with rationale and a concrete action.
15. **Overall assessment** — concise readiness verdict and the conditions for successful delivery.

Use evidence-specific language. Cite file, slide, section, exercise, or schedule locations when available. State both advantages and disadvantages of substantial redesign recommendations. Do not praise generally; explain what works and why.

For prioritized recommendations, use:

| Priority | Finding | Evidence | Why it matters | Recommended action | Effort |
|---|---|---|---|---|---|

Separate must-fix delivery blockers from worthwhile improvements and optional refinements.

## Final quality check

Before delivering a design or review, verify that:

- the audience and delivery mode are explicit;
- instructor-led slides are assessed as guides for live teaching, not as standalone documentation;
- claims about missing explanation are qualified when the live narrative or speaker notes were unavailable;
- mandatory opening logistics are present;
- prerequisites are minimal, explicit, and correctly ordered;
- durable principles and transferable concepts take priority over volatile API detail;
- every core item supports a learning objective;
- objectives, instruction, practice, and evidence align;
- scope and timing include interaction, breaks, and contingency;
- cognitive load and progression are defensible;
- theory and practice serve the objectives;
- hands-on work is grouped so non-participants can leave without losing core content;
- exercises require reasoning, choice, diagnosis, interpretation, or transfer rather than transcription;
- starter materials eliminate copying and boilerplate when those mechanics are not objectives;
- every exercise has a complete explained solution;
- self-paced companion materials do not rely on invisible instructor knowledge or on the slide deck alone;
- recommendations explain why, acknowledge trade-offs, and are prioritized;
- observed defects are distinguished from missing evidence;
- participant time is respected throughout.
