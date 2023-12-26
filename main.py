import requests
from bs4 import BeautifulSoup
import re
import httpx


baseurl = "https://www.ktunotes.in/ktu-2019-new-scheme-notes/"
departments = ["CSE", "ECE", "EEE", "MECH", "I - T"]

class Web_Scrap():

    def get_direct_download_link(drive_link):
        # Extract the file ID from the Google Drive link
        file_id_match = re.search(r'/file/d/([a-zA-Z0-9_-]+)', drive_link)
        
        if file_id_match:
            file_id = file_id_match.group(1)
            
            # Construct the direct download link
            direct_download_link = f'https://drive.google.com/uc?id={file_id}&export=download'
            return direct_download_link
        else:
            print("Invalid Google Drive link.")
            return None

    def fetchSemLinks(web_url):
        response = requests.get(web_url)

        semLinkDict = {

        }

        if response.status_code == 200:

            soup = BeautifulSoup(response.text, 'html.parser')

            all_links = soup.find_all('a')

            
            for link in all_links:
                href = link.get('href')
                text = link.text.strip()
                if text != "" and "notes-2019" in href:
                    semLinkDict[text] = href
                    
            return semLinkDict
        else:
            return {"error": f'Failed to retrieve the page. Status code: {response.status_code}' }
    
    def getLinkBySem(semester):
        try:
            if semester not in ["S1","S2"]:
                data = Web_Scrap.fetchSemLinks(baseurl)
                if data[semester] != None:
                    return data[semester]
                else:
                    return "Invalid Semester"
            else:
                return ""
        except:
            return "something went wrong"


    def fetchDeptLinks(url):


        deptLinkDict = {}


        response = requests.get(url)

            
        if response.status_code == 200:

            soup = BeautifulSoup(response.text, 'html.parser')

            all_links = soup.find_all('a')

                
            for link in all_links:
                href = link.get('href')
                text = link.text.strip()
                if text and len(text) > 1:
                    if any(department in text for department in departments):
                        # print(f"Link - {href}, Text = {text}")
                        deptLinkDict[text] = href 

            # print(deptLinkDict)
            return deptLinkDict
                
        else:
            return {"error": f'Failed to retrieve the page. Status code: {response.status_code}' }
        

    def getLinkByDept(dept,semLink):
        try:

            data = Web_Scrap.fetchDeptLinks(semLink)
            if data[dept] != None:
                return data[dept]
            else:
                return "Invalid Department" 
        except:
            return "something went wrong"

    def fetchSubLinks(dept,semLink):
        subLinkDict = {}
        dept_sem_link = Web_Scrap.getLinkByDept(dept=dept,semLink=semLink) 

        response = requests.get(dept_sem_link)

        semLinkDict = {

        }

        if response.status_code == 200:

            soup = BeautifulSoup(response.text, 'html.parser')

            all_links = soup.find_all('a')

                
            for link in all_links:
                href = link.get('href')
                text = link.text.strip()

                if text and ("-notes/" in href) and ("Notes" not in text) and ("upload-notes/" not in href) and "KTU" not in text:
                    # print(f"Link = {href}, text = {text}")
                    subLinkDict[text] = href
            return subLinkDict
                
        else:
            return {"error": f'Failed to retrieve the page. Status code: {response.status_code}' }


    def getLinkBySub(subject,dept,semLink):
        try:

            data = Web_Scrap.fetchSubLinks(dept=dept,semLink=semLink)
            # (data.keys())
            if data[subject] != None:
                return data[subject]
            else:
                return "Invalid Subject" 
        except:
            return "something went wrong"


    async def getNotes(subject,dept,semLink):
        subLink = Web_Scrap.getLinkBySub(subject,dept,semLink)

        response = requests.get(subLink)

        result = []
                
        if response.status_code == 200:

            soup = BeautifulSoup(response.text, 'html.parser')

            all_links = soup.find_all('a')
            
            x = 0
            y = 0
            i = 1
            module_set = set()  # Change {} to set()

            for link in all_links:
                href = link.get('href')
                text = link.text.strip()
                try:
                    if "drive.google.com" in href:
                        # print(module_set)
                        # print(f"Link = {href}, Text = {text}")
                        module_set.add(text)
                        y = len(module_set)
                        # print(f"x = {x}, y = {y}, i = {i}")
                        
                        if "module" not in text:
                            link = Web_Scrap.get_direct_download_link(href)
                            content = f"{text}"
                            content = f"{subject} " + content
                            result.append([link,content])
                            print(link, content)

                        elif x >= y and "module" in text:
                            link = Web_Scrap.get_direct_download_link(href)
                            i = int((x+2)/y) + 1
                            content = f" {text} - SET {i}"
                            content = f"{subject} " + content
                            result.append([link,content])
                            print(link, content)

                        elif "module" in text and x <y :
                            link = Web_Scrap.get_direct_download_link(href)
                            content = f"{text} - SET {i}"
                            content = f"{subject} " + content
                            result.append([link,content])
                            print(link, content)
                        

                        x = x + 1

                except Exception as e:
                    # print("Error:", e)
                    pass
            return result
        else:
            print({"error": f'Failed to retrieve the page. Status code: {response.status_code}' })

