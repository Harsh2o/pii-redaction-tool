"""
ground_truth.py
Manually verified PII instances from the Red Herring Prospectus.
"""

GROUND_TRUTH = {

    "EMAIL_ADDRESS": [
        "cs.connect@kshinternational.com",
        "Sarthak.malvadkar@kshinterantional.com",
        "rm6.ifbpune@sbi.co.in",
        "Ipocmg@icicibank.com",
        "tushar.gavankar@hdfcbank.com",
        "manisha.shukla@hdfcbank.com",
        "cherag.gyara@icicibank.com",
        "sharmila.joshi@indusind.com",
        "sachin.gawade@hdfcbank.com",
        "sheetal.parab@nuvama.com",
        "customerservice.mb@nuvama.com",
        "parag.pansare@kirtanepandit.com",
        "customercare@icicisecurities.com",
        "ksh@icicisecurities.com",
        "ipo@trilegal.com",
        "ashishmp@federalbank.co.in",
        "kshinternational.ipo@in.mpms.mufg.com",
        "hitesh.ramani@citi.com",
        "anand.soni@bajajfinserv.in",
        "pravin.teli2@hdfcbank.com",
        "hingnetare@gmail.com",
        "eric.bacha@hdfcbank.com",
        "prakash.boricha@nuvama.com",
        "siddharth.jadhav@hdfcbank.com",
        "pro@eximbankindia.in",
        "ksh.ipo@nuvama.com",
    ],

    "IN_CIN": [
        "U28129PN1979PLC141032",
        "U67190MH1999PTC118368",
        "L65920MH1994PLC080618",
        "L65190GJ1994PLC021012",
    ],

    "PHONE_NUMBER": [
        "+91 20 4505 3237",
        "+91 20 45053237",
        "+91 22 40094400",
        "+91 22 6807 7100",
        "+91 22 4009 4400",
    ],

    "PERSON": [
        "Sarthak Malvadkar",
        "Kushal Subbayya Hegde",
        "Pushpa Kushal Hegde",
        "Prakash Boricha",
        "Chitra Raste",
        "Tushar Gavankar",
        "Manisha Shukla",
        "Sheetal Parab",
        "Parag Pansare",
        "Hitesh Ramani",
        "Anand Soni",
        "Eric Bacha",
        "Siddharth Jadhav",
    ],

    "ORGANIZATION": [
        "KSH International Limited",
        "Nuvama Wealth Management Limited",
        "HDFC Bank Limited",
        "ICICI Securities Limited",
        "Trilegal",
        "Federal Bank",
        "IndusInd Bank",
        "Bajaj Finance Limited",
        "Citi Bank",
        "MUFG Bank",
    ],

    "ADDRESS": [
        "11/3, 11/4 and 11/5, Village Birdewadi, Chakan Taluka - Khed, Pune",
        "201, Tower 2, Montreal Business Centre, Off Pallod Farms, Baner, Pune",
    ],

    "WEBSITE_URL": [
        "www.kshinternational.com",
        "www.nuvama.com",
        "www.hdfcbank.com",
        "www.icicibank.com",
        "www.icicisecurities.com",
        "www.indusind.com",
        "www.federalbank.co.in",
        "www.sbi.co.in",
        "www.bajajfinance.com",
        "www.eximbankindia.in",
        "www.in.mpms.mufg.com",
    ],
}


def get_all_ground_truth_strings() -> list:
    """Flat list of all known PII strings (for quick lookup)."""
    all_pii = []
    for pii_list in GROUND_TRUTH.values():
        all_pii.extend(pii_list)
    return all_pii


def get_by_type(entity_type: str) -> list:
    """Get ground truth list for a specific PII type."""
    return GROUND_TRUTH.get(entity_type, [])
