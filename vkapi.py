# -*- coding: utf-8 -*-
import vk
import requests as r
import io

session = vk.Session()
api = vk.API(session, v=5.0)


def send_message(user_id, token, message, attachment=""):
    api.messages.send(access_token=token, user_id=str(user_id), message=message, attachment=attachment)

def send_message_with_buttons(user_id, token, message, attachment="", keyboard=""):
    api.messages.send(access_token=token, user_id=str(user_id), message=message, attachment=attachment, keyboard=keyboard)

def send_image(token, user_id, hash):
    url = api.photos.getMessagesUploadServer(access_token=token, peer_id=user_id)['upload_url']
    filename = 'QR/'+hash+'.png'
    photo_data = r.post(url, files={'photo': open(filename, "rb")})
    params = {'access_token': token,
              'server': photo_data.json()['server'],
              'photo': photo_data.json()['photo'],
              'hash': photo_data.json()['hash']}
    photo = api.photos.saveMessagesPhoto(**params)[0] #картинка
    photo_url = 'photo'+str(photo['owner_id'])+'_'+str(photo['id'])
    return photo_url

def send_file(token, user_id, active_students, filename, department):
    url = api.docs.getMessagesUploadServer(access_token=token, type='doc', peer_id=user_id)['upload_url']
    doc_data = r.post(url, files={'file': io.open('CSV/'+filename, 'rb')})
    params = {'access_token': token,
              'file': doc_data.json()['file'],
              'title': filename,
              'tags': ''}
    document = api.docs.save(**params)[0] #документ
    document_url = 'doc'+str(document['owner_id'])+'_'+str(document['id'])
    return document_url