# Manually
# sem = input("Enter Your Semester :- ")
# dept = input("Enter Your Department :- ")


# semLink = Web_Scrap.getLinkBySem(sem)

# subLinkDict = Web_Scrap.fetchSubLinks(dept,semLink)
# print(subLinkDict.keys())


# subject = input("Enter Subject Name :- ")
# Web_Scrap.getNotes(subject,dept,semLink)



# Telegram BOT
            

bot_token = "6782675554:AAGQEuIMAWlf71Q9gbWajqsMeKAIgRO0eMQ"

import logging
from telegram import Update
from telegram.ext import CommandHandler, ApplicationBuilder, ContextTypes, MessageHandler, filters

from io import BytesIO
from telegram import Update
from telegram.ext import CommandHandler, ApplicationBuilder, ContextTypes, MessageHandler

import logging
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CommandHandler, ApplicationBuilder, ContextTypes, MessageHandler, filters, CallbackQueryHandler






from io import BytesIO
from telegram import Update
from telegram.ext import CommandHandler, ApplicationBuilder, ContextTypes, MessageHandler, filters



# Logging configuration
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

semesters = ["S1", "S2", "S3", "S4", "S5", "S6", "S7", "S8"]
departments = ["CSE", "ECE", "EEE", "MECH", "I - T"]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_message = "Welcome! Please select your semester and department."
    keyboard = [
        [InlineKeyboardButton(sem, callback_data=f"sem:{sem}") for sem in semesters],
        [InlineKeyboardButton(dep, callback_data=f"dept:{dep}") for dep in departments],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await context.bot.send_message(chat_id=update.effective_chat.id, text=welcome_message, reply_markup=reply_markup)

async def handle_query_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()  # Acknowledge the query

    data_parts = query.data.split(":")
    query_type, value = data_parts[0], data_parts[1]

    if query_type == "sem":
        context.user_data["selected_semester"] = value
    elif query_type == "dept":
        context.user_data["selected_department"] = value

    if "selected_semester" in context.user_data and "selected_department" in context.user_data:
        sem = context.user_data["selected_semester"]
        dept = context.user_data["selected_department"]

        semLink = Web_Scrap.getLinkBySem(sem)
        subLinkDict = Web_Scrap.fetchSubLinks(dept, semLink)

        # Store subLinkDict in user_data for later use
        context.user_data["subLinkDict"] = subLinkDict

        # Create buttons for each dictionary key, each taking 100% width
        keyboard = [
            [InlineKeyboardButton(sub, callback_data=f"sub:{sub}") for sub in subLinkDict.keys()]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        # Check if the message content or keyboard buttons are different before editing
        if (
            query.message.text != "Please select a subject:" or
            query.message.reply_markup.inline_keyboard != reply_markup.inline_keyboard
        ):
            await query.edit_message_text(text="Please select a subject:", reply_markup=reply_markup)


async def handle_subject_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()  # Acknowledge the query

    subject_key = query.data.split(":")[1]

    # Retrieve subLinkDict from user_data
    subLinkDict = context.user_data.get("subLinkDict", {})

    # Get the corresponding value (link) from the subLinkDict
    link = subLinkDict.get(subject_key, "Link not found")

    # Send a new message instead of editing the existing one
    await query.message.reply_text(text=f"Selected subject: {subject_key}\nLink: {link}")

    # Call getNotes to fetch and display notes
    sem = context.user_data.get("selected_semester")
    dept = context.user_data.get("selected_department")
    semLink = Web_Scrap.getLinkBySem(sem)
    
    try:
        # Get the notes as a list of [link, content] pairs
        notes = await Web_Scrap.getNotes(subject_key, dept, semLink)

        # Send each note as a separate message
        for note in notes:
            note_link, note_content = note
            await query.message.reply_text(text=f"{note_content}\nLink: {note_link}")

    except Exception as e:
        logging.error(f"Error in getNotes: {e}")


if __name__ == '__main__':
    try:
        application = ApplicationBuilder().token(bot_token).build()

        # Add command handlers
        start_handler = CommandHandler('start', start)

        # Add callback query handlers
        callback_query_handler = CallbackQueryHandler(handle_query_selection, pattern=r'^sem:|dept:')
        subject_selection_handler = CallbackQueryHandler(handle_subject_selection, pattern=r'^sub:')

        application.add_handler(start_handler)
        application.add_handler(callback_query_handler)
        application.add_handler(subject_selection_handler)

        application.run_polling()
    except Exception as e:
        logging.error(f"Error running the bot: {e}")