import qrcode

#Creating an instance of qrcode
def init_qrcode():
    qr = qrcode.QRCode(version=1,box_size=10,border=5)
    return qr

def create_qrcode(qr, input_data):
    qr.add_data(input_data)
    qr.make(fit=True)
    return qr 

def generate_qrcode_image(qr, filename):
    img = qr.make_image(fill='black', back_color='white')
    img.save(filename)