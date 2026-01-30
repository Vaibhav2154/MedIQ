"""
Consent Templates for Seeding
Provides various consent text templates for different scenarios
"""

# Full research consent with broad permissions
FULL_RESEARCH_CONSENT = """
PATIENT CONSENT FOR MEDICAL RESEARCH AND DATA SHARING

I, the undersigned patient, hereby provide my informed consent for the following:

1. DATA SHARING FOR RESEARCH
I authorize the use and disclosure of my medical records, including but not limited to:
- Diagnoses and medical conditions
- Laboratory test results and observations
- Medication history and prescriptions
- Encounter and visit records
- Imaging and pathology reports

2. PURPOSE
My data may be used for:
- Medical research studies
- Clinical trials and drug development
- Healthcare quality improvement initiatives
- Public health surveillance
- Academic and educational purposes

3. DATA RECIPIENTS
My data may be shared with:
- Approved research institutions
- Academic medical centers
- Pharmaceutical companies conducting clinical trials
- Government health agencies
- Healthcare quality organizations

4. DURATION
This consent is valid for a period of 5 years from the date of signing.

5. RIGHTS
I understand that:
- My participation is voluntary
- I can revoke this consent at any time
- My treatment will not be affected if I refuse or revoke consent
- My data will be de-identified when possible
- Confidentiality will be maintained according to applicable laws

Date: {date}
Patient ABHA ID: {abha_id}
"""

# Limited data sharing consent (care and quality improvement only)
LIMITED_CARE_CONSENT = """
PATIENT CONSENT FOR HEALTHCARE DATA SHARING

I consent to the sharing of my medical information for the following limited purposes:

1. PERMITTED USES
- Direct patient care and treatment
- Care coordination between healthcare providers
- Healthcare quality improvement within my treating facility
- Billing and insurance purposes

2. DATA SCOPE
The following information may be shared:
- Current diagnoses and active problems
- Current medications and allergies
- Recent vital signs and observations
- Encounter summaries

3. RESTRICTIONS
I DO NOT consent to:
- Use of my data for research purposes
- Sharing with external research organizations
- Use in clinical trials
- Commercial use of my data

4. DURATION
This consent remains valid until revoked by me in writing.

Date: {date}
Patient ABHA ID: {abha_id}
"""

# Research consent with specific disease focus
DISEASE_SPECIFIC_CONSENT = """
CONSENT FOR {disease_name} RESEARCH STUDY

I consent to participate in research related to {disease_name}.

1. RESEARCH PURPOSE
My medical data will be used specifically for:
- Understanding {disease_name} progression and outcomes
- Developing new treatments for {disease_name}
- Identifying risk factors and biomarkers
- Improving diagnostic methods

2. DATA INCLUDED
- All medical records related to {disease_name}
- Laboratory results and biomarkers
- Treatment history and medication responses
- Imaging and diagnostic test results
- Long-term outcome data

3. DURATION
Valid for 3 years from signing date.

4. DATA SHARING
Data may be shared with qualified {disease_name} researchers at approved institutions.

Date: {date}
Patient ABHA ID: {abha_id}
"""

# Expired consent (for testing)
EXPIRED_CONSENT = """
PATIENT CONSENT FOR MEDICAL RESEARCH

I consent to the use of my medical data for research purposes.

This consent was valid from January 1, 2023 to December 31, 2024.

NOTICE: This consent has EXPIRED and is no longer valid.

Date: 2023-01-01
Patient ABHA ID: {abha_id}
"""

# Ambiguous consent (low confidence scenario)
AMBIGUOUS_CONSENT = """
Medical Information Sharing

I agree to share some of my medical information with doctors and maybe researchers
if they need it for important stuff. I think it's okay to use my test results and
diagnoses but I'm not sure about everything else.

I want my information kept private but understand it might be shared sometimes.

This is valid for a while, maybe a few years or so.

Patient: {abha_id}
"""

# Revoked consent
REVOKED_CONSENT = """
CONSENT REVOCATION NOTICE

I hereby REVOKE my previous consent for medical data sharing and research participation.

Effective immediately, I withdraw permission for:
- Use of my data in research studies
- Sharing of my medical records with external parties
- Participation in any ongoing studies

This revocation applies to all previous consents signed.

Date: {date}
Patient ABHA ID: {abha_id}
Status: REVOKED
"""

# Consent with specific exclusions
PARTIAL_CONSENT = """
SELECTIVE CONSENT FOR MEDICAL DATA SHARING

I provide consent for medical data sharing with the following specific conditions:

PERMITTED:
- Sharing of vital signs and basic observations
- Use of de-identified data for research
- Sharing with healthcare providers involved in my care

EXCLUDED:
- Mental health records
- Genetic information
- HIV/AIDS related information
- Substance abuse treatment records

DURATION: 2 years from date of signing

Date: {date}
Patient ABHA ID: {abha_id}
"""


def get_consent_template(consent_type, **kwargs):
    """
    Get a consent template with filled-in values
    
    Args:
        consent_type: Type of consent template
        **kwargs: Values to fill in the template
        
    Returns:
        Filled consent text
    """
    templates = {
        'full_research': FULL_RESEARCH_CONSENT,
        'limited_care': LIMITED_CARE_CONSENT,
        'disease_specific': DISEASE_SPECIFIC_CONSENT,
        'expired': EXPIRED_CONSENT,
        'ambiguous': AMBIGUOUS_CONSENT,
        'revoked': REVOKED_CONSENT,
        'partial': PARTIAL_CONSENT
    }
    
    template = templates.get(consent_type, FULL_RESEARCH_CONSENT)
    return template.format(**kwargs)
