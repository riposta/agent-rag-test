from agents import Agent

def build_agent(context:str):
    return Agent(
        name="RAG Agent",
        instructions=f"Jesteś ekspertem. Odpowiadaj tylko na podstawie poniższego kontekstu. Jeżeli nie znajdziesz odpowiedzi, powiedz: 'Nie wiem'.\n\nKontekst:\n{context}"
    )
