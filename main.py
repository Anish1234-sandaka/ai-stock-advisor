from crewai import Crew
from tasks import analyze_stock_task, advise_investment_task

crew = Crew(
    agents=[analyze_stock_task.agent, advise_investment_task.agent],
    tasks=[analyze_stock_task, advise_investment_task],
    verbose=True
)

