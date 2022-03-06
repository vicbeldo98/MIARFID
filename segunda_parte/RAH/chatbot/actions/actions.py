from typing import Dict, Text, Any, List
from rasa_sdk import Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormValidationAction, Action
import datetime
import json
import os
from apscheduler.schedulers.background import BackgroundScheduler
import smtplib
import ssl
import unidecode
from rasa_sdk.events import SlotSet


scheduler = BackgroundScheduler(timezone='Europe/Berlin')
scheduler.start()


class ValidarEventoForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_añadir_evento_form"

    def validate_alarma(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        try:
            d = datetime.datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f%z").replace(tzinfo=None)

            if d < datetime.datetime.now():
                dispatcher.utter_message(response="utter_wrong_alarma")
                return {"alarma": None}
            else:
                return {"alarma": d.strftime("%d-%m-%Y %H:%M")}

        except ValueError:
            dispatcher.utter_message(response="utter_error_alarma")
            return {"alarma": None}


class ProgramarAlarma(Action):
    def name(self) -> Text:
        return "programar_alarma"

    async def run(self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        evento = unidecode.unidecode(tracker.get_slot('evento'))
        alarma = tracker.get_slot('alarma')
        email = tracker.get_slot('email_propio')

        def email_me(email, content):
            print('Sending email...')
            user = 'agenda-bot@gmx.es'
            password = 'soyunbotagenda1234'
            smtp_server = "mail.gmx.com"
            port = 587
            sender_email = user
            password = password
            context = ssl.create_default_context()

            try:
                server = smtplib.SMTP(smtp_server, port)
                server.starttls(context=context)
                server.login(sender_email, password)
                from_email = user
                to_emails = [email]
                body = content
                headers = f"From: {from_email}\r\n"
                headers += f"To: {', '.join(to_emails)}\r\n"
                headers += f"Subject: Recordatorio agenda-bot!\r\n"
                email_message = headers + "\r\n" + body
                server.sendmail(from_email, to_emails, email_message)
                print("Email sent successfully!")

            except Exception as e:
                print(e)

            finally:
                server.quit()

        d = datetime.datetime.strptime(alarma, "%d-%m-%Y %H:%M").replace(tzinfo=None)
        if d < datetime.datetime.now():
            d = datetime.datetime.now()
        scheduler.add_job(email_me, 'date', run_date=datetime.datetime(d.year, d.month, d.day, d.hour, d.minute, d.second), args=[email, evento])
        return []



class Save(Action):
    def name(self) -> Text:
        return "action_guardar_contacto"

    async def run(self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        nick = tracker.get_slot('nick')
        email = tracker.get_slot('email_amigo')
        phone_number = tracker.get_slot('phone-number')
        message = "Guardando nuevo contacto con:\n\tNick:" + nick + "\n\tEmail:" + email + "\n\tTeléfono:" + phone_number
        dispatcher.utter_message(text=message)
        new_nick = nick.replace(" ", "_")
        new_nick = new_nick.lower()
        data = {"email": email, "phone": phone_number}
        if os.path.exists('agenda.json'):
            with open('agenda.json', 'r') as f:
                all_data = json.load(f)
                if new_nick in all_data.keys():
                    dispatcher.utter_message(text="Contacto duplicado! Sobreescribiendo el anterior...")
        else:
            all_data = dict()

        all_data[new_nick] = data
        with open('agenda.json', 'w') as f:
            json.dump(all_data, f)
        dispatcher.utter_message(text="Todo perfecto!")
        
        return []


class Delete(Action):
    def name(self) -> Text:
        return "action_borrar_contacto"

    async def run(self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        nick = tracker.get_slot('nick_contacto')
        new_nick = nick.replace(" ", "_")
        new_nick = new_nick.lower()
        if not os.path.exists('agenda.json'):
            dispatcher.utter_message(text="No existe ningún usuario")
            return []
        with open('agenda.json', 'r') as f:
            all_data = json.load(f)
        try:
            del all_data[new_nick]
            with open('agenda.json', 'w') as f:
                json.dump(all_data, f)
            dispatcher.utter_message(text="Usuario " + nick + " borrado con éxito")
        except Exception:
            dispatcher.utter_message(text="No tengo guardado al usuario " + nick)

        return []


class DisplayInfo(Action):
    def name(self) -> Text:
        return "action_dar_info"

    async def run(self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        message = tracker.latest_message['text']
        message = set(message.split(" "))
        email = {'correo', 'electrónico', 'electronico', 'email', 'gmail', 'hotmail', 'yahoo'}
        phone = {'telefono', 'teléfono', 'movil', 'móvil', 'numero', 'número'}
        events = list(filter(lambda x: ('parse_data' in x and 'entities' in x['parse_data']), tracker.events))
        if events == []:
            dispatcher.utter_message(text="No he entendido de quién quieres la información")
            return []
        event = events[-1]
        entities = list(filter(lambda x: (x['entity'] == 'nick'), event['parse_data']['entities']))
        if len(entities) > 1:
            dispatcher.utter_message(text="Sólo puedo darte la información de un contacto a la vez")
            return []
        nick = entities[0]['value']
        has_answered = False
        new_nick = nick.replace(" ", "_")
        new_nick = new_nick.lower()
        if not os.path.exists('agenda.json'):
            dispatcher.utter_message(text="Primero debes registrar algún usuario")
            return []
        with open('agenda.json', 'r') as f:
            all_data = json.load(f)
            try:
                data = all_data[new_nick]
            except Exception:
                dispatcher.utter_message(text="No tengo guardado el usuario " + nick)
                return []
        if len(email.intersection(message)) != 0:
            ans = "El email de " + nick + " es " + data['email']
            dispatcher.utter_message(text=ans)
            has_answered = True

        if len(phone.intersection(message)) != 0:
            ans = "El teléfono de " + nick + " es " + data['phone']
            dispatcher.utter_message(text=ans)
            has_answered = True
        if not has_answered:
            ans = "El email de " + nick + " es " + data['email'] + " y el teléfono es " + data['phone']
            dispatcher.utter_message(text=ans)
        return []

class ResetSlots(Action):
    def name(self) -> Text:
        return "reset"

    async def run(self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        return [SlotSet("evento", None), SlotSet("alarma", None), SlotSet("nick", None),
                SlotSet("email_propio", None), SlotSet("email_amigo", None), SlotSet("phone-number", None),
                SlotSet("nick_contacto", None)]

class ObtenerTodos(Action):
    def name(self) -> Text:
        return "action_obtener_todos_contactos"

    async def run(self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        if not os.path.exists('agenda.json'):
            dispatcher.utter_message(text="No existe ningún usuario")
            return []
        with open('agenda.json', 'r') as f:
            all_data = json.load(f)
            nicks = all_data.keys()
            if nicks==[]:
                dispatcher.utter_message(text="No existe ningún usuario")
                return []
            else:
                dispatcher.utter_message(text="Existen " + str(len(nicks)) + " contactos guardados en tu agenda:\n")
                dispatcher.utter_message(text=", ".join(nicks))

        return []
