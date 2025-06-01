def generate_interview_pdf(filepath, candidate, questions, answers, emotions, postures, sentiments):
    from fpdf import FPDF

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="Interview Feedback Report", ln=True, align="C")
    pdf.ln(10)

    for i, (q, a, emo, pos, sent) in enumerate(zip(questions, answers, emotions, postures, sentiments)):
        pdf.multi_cell(0, 10, f"Q{i+1}: {q}")
        pdf.multi_cell(0, 10, f"A{i+1}: {a}")
        pdf.multi_cell(0, 10, f"Emotion: {emo}")
        pdf.multi_cell(0, 10, f"Posture: {pos}")
        pdf.multi_cell(0, 10, f"Sentiment: {sent}")
        pdf.ln(5)

    pdf.output(filepath)
