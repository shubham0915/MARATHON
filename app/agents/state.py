from typing import TypedDict, List, Annotated
import operator


class AgentState(TypedDict):
    # Using Annotated with operator.add ensures that messages 
    # are appended to the history rather than replaced.
    messages: Annotated[List[dict], operator.add] # AI, human ,tool(DB), system
    current_query: str # current querry to be searched
    documents: List[str] # document that retrieve from vector search  
    plan: List[str] # what i should do (planner, retriever, responder nodes) 
    #planner node - should i go for direct conversation or is it a techinal question and i should search for it in DB
    status: str # what i am doing right now 
    final_answer: str # final answer of the user


