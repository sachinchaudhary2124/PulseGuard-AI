import pandas as pd
import plotly.express as px


def create_latency_chart(logs):

    df = pd.DataFrame(logs)

    fig = px.line(
        df,
        x="timestamp",
        y="response_time_ms",
        color="endpoint",
        title="API Response Time Monitoring"
    )

    return fig