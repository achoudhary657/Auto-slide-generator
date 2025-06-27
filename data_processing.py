"""
Module for data processing and summarization.
"""

def summarize_data(df):
    """
    Summarize the DataFrame into a human-readable string.
    """
    try:
        columns = df.columns.tolist()
        num_rows = len(df)
        data_types = df.dtypes.apply(lambda x: x.name).to_dict()
        head = df.head(5).to_dict(orient='records')
        description = df.describe(include='all').to_dict()

        summary_lines = []
        summary_lines.append(f"Columns: {columns}")
        summary_lines.append(f"Number of rows: {num_rows}")
        summary_lines.append("Data types:")
        for col, dtype in data_types.items():
            summary_lines.append(f"  - {col}: {dtype}")
        summary_lines.append("First 5 rows:")
        for i, row in enumerate(head, 1):
            row_str = ", ".join(f"{k}: {v}" for k, v in row.items())
            summary_lines.append(f"  {i}. {row_str}")
        summary_lines.append("Summary statistics:")
        for col, stats in description.items():
            summary_lines.append(f"  {col}:")
            for stat_name, stat_value in stats.items():
                summary_lines.append(f"    {stat_name}: {stat_value}")

        return "\\n".join(summary_lines)
    except Exception as e:
        return f"Error summarizing data: {str(e)}"
