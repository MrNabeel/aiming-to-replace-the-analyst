# Aiming to replace the analyst?

### Two people read 30 earnings releases and called the stock's move right 33% of the time. An AI got 58%. Neither can see what the market sees. Here is what that means for a business that wants to automate the reading.

*INFO 367, Applied Large Language Models for Business, Montclair State University, Fall 2026. Team project, Deliverable 1. I led the team of four.*

## Why this project exists

Every business is asking the same question about AI right now: can it do this job, and if it can, what does that save? The course I took this semester is built around one rule for answering it honestly. Nothing gets judged against perfect. It gets judged against the person who does the work today, on cost, on quality and on speed, with the numbers written down.

My professor put it this way in class. On October 7: *"Baseline is often human labor. That's usually quite costly and quite problematic in terms of quality."* On October 28: *"LLMs do not have to be perfect. They just have to be better and cheaper and faster than humans. And that gives them plenty opportunity to replace humans in the task."* And the warning that goes with it, the same night: *"Be careful what you benchmark."* Measure what the customer actually wants, not what is easy to count.

So before you can say whether AI replaces a job, you need three things: a real task, a measured human baseline on that task, and the model measured the same way on the same records. That is the whole project. We picked a task with money in it, built the dataset from public filings, measured people, measured a word-counting model, measured an LLM five ways, and priced every call.

## The task we picked, and the money in it

Every quarter, every public company releases its earnings in a press release. For the S&P 500 alone that is about 2,000 releases a year; the 110 companies we sampled produced 908 of them in two years. Someone reads each one and decides what it means for the stock. In the United States, that someone is often a financial analyst: 443,100 of them, a median wage of $103,570 a year, about $50 an hour before benefits (Bureau of Labor Statistics, Occupational Outlook Handbook, May 2025).

Our question: can a model read the first 400 words of a release and predict whether the stock beat the S&P 500 by more than 3% (up), trailed it by more than 3% (down), or stayed within 3% (flat) by the next close? If it can, the first read of every release costs cents instead of analyst minutes.

The model side we measured exactly: Gemini read a release for about half a cent in the zero-shot setting ($0.47 for 88 releases) and about 2.6 cents with ten examples per label ($2.27 for 88), in about ten seconds per call. The human side we have not timed yet; that is in the final project. As an illustration only: if a careful read takes five minutes at the BLS median wage, that is about $4 per release, several hundred times the model's cost. The course's cost model is where this becomes a business decision, not a demo: annual cost = volume × (cost per record + error rate × cost of an error). The error term is where the whole human-versus-AI question actually lives, so the rest of this page is about errors.

## What we measured

<p align="center">
  <img src="figures/zero-shot-confusion-and-cost.png" width="640" alt="Confusion matrix for Gemini zero-shot, with the cost and speed of each Gemini setting">
</p>

