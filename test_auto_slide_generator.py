import os
import sys
import pytest
import pandas as pd

# Add the auto-slide-generator directory to sys.path for imports
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

import data_ingestion
import data_processing
import ai_integration
import slide_generation

def test_read_csv():
    # Create a sample CSV file
    sample_csv = 'test_sample.csv'
    df_original = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
    df_original.to_csv(sample_csv, index=False)

    df = data_ingestion.read_csv(sample_csv)
    assert df.equals(df_original)

    os.remove(sample_csv)

def test_read_excel():
    # Test reading the provided Excel file
    excel_file = os.path.join(os.path.dirname(__file__), 'CALE 2010 SH 042417.xls')
    if os.path.exists(excel_file):
        df = data_ingestion.read_excel(excel_file)
        assert not df.empty
    else:
        pytest.skip("Excel file for testing not found.")

def test_summarize_data():
    df = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
    summary = data_processing.summarize_data(df)
    assert 'Columns' in summary
    assert 'Number of rows' in summary

def test_generate_slide_content_summary():
    summary = {'columns': ['A', 'B'], 'num_rows': 2}
    content = ai_integration.generate_slide_content_summary(summary)
    assert isinstance(content, str)

def test_slide_generation():
    prs = slide_generation.create_presentation()
    slide_generation.add_title_slide(prs, "Test Title", "Test Subtitle")
    slide_generation.add_content_slide(prs, "Test Content", ["Point 1", "Point 2"])
    output_file = "test_presentation.pptx"
    slide_generation.save_presentation(prs, output_file)
    assert os.path.exists(output_file)
    os.remove(output_file)
