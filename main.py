# Developed by @sanuja : https://www.fiverr.com/sanuja_kumara

from spyder import spyder

if __name__ == "__main__":
    spyder.spyder_main()


# from api import api
# import os
# from database import *

# GOOGLE_SHEET_SCOPES = "https://www.googleapis.com/auth/spreadsheets"
# GOOGLE_DRIVE_SCOPES = "https://www.googleapis.com/auth/drive"
# temp_pdfs_dir_path = os.path.join(os.getcwd(), './spyder/temp_pdfs')
# files = [f for f in os.listdir(temp_pdfs_dir_path) if os.path.isfile(f"{temp_pdfs_dir_path}/{f}") and f.endswith('.pdf')]

# for file in files:
#     pdf_title=file.split(".")[0]
#     pdf_domain="https://www.npci.org.in/"
#     pdf_url=""
#     pdf_date=date.today().strftime("%Y/%m/%d")

#     print("Uploading...")      
#     apiDriveInstance = api.Api(api_scope=GOOGLE_DRIVE_SCOPES)
#     drive_response = apiDriveInstance.api_upload_to_drive(pdf_file_path = f"{temp_pdfs_dir_path}/{file}", pdf_file_title=f"{pdf_title}")
#     pdf_id=drive_response[1]
#     # create api instance
#     apiInstance = api.Api(api_scope=GOOGLE_SHEET_SCOPES)
#     # save data to google drive & google sheet
#     data = [pdf_id, pdf_date, pdf_domain, pdf_title, pdf_url, drive_response[0], "New"]
#     # print(data)
#     apiInstance.api_append_spreadsheet(data)
#     # if os.path.exists(f"{temp_pdfs_dir_path}/{file}"):
#     #     os.remove(f"{temp_pdfs_dir_path}/{file}")
#     # mark pdf upload ststus as "uploaded" 
#     # with database.Database() as db:
#     #     db.update_table_pdf_url_ststus(pdf_url)      







# from spyder.selenium_pdf_downloader import selenium_pdf_downloader_main


# url="https://www.npci.org.in/PDF/npci/others/UPI-Settlement-Process.pdf"
# print(selenium_pdf_downloader_main(url))





