from langchain_core.prompts import ChatPromptTemplate

DOCUMENT_STRUCTURE_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are an academic records data parser. Analyze the raw text extracted from an academic document (PDF report, card, or transcript) and structure it into a JSON object.

Format the output JSON as:
{{
  "student_name": "Full name of the student or null if not found",
  "student_id": "Student identifier/code or null if not found",
  "subjects": ["List of subject names found in the document"],
  "grades": [List of numerical scores or grades matching the subjects (scaled 0-20 if possible)],
  "attendance": "Attendance percentage (0-100) or decimal fraction (0-1), or null",
  "teacher_comments": ["List of teacher comments/evaluations found"],
  "academic_concerns": ["List of specific issues identified, e.g. 'failing math', 'absences'"]
}}

Only output the raw JSON object. Do not wrap in markdown code blocks.

Text:
{extracted_text}
"""),
    ("human", "Parse this document text.")
])

TEACHER_NOTES_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are an academic counselor notes parser. Analyze the unstructured notes written by a teacher or academic advisor about a student.
Translate these notes into structured categorical concern flags.

You must format your response as a JSON object matching this structure:
{{
  "attendance_concern": true/false (true if notes mention missing classes, tardiness, etc.),
  "engagement_concern": true/false (true if notes mention lack of participation, disengagement, sleepiness, etc.),
  "assignment_concern": true/false (true if notes mention homework/assignment delays, poor scores, incomplete work, etc.),
  "behavioral_concern": true/false (true if notes mention classroom disruption, attitude issues, conflicts, etc.),
  "summary": "A concise 1-sentence synthesis of the educator's notes."
}}

Only output the raw JSON object. Do not wrap in markdown code blocks.

Educator Notes:
{notes}
"""),
    ("human", "Translate these educator notes.")
])
