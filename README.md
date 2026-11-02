# Survivor Data Analysis and Winner Profiles - CS 410/510

*Group project - Data With Python, Portland State University (Spring 2026)*

We wanted to see what the numbers behind *Survivor* could tell us about winning. For this group project, we worked with five public datasets, cleaned and joined the data with pandas, and looked at how challenge wins, idols, votes, and time in the game relate to a contestant's outcome. The [Jupyter notebook](survivoR.ipynb) walks through our analysis, visualizations, and comparisons across seasons.

We also trained a Random Forest classifier and built a [Streamlit app](deployment/README.md) that lets you compare a custom cast of contestants based on their gameplay profiles. The model uses end-of-season statistics, so it's better for exploring what past winners have in common than predicting who will win a future season.

## Where to start

- [Survivor analysis notebook](survivoR.ipynb) - Data cleaning, exploratory analysis, visualizations, and machine learning.
- [Winner profile app](deployment/README.md) - Setup instructions for the Streamlit app and its saved model.
- [App source code](deployment/app.py) - The interface for entering contestants and comparing model scores.

## Project phases and documentation

These notes were used throughout the course and are kept here for reference:

- [Phase 1 - Data acquisition and cleaning](docs/PHASE1_DATA_ACQUISITION.md)
- [Phase 2 - Exploratory analysis and visualizations](docs/PHASE2_EDA_VISUALIZATIONS.md)
- [Phase 3 - Questions, findings, and reflection](docs/PHASE3_QUESTION_ANSWERING_CONCLUSION.md)
- [Phase 4 - Machine learning](docs/PHASE4_MACHINE_LEARNING.md)
- [Interactive model deployment](docs/INTERACTIVE_MODEL_DEPLOYMENT.md)

## Course policy and team workflow

The original project was collaborative, so I kept the documentation that helped us work on the same notebook and follow course requirements:

- [Course policy](docs/COURSE_POLICY.md) - Academic integrity, code standards, source attribution, and permitted AI assistance.
- [AI assistance disclosure](docs/AI_DISCLOSURE.md) - How AI was used for repository documentation and tooling. Graded notebook work has its own source-attribution requirements.
- [Notebook collaboration workflow](docs/JUPYTER_TEAM_WORKFLOW.md) - Git hooks, output stripping, and working together on Jupyter files.
- [Notebook recovery notes](docs/NOTEBOOK_RECOVERY.md) - Fixing a notebook after a difficult merge.
- [Assistant guidelines](AGENTS.md) - Project-specific guidance for development tools.

The [app README](deployment/README.md) has instructions for running the predictor locally. The original datasets are credited in the [project notebook](survivoR.ipynb).