| Who or what read the release | Right | Notes |
|---|---|---|
| Two people, hand labels on 30 releases | **33%** | They agreed with each other 28 of 30 times (Cohen's kappa 0.88). They still matched the market only 10 of 30 times. |
| Always guess flat | 46.6% | the floor |
| TF-IDF + logistic regression (baseline) | 45.5% | macro F1 0.438; no better than the floor |
| Gemini zero-shot | **58.0%** | macro F1 0.577; cheapest setting, $0.47 |
| Gemini, 1 example per label | 53.4% | |
| Gemini, 5 per label | 51.1% | |
| Gemini, 10 per label | 48.9% | $2.27, about 21,000 input tokens per call |

Same 88 test releases for every model, one stratified split, one scorer, zero invalid answers. The humans labeled a different set of 30, chosen so that there were 10 of each label, so their 33% is a baseline for the task, not a head-to-head on the same records; the final project fixes that.

Then I re-ran all four Gemini settings two days later. 55 of the 352 answers changed. Zero-shot fell to 48.9% and ten examples rose to 52.3%. With 88 records the gaps between settings are noise, and a paired test of zero-shot against the baseline does not reach significance (p = 0.13). Both runs are in `results/`.

The one finding that matters most: the careful humans were right one time in three. The homebuilder release that both labelers called down (EPS down 42%, revenue down 5%) was followed by the stock beating the S&P 500 by 3.4%. The market reacts to what it expected, and the press release does not say what that was.

## Is AI going to replace humans here? Why, and why not

**Where the answer is in the text, the model already competes on cost and consistency.** Gilardi, Alizadeh and Kubli (PNAS, 2023) had ChatGPT label 6,183 tweets and news articles for relevance, stance, topic and frame: its zero-shot accuracy *"exceeds that of crowd workers by about 25 percentage points on average,"* its agreement with itself beat both crowd workers and trained annotators, and the cost was *"less than $0.003"* per annotation, about thirty times cheaper than Mechanical Turk. Our half a cent per release is the same order of magnitude.

**But reliability is task by task, and you only know by checking against people.** Pangakis, Wolken and Fasching (2023) ran GPT-4 on 27 annotation tasks across 11 social-science datasets: good overall, but precision or recall fell below 0.5 on 9 of the 27. Their title is the rule my course teaches: automated annotation with generative AI requires validation. A golden set labeled by two people, a kappa, a written rule for disagreements. Not once, every task.

**On our task, the answer is not in the text, for anyone.** Finance research has known this since Ball and Brown (1968) and Bernard and Thomas (1989): the price moves on the surprise against expectations, and keeps drifting in the direction of the surprise. The release carries the results, not the expectations. That is why two careful readers scored 33% and the best model scored 58% with a nine-point swing between runs. Neither replaces anything here. The task has to change before automation is worth discussing: label what the text can actually tell you (guidance raised or lowered, a beat or a miss against the stated consensus, the numbers themselves extracted), then measure again.

**A caution about the research itself.** A widely covered 2024 paper claimed GPT-4 beat human analysts at predicting the direction of earnings changes. In February 2025 the authors withdrew it after one of them found inconsistencies in the data and analyses. Measure before you believe, including the papers.

So my answer to "will AI replace the analyst?" is the one the evidence supports: it will take the reading, not the judgment, and only on tasks where the information needed is on the page and the human baseline has been measured first. Where the information is not on the page, it replaces nobody, because nobody can do the task from the page.

## What I would tell a business

If I were putting an LLM into an earnings workflow tomorrow, this is the plan, and every step comes from something we measured or something the course made us do:

1. **Measure the human baseline before the pilot.** Time a few analysts reading releases, score them against a label you trust, and write down minutes per record and accuracy. Without it there is nothing to beat.
2. **Build a golden set.** Two people label the same records from written rules, report Cohen's kappa, settle every disagreement with a rule you write down, and keep the record of why.
3. **Use the model for the first read, not the decision.** Within seconds of a filing, extract the numbers, flag guidance changes, route the release to the right analyst with a summary. That is where the cents replace minutes.
4. **Never let it call the market move.** Our data says the information is not there. A confident wrong label costs more than no label.
5. **Price every call and every error.** Tokens in and out, cost per record, the 50th and 95th percentile response time, and a cost for each kind of mistake. Our logs have every call.
6. **Test for stability and bias before trusting it.** Re-run the same inputs and count what changed; check whether extra text in the input moves the label; judge the output with a different model family and against the human labels, never with the same model twice.
7. **Keep a person in the loop where the model is unsure.** Route the cases where the baseline and the model disagree to a human, and track accuracy against the share handled automatically.

That plan is the business model of this course in one paragraph: the saving is real only when the human baseline is measured, the task is one the text can answer, and the errors are priced.

## What I learned

- **Where a label comes from matters more than which model you use.** A label from prices is cheap and repeatable. A label from people cost two teammates an evening and matched the market one time in three. Hand labels still earned their keep: they proved the guide was clear and gave us the human baseline the whole question rests on.
- **Report the run you saved, and say what a re-run did.** The same prompt does not answer the same way twice. A few points of difference between settings on 88 records is noise, and I would rather say so than claim a win.
- **More context is not free and not always better.** Ten examples per label multiplied the input tokens by 25 and lowered the score in the submitted run.
- **Evaluation discipline is most of the work.** One split for every model, one scorer, invalid answers counted as wrong, every call logged, a spend ceiling set before the first call, answers saved as they arrive.
- **Clean before you sample.** Nine of 300 records were not earnings releases, and a teammate found them by reading. The next round removes them before the sample is drawn and records the reason for every drop.

## How we did it, briefly

**The data.** Two Python scripts (written with Claude as my coding tool, in `data/`) pull every earnings filing (Form 8-K, Item 2.02, Exhibit 99.1) for 110 random S&P 500 companies from SEC EDGAR, 10 per sector with a fixed seed, and the daily closes for each stock and SPY from Yahoo Finance. 908 filings, 895 with a release, 617 released outside market hours, 616 after checks, a random sample of 300, and 291 after the nine non-earnings records were removed in the notebook (83 up, 73 down, 135 flat). Each record is the first 400 words, with the SEC header removed and any sentence describing the stock's own move taken out. The dataset text is not in this repository because the releases are company documents; the scripts rebuild it.

<p align="center">
  <img src="figures/records-per-label.png" width="520" alt="Records per label: up 83, down 73, flat 135">
</p>

**The labeling guide.** One sentence per label, one clear example and one boundary case each, a tie-breaking rule (exactly 3% is flat), and a timing rule (before the open: prior close to that day's close; after the close: to the next day's close). Two teammates labeled 30 releases independently from the guide alone. 28 of 30 agreed, kappa 0.88. The two disagreements each became a rule.

<p align="center">
  <img src="figures/labeler-agreement.png" width="440" alt="The agreement summary from the labeling sheet: 30 releases, 93% agreement, 45% expected by chance, kappa 0.88">
</p>

**The five models.** TF-IDF + logistic regression tuned by five-fold cross-validation on the training set only. Gemini (`gemini-3.7-flash`) with the same label definitions as the guide, asked for JSON only, zero-shot and then with 1, 5 and 10 nested examples per label drawn from the training set with a fixed seed. The zero-shot prompt:

```
You read company earnings press releases and predict how the stock reacted.

Choose the ONE label that best describes how the stock moved compared to the S&P 500,
from the close right before the release to the close of the next trading day.

Labels:
- up: after this release, the stock beat the S&P 500 by more than 3% from the close before the release to the close of the next trading day
- down: after this release, the stock did worse than the S&P 500 by more than 3% over the same window
- flat: the stock finished within 3% of the S&P 500 over the same window

Press release:
{text}

Return JSON only.
```

<p align="center">
  <img src="figures/results-table.png" width="720" alt="The results table printed by the notebook">
</p>

**My part.** I led the group and kept the two-week timeline; designed the label and wrote the guide and the plan; built the data pipeline; built the notebook from the course template and ran the setup, cleaning, the single split, the baseline, the shared scorer and the exports; and wrote and submitted the report. Teammates ran the Gemini steps, labeled the 30 records, reviewed the errors and wrote the first read of what it means.

## What's next

The final project in December scales this to 500 or more records with a fresh test set, bootstrap confidence intervals, a measured run-to-run variation, a timed human baseline on the same records as the models, a judge from a different model family, a test for whether extra text moves the label, and a cost model against the analyst wage, presented as a 12-minute business case.

## What's in this repository

| Path | What it is |
|---|---|
| `notebook/earnings_release_notebook.ipynb` | The submitted Colab notebook, run top to bottom with every output. Teammates' names are replaced with roles in this public copy. It reads the saved Gemini answers and makes no new calls. |
| `data/pull_earnings_data.py` | Finds each company's earnings filings on SEC EDGAR and pulls the daily closes from Yahoo Finance. No API keys. |
| `data/pull_press_release_text.py` | Downloads each press release (Exhibit 99.1) and converts it to plain text. |
| `data/tickers.csv` | The 110 companies sampled, with sector. |
| `results/results_table_submitted_run.csv` | The five-model table from the submitted run (Oct 25). |
| `results/results_table_second_run.csv` | The same table from the re-run two days later (Oct 27), not submitted, kept for honesty. |
| `results/gemini_call_log.csv` | Every Gemini call: setting, model, tokens in and out, cost, latency, attempts. |
| `results/gemini_predictions.csv` | Every Gemini answer by setting and record id, with the raw JSON. |
| `figures/` | The four pictures above, from the notebook and the labeling sheet. |

## Sources

- Gilardi, F., Alizadeh, M., Kubli, M. (2023). ChatGPT outperforms crowd workers for text-annotation tasks. *PNAS* 120(30). [doi:10.1073/pnas.2305016120](https://doi.org/10.1073/pnas.2305016120)
- Pangakis, N., Wolken, S., Fasching, N. (2023). Automated annotation with generative AI requires validation. [arXiv:2306.00176](https://arxiv.org/abs/2306.00176)
- Ball, R., Brown, P. (1968). An empirical evaluation of accounting income numbers. *Journal of Accounting Research* 6(2). [RePEc](https://econpapers.repec.org/RePEc:bla:joares:v:6:y:1968:i:2:p:159-178)
- Bernard, V., Thomas, J. (1989). Post-earnings-announcement drift: delayed price response or risk premium? *Journal of Accounting Research* 27. [RePEc](https://econpapers.repec.org/RePEc:bla:joares:v:27:y:1989:i::p:1-36)
- Kim, A., Muhn, M., Nikolaev, V. (2024). Financial statement analysis with large language models. [arXiv:2407.17866](https://arxiv.org/abs/2407.17866), withdrawn by the authors, February 2025.
- U.S. Bureau of Labor Statistics, Occupational Outlook Handbook, Financial Analysts, May 2025 wages. [bls.gov](https://www.bls.gov/ooh/business-and-financial/financial-analysts.htm)
- The professor's words are quoted from my own notes and the recordings of the October 7 and October 28 classes.

## AI use

The course requires an AI use note on every submission, and I keep the same rule here. Claude (Anthropic) wrote and ran the two data scripts under my direction, cleaned the data, built the Excel sheets and the first version of the notebook from the course template, and helped draft the report and this page. Gemini (Google) was the model under test. The labeling decisions, the calls on the two disagreements, the error review and every "what this shows" sentence were ours, and we checked every number against the saved files.

## Course

INFO 367, Applied Large Language Models for Business, Montclair State University, Fall 2026. Deliverable 1 of the team project, submitted October 27, 2026. Group project grade: 95/100.

## About me

I'm Muhammad Nabeel, a Business Analytics student at Montclair State University (BBA, graduating Fall 2026). I build things that have to be measured before they are believed: this project, a deployed RAG advising chatbot, a live systematic trading system, and [Ember](https://embernotebook.com), a private AI notebook for Mac that I designed and built and that went public in October 2026.

[GitHub profile](https://github.com/MrNabeel) · [LinkedIn](https://www.linkedin.com/in/mrnabeel1) · [Ember](https://embernotebook.com)
