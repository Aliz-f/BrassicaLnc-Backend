"""LncRna project utils for submit app"""
import os
from dotenv import load_dotenv
from mailer import Mailer

load_dotenv()

def send_email(data) -> bool:
    """no docstring"""
    try:
        subject=f"BrassicaLnc-Website, a new submited data from {data.get('email')}"
        message = f'''
        data suhmitied : 
        Chromosome:{data.get('chromosome', None)},\n
        Location:{data.get('location', None)},\n
        Strand:{data.get('strand', None)},\n
        Exon Location:{data.get('exonLocation', None)},\n
        Sequence:{data.get('sequence', None)},\n
        See the other data in admin Panel
        '''
        mail = Mailer(email=os.getenv('SENDER_MAIL'), password=os.getenv('SENDER_PASSWORD'))
        mail.send(receiver='fad127alireza2@gmail.com', subject=subject, message=message)
        return True
    except Exception:
        return False
