# l2p : LLM-driven PDDL library kit

This library is a collection of tools for PDDL model generation extracted from natural language driven by large language models. This library is an expansion from the survey paper **Leveraging Large Language Models for Automated Planning and Model Construction: A Survey** (coming soon)

L2P is an offline, NL to PDDL system that supports domain-agnostic planning. It does this via creating an intermediate [PDDL](https://planning.wiki/guide/whatis/pddl) representation of the domain and task, which can then be solved by a classical planner. 

## Usage

This is the general setup to build domain predicates:
```python
import os
from l2p import *

domain_builder = DomainBuilder()

api_key = os.environ.get('OPENAI_API_KEY')
llm = OPENAI(model="gpt-4o-mini", api_key=api_key)

# retrieve prompt information
base_path='tests/usage/prompts/domain/'
domain_desc = load_file(f'{base_path}blocksworld_domain.txt')
extract_predicates_prompt = load_file(f'{base_path}extract_predicates.txt')
types = load_file(f'{base_path}types.json')
action = load_file(f'{base_path}action.json')

# extract predicates via LLM
predicates, llm_output = domain_builder.extract_predicates(
    model=llm,
    domain_desc=domain_desc,
    prompt_template=extract_predicates_prompt,
    types=types,
    nl_actions={action['action_name']: action['action_desc']}
    )

# format key info into PDDL strings
predicate_str = "\n".join([pred["clean"].replace(":", " ; ") for pred in predicates])

print(f"PDDL domain predicates:\n{predicate_str}")
```

Here is how you would setup a PDDL problem:
```python
from l2p.task_builder import TaskBuilder

task_builder = TaskBuilder()
    
api_key = os.environ.get('OPENAI_API_KEY')
llm = OPENAI(model="gpt-4o-mini", api_key=api_key)

# load in assumptions
problem_desc = load_file(r'tests/usage/prompts/problem/blocksworld_problem.txt')
extract_task_prompt = load_file(r'tests/usage/prompts/problem/extract_task.txt')
types = load_file(r'tests/usage/prompts/domain/types.json')
predicates_json = load_file(r'tests/usage/prompts/domain/predicates.json')
predicates: List[Predicate] = [Predicate(**item) for item in predicates_json]

# extract PDDL task specifications via LLM
objects, initial_states, goal_states, llm_response = task_builder.extract_task(
    model=llm,
    problem_desc=problem_desc,
    prompt_template=extract_task_prompt,
    types=types,
    predicates=predicates
    )

# format key info into PDDL strings
objects_str = task_builder.format_objects(objects)
initial_str = task_builder.format_initial(initial_states)
goal_str = task_builder.format_goal(goal_states)

# generate task file
pddl_problem = task_builder.generate_task(
    domain="blocksworld", 
    problem="blocksworld_problem", 
    objects=objects_str, 
    initial=initial_str, 
    goal=goal_str)

print(f"### LLM OUTPUT:\n {pddl_problem}")
```

Here is how you would setup a Feedback Mechanism:
```python
from l2p.feedback_builder import FeedbackBuilder

feedback_builder = FeedbackBuilder()
    
api_key = os.environ.get('OPENAI_API_KEY')
llm = OPENAI(model="gpt-4o-mini", api_key=api_key)

problem_desc = load_file(r'tests/usage/prompts/problem/blocksworld_problem.txt')
types = load_file(r'tests/usage/prompts/domain/types.json')
feedback_template = load_file(r'tests/usage/prompts/problem/feedback.txt')
predicates_json = load_file(r'tests/usage/prompts/domain/predicates.json')
predicates: List[Predicate] = [Predicate(**item) for item in predicates_json]
llm_response = load_file(r'tests/usage/prompts/domain/llm_output_task.txt')

objects, initial, goal, feedback_response = feedback_builder.task_feedback(
    model=llm, 
    problem_desc=problem_desc, 
    feedback_template=feedback_template, 
    feedback_type="llm", 
    predicates=predicates,
    types=types, 
    llm_response=llm_response)

print("FEEDBACK:\n", feedback_response)
```


## Installation and Setup
Currently, this repo has been tested for Python 3.11.10

You can set up a Python environment using either [Conda](https://conda.io) or [venv](https://docs.python.org/3/library/venv.html) and install the dependencies via the following steps.

**Conda**
```
conda create -n L2P python=3.11.10
conda activate L2P
pip install -r requirements.txt
```

**venv**
```
python3.11.10 -m venv env
source env/bin/activate
pip install -r requirements.txt
``` 

These environments can then be exited with `conda deactivate` and `deactivate` respectively. The instructions below assume that a suitable environemnt is active. 

**API keys**
L2P requires access to an LLM. L2P provides support for OpenAI's GPT-series models. To configure these, provide the necessary API-key in an environment variable.

**OpenAI**
```
export OPENAI_API_KEY='YOUR-KEY' # e.g. OPENAI_API_KEY='sk-123456'
```

Refer to [here](https://platform.openai.com/docs/quickstart) for more information.

**HuggingFace**

Additionally, we have included support for using Huggingface models. One can set up their environment like so:
```
parser = argparse.ArgumentParser(description="Define Parameters")
parser.add_argument('-test_dataset', action='store_true')
parser.add_argument("--temp", type=float, default=0.01, help = "temperature for sampling")
parser.add_argument("--max_len", type=int, default=4e3, help = "max number of tokens in answer")
parser.add_argument("--num_sample", type=int, default=1, help = "number of answers to sample")
parser.add_argument("--model_path", type=str, default="/path/to/model", help = "path to llm")
args = parser.parse_args()    

huggingface_model = HUGGING_FACE(model_path=args.model_path, max_tokens=args.max_len, temperature=args.temp)
```

**llm_builder.py** contains an abstract class and method for implementing any model classes in the case of other third-party LLM uses.

## Planner
For ease of use, our library contains submodule [FastDownward](https://github.com/aibasel/downward/tree/308812cf7315fe896dbcd319493277d82aa36bd2). Fast Downward is a domain-independent classical planning system that users can run their PDDL domain and problem files on. The motivation is that the majority of papers involving PDDL-LLM usage uses this library as their planner.

## Current Works Reconstructed Using L2P
The following are papers that have been reconstructed so far. This list will be updated in the future.

- [x] `NL2Plan`
- [x] `LLM+DM` 
- [x] `LLM+P`
- [x] `PROC2PDDL`

## Current Model Construction Works
This section provides a taxonomy of research within Model Construction. **More detailed overview coming soon**.

**Model Generation**

***Task Translation Frameworks***
- **"Structured, flexible, and robust: benchmarking and improving large language models towards more human-like behaviour in out-of-distribution reasoning tasks"** Collins et al. (2022) [paper](https://arxiv.org/abs/2205.05718) [code](https://github.com/collinskatie/structured_flexible_and_robust)
- **"Translating natural language to planning goals with large-language models"** Xie et al. (2023) [paper](https://arxiv.org/abs/2302.05128) [code](https://github.com/clear-nus/gpt-pddl)
- **"Faithful Chain-of-Thought Reasoning"** Lyu et al. (2023) [paper](https://arxiv.org/abs/2301.13379) [code](https://github.com/veronica320/faithful-cot)
- **"LLM+P: Empowering Large Language Models with Optimal Planning Proficiency"** Liu et al. (2023) [paper](https://arxiv.org/abs/2304.11477) [code](https://github.com/Cranial-XIX/llm-pddl)
- **"Dynamic Planning with a LLM"** Dagan et al. (2023) [paper](https://arxiv.org/abs/2308.06391) [code](https://github.com/itl-ed/llm-dp)
- **"TIC: Translate-Infer-Compile for accurate 'text to plan' using LLMs and logical intermediate representations"** Agarwal and Sreepathy (2024) [paper](https://arxiv.org/abs/2402.06608) [code](N/A)
- **"PDDLEGO: Iterative Planning in Textual Environments"** Zhang et al. (2024) [paper](https://arxiv.org/abs/2405.19793) [code](https://github.com/zharry29/nl-to-pddl)

***Domain Translation Frameworks***
- **"Learning adaptive planning representations with natural language guidance"** Wong et al. (2023) [paper](https://arxiv.org/abs/2312.08566) [code](N/A)
- **"Leveraging Pre-trained Large Language Models to Construct and Utilize World Models for Model-based Task Planning"** Guan et al. (2023) [paper](https://arxiv.org/abs/2305.14909) [code](https://github.com/GuanSuns/LLMs-World-Models-for-Planning)
- **"PROC2PDDL: Open-Domain Planning Representations from Texts"** Zhang et al. (2024) [paper](https://arxiv.org/abs/2403.00092) [code](https://github.com/zharry29/proc2pddl)

***Hybrid Translation Frameworks***
- **"There and Back Again: Extracting Formal Domains for Controllable Neurosymbolic Story Authoring"** Kelly et al. (2023) [paper](https://ojs.aaai.org/index.php/AIIDE/article/view/27502/27275) [code](https://github.com/alex-calderwood/there-and-back)
- **"DELTA: Decomposed Efficient Long-Term Robot Task Planning using Large Language Models"** Liu et al. (2024) [paper](https://arxiv.org/abs/2404.03275) [code](N/A)
- **"ISR-LLM: Iterative Self-Refined Large Language Model for Long-Horizon Sequential Task Planning"** Zhou et al. (2023) [paper](https://arxiv.org/abs/2308.13724) [code](https://github.com/ma-labo/ISR-LLM)
- **"Consolidating Trees of Robotic Plans Generated Using Large Language Models to Improve Reliability"** Sakib and Sun (2024) [paper](https://arxiv.org/abs/2401.07868) [code](N/A)
- **"NL2Plan: Robust LLM-Driven Planning from Minimal Text Descriptions"** Gestrin et al. (2024) [paper](https://arxiv.org/abs/2405.04215) [code](https://github.com/mrlab-ai/NL2Plan)
- **"Leveraging Environment Interaction for Automated PDDL Generation and Planning with Large Language Models"** Mahdavi et al. (2024) [paper](https://arxiv.org/abs/2407.12979) [code]()
- **"Generating consistent PDDL domains with Large Language Models"** Smirnov et al. (2024) [paper](https://arxiv.org/abs/2404.07751) [code](N/A)

**Model Editing and Benchmarking**
- **"Exploring the limitations of using large language models to fix planning tasks"** Gragera and Pozanco (2023) [paper](https://icaps23.icaps-conference.org/program/workshops/keps/KEPS-23_paper_3645.pdf) [code](N/A)
- **"Can LLMs Fix Issues with Reasoning Models? Towards More Likely Models for AI Planning"** Caglar et al. (2024) [paper](https://arxiv.org/abs/2311.13720) [code](N/A)
- **"Large Language Models as Planning Domain Generators"** Oswald et al. (2024) [paper](https://arxiv.org/abs/2405.06650) [code](https://github.com/IBM/NL2PDDL)
- **"Planetarium: A Rigorous Benchmark for Translating Text to Structured Planning Languages"** Zuo et al. (2024) [paper](https://arxiv.org/abs/2407.03321) [code](https://github.com/batsresearch/planetarium)

## Contact
Please contact `20mt1@queensu.ca` for questions, comments, or feedback about the L2P library.
