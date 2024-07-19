from l2p.prompt_builder import PromptBuilder
from l2p.feedback_builder import Feedback_Builder
from l2p.domain_builder import Domain_Builder
from l2p.task_builder import Task_Builder
from l2p.llm_builder import LLM_Chat, get_llm
from l2p.utils.pddl_parser import prune_predicates, prune_types, extract_types
from l2p.utils.pddl_types import Action, Predicate
from l2p.utils.pddl_validator import Syntax_Validator
import os, json

# micro-functions
def format_json_output(data):
        return json.dumps(data, indent=4)

def open_file(file_path):
    with open(file_path, 'r') as file:
        file = file.read().strip()
    return file

def run_granular_action_pipeline(
        model: LLM_Chat,
        domain_desc: str,
        param_prompt: PromptBuilder,
        precondition_prompt: PromptBuilder,
        effects_prompt: PromptBuilder,
        nl_actions: dict[str,str]
        ):
    predicates = []
    max_iters = 2
    for iter in range(max_iters):

        actions = []
        current_preds = len(predicates)

        for action_name, action_desc in nl_actions.items():
            params = domain_builder.extract_parameters(
                model=model,
                domain_desc=domain_desc,
                prompt_template=param_prompt.generate_prompt(),
                action_name=action_name,
                action_desc=action_desc,
                types=domain_builder.get_type_hierarchy()
            )

            preconditions, new_predicates = domain_builder.extract_preconditions(
                model=model,
                domain_desc=domain_desc,
                prompt_template=precondition_prompt.generate_prompt(),
                action_name=action_name,
                action_desc=action_desc,
                params=params,
                predicates=predicates
            )
            predicates.extend(new_predicates)

            effects, new_predicates = domain_builder.extract_effects(
                model=model,
                domain_desc=domain_desc,
                prompt_template=effects_prompt.generate_prompt(),
                action_name=action_name,
                action_desc=action_desc,
                params=params,
                precondition=preconditions,
                predicates=predicates
            )
            predicates.extend(new_predicates)
            action = {"name": action_name, "parameters": params, "preconditions": preconditions, "effects": effects}
            actions.append(action)

        if len(predicates) == current_preds:
            print("No new predicates created. Stopping action construction.")
            break

    return actions, predicates

def run_compact_action_pipeline(model: LLM_Chat, domain_builder: Domain_Builder, prompt: PromptBuilder, nl_actions: dict[str,str]):
    # action-by-action method used in Guan et al. (2023): https://arxiv.org/abs/2305.14909
    predicates = []
    actions = []
    # iterate through each action, dynamically create new predicates
    for action_name, action_desc in nl_actions.items():
        action, new_predicates = domain_builder.extract_pddl_action(
            model=model,
            prompt_template=prompt.generate_prompt(),
            action_name=action_name,
            action_desc=action_desc,
            predicates=predicates
        )
        actions.append(action)
        predicates.extend(new_predicates)
        predicates = prune_predicates(predicates=predicates, actions=actions)

    return actions, predicates

def run_granular_task_pipeline(
        model: LLM_Chat,
        problem_desc: str,
        domain_desc: str,
        object_extraction_prompt: PromptBuilder,
        initial_extraction_prompt: PromptBuilder,
        goal_extraction_prompt: PromptBuilder,
        types: dict[str,str],
        predicates: list[Predicate]
        ) -> tuple[str,str,str]:
    
    objects = task_builder.extract_objects(
        model=model,
        problem_desc=problem_desc,
        domain_desc=domain_desc,
        prompt_template=object_extraction_prompt.generate_prompt(),
        type_hierarchy=types,
        predicates=predicates
        )

    initial = task_builder.extract_initial_state(
        model=model,
        problem_desc=problem_desc,
        domain_desc=domain_desc,
        prompt_template=initial_extraction_prompt.generate_prompt(),
        type_hierarchy=types,
        predicates=predicates,
        objects=objects
        )

    goal = task_builder.extract_goal_state(
        model=model,
        problem_desc=problem_desc,
        domain_desc=domain_desc,
        prompt_template=goal_extraction_prompt.generate_prompt(),
        type_hierarchy=types,
        predicates=predicates,
        objects=objects
        )
    
    objects = "\n".join([f"{obj} - {type}" for obj, type in objects.items()])
    return objects, initial, goal
    
