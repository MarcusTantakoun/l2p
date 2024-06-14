"""
This file contains collection of functions for PDDL generation purposes
"""

## type extraction
def extract_type(description):
    """
    Extract types from the domain description using the LLM.
    
    Args:
    - domain_description (str): The text description of the PDDL domain.
    
    Returns:
    - List of types with descriptive comments.
    """
    prompt = f"Extract types from the following domain description:\n\n{description}\n\nList the types along with descriptive comments."
    response = llm_query(prompt)
    return response.strip()

## hierarchy type organzation
def extract_type_hierarchy():
    pass

## NL action extraction
def extract_NL_action():
    # given NL domain description + types, output (in NL) suggested actions to be created
    # this function is purely just for helping the user (and LLM) structure their actions easier
    pass

## action-aquisition pipeline
"""
This pipeline is split into (5) sections:
    1. User provides NL of simple action to LLM to produce necessary predicates stored in a list
    2. User reviews/modifies predicates as needed. Loops until user permits.
    3. User provided more precise NL description of action using refined predicates.
        LLM generates formal PDDL action model (to be stored in a list)
    4. User reviews/modifies PDDL action model as needed
    5. After each action has been defined, all actions are generated again w/
        full list of generated predicates


    # I WANT TO ADD IN AUTO-CHECKLIST FOR EACH STEP (give option)
"""

def extract_action(domain_description, initial_predicates=None, autocheck=False):
    """
    Complete action acquisition pipeline.
    
    Args:
    - domain_description (str): The text description of the PDDL domain.
    - initial_predicates (str, optional): Initial list of predicates if available.
    
    Returns:
    - Updated list of predicates and refined PDDL actions.
    """
    predicates_list = initial_predicates if initial_predicates else []
    actions_list = []

    while True:

        # we want to overcome limitations of context window (while maintaining low conversation 
        # history token usage). Therefore, we just include the outputted predicate in the reprompt stage

        # step 1:
        user_input = input("Describe the action in simple natural language (e.g., 'A robot moves from one location to another.'): ")
        # CHANGE PROMPT SO THAT USER CAN CUSTOMIZE
        prompt = f"The current PDDL domain is: {domain_description}\n\nUser: {user_input}\n\nLLM: Generate necessary predicates for this action."
        predicates = llm_query(prompt)
        predicates_list.append(predicates.strip())
        print("Generated Predicates:\n", predicates)

        # step 2:
        while True:
            user_review = input("Review the predicates and add input if needed (or type 'okay' to proceed): ")
            if user_review.lower() == "okay":
                break
            # CHANGE PROMPT SO THAT USER CAN CUSTOMIZE
            prompt = f"The current predicates are: {predicates_list}\n\nUser: {user_review}\n\nLLM: Modify or add predicates based on the user's input."
            predicates = llm_query(prompt)
            predicates_list[-1] = predicates.strip() # update last precdicates set
            print("Updated Predicates:\n", predicates)

        # step 3:
        user_input = input("Describe the action more precisely with refined predicates (e.g., 'The robot moves if it is at a location and the destination is connected.'): ")
        all_predicates = " ".join(predicates_list)
        # CHANGE PROMPT SO THAT USER CAN CUSTOMIZE
        prompt = f"The current predicates are: {all_predicates}\n\nUser: {user_input}\n\nLLM: Generate the formal PDDL action model for this description."
        action_model = llm_query(prompt)
        actions_list.append(action_model.strip())
        print("Generated PDDL Action Model:\n", action_model)

        # step 4:
        while True:
            user_review = input("Review the PDDL action model and add input if needed (or type 'okay' to proceed): ")
            if user_review.lower() == "okay":
                break
            # CHANGE PROMPT SO THAT USER CAN CUSTOMIZE
            prompt = f"The current PDDL action model is: {action_model}\n\nUser: {user_review}\n\nLLM: Modify or add to the PDDL action model based on the user's input."
            action_model = llm_query(prompt)
            actions_list[-1] = action_model.strip()
            print("Updated PDDL Action Model:\n", action_model)

        user_input = input("Would you like to make any other changes? (yes\no): ")
        if user_input.lower() != "yes":
            break

    # re-run pipeline w/ full list of generate predicates
    print("\nRe-running pipeline")

    refined_actions_list = []
    for action in actions_list:
        prompt = f"The current PDDL domain is: {domain_description}\n\nThe full list of predicates are: {all_predicates}\n\nAction: {action}\n\nLLM: Generate the formal PDDL action model considering all predicates."
        refined_action = llm_query(prompt)
        refined_actions_list.append(refined_action.strip())
        print("Refined PDDL Action Model:\n", refined_action)

        while True:
            user_review = input("Review the refined PDDL action model and add input if needed (or type 'okay' to proceed): ")
            if user_review.lower() == "okay":
                break
            prompt = f"The current PDDL action model is: {refined_action}\n\nUser: {user_review}\n\nLLM: Modify or add to the PDDL action model based on the user's input."
            refined_action = llm_query(prompt)
            refined_actions_list[-1] = refined_action.strip()
            print("Updated Refined PDDL Action Model:\n", refined_action)

    return predicates_list, refined_actions_list




## auto-checklist


# get functions
def get_types():
    pass

def get_type_hierarchy():
    pass

def get_actions():
    pass

# retrieve checklist - displays to user the feedbacks
def get_type_checklist():
    pass

def get_hierarchy_checklist():
    pass

def get_action_checklist():
    pass

if __name__ == "__main__":
    pass