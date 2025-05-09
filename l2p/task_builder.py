"""
This file contains collection of functions for PDDL task generation purposes
"""

from .utils import *
from .llm import BaseLLM, require_llm
import time


class TaskBuilder:
    def __init__(
        self,
        objects: dict[str, str] = None,
        initial: list[dict[str, str]] = None,
        goal: list[dict[str, str]] = None,
    ):
        """
        Initializes a task builder object

        Args:
            objects (dict[str,str]): current dictionary of task objects in model
            initial (list[dict[str,str]]): current initial states in model
            goal (list[dict[str,str]]): current goal states in model
        """

        self.objects = objects
        self.initial = initial
        self.goal = goal

    """Extract functions"""

    @require_llm
    def extract_objects(
        self,
        model: BaseLLM,
        problem_desc: str,
        prompt_template: str,
        types: dict[str, str] = None,
        predicates: list[Predicate] = None,
        max_retries: int = 3,
    ) -> tuple[dict[str, str], str]:
        """
        Extracts objects with given predicates in current model

        Args:
            model (BaseLLM): BaseLLM
            problem_desc (str): problem description
            domain_desc (str): domain description
            prompt_template (str): prompt template class
            types (dict[str,str]): current types in model
            predicates (list[Predicate]): list of predicates in current model
            max_retries (int): max # of retries if failure occurs

        Returns:
            objects (dict[str,str]): dictionary of object types {name:description}
            llm_response (str): the raw string BaseLLM response
        """

        # replace prompt placeholders
        predicate_str = (
            "\n".join([f"- {pred['name']}: {pred['desc']}" for pred in predicates])
            if predicates
            else "No predicates provided."
        )
        types_str = "\n".join(types) if types else "No types provided."

        prompt_template = prompt_template.replace("{types}", types_str)
        prompt_template = prompt_template.replace("{predicates}", predicate_str)
        prompt_template = prompt_template.replace("{problem_desc}", problem_desc)

        # iterate through attempts in case of extraction failure
        for attempt in range(max_retries):
            try:
                model.reset_tokens()

                llm_response = model.query(prompt=prompt_template)  # get BaseLLM response

                # extract respective types from response
                objects = parse_objects(llm_response)

                return objects, llm_response

            except Exception as e:
                print(
                    f"Error encountered: {e}. Retrying {attempt + 1}/{max_retries}..."
                )
                time.sleep(2)  # add a delay before retrying

        raise RuntimeError("Max retries exceeded. Failed to extract objects.")

    @require_llm
    def extract_initial_state(
        self,
        model: BaseLLM,
        problem_desc: str,
        prompt_template: str,
        types: dict[str, str] = None,
        predicates: list[Predicate] = None,
        objects: dict[str, str] = None,
        initial: list[dict[str, str]] = None,
        goal: list[dict[str, str]] = None,
        max_retries: int = 3,
    ) -> tuple[list[dict[str, str]], str]:
        """
        Extracts initial states with given predicates, objects, and states in current model

        Args:
            model (BaseLLM): BaseLLM
            problem_desc (str): problem description
            domain_desc (str): domain description
            prompt_template (str): prompt template class
            types (dict[str,str]): current types in model
            predicates (list[Predicate]): current list of predicates in model
            objects (dict[str,str]): current dictionary of task objects in model
            initial (list[dict[str,str]]): current initial states in model
            goal (list[dict[str,str]]): current goal states in model
            max_retries (int): max # of retries if failure occurs

        Returns:
            initial (list[dict[str,str]]): list of dictionary of initial states [{predicate,params,neg}]
            llm_response (str): the raw string BaseLLM response
        """

        # replace prompt placeholders
        predicate_str = (
            format_predicates(predicates) if predicates else "No predicates provided."
        )
        types_str = "\n".join(types) if types else "No types provided."
        objects_str = (
            format_objects(objects) if objects else "No objects provided."
        )
        initial_str = (
            format_initial(initial) if initial else "No initial state provided."
        )
        goal_str = format_goal(goal) if goal else "No goal state provided."

        prompt_template = prompt_template.replace("{types}", types_str)
        prompt_template = prompt_template.replace("{predicates}", predicate_str)
        prompt_template = prompt_template.replace("{objects}", objects_str)
        prompt_template = prompt_template.replace("{initial_state}", initial_str)
        prompt_template = prompt_template.replace("{goal_state}", goal_str)
        prompt_template = prompt_template.replace("{problem_desc}", problem_desc)

        # iterate through attempts in case of extraction failure
        for attempt in range(max_retries):
            try:
                model.reset_tokens()

                llm_response = model.query(prompt=prompt_template)

                # extract respective types from response
                initial = parse_initial(llm_response)

                return initial, llm_response

            except Exception as e:
                print(
                    f"Error encountered: {e}. Retrying {attempt + 1}/{max_retries}..."
                )
                time.sleep(2)  # add a delay before retrying

        raise RuntimeError("Max retries exceeded. Failed to extract initial states.")

    @require_llm
    def extract_goal_state(
        self,
        model: BaseLLM,
        problem_desc: str,
        prompt_template: str,
        types: dict[str, str] = None,
        predicates: list[Predicate] = None,
        objects: dict[str, str] = None,
        initial: list[dict[str, str]] = None,
        goal: list[dict[str, str]] = None,
        max_retries: int = 3,
    ) -> tuple[list[dict[str, str]], str]:
        """
        Extracts goal states with given predicates, objects, and states in current model

        Args:
            model (BaseLLM): BaseLLM
            problem_desc (str): problem description
            domain_desc (str): domain description
            prompt_template (str): prompt template class
            types (dict[str,str]): current types in model
            predicates (list[Predicate]): current list of predicates in model
            objects (dict[str,str]): current dictionary of task objects in model
            initial (list[dict[str,str]]): current initial states in model
            goal (list[dict[str,str]]): current goal states in model
            max_retries (int): max # of retries if failure occurs

        Returns:
            goal (list[dict[str,str]]): list of dictionary of goal states [{predicate,params,neg}]
            llm_response (str): the raw string BaseLLM response
        """

        # replace prompt placeholders
        predicate_str = (
            format_predicates(predicates) if predicates else "No predicates provided."
        )
        types_str = "\n".join(types) if types else "No types provided."
        objects_str = (
            format_objects(objects) if objects else "No objects provided."
        )
        initial_str = (
            format_initial(initial) if initial else "No initial state provided."
        )
        goal_str = format_goal(goal) if goal else "No goal state provided."

        prompt_template = prompt_template.replace("{types}", types_str)
        prompt_template = prompt_template.replace("{predicates}", predicate_str)
        prompt_template = prompt_template.replace("{objects}", objects_str)
        prompt_template = prompt_template.replace("{initial_state}", initial_str)
        prompt_template = prompt_template.replace("{goal_state}", goal_str)
        prompt_template = prompt_template.replace("{problem_desc}", problem_desc)

        # iterate through attempts in case of extraction failure
        for attempt in range(max_retries):
            try:
                model.reset_tokens()

                llm_response = model.query(prompt=prompt_template)

                # extract respective types from response
                goal = parse_goal(llm_response)

                return goal, llm_response

            except Exception as e:
                print(
                    f"Error encountered: {e}. Retrying {attempt + 1}/{max_retries}..."
                )
                time.sleep(2)  # add a delay before retrying

        raise RuntimeError("Max retries exceeded. Failed to extract goal states.")

    @require_llm
    def extract_task(
        self,
        model: BaseLLM,
        problem_desc: str,
        prompt_template: str,
        types: dict[str, str] = None,
        predicates: list[Predicate] = None,
        actions: list[Action] = None,
        max_retries: int = 3,
    ) -> tuple[dict[str, str], list[dict[str, str]], list[dict[str, str]], str]:
        """
        Extracts whole task specification in current model

        Args:
            model (BaseLLM): BaseLLM
            problem_desc (str): problem description
            domain_desc (str): domain description
            prompt_template (str): prompt template class
            types (dict[str,str]): current types in model
            predicates (list[Predicate]): current list of predicates in model
            actions (list[Action]): current list of Action instances in model
            max_retries (int): max # of retries if failure occurs

        Returns:
            objects (dict[str,str]): dictionary of object types {name:description}
            initial (list[dict[str,str]]): list of dictionary of initial states [{predicate,params,neg}]
            goal (list[dict[str,str]]): list of dictionary of goal states [{predicate,params,neg}]
            llm_response (str): the raw string BaseLLM response
        """

        model.reset_tokens()

        # replace prompt placeholders
        predicate_str = (
            format_predicates(predicates) if predicates else "No predicates provided."
        )
        types_str = "\n".join(types) if types else "No types provided."
        action_str = (
            format_actions(actions=actions) if actions else "No actions provided."
        )

        prompt_template = prompt_template.replace("{types}", types_str)
        prompt_template = prompt_template.replace("{predicates}", predicate_str)
        prompt_template = prompt_template.replace("{actions}", action_str)
        prompt_template = prompt_template.replace("{problem_desc}", problem_desc)

        # iterate through attempts in case of extraction failure
        for attempt in range(max_retries):
            try:
                model.reset_tokens()

                llm_response = model.query(prompt=prompt_template)

                # extract respective types from response
                objects = parse_objects(llm_response)
                initial = parse_initial(llm_response)
                goal = parse_goal(llm_response)

                return objects, initial, goal, llm_response

            except Exception as e:
                print(
                    f"Error encountered: {e}. Retrying {attempt + 1}/{max_retries}..."
                )
                time.sleep(2)  # add a delay before retrying

        raise RuntimeError("Max retries exceeded. Failed to extract task.")

    # NOTE: This function is experimental and may be subject to change in future versions.
    @require_llm
    def extract_nl_conditions(
        self,
        model: BaseLLM,
        problem_desc: str,
        prompt_template: str,
        types: dict[str, str] = None,
        predicates: list[Predicate] = None,
        actions: list[Action] = None,
        objects: dict[str, str] = None,
        max_retries: int = 3,
    ) -> str:
        """
        Extracts initial and goal states in natural language

        Args:
            model (BaseLLM): BaseLLM
            problem_desc (str): problem description
            domain_desc (str): domain description
            prompt_template (str): prompt template class
            types (dict[str,str]): current types in model
            predicates (list[Predicate]): current list of predicates in model
            actions (list[Action]): current list of Action instances in model
            objects (dict[str,str]): current dictionary of task objects in model
            max_retries (int): max # of retries if failure occurs

        Returns:
            llm_response (str): the raw string BaseLLM response
        """

        # replace prompt placeholders
        predicate_str = (
            format_predicates(predicates) if predicates else "No predicates provided."
        )
        types_str = "\n".join(types) if types else "No types provided."
        objects_str = (
            format_objects(objects) if objects else "No objects provided."
        )
        action_str = (
            format_actions(actions=actions) if actions else "No actions provided."
        )

        prompt_template = prompt_template.replace("{problem_desc}", problem_desc)
        prompt_template = prompt_template.replace("{actions}", action_str)
        prompt_template = prompt_template.replace("{types}", types_str)
        prompt_template = prompt_template.replace("{predicates}", predicate_str)
        prompt_template = prompt_template.replace("{objects}", objects_str)

        # iterate through attempts in case of extraction failure
        for attempt in range(max_retries):
            try:
                model.reset_tokens()

                llm_response = model.query(prompt=prompt_template)

                return llm_response

            except Exception as e:
                print(
                    f"Error encountered: {e}. Retrying {attempt + 1}/{max_retries}..."
                )
                time.sleep(2)  # add a delay before retrying

        raise RuntimeError("Max retries exceeded. Failed to extract NL task states.")

    """Delete function"""

    def delete_objects(self, object: dict[str,str]):
        if self.objects is not None:
            self.objects = {
                var: type_ for var, type_ in self.objects.items() if var != object
            }

    def delete_initial_state(self, state: dict[str, str]):
        if self.initial is not None:
            self.initial = [s for s in self.initial if s != state]

    def delete_goal_state(self, state: dict[str, str]):
        if self.goal is not None:
            self.goal = [s for s in self.goal if s != state]

    """Set functions"""

    def set_objects(self, objects: dict[str, str]):
        self.objects = objects

    def set_initial(self, initial: list[dict[str, str]]):
        self.initial = initial

    def set_goal(self, goal: list[dict[str,str]]):
        self.goal = goal

    """Get functions"""

    def get_objects(self) -> dict[str, str]:
        return self.objects

    def get_initial(self) -> list[dict[str, str]]:
        return self.initial

    def get_goal(self) -> list[dict[str,str]]:
        return self.goal

    def generate_task(
        self, 
        domain_name: str, 
        problem_name: str, 
        objects: dict[str,str], 
        initial: list[dict[str,str]], 
        goal: list[dict[str,str]]
    ):
        # Write problem file
        desc = "(define\n"
        desc += f"   (problem {problem_name})\n"
        desc += f"   (:domain {domain_name})\n\n"
        desc += f"   (:objects \n{indent(format_objects(objects))}\n   )\n\n"
        desc += f"   (:init\n{indent(format_initial(initial))}\n   )\n\n"
        desc += f"   (:goal\n{indent(format_goal(goal))}\n   )\n\n"
        desc += ")"
        desc = desc.replace("AND", "and").replace("OR", "or")
        return desc
