import streamlit as st
from transcript_ingestion import ingest_transcript
from nlu_processing import TranscriptNLU
from info_extraction import extract_structured_insights
from phase_planning import plan_phases
from slide_text_generation import (
    generate_cover_slide,
    generate_objectives_slide,
    generate_pain_points_slide,
    generate_phases_overview_slide,
    generate_phase_slide,
    generate_expected_outcomes_slide,
    generate_next_steps_slide,
)
from slide_generation import (
    create_presentation,
    add_cover_slide,
    add_content_slide,
    add_horizontal_roadmap_slide,
    save_presentation,
)
from ai_integration import generate_slide_content_summary
import os
import logging

logging.basicConfig(level=logging.DEBUG)

def main():
    st.title("🛠️ Project Autodeck - Client Deck Generator")
    st.write("Upload a meeting transcript (.txt or .docx) to auto-generate a client-facing PowerPoint presentation.")

    uploaded_file = st.file_uploader("Choose a transcript file", type=["txt", "docx"])

    if uploaded_file is not None:
        st.success("File uploaded successfully!")
        with open("temp_transcript_file", "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Rename temp file with proper extension to help ingestion
        ext = os.path.splitext(uploaded_file.name)[1].lower()
        temp_file_with_ext = "temp_transcript_file" + ext
        os.rename("temp_transcript_file", temp_file_with_ext)

        transcript_text = ingest_transcript(temp_file_with_ext)

        nlu = TranscriptNLU()
        segmented = nlu.segment_transcript(transcript_text)

        insights = extract_structured_insights(segmented)

        phases = plan_phases([phase["title"] + ". " + phase.get("description", "") for phase in insights["phases"]], num_phases=6)

        # Add progress indicator for slide text generation
        progress_text = st.empty()
        progress_text.text("Generating slide content...")

        # Chunk transcript text by paragraphs for better semantic chunking
        paragraphs = [p.strip() for p in transcript_text.split('\\n\\n') if p.strip()]
        if not paragraphs:
            paragraphs = [transcript_text]  # fallback to whole text if no paragraphs

        # Generate slide texts with error handling and logging
        try:
            import time
            # Generate summaries for each paragraph chunk
            summarized_chunks = []
            total_paragraphs = len(paragraphs)

            def chunk_text(text, max_length=1000):
                """Simple chunking of text by max character length."""
                return [text[i:i+max_length] for i in range(0, len(text), max_length)]

            for i, para in enumerate(paragraphs):
                # Limit the number of chunks per paragraph to avoid long processing times
                chunks = chunk_text(para, max_length=1000)[:5]

                start_time = time.time()
                progress_text.text(f"Generating summary for paragraph {i+1} of {total_paragraphs}...")
                logging.debug(f"Generating summary for paragraph {i+1} with {len(chunks)} chunks")

                chunk_summaries = []
                for k, chunk in enumerate(chunks):
                    logging.debug(f"Generating summary for chunk {k+1} of paragraph {i+1}")
                    chunk_summary = generate_slide_content_summary(chunk)
                    if chunk_summary:
                        chunk_summary = chunk_summary.strip()
                        chunk_summaries.append(chunk_summary)
                    else:
                        st.warning(f"Skipping empty or invalid summary for chunk {k+1} of paragraph {i+1}")

                summary = ' '.join(chunk_summaries)
                elapsed = time.time() - start_time
                logging.debug(f"Summary generation for paragraph {i+1} took {elapsed:.2f} seconds")

                if summary:
                    # Postprocess summary: strip whitespace and remove duplicates
                    summary = summary.strip()
                    if summary and summary not in summarized_chunks:
                        summarized_chunks.append(summary)
                else:
                    st.warning(f"Skipping empty or invalid summary for paragraph {i+1}")

            # Combine summarized chunks for slide generation
            combined_summary = ' '.join(summarized_chunks)

            # Use enhanced AI-based slide text generation with combined summary
            cover_slide = generate_cover_slide(insights["client_name"])
            objectives_slide = generate_objectives_slide(insights["objectives"])
            pain_points_slide = generate_pain_points_slide(insights["pain_points"])
            phases_overview_slide = generate_phases_overview_slide(phases)
            expected_outcomes_slide = generate_expected_outcomes_slide(insights["expected_outcomes"])
            next_steps_slide = generate_next_steps_slide(["Contact sales team", "Schedule follow-up meeting"])
            progress_text.text("Slide content generated successfully.")
        except Exception as e:
            progress_text.text(f"Error generating slide content: {str(e)}")
            st.error(f"Error generating slide content: {str(e)}")
            return

        # Create presentation
        prs = create_presentation()
        logging.debug(f"Adding cover slide: {cover_slide}")
        add_cover_slide(prs, cover_slide["title"], cover_slide["subtitle"])
        logging.debug(f"Adding objectives slide: {objectives_slide}")
        add_content_slide(prs, objectives_slide["title"], objectives_slide["bullets"])
        logging.debug(f"Adding pain points slide: {pain_points_slide}")
        add_content_slide(prs, pain_points_slide["title"], pain_points_slide["bullets"])
        logging.debug(f"Adding phases overview slide: {phases_overview_slide}")
        add_horizontal_roadmap_slide(prs, phases_overview_slide["title"], phases)
        # Add one slide per phase
        for phase in phases:
            logging.debug(f"Adding phase slide: {phase}")
            add_content_slide(prs, phase["title"], [phase["description"]])
        logging.debug(f"Adding expected outcomes slide: {expected_outcomes_slide}")
        add_content_slide(prs, expected_outcomes_slide["title"], expected_outcomes_slide["bullets"])
        logging.debug(f"Adding next steps slide: {next_steps_slide}")
        add_content_slide(prs, next_steps_slide["title"], next_steps_slide["bullets"])

        output_path = "client_presentation.pptx"
        save_presentation(prs, output_path)
        logging.debug(f"Presentation saved to {output_path}")

        with open(output_path, "rb") as f:
            st.download_button(
                label="Download Presentation",
                data=f,
                file_name=output_path,
                mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
            )

import nest_asyncio

if __name__ == "__main__":
    try:
        import asyncio
        asyncio.get_running_loop()
    except RuntimeError:
        import nest_asyncio
        nest_asyncio.apply()
    main()
