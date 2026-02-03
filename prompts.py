def full_case_analysis_prompt(
    story,
    additional_statement,
    truth,
    severity,
    case_type,
    evidence_type,
    evidence_description
):
    return f"""
You are ANDHA KANOON, an Indian legal assistant.

Analyze the case under:
- Indian Penal Code (IPC)
- Criminal Procedure Code (CrPC)
- Indian Evidence Act

Case Type: {case_type}
Truth Percentage: {truth}%
Severity Score: {severity}/100

Case Story:
{story}

Additional Statement:
{additional_statement}

Evidence:
Type: {evidence_type}
Description: {evidence_description}

Explain:
1. Nature of offence
2. Applicable IPC sections
3. Legal procedure
4. Role of evidence
5. Overall legal position

Do NOT decide guilt.
"""


def lawyer_guilty_verdict_prompt(case_summary: str) -> str:
    return f"""
You are a senior criminal lawyer under Indian law.
Give a professional legal opinion (not a court judgment).

Case Summary:
{case_summary}

Explain:
1. Applicable IPC sections
2. Cognizable / bailable status
3. Police & court procedure
4. Possible punishment
5. Bail / plea options
6. Legal advice
"""


def lawyer_not_guilty_verdict_prompt(case_summary: str) -> str:
    return f"""
You are a senior criminal lawyer under Indian law.
The accused claims innocence.

Case Summary:
{case_summary}

Explain:
1. Rights of the accused
2. Burden of proof
3. Investigation & trial procedure
4. Defence strategy
5. Legal advice
"""
