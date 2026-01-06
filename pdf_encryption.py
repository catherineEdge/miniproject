import pikepdf
old_pdf=pikepdf.Pdf.open("da.pdf")
old_pdf.save("prt_da.pdf",encryption=pikepdf.Encryption(user="cat",owner="catherine"))