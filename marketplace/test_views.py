from django.forms import ValidationError
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from marketplace.models import ChatMessage
from django.utils import timezone
import datetime

class ViewTest(TestCase):

    def test_messages_page(self):
        """
        These tests create a couple of users and some chat messages 
        so that "user_list" can be tested to make sure 
        we aren't in it when logged in, plus we test that
        the logged in user can send a message to another user
        but cannot send a message to themselves.
        """
        date = datetime.datetime.now(tz=timezone.utc)
        
        # # create the first User
        user_1 = User.objects.create_user(username='testuser1', password='12345')
        # user_1 = User.objects.create_user(username='testuser1', password='12345')
        print(user_1.username + ' was just created')

        # create the second User, login, and send the first user a message
        user_2 = User.objects.create_user(username='testuser2', password='12345')
        login = self.client.login(username='testuser2', password='12345')
        message1 = ChatMessage.objects.create(sender=user_2, reciever=user_1, msg_content='Test Message', created_at= date,)
        print(user_2.username + ' just logged in and the message "' + message1.msg_content + '" was just created')
        self.client.logout()

        # # login the first user and send some messages to another user
        login = self.client.login(username='testuser1', password='12345')
        message1 = ChatMessage.objects.create(sender=user_1, reciever=user_2, msg_content='Test Message', created_at= date,)
        print(user_1.username + ' just logged in and the message "' + message1.msg_content + '" was just created')
        
        # check "user_list" to make sure user_1 (currently logged in user) isn't in the list
        response = self.client.get(reverse('messages'))
        userlist = list(response.context['user_list'])
        print('Your username is: ' + user_1.username + ' and the usernames in "user_list" context are: ' + str(response.context['user_list']))
        self.assertEqual(str(userlist[0]), user_2.username)

        # assert the logged in user *can* send a message to another user
        data = {'message': 'test123', 'respond_to_user': "2",}
        response = self.client.post(reverse('messages'), data)
        print('Response status code for sending message to another user: ' + str(response.status_code))
        self.assertEqual(response.status_code, 200) 

        # assert the logged in user *cannot* send a message to themselves
        data = {'message': 'test123', 'respond_to_user': "1",}
        with self.assertRaises(Exception):
            response = self.client.post(reverse('messages'), data)
         