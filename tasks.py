from crewai import Task
from agents import stock_data_analyst, investment_advisor

analyze_stock_task = Task(
    description="Analyze the stock performance for the ticker {{ticker}} with a focus on {{time_horizon}} investment strategy.",
    expected_output="Stock risk level, trend summary, and data insights",
    agent=stock_data_analyst
)

advise_investment_task = Task(
    description=(
        "Using the trend data {{trend_data}} and recent news {{news_context}}, "
        "provide a recommendation for {{ticker}} as a {{time_horizon}} investment."
    ),
    expected_output="Buy/Hold/Sell decision with rationale, factoring in recent news.",
    agent=investment_advisor
)
