"""
Main script to run the automated slide deck generator.
"""

from data_ingestion import read_excel, read_csv, read_sql_file, read_database_table
from data_processing import summarize_data
from ai_integration import generate_slide_content_summary
from slide_generation import create_presentation, add_title_slide, add_content_slide, save_presentation

def main():
    # Example usage with a CSV file
    data_file = 'sample_data.csv'  # Replace with actual data file path
    import os
    data_file = os.path.join(os.path.dirname(__file__), 'CALE 2010 SH 042417.xls')
    if os.path.exists(data_file):
        df = read_excel(data_file)
    else:
        print(f"Data file not found: {data_file}")
        return

    # Process data
    summary = summarize_data(df)

    # Generate slide content using AI integration
    slide_content = generate_slide_content_summary(summary)

    # Create presentation
    prs = create_presentation()
    add_title_slide(prs, "Automated Slide Deck", "Generated from Data")
    add_content_slide(prs, "Data Summary", summary.split("\\n"))
    add_content_slide(prs, "AI Generated Insights", [slide_content])

    # Save presentation
    output_file = os.path.join(os.path.dirname(__file__), 'output_presentation.pptx')
    save_presentation(prs, output_file)
    print(f"Presentation saved to {output_file}")

if __name__ == "__main__":
    main()
