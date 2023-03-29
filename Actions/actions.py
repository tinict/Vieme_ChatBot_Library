# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import ConversationPaused
from rasa_sdk.events import UserUtteranceReverted

from _sqlite3 import *
from sqlite3.dbapi2 import *
from sqlite3 import dbapi2 as sqlite
import pyodbc
import gc
import urllib.request

def ConnectDataBase (server, database, username, password):
    connection = pyodbc.connect ('DRIVER={SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
    return connection

# name_author = "Kim"
# print(type(name_author))
# connection = ConnectDataBase("localhost", "QL_THUVIEN", "sa", "123");
# cursor = connection.cursor()
# query = "select count(*) from DauSach as ds where ds.TacGia like N'%Kim%'"
# cursor.execute(query)
# print(type(cursor.fetchall()[0][0]))
# for row in cursor:
#     print(row[1]);

class action_find_book(Action):

    def name(self) -> Text:
        return "action_find_book"

    async def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        name_author = next(tracker.get_latest_entity_values("name_author"), None)
        
        print(type(name_author))
        server = "localhost" 
        database = "QL_THUVIEN"
        username = "sa"
        password = "123"
        connection = pyodbc.connect('DRIVER={SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
        connection = ConnectDataBase("localhost", "QL_THUVIEN", "sa", "123");
        cursor = connection.cursor()
        # query = "select count(*) from DauSach as ds where ds.TacGia like N'%" + name_author +"%'"
        # cursor.execute(query)
        # print(type(cursor.fetchall()[0][0]))
        # result = cursor.fetchall()[0][0];
      
        cursor.execute("SELECT * FROM LoaiSach")
        db = "";
        for row in cursor:
            db += row[1] + "\n";
        
        # if (result == 0):
        #     dispatcher.utter_message(text = "Trong cơ sở dữ liệu không tồn tại tác giả này!")
        # else:
        #     str = "Ý bạn đang tìm những quyển sách của thầy " + name_author
        dispatcher.utter_message(text = db)
            
        return [ConversationPaused(), UserUtteranceReverted()]
        
class ActionDefaultFallback(Action):

    def name(self) -> Text:
        return "action_default_fallback"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(template="my_custom_fallback_template")
        
        # call_customer_service(tracker)
        
        return [ConversationPaused(), UserUtteranceReverted()]
