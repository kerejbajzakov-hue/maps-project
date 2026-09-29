import qrcode, io
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import glob
bold=[f for f in glob.glob('/usr/share/fonts/**/DejaVuSans-Bold.ttf',recursive=True)][0]
reg=bold.replace('-Bold','')
pdfmetrics.registerFont(TTFont('B',bold)); pdfmetrics.registerFont(TTFont('R',reg))
from clay_common import BASE
items=[("0","Весь тур · карта",BASE)]+[(str(i+1),n,BASE+"#"+id) for i,(id,n) in enumerate([
("abat-baitak","Мавзолей Абат-Байтак"),("kobylandy","Комплекс «Кобыланды батыр»"),("eset-kokiuly","Комплекс Есета Кокиулы"),
("khan-molasy","Комплекс «Хан моласы»"),("kotibar","Мавзолей Котибар батыра"),("eset-daribay","Мавзолей «Есет-Дарибай»"),("kyzyltam","Мавзолей Кызылтам")])]
W,H=A4; c=canvas.Canvas("../poster/qr-codes-A4.pdf",pagesize=A4)
c.setFont('B',12); c.drawCentredString(W/2,H-40,"Цифровая карта исторических памятников Актюбинского края")
c.setFont('R',9); c.drawCentredString(W/2,H-56,"Вырежьте и наклейте рядом с меткой того же номера. Сканируйте обычной камерой телефона.")
cols,cw,ch=3,W/3,(H-80)/3
for k,(num,name,url) in enumerate(items):
    r,col=divmod(k,cols); x=col*cw; y=H-80-(r+1)*ch
    q=qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M,box_size=10,border=2); q.add_data(url); q.make()
    b=io.BytesIO(); q.make_image(fill_color="#16282B",back_color="white").save(b,"PNG"); b.seek(0)
    s=150; c.drawImage(ImageReader(b),x+(cw-s)/2,y+ch-s-20,s,s)
    c.setDash(3,3); c.setStrokeColorRGB(.7,.7,.7); c.rect(x+8,y+8,cw-16,ch-16); c.setDash()
    c.setFont('B',9); c.drawCentredString(x+cw/2,y+ch-s-38,(f"{num}. " if num!="0" else "")+name)
c.save()
