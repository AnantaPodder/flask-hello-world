from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    from datetime import datetime, timedelta
    import time
    # selenium 4
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service as ChromiumService
    from webdriver_manager.chrome import ChromeDriverManager
    from webdriver_manager.core.utils import ChromeType
    from selenium.webdriver.common.by import By
    from selenium.webdriver.chrome.options import Options
    import os


    # python Telegram bot
    from telegram import Update
    from telegram.ext import CommandHandler, CallbackContext, Updater

    # pymysql
    import pymysql.cursors


    connection = pymysql.connect(host='sql348.main-hosting.eu',
                                user='u841345258_College',
                                password='AnantaPodder08@@',
                                database='u841345258_College')


    # tg_updater = Updater(os.getenv("token"), use_context=True)
    tg_updater = Updater("5146353719:AAGIaZfO11ghjmk9388x8FZ1z3BvNPo3Wi8", use_context=True)
    tg_dispatcher = tg_updater.dispatcher


    def start(update: Update, context: CallbackContext):
        context.bot.send_message(update.effective_user.id, text="I'm live.")


    def find(update: Update, context: CallbackContext):
        txt = update.message.text

        dataList = txt[6:].split(",")
        department = dataList[0]

        for i in range(1, len(dataList)):
            finder(dataList[i], department, 3000)
        # print(txt[6:16])
        # finder(txt[6:16], txt[17:27], int(txt[28:]))


    def status_sender(data):
        return tg_updater.bot.sendMessage(chat_id=1187756746, text=data, parse_mode="HTML").message_id


    def update_status_message(data, message_id):
        return tg_updater.bot.edit_message_text(chat_id=1187756746, text=data, message_id=message_id).message_id


    def finder(college_id, department, numberOfDays: int):
        options = Options()
        options.headless = True
        driver = webdriver.Chrome(service=ChromiumService(
            ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()), options=options)

        driver.get("http://coochbeharcollegeonlineadmission.org.in/frmlogin.aspx")

        date_str = '01/01/2001'
        # date_str = date_Start

        # print(date.strftime("%d/%m/%Y"))
        message_id = 0

        print("College id: ", college_id)

        for i in range(0, numberOfDays):
            date = datetime.strptime(date_str, "%d/%m/%Y")+timedelta(days=i)
            driver.find_element(By.ID, "txt_user").send_keys(f"{college_id}")
            driver.find_element(By.ID, "txt_pass").send_keys(
                date.strftime("%d/%m/%Y"))
            driver.find_element(By.ID, "btn_login").click()

            if (driver.current_url != "http://coochbeharcollegeonlineadmission.org.in/frmlogin.aspx"):
                # data found

                # putting it into database
                connection.ping(reconnect=True)
                with connection.cursor() as cursor:
                    sql = "INSERT INTO `loginData` (`ID`, `DOB`, `DEPT`) VALUES (%s, %s, %s);"
                    cursor.execute(
                        sql, (college_id, date.strftime("%d/%m/%Y"), department))

                    connection.commit()
                status_sender(
                    f"Data Found: <code>{college_id}</code> - <code>{date.strftime('%d/%m/%Y')}</code>")

                break

            time.sleep(0.01)
            driver.find_element(By.ID, "txt_pass").clear()
            driver.find_element(By.ID, "txt_user").clear()

            if (i % 25 == 0):
                statusMessage = "Checked - " + \
                    date.strftime("%d/%m/%Y")+" for "+college_id
                if (message_id == 0):

                    message_id = status_sender(statusMessage)
                else:
                    update_status_message(statusMessage, message_id)

        time.sleep(5)


    def details(update: Update, context: CallbackContext):

        dept = update.message.text[8:].strip()
        # how many record done plz let me know

        options = Options()
        options.headless = True
        driver = webdriver.Chrome(service=ChromiumService(
            ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()), options=options)

        # Function Definition Below

        def presentAddressGen() -> str:
            text = ""
            if (driver.find_element(By.ID, "lbl_Pre_Houseno").text != ""):
                text += f'''House No./Street: {driver.find_element(By.ID,"lbl_Pre_Houseno").text}, '''

            if (driver.find_element(By.ID, "lbl_Pre_wardno").text != ""):
                text += f'''Ward No: {driver.find_element(By.ID,"lbl_Pre_wardno").text}, '''

            if (driver.find_element(By.ID, "lbl_Pre_village").text != ""):
                text += f'''Village/Town: {driver.find_element(By.ID,"lbl_Pre_village").text}, '''

            if (driver.find_element(By.ID, "lbl_Pre_po").text != ""):
                text += f'''P.O.: {driver.find_element(By.ID,"lbl_Pre_po").text}, '''

            if (driver.find_element(By.ID, "lbl_Pre_block").text != ""):
                text += f'''Block: {driver.find_element(By.ID,"lbl_Pre_block").text}, '''

            if (driver.find_element(By.ID, "lbl_Pre_ps").text != ""):
                text += f''' P.S.: {driver.find_element(By.ID,"lbl_Pre_ps").text}, '''

            if (driver.find_element(By.ID, "lbl_Pre_Dis").text != ""):
                text += f''' District: {driver.find_element(By.ID,"lbl_Pre_Dis").text}, '''

            if (driver.find_element(By.ID, "lbl_Pre_pin").text != ""):
                text += f''' PIN: {driver.find_element(By.ID,"lbl_Pre_pin").text}'''

            return text

        def permanentAddressGen() -> str:
            text = ""
            if (driver.find_element(By.ID, "lbl_Per_Houseno").text != ""):
                text += f'''House No./Street: {driver.find_element(By.ID,"lbl_Per_Houseno").text}, '''

            if (driver.find_element(By.ID, "lbl_Per_wardno").text != ""):
                text += f'''Ward No: {driver.find_element(By.ID,"lbl_Per_wardno").text}, '''

            if (driver.find_element(By.ID, "lbl_Per_village").text != ""):
                text += f'''Village/Town: {driver.find_element(By.ID,"lbl_Per_village").text}, '''

            if (driver.find_element(By.ID, "lbl_Per_po").text != ""):
                text += f'''P.O.: {driver.find_element(By.ID,"lbl_Per_po").text}, '''

            if (driver.find_element(By.ID, "lbl_Per_block").text != ""):
                text += f'''Block: {driver.find_element(By.ID,"lbl_Per_block").text}, '''

            if (driver.find_element(By.ID, "lbl_Per_ps").text != ""):
                text += f''' P.S.: {driver.find_element(By.ID,"lbl_Per_ps").text}, '''

            if (driver.find_element(By.ID, "lbl_Per_Dis").text != ""):
                text += f''' District: {driver.find_element(By.ID,"lbl_Per_Dis").text}, '''

            if (driver.find_element(By.ID, "lbl_Per_pin").text != ""):
                text += f''' PIN: {driver.find_element(By.ID,"lbl_Per_pin").text}'''
            return text
        connection.ping(reconnect=True)
        with connection.cursor() as cursor:
            # Read a single record
            sql = "SELECT `ID`, `DOB` FROM `loginData` where DEPT=%s;"
            cursor.execute(sql, (dept))
            result = cursor.fetchall()
            total = len(result)
            count = 0

            for row in result:
                ID = row[0]
                DOB = row[1]

                # logging in
                driver.get(
                    "http://coochbeharcollegeonlineadmission.org.in/frmlogin.aspx")
                driver.find_element(By.ID, "txt_user").send_keys(ID)
                driver.find_element(By.ID, "txt_pass").send_keys(DOB)
                driver.find_element(By.ID, "btn_login").click()

                # logged in and getting printing page
                driver.get(
                    "http://coochbeharcollegeonlineadmission.org.in/frmForm.aspx")

                # getting required data
                Name = driver.find_element(By.ID, "lbl_name").text
                Contact = driver.find_element(By.ID, "lbl_contect").text
                Email = driver.find_element(By.ID, "lblEmail").text
                ImgUrl = driver.find_element(By.ID, "Image1").get_attribute("src")
                BloodGroup = driver.find_element(By.ID, "txtbgr").text
                Religion = driver.find_element(By.ID, "lbl_religion").text
                Gender = driver.find_element(By.ID, "lbl_gender").text
                Caste = driver.find_element(By.ID, "lbl_caste").text
                Father = driver.find_element(By.ID, "lbl_father").text
                Mother = driver.find_element(By.ID, "lbl_mother").text
                GuardianOccupation = driver.find_element(By.ID, "lbl_gocupa").text
                MonthlyIncome = driver.find_element(By.ID, "lblIncome").text
                CommunicationAddress = presentAddressGen()
                PermanentAddress = permanentAddressGen()
                School = driver.find_element(By.ID, "lbl_sname").text
                Board = driver.find_element(By.ID, "lbl_concilbname").text
                Adhar = driver.find_element(By.ID, "lblGeo1").text
                Stream = driver.find_element(By.ID, "GridView1_lblStream_0").text
                Course = driver.find_element(By.ID, "GridView1_lblType_0").text
                Department = driver.find_element(
                    By.ID, "GridView1_lblHonours_0").text

                insertCommand = '''INSERT INTO `StudentData` (`ID`, `Name`, `DOB`, `Contact`, `Email`, `imgURL`, `BloodGroup`, `Religion`, `Gender`, `Caste`, `Father`, `Mother`, `GuardianOccupation`, `MonthlyIncome`, `CommunicationAddress`, `PermanentAddress`, `School`, `Board`, `Adhar`, `Stream`, `Course`, `Department`) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'''
                cursor.execute(insertCommand, (ID, Name, DOB, Contact, Email, ImgUrl, BloodGroup, Religion, Gender, Caste, Father, Mother,
                                            GuardianOccupation, MonthlyIncome, CommunicationAddress, PermanentAddress, School, Board, Adhar, Stream, Course, Department))

                count += 1
            connection.commit()
            status_sender(
                f"Total details Fetched: {count} out of {total} for department: {dept}")

    def getimg(update: Update, context: CallbackContext):
        dept = update.message.text[7:].strip()
        # how many record done plz let me know

        options = Options()
        options.headless = True
        driver = webdriver.Chrome(service=ChromiumService(
            ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()), options=options)

        connection.ping(reconnect=True)

        with connection.cursor() as cursor:
            # Read a single record
            sql = "SELECT `ID`, `imgURL` FROM `StudentData` where Department=%s;"
            cursor.execute(sql, (dept))
            result = cursor.fetchall()

            for row in result:
                context.bot.send_photo(
                    chat_id=1187756746, photo=row[1], caption=row[0])

    tg_dispatcher.add_handler(CommandHandler("start", start))
    tg_dispatcher.add_handler(CommandHandler("find", find))
    tg_dispatcher.add_handler(CommandHandler("details", details))
    tg_dispatcher.add_handler(CommandHandler("getimg",getimg))
    tg_updater.start_polling()
