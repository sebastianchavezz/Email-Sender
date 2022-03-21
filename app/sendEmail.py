import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from tabulate import tabulate


class EmailSender:
    name_template_html :str = '.\\app\\template.html'
    port :int = 465  # For SSL
    smtp_server : str = "smtp.gmail.com"
    sender_email :str = "testemailtom420@gmail.com"  # Enter your address
    receiver_email :str= "sebastianchavez940@gmail.com"  # Enter receiver address
    subject: str = 'Daily reminder'
    __password :str= 'Testemailtom.420'
    context = ssl.create_default_context()

    def __init__(self,df):
    
        self.headers = ['producten','omschrijvingen']
        self.table = self.generate_table(df,self.headers)
        self.html_text = self.generate_html_text(self.table)
        print(type(self.html_text))
        self.message = self._generate_message(self.subject,self.send_mail,self.receiver_email,self.html_text)
        

    def generate_table(self,df,header):
        table =  tabulate(df, header, tablefmt="html",showindex=False)
        return table

    
    def generate_html_text(self,table):
        file = open(self.name_template_html)
        content = file.read()
        content = content + table + '</html>'
        print(type(content))
        return content

    def _generate_message(self,subject:str,sender:str,receiver:str,html)->MIMEMultipart:
        
        message = MIMEMultipart('alternative')
        message['Subject'] ='Daily reminder'
        message['From'] = sender
        message['To'] = receiver
        txt_hmtl =  MIMEText(html,'html', 'utf-8')
        message.attach(txt_hmtl)
        return message
    
    def send_mail(self):
        m = self._generate_message(self.subject,self.send_mail,self.receiver_email,self.html_text)
        mssg = MIMEText(self.generate_html_text(self.table),'html')
        print(type(mssg))
        with smtplib.SMTP_SSL(self.smtp_server, self.port, context=self.context) as server:
            print('send..')
            server.login(self.sender_email, self.__password)
            server.sendmail(self.sender_email, self.receiver_email, mssg.as_string())
            
