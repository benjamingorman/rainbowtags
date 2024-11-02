from io import BytesIO

import barcode

code39 = barcode.Code39
barcode = code39("05713", add_checksum=False)
barcode.save("barcode", options={"write_text": False})
