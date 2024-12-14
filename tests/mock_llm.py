class MockLLM:
    def __init__(self, responses):
        """
        Initialize with a list of responses to simulate the LLM's outputs.
        """
        self.responses = responses
        self.current_index = 0

    def query(self, prompt):
        """
        Simulates the LLM query response.
        """
        response = self.responses[self.current_index]
        self.current_index += 1
        return response

    def reset_tokens(self):
        """
        Placeholder for resetting tokens; not needed for testing.
        """
        pass
