from agents import Runner
from app.agent_config import build_agent


class RAGAgentOpenAI:
    def __init__(self, retriever, threshold=0.7):
        self.retriever = retriever
        self.threshold = threshold

    async def __call__(self, prompt):
        contexts, dist = self.retriever.get_top(prompt)
        if not contexts or dist is None or dist > self.threshold:
            return "Nie wiem. Ta informacja nie znajduje się w mojej bazie wiedzy."
        agent = build_agent(contexts[0])
        result = await Runner.run(agent, prompt)
        return result.final_output