def run_compact_task_pipeline(
        model: LLM_Chat,
        problem_desc: str, 
        domain_desc: str, 
        task_extraction_prompt: PromptBuilder, 
        types: dict[str,str], 
        predicates: list[Predicate],
        actions: list[Action]
        ) -> tuple[str,str,str]:

    objects, initial, goal = task_builder.extract_task(
        model=model,
        problem_desc=problem_desc,
        domain_desc=domain_desc,
        prompt_template=task_extraction_prompt.generate_prompt(),
        types=types,
        predicates=predicates,
        actions=actions
        )

    objects = "\n".join([f"{obj} - {type}" for obj, type in objects.items()])
    return objects, initial, goal

def open_examples(examples_dir):
    example_files = [f for f in os.listdir(examples_dir) if os.path.isfile(os.path.join(examples_dir, f))]
    examples = [open_file(os.path.join(examples_dir, f)) for f in example_files]
    return examples

if __name__ == "__main__":

    # THIS IS IMPORTANT TO LOOK INTO
    unsupported_keywords = ['object']

    # model = get_llm("gpt-3.5-turbo-0125")
    # model = get_llm("gpt-4o")
    model = get_llm("gpt-4o-mini")

    # instantiate domain builder class
    domain_desc = open_file('data/domains/household.txt')
    domain_builder = Domain_Builder(types=None,type_hierarchy=None,predicates=None,nl_actions=None,pddl_actions=None)

    problem_desc = open_file("data/problems/blocksworld_p1.txt")
    task_builder = Task_Builder(objects=None, initial=None, goal=None)

    # open and create type extraction prompt builder class
    role_desc = open_file('data/prompt_templates/type_extraction/role.txt')
    tech_desc = open_file('data/prompt_templates/type_extraction/technique.txt')
    ex_desc = open_examples('data/prompt_templates/type_extraction/examples/')
    task_desc = open_file('data/prompt_templates/type_extraction/task.txt')
    type_extraction_prompt = PromptBuilder(role_desc, tech_desc, ex_desc, task_desc)

    # open and create type hierarchy prompt builder class
    role_desc = open_file('data/prompt_templates/hierarchy_construction/role.txt')
    tech_desc = open_file('data/prompt_templates/hierarchy_construction/technique.txt')
    ex_desc = open_examples('data/prompt_templates/hierarchy_construction/examples/')
    task_desc = open_file('data/prompt_templates/hierarchy_construction/task.txt')
    type_hierarchy_prompt = PromptBuilder(role_desc, tech_desc, ex_desc, task_desc)

    # open and create NL action prompt builder class      
    role_desc = open_file('data/prompt_templates/action_extraction/role.txt')
    tech_desc = open_file('data/prompt_templates/action_extraction/technique.txt')
    ex_desc = open_examples('data/prompt_templates/action_extraction/examples/')
    task_desc = open_file('data/prompt_templates/action_extraction/task.txt')
    nl_action_extraction_prompt = PromptBuilder(role_desc, tech_desc, ex_desc, task_desc)

    # open and create PDDL action prompt builder class
    role_desc = open_file('data/prompt_templates/action_construction/extract_action/role.txt')
    tech_desc = open_file('data/prompt_templates/action_construction/extract_action/technique.txt')
    ex_desc = open_examples('data/prompt_templates/action_construction/extract_action/examples/')
    task_desc = open_file('data/prompt_templates/action_construction/extract_action/task.txt')
    pddl_action_extraction_prompt = PromptBuilder(role_desc, tech_desc, ex_desc, task_desc)

    role_desc = open_file('data/prompt_templates/action_construction/extract_params/role.txt')
    tech_desc = open_file('data/prompt_templates/action_construction/extract_params/technique.txt')
    ex_desc = open_examples('data/prompt_templates/action_construction/extract_params/examples/')
    task_desc = open_file('data/prompt_templates/action_construction/extract_params/task.txt')
    pddl_param_extraction_prompt = PromptBuilder(role_desc, tech_desc, ex_desc, task_desc)

    role_desc = open_file('data/prompt_templates/action_construction/extract_preconditions/role.txt')
    tech_desc = open_file('data/prompt_templates/action_construction/extract_preconditions/technique.txt')
    ex_desc = open_examples('data/prompt_templates/action_construction/extract_preconditions/examples/')
    task_desc = open_file('data/prompt_templates/action_construction/extract_preconditions/task.txt')
    pddl_precondition_extraction_prompt = PromptBuilder(role_desc, tech_desc, ex_desc, task_desc)

    role_desc = open_file('data/prompt_templates/action_construction/extract_effects/role.txt')
    tech_desc = open_file('data/prompt_templates/action_construction/extract_effects/technique.txt')
    ex_desc = open_examples('data/prompt_templates/action_construction/extract_effects/examples/')
    task_desc = open_file('data/prompt_templates/action_construction/extract_effects/task.txt')
    pddl_effects_extraction_prompt = PromptBuilder(role_desc, tech_desc, ex_desc, task_desc)

    role_desc = open_file('data/prompt_templates/task_extraction/extract_objects/role.txt')
    tech_desc = open_file('data/prompt_templates/task_extraction/extract_objects/technique.txt')
    ex_desc = open_examples('data/prompt_templates/task_extraction/extract_objects/examples/')
    task_desc = open_file('data/prompt_templates/task_extraction/extract_objects/task.txt')
    object_extraction_prompt = PromptBuilder(role_desc, tech_desc, ex_desc, task_desc)

    role_desc = open_file('data/prompt_templates/task_extraction/extract_initial/role.txt')
    tech_desc = open_file('data/prompt_templates/task_extraction/extract_initial/technique.txt')
    ex_desc = open_examples('data/prompt_templates/task_extraction/extract_initial/examples/')
    task_desc = open_file('data/prompt_templates/task_extraction/extract_initial/task.txt')
    initial_extraction_prompt = PromptBuilder(role_desc, tech_desc, ex_desc, task_desc)

    role_desc = open_file('data/prompt_templates/task_extraction/extract_goal/role.txt')
    tech_desc = open_file('data/prompt_templates/task_extraction/extract_goal/technique.txt')
    ex_desc = open_examples('data/prompt_templates/task_extraction/extract_goal/examples/')
    task_desc = open_file('data/prompt_templates/task_extraction/extract_goal/task.txt')
    goal_extraction_prompt = PromptBuilder(role_desc, tech_desc, ex_desc, task_desc)

    # open and create compact action prompt builder class
    role_desc = open_file('data/prompt_templates/task_extraction/extract_task/role.txt')
    tech_desc = open_file('data/prompt_templates/task_extraction/extract_task/technique.txt')
    ex_desc = open_examples('data/prompt_templates/task_extraction/extract_task/examples/')
    task_desc = open_file('data/prompt_templates/task_extraction/extract_task/task.txt')
    task_extraction_prompt = PromptBuilder(role_desc, tech_desc, ex_desc, task_desc)

    # extract types
    print("Extracted types output:\n")
    types, response = domain_builder.extract_type(model, domain_desc, type_extraction_prompt.generate_prompt())
    domain_builder.set_types(types=types)
    print("Types: ", format_json_output(domain_builder.get_types()))


    feedback_template = open_file('data/prompt_templates/type_extraction/feedback.txt')
    feedback_builder = Feedback_Builder()
    
    feedback = feedback_builder.type_feedback(model, domain_desc, feedback_template, types, response)
    print("FEEDBACK:\n", feedback)
    
    # extract type hierarchy
    print("\n\n---------------------------------\n\nType hierarchy output:\n")
    type_hierarchy, response = domain_builder.extract_type_hierarchy(model, domain_desc, type_hierarchy_prompt.generate_prompt(), domain_builder.get_types())
    domain_builder.set_type_hierarchy(type_hierarchy=type_hierarchy)
    print(format_json_output(type_hierarchy))

    feedback_template = open_file('data/prompt_templates/hierarchy_construction/feedback.txt')
    feedback = feedback_builder.type_hierarchy_feedback(model, domain_desc, feedback_template, type_hierarchy, response)
    print("FEEDBACK:\n", feedback)

    # # extract NL action descriptions
    # print("\n\n---------------------------------\n\nNatural language action output:\n")
    # nl_actions = domain_builder.extract_nl_actions(model, domain_desc, nl_action_extraction_prompt.generate_prompt(), type_hierarchy)
    # domain_builder.set_nl_actions(nl_actions)
    # for i in nl_actions: print(i)
    
    # # extract PDDL formatted actions
    # print("\n\n---------------------------------\n\nPDDL action output:\n")

    # # GRANULAR ACTION EXTRACTION PIPELINE
    # actions, predicates = run_granular_action_pipeline(
    #     model=model, 
    #     domain_desc=domain_desc, 
    #     param_prompt=pddl_param_extraction_prompt,
    #     precondition_prompt=pddl_precondition_extraction_prompt,
    #     effects_prompt=pddl_effects_extraction_prompt,
    #     nl_actions=nl_actions
    #     )
    
    # # COMPACT ACTION EXTRACTION PIPELINE
    # # actions, predicates = run_compact_action_pipeline(
    # #     model=model, 
    # #     domain_builder=domain_builder, 
    # #     prompt=pddl_action_extraction_prompt,
    # #     nl_actions=nl_actions
    # # )

    # predicates = prune_predicates(predicates=predicates, actions=actions) # discard predicates not found in action models + duplicates
    # types = extract_types(type_hierarchy) # retrieve types
    # pruned_types = prune_types(types=types, predicates=predicates, actions=actions) # discard types not in predicates / actions + duplicates

    # pruned_types = {name: description for name, description in pruned_types.items() if name not in unsupported_keywords} # remove unsupported words

    # predicate_str = "\n".join([pred["clean"].replace(":", " ; ") for pred in predicates])
    # types_str = "\n".join(pruned_types)

    # requirements = [':strips',':typing',':equality',':negative-preconditions',':disjunctive-preconditions',':universal-preconditions',':conditional-effects']
    # print("[DOMAIN]\n") 
    # pddl_domain = domain_builder.generate_domain(
    #     domain="test_domain", 
    #     requirements=requirements,
    #     types=types_str,
    #     predicates=predicate_str,
    #     actions=actions
    #     )
    
    # print(pddl_domain)

    # domain_file = "data/domain.pddl"
    # with open(domain_file, "w") as f:
    #     f.write(pddl_domain)
    # print(f"PDDL domain written to {domain_file}")

    # print("\n\n---------------------------------\n\nPDDL task extraction:\n")

    # # GRANULAR TASK PIPELINE
    # objects, initial_states, goal_states = run_granular_task_pipeline(
    #      model=model, 
    #      problem_desc=problem_desc, 
    #      domain_desc=domain_desc, 
    #      object_extraction_prompt=object_extraction_prompt,
    #      initial_extraction_prompt=initial_extraction_prompt,
    #      goal_extraction_prompt=goal_extraction_prompt,
    #      types=pruned_types,
    #      predicates=predicates
    # )

    # # COMPACT TASK PIPELINE
    # # objects, initial_states, goal_states = run_compact_task_pipeline(
    # #      model=model, 
    # #      problem_desc=problem_desc, 
    # #      domain_desc=domain_desc, 
    # #      task_extraction_prompt=task_extraction_prompt,
    # #      types=pruned_types,
    # #      predicates=predicates,
    # #      actions=actions
    # # )

    # print("[TASK]\n") 
    # pddl_problem = task_builder.generate_task(domain="test_domain", objects=objects, initial=initial_states, goal=goal_states)
    # print(pddl_problem)

    # problem_file = "data/problem.pddl"
    # with open(problem_file, "w") as f:
    #     f.write(pddl_problem)
    # print(f"PDDL domain written to {problem_file}")