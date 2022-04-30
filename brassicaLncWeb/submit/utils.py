import os
from dotenv import load_dotenv
from mailer import Mailer

load_dotenv()


def sendEmail(data):
    try:
        subject='BrassicaLnc-Website, a new submited data from {}'.format(data.get('email'))
        message = '''
        data suhmitied : 
        Chromosome:{},\n
        Location:{},\n
        Strand:{},\n
        Exon Location:{},\n
        Sequence:{},\n
        See the other data in admin Panel
        '''.format(
            data.get('chromosome', None),         data.get('location', None),
            data.get('strand', None),             data.get('exonLocation', None), 
            data.get('sequence', None))

        mail = Mailer(email=os.getenv('SENDER_MAIL'), password=os.getenv('SENDER_PASSWORD'))
        mail.send(receiver='fad127alireza2@gmail.com', subject=subject, message=message)
        return True
    except Exception as e:
        print(str(e))
        return False