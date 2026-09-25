import os
import time
from dotenv import load_dotenv
from google import genai

load_dotenv()


class GeminiDocumentGenerator:

    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError("GEMINI_API_KEY is not set in .env file")

        self.client = genai.Client(api_key=api_key)
        self.model_name = "gemini-3.8-flash"

    def generate_document(self, document_type, parties, terms, dates):

        prompt = f"""
You are an AI assistant for a legal document generation project.

Generate a professional and well-structured draft legal document.

Document Type:
{document_type}

Involved Parties:
{parties}

Effective Date:
{dates}

Terms and Conditions:
{terms}

Requirements:
- Give the document a clear title.
- Use proper sections and headings.
- Include relevant clauses based on the provided information.
- Keep the language formal and professional.
- Do not invent important personal or financial information.
- Clearly state that the generated document is an AI-generated draft
  and should be reviewed by a qualified legal professional.
"""

        for attempt in range(3):
            try:
                response = self.client.models.generate_content(
                    model=self.model_name,
                    contents=prompt
                )

                return response.text

            except Exception as e:
                if "503" in str(e) and attempt < 2:
                    time.sleep(3)
                else:
                    return self.get_fallback_document(
                        document_type,
                        parties,
                        terms,
                        dates
                    )

    def get_fallback_document(self, document_type, parties, terms, dates):

        return f"""
==================================================
              {document_type.upper()}
==================================================

AI-GENERATED DRAFT LEGAL DOCUMENT

Effective Date:
{dates}

PARTIES INVOLVED:
{parties}

TERMS AND CONDITIONS:

1. PURPOSE
The parties agree to enter into this agreement based on the
terms and conditions provided below.

2. AGREEMENT TERMS
{terms}

3. RESPONSIBILITIES
The parties agree to follow the responsibilities and conditions
mentioned in this agreement.

4. EFFECTIVE DATE
This agreement becomes effective from {dates}.

5. LEGAL REVIEW
This document is an AI-generated draft and should be reviewed
by a qualified legal professional before signing or using it
for official purposes.

IN WITNESS WHEREOF, the parties have agreed to the terms
mentioned above.

SIGNATURES:

Party 1:
____________________________

Party 2:
____________________________

Date:
____________________________
"